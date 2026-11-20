#!/usr/bin/env python3
"""Calcule un trajet à pied sur une carte de Heart & Soul et l'écrit en commandes `walk`.

Usage :
  chemin.py CARTE X0 Y0 X1 Y1 [--bloque x,y ...] [--herbe-ok]
  ex. : chemin.py Route29_hns 69 18 0 12

Lit les données de carte de build/upstream_orig (lecture seule) :
  data/maps/<CARTE>/map.json, data/layouts/layouts.json, map.bin, metatile_attributes.bin.
Règles : case franchissable si collision 0, pas d'eau, pas de PNJ fixe ; les rebords
(MB_JUMP_*) ne se franchissent que dans le sens du saut (on atterrit 2 cases plus loin).
Les hautes herbes coûtent cher (rencontres) sauf --herbe-ok.
"""
import heapq
import json
import os
import re
import sys

P = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UP = os.path.join(P, "build", "upstream_orig")
NUM_PRIMARY = 640


def behaviours():
    noms = []
    with open(os.path.join(UP, "include/constants/metatile_behaviors.h")) as f:
        dans = False
        for ligne in f:
            if ligne.strip().startswith("enum"):
                dans = True
                continue
            if dans:
                m = re.match(r"\s*(MB_\w+)", ligne)
                if m:
                    noms.append(m.group(1))
                if "}" in ligne:
                    break
    return noms


def chemin_tileset(symbole):
    with open(os.path.join(UP, "src/data/tilesets/headers.h")) as f:
        txt = f.read()
    m = re.search(r"const struct Tileset %s =\s*\{(.*?)\};" % re.escape(symbole), txt, re.S)
    attr = re.search(r"\.metatileAttributes = (\w+)", m.group(1)).group(1)
    with open(os.path.join(UP, "src/data/tilesets/metatiles.h")) as f:
        for ligne in f:
            if attr + "[]" in ligne:
                return os.path.join(UP, re.search(r'"([^"]+)"', ligne).group(1))
    raise SystemExit("attributs introuvables pour " + symbole)


def u16(path):
    data = open(path, "rb").read()
    return [data[i] | data[i + 1] << 8 for i in range(0, len(data), 2)]


def charger(carte):
    mj = json.load(open(os.path.join(UP, "data/maps", carte, "map.json")))
    lay = next(l for l in json.load(open(os.path.join(UP, "data/layouts/layouts.json")))["layouts"]
               if l.get("id") == mj["layout"])
    w, h = lay["width"], lay["height"]
    blocs = u16(os.path.join(UP, lay["blockdata_filepath"]))
    a1 = u16(chemin_tileset(lay["primary_tileset"]))
    a2 = u16(chemin_tileset(lay["secondary_tileset"]))
    return mj, w, h, blocs, a1, a2


def main():
    args = sys.argv[1:]
    herbe_ok = "--herbe-ok" in args
    bloques = set()
    if "--bloque" in args:
        i = args.index("--bloque")
        for t in args[i + 1:]:
            if t.startswith("--"):
                break
            x, y = t.split(",")
            bloques.add((int(x), int(y)))
    carte, x0, y0, x1, y1 = args[0], *map(int, args[1:5])
    mj, w, h, blocs, a1, a2 = charger(carte)
    noms = behaviours()
    explicites = set(bloques)
    for o in mj.get("object_events", []):
        if "MON_BASE" not in o.get("graphics_id", ""):
            bloques.add((o["x"], o["y"]))
    if (x1, y1) not in explicites:
        bloques.discard((x1, y1))  # un PNJ caché (drapeau) peut occuper la case visée

    def info(x, y):
        b = blocs[y * w + x]
        mt, coll = b & 0x3FF, (b >> 10) & 3
        att = a1[mt] if mt < NUM_PRIMARY else a2[mt - NUM_PRIMARY]
        beh = att & 0xFF
        return coll, noms[beh] if beh < len(noms) else "?"

    dirs = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
    saut = {"MB_JUMP_SOUTH": "DOWN", "MB_JUMP_NORTH": "UP", "MB_JUMP_EAST": "RIGHT", "MB_JUMP_WEST": "LEFT"}

    def libre(x, y):
        if not (0 <= x < w and 0 <= y < h) or (x, y) in bloques:
            return False
        coll, beh = info(x, y)
        return coll == 0 and "WATER" not in beh

    dist = {(x0, y0): 0}
    prec = {}
    tas = [(0, x0, y0)]
    while tas:
        d, x, y = heapq.heappop(tas)
        if (x, y) == (x1, y1):
            break
        if d > dist[(x, y)]:
            continue
        for nom, (dx, dy) in dirs.items():
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h):
                continue
            coll, beh = info(nx, ny)
            if beh in saut:
                if saut[beh] != nom:
                    continue
                nx, ny = nx + dx, ny + dy
                if not libre(nx, ny):
                    continue
                cout = 2
            elif (nx, ny) == (x1, y1) and (nx, ny) not in bloques:
                cout = 1
            elif not libre(nx, ny) or beh.startswith("MB_JUMP"):
                continue
            else:
                cout = 1
            if "GRASS" in beh and not herbe_ok:
                cout += 15
            nd = d + cout
            if nd < dist.get((nx, ny), 1 << 30):
                dist[(nx, ny)] = nd
                prec[(nx, ny)] = ((x, y), nom)
                heapq.heappush(tas, (nd, nx, ny))
    if (x1, y1) not in prec and (x1, y1) != (x0, y0):
        raise SystemExit("aucun chemin")
    pas = []
    c = (x1, y1)
    while c != (x0, y0):
        c, nom = prec[c]
        pas.append(nom)
    pas.reverse()
    # regroupe ; un saut compte pour 2 cases dans le contrôle de position
    sortie = []
    for nom in pas:
        if sortie and sortie[-1][0] == nom:
            sortie[-1][1] += 1
        else:
            sortie.append([nom, 1])
    # recalcul des longueurs réelles (sauts = 2 cases)
    x, y = x0, y0
    lignes = []
    for nom, n in sortie:
        dx, dy = dirs[nom]
        reel = 0
        for _ in range(n):
            _, beh = info(x + dx, y + dy)
            k = 2 if beh in saut else 1
            x, y = x + dx * k, y + dy * k
            reel += k
        lignes.append("walk %s %d" % (nom, reel))
    print("\n".join(lignes))
    print("# %d pas, coût %d" % (len(pas), dist[(x1, y1)]), file=sys.stderr)


if __name__ == "__main__":
    main()
