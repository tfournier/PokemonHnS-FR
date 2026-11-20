#!/usr/bin/env python3
"""Tables par index Émeraude US <-> Émeraude FR (lot A).

Pour chaque table de noms de l'upstream (ordre du fichier source = ordre des index), on retrouve la
table dans Émeraude US (noms consécutifs à pas constant), puis la table FR au même index
(base FR = cible FR du pointeur de code qui précède, ou recherche du squelette de la structure),
et on vérifie la structure entrée par entrée (octets hors nom identiques, nom FR bien formé).
Sortie : $TMP/em_tables.pkl {msgid: [('tidx', octets_fr, preuve, fichier)]} et un résumé par table.
"""
import os, sys, re, pickle, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from em_commun import roms, TMP, G, ROOT, CODE

us, fr = roms(); N = len(us)
d = pickle.load(open(os.path.join(TMP, 'em_ptr.pkl'), 'rb'))
pairs = d['ptr']
TG = sorted(pairs)
import bisect

MA = bytearray(us); MF = bytearray(fr)


def lire(path):
    return open(os.path.join(ROOT, path), encoding='utf-8').read()


def noms_fichier(path, champ):
    txt = lire(path)
    return [m.group(1) for m in re.finditer(r'\.' + champ + r'\s*=\s*_\("((?:[^"\\]|\\.)*)"\)', txt)]


def noms_party(path):
    out = []
    for blk in re.split(r'^=== ', lire(path), flags=re.M)[1:]:
        cst = blk.split(' ===')[0].strip()
        m = re.search(r'^Name:[ \t]*(.*?)[ \t]*$', blk, re.M)
        out.append((cst, m.group(1) if m else ''))
    return out


def chaine(rom, a, lim=40):
    e = rom.find(b'\xff', a, a + lim)
    return rom[a:e] if e >= 0 else None


def trouver_us(noms, pas_max=128, min_ok=0.8):
    """base US et pas d'une table dont les noms sont `noms` (dans l'ordre)."""
    enc = [G.encode(n) if n else None for n in noms]
    k0 = next(i for i, e in enumerate(enc) if e)
    first = enc[k0] + b'\xff'
    best = None
    i = us.find(first)
    while i >= 0:
        for s in range(len(first), pas_max + 1):
            ok = tot = 0
            for k in range(1, min(len(noms) - k0, 12)):
                if not enc[k0 + k]: continue
                tot += 1
                a = i + k * s
                if us[a:a + len(enc[k0 + k]) + 1] == enc[k0 + k] + b'\xff': ok += 1
            if tot and ok >= 0.8 * tot and ok >= min(3, tot):
                base = i - k0 * s
                # score global
                tout = sum(1 for k, e in enumerate(enc) if e and us[base + k * s:base + k * s + len(e) + 1] == e + b'\xff')
                if best is None or tout > best[2]: best = (base, s, tout)
        i = us.find(first, i + 1)
    if best and best[2] >= min_ok * sum(1 for e in enc if e): return best
    return None


def base_fr(base, s, n, lname):
    """base FR : par le pointeur de code précédent (même écart), validée par la forme des noms FR."""
    cands = []
    k = bisect.bisect_right(TG, base + lname) - 1
    for T in TG[max(0, k - 4):k + 1]:
        if base - T > 0x20000: continue
        for Tf in pairs[T]:
            cands.append(Tf + (base - T))
    best = None
    for b in set(cands):
        if b < 0 or b + n * s > N: continue
        ok = 0
        for i in range(n):
            x = chaine(fr, b + i * s, lname + 1)
            if x is not None and len(x) <= lname and (b + i * s == 0 or fr[b + i * s - 1] not in range(0xBB, 0xEF)) \
                    and G.decode(x) is not None:
                ok += 1
        # octets hors nom identiques
        same = tot = 0
        for i in range(min(n, 50)):
            u = us[base + i * s:base + (i + 1) * s]; f = fr[b + i * s:b + (i + 1) * s]
            for j in range(lname + 1, s):
                tot += 1; same += u[j] == f[j]
        r = (ok / n, same / max(1, tot))
        if best is None or r > best[1]: best = (b, r)
    return best


def table(label, noms, lname, decal=0, **kw):
    """noms : liste (msgid ou '') dans l'ordre des index ; renvoie [(i, msgid, octets FR, preuve)]"""
    t = trouver_us(noms, **kw)
    if not t:
        print('%-28s introuvable dans Émeraude US' % label, file=sys.stderr); return []
    base, s, tout = t
    enc = [G.encode(n) if n else None for n in noms]
    neff = 1 + max(i for i, e in enumerate(enc) if e and us[base + i * s:base + i * s + len(e) + 1] == e + b'\xff')
    noms = noms[:neff]
    bf = base_fr(base, s, len(noms), lname)
    if not bf or bf[1][0] < 0.95:
        print('%-28s US %06X pas %d : table FR non validée %s' % (label, base, s, bf), file=sys.stderr); return []
    b, (rn, rs) = bf
    out = []
    for i, n in enumerate(noms):
        e = G.encode(n) if n else None
        if not e: continue
        if us[base + i * s:base + i * s + len(e) + 1] != e + b'\xff': continue
        x = chaine(fr, b + i * s, lname + 1)
        if x is None: continue
        out.append((i, n, x, '%s[%d] US %06X -> FR %06X' % (label, i, base + i * s, b + i * s)))
    PLAGES.append((label, base, base + len(noms) * s))
    print('%-28s US %06X FR %06X pas %d : %d/%d noms identiques à l’upstream, noms FR bien formés %.0f%%, octets hors nom identiques %.0f%%'
          % (label, base, b, s, len(out), len(noms), 100 * rn, 100 * rs), file=sys.stderr)
    return out


res = collections.defaultdict(list)
resume = []
PLAGES = []


def ajoute(label, out, fichier):
    for i, n, x, pr in out:
        res[n].append(('tidx', x, pr, fichier))
    resume.append((label, len(out)))


# Dresseurs (gTrainers) : ordre de trainers.party = ordre des constantes TRAINER_*
party = noms_party('src/data/trainers.party')
ajoute('gTrainers', table('gTrainers', [n for c, n in party], 11), 'src/data/trainers.party')
# Dresseurs Frontier, Tentes, adversaires de Concours, échanges
ajoute('gBattleFrontierTrainers', table('gBattleFrontierTrainers', noms_fichier('src/data/battle_frontier/battle_frontier_trainers.h', 'trainerName'), 7),
       'src/data/battle_frontier/battle_frontier_trainers.h')
tent = noms_fichier('src/data/battle_frontier/battle_tent.h', 'trainerName')
for k, nom in enumerate(('Slateport', 'Verdanturf', 'Fallarbor')):
    part = tent[k * 30:(k + 1) * 30]
    ajoute('gBattleTent%s' % nom, table('gBattleTent%s' % nom, part, 7), 'src/data/battle_frontier/battle_tent.h')
txt = lire('src/data/contest_opponents.h')
ajoute('gContestOpponents.trainerName', table('gContestOpponents.trainerName', noms_fichier('src/data/contest_opponents.h', 'trainerName')[-96:], 10),
       'src/data/contest_opponents.h')
ajoute('gContestOpponents.nickname', table('gContestOpponents.nickname', noms_fichier('src/data/contest_opponents.h', 'nickname')[-96:], 10),
       'src/data/contest_opponents.h')
ajoute('gDefaultContestWinners.trainerName', table('gDefaultContestWinners.trainerName', noms_fichier('src/data/contest_opponents.h', 'trainerName')[:8], 7, min_ok=0.6),
       'src/data/contest_opponents.h')
ajoute('gDefaultContestWinners.monName', table('gDefaultContestWinners.monName', noms_fichier('src/data/contest_opponents.h', 'monName')[:8], 10, min_ok=0.6),
       'src/data/contest_opponents.h')
ajoute('sIngameTrades.nickname', table('sIngameTrades.nickname', noms_fichier('src/data/trade.h', 'nickname')[:4], 10, min_ok=0.6), 'src/data/trade.h')
ajoute('sIngameTrades.otName', table('sIngameTrades.otName', noms_fichier('src/data/trade.h', 'otName')[:4], 7, min_ok=0.6), 'src/data/trade.h')

# Catégories du Pokédex d'Émeraude (gPokedexEntries.categoryName) : seulement pour repérer la plage
# (dans HnS les catégories sont en casse mixte : une correspondance dans cette plage est un autre sens)
cats = ['UNKNOWN', 'SEED', 'SEED', 'SEED', 'LIZARD', 'FLAME', 'FLAME', 'TINY TURTLE', 'TURTLE', 'SHELLFISH']
t = trouver_us(cats, pas_max=64)
if t:
    PLAGES.append(('gPokedexEntries.categoryName', t[0], t[0] + 387 * t[1]))
    print('catégories Pokédex Émeraude US %06X pas %d' % (t[0], t[1]), file=sys.stderr)

# Apprentis : le nom FR est dans la même structure (emplacement LANGUAGE_FRENCH)
app = []
for m in re.finditer(r'\.name\s*=\s*\{([^}]*)\}', lire('src/data/battle_frontier/apprentice.h')):
    ns = re.findall(r'_\("((?:[^"\\]|\\.)*)"\)', m.group(1))
    if len(ns) >= 3: app.append(ns)
na = 0
for i, ns in enumerate(app):
    en, frn = ns[1], ns[2]
    e, f = G.encode(en), G.encode(frn)
    if e and f and us.find(f + b'\xff') >= 0 and fr.find(f + b'\xff') >= 0:
        res[en].append(('tidx', f, 'gApprentices[%d].name : anglais %s / français %s (présent dans les deux ROM)' % (i, en, frn),
                        'src/data/battle_frontier/apprentice.h'))
        na += 1
resume.append(('gApprentices.name', na))
print('apprentis :', na, file=sys.stderr)

# Mots Easy Chat : tables {texte*, ordre alphabétique, activé} indexées par EC_WORD (même index en FR)
import struct, glob
dl = np.load(os.path.join(TMP, 'em_delta.npz'))['dl']; NONE = np.iinfo(np.int32).min


def p32(rom, a):
    v = struct.unpack_from('<I', rom, a)[0] - 0x08000000
    return v if 0 <= v < N else None


nec = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/easy_chat/easy_chat_group_*.h'))):
    rel = os.path.relpath(f, ROOT)
    mots = [m.group(1) for m in re.finditer(r'\.text\s*=\s*COMPOUND_STRING\("((?:[^"\\]|\\.)*)"\)', open(f, encoding='utf-8').read())]
    if len(mots) < 3: continue
    e0, e1 = G.encode(mots[0]), G.encode(mots[1])
    if not e0 or not e1: continue
    T = None
    i = us.find(e0 + b'\xff')
    while i >= 0 and T is None:
        pb = struct.pack('<I', i + 0x08000000)
        j = us.find(pb)
        while j >= 0:
            q = p32(us, j + 12)
            if q is not None and us[q:q + len(e1) + 1] == e1 + b'\xff':
                T = j; break
            j = us.find(pb, j + 1)
        i = us.find(e0 + b'\xff', i + 1)
    if T is None:
        print('%-28s table US introuvable' % os.path.basename(rel), file=sys.stderr); continue
    Tf = T + int(dl[T]) if dl[T] != NONE else None
    if Tf is None and T in pairs: Tf = pairs[T].most_common(1)[0][0]
    if Tf is None:
        print('%-28s table FR introuvable' % os.path.basename(rel), file=sys.stderr); continue
    ok = bad = 0; out = []
    for k, w in enumerate(mots):
        e = G.encode(w)
        pu, pf = p32(us, T + 12 * k), p32(fr, Tf + 12 * k)
        if pu is None or pf is None or us[T + 12 * k + 8] != fr[Tf + 12 * k + 8]: bad += 1; continue
        x = chaine(fr, pf, 40)
        if x is None or G.decode(x) is None: bad += 1; continue
        ok += 1
        if e and us[pu:pu + len(e) + 1] == e + b'\xff':
            out.append((k, w, x, 'EasyChat %s[%d] US %06X -> FR %06X' % (os.path.basename(rel)[16:-2], k, pu, pf)))
    if bad > 0.05 * len(mots):
        print('%-28s US %06X FR %06X : structure non conforme (%d/%d)' % (os.path.basename(rel), T, Tf, bad, len(mots)), file=sys.stderr); continue
    for k, w, x, pr in out: res[w].append(('tidx', x, pr, rel))
    ptrs = [p32(us, T + 12 * k) for k in range(len(mots))]
    PLAGES.append(('EasyChat', min(p for p in ptrs if p is not None), T + 12 * len(mots)))
    nec += len(out)
    print('%-28s US %06X FR %06X : %d mots, %d identiques à l’upstream' % (os.path.basename(rel), T, Tf, len(mots), len(out)), file=sys.stderr)
resume.append(('EasyChat', nec))

# Noms de personnages Hoenn (graphie Émeraude FR en capitales) que le glossaire SoulSilver transformerait
# (ARTHUR, PIERRE…) : noms FR des tables de Dresseurs + locuteurs « NOM: » des dialogues Émeraude FR.
import style
GLT = {}
for line in open(os.path.join(os.path.dirname(ROOT), '..', 'traductions', 'glossaire.tsv'), encoding='utf-8'):
    if line.startswith('#') or not line.strip(): continue
    k, v, t = (line.rstrip('\n').split('\t') + ['', ''])[:3]; GLT[k] = t
noms = collections.Counter()
for n, l in res.items():
    for meth, x, pr, f in l:
        if pr.startswith(('gTrainers', 'gBattleFrontierTrainers', 'gBattleTent', 'gContestOpponents.trainerName')):
            t = G.decode(x)
            if t: noms[t] += 1
tm2 = pickle.load(open(os.path.join(TMP, 'tm_em_bytes_v2.pkl'), 'rb'))
for eb, fb in tm2.items():
    f = G.decode(fb)
    if not f: continue
    for mm in re.finditer(r'(?:^|\\p|\\n|\\l)([A-ZÉÈ][A-ZÉÈ’\'\-\.]{1,14}):', f):
        noms[mm.group(1)] += 1
PROTEGES = sorted(n for n in noms if GLT.get(style.cle(n)) == 'personnage' and n not in ('MAMAN', 'PAPA', 'MAMIE', 'PAPI'))
print('noms Hoenn protégés du glossaire :', len(PROTEGES), file=sys.stderr)

pickle.dump({'res': dict(res), 'resume': resume, 'plages': PLAGES, 'proteges': PROTEGES}, open(os.path.join(TMP, 'em_tables.pkl'), 'wb'))
print('msgid avec candidat de table :', len(res), file=sys.stderr)
