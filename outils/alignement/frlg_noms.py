#!/usr/bin/env python3
"""Lot F : noms des Dresseurs FRLG (src/data/trainers_frlg.party, src/trainer_tower_sets.c) -> Rouge Feu FR.

- trainers_frlg.party : TRAINER_X -> indice dans pokefirered (include/constants/opponents.h) ->
  gTrainers[indice].trainerName (struct Trainer de 40 octets, nom à +4) dans BPRE puis BPRF (adresse FR de
  gTrainers par les pointeurs).
- trainer_tower_sets.c : sTrainerTowerFloor_X.trainers[k].name (étage : 4 octets + 3 × 328) ; adresse FR de
  l'étage par les pointeurs.
Sortie : build/lotF/frlg_noms.pkl = liste de dict(msgid, fichier, ligne, en_us, fr, adr_fr, cle)
"""
import os, sys, re, pickle, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frlg_commun import ROOT, PFR, TMP, G, roms, symboles, lire

us, fr = roms(); syms = symboles()
d = pickle.load(open(os.path.join(TMP, 'frlg_ptr.pkl'), 'rb'))


def adr_fr(a):
    c = d['ptr'].get(a)
    return c.most_common(1)[0][0] if c else None


def nom(rom, a, n):
    b = rom[a:a + n]; e = b.find(b'\xff')
    return G.decode(b[:e] if e >= 0 else b)


out = []
# --- gTrainers
idx = {}
for l in open(os.path.join(PFR, 'include', 'constants', 'opponents.h')):
    m = re.match(r'#define (TRAINER_\w+)\s+(\d+)\s*$', l)
    if m: idx[m.group(1)] = int(m.group(2))
gu = syms['gTrainers']; gf = adr_fr(gu)
txt = open(os.path.join(ROOT, 'src/data/trainers_frlg.party'), encoding='utf-8').read().split('\n')
const = None
for i, l in enumerate(txt):
    m = re.match(r'=== (TRAINER_\w+) ===', l)
    if m: const = m.group(1); continue
    m = re.match(r'Name: (.*)$', l)
    if m and const:
        k = idx.get(const) or idx.get(re.sub(r'_FRLG$', '', const))
        if k is None:
            out.append(dict(msgid=m.group(1), fichier='src/data/trainers_frlg.party', ligne=i + 1, cle=const, en_us=None, fr=None, adr_fr=None)); continue
        a = gu + 40 * k + 4; f = gf + 40 * k + 4
        out.append(dict(msgid=m.group(1), fichier='src/data/trainers_frlg.party', ligne=i + 1, cle=const,
                        en_us=nom(us, a, 12), fr=nom(fr, f, 12), adr_fr=f))
# --- Tour de Combat (Trainer Tower)
txt = open(os.path.join(ROOT, 'src/trainer_tower_sets.c'), encoding='utf-8').read().split('\n')
floor = None; k = 0
for i, l in enumerate(txt):
    m = re.search(r'(sTrainerTowerFloor_\w+)\s*=', l)
    if m: floor = m.group(1); k = 0; continue
    m = re.search(r'\.name = _\("([^"]*)"\)', l)
    if m and floor:
        a0 = syms.get(floor); f0 = adr_fr(a0) if a0 is not None else None
        if a0 is not None and f0 is None:
            # étage inutilisé (non visé par un pointeur) : même décalage que l'étage visé le plus proche
            # (étages contigus de taille fixe ; décalage vérifié identique pour tous les étages visés)
            ref = min((x for x in syms if x.startswith('sTrainerTowerFloor_') and adr_fr(syms[x])), key=lambda x: abs(syms[x] - a0))
            f0 = adr_fr(syms[ref]) + a0 - syms[ref]
        if a0 is None or f0 is None:
            out.append(dict(msgid=m.group(1), fichier='src/trainer_tower_sets.c', ligne=i + 1, cle='%s[%d]' % (floor, k), en_us=None, fr=None, adr_fr=None))
        else:
            a = a0 + 4 + 328 * k; f = f0 + 4 + 328 * k
            out.append(dict(msgid=m.group(1), fichier='src/trainer_tower_sets.c', ligne=i + 1, cle='%s[%d]' % (floor, k),
                            en_us=nom(us, a, 11), fr=nom(fr, f, 11), adr_fr=f))
        k += 1
pickle.dump(out, open(os.path.join(TMP, 'frlg_noms.pkl'), 'wb'))
c = collections.Counter((o['fichier'], o['fr'] is not None, (o['en_us'] or '').upper() == o['msgid'].upper()) for o in out)
print(c)
for o in out:
    if o['fr'] is None or (o['en_us'] or '').upper() != o['msgid'].upper(): print(o)
