#!/usr/bin/env python3
"""Candidats Émeraude FR pour les msgid des .po (lot A).

Prérequis : em_pointeurs.py (carte des pointeurs et décalages, dans $LOTA_TMP ou memoires/lotA).
Méthodes (chaque candidat = (méthode, octets FR, preuve)) :
  ptr    texte anglais trouvé octet pour octet dans Émeraude US, pointé ; cible FR du même pointeur
  delta  texte dans une zone parcourue en parallèle (table à champs fixes, segment resynchronisé)
  tm     table octets EN -> FR (memoires/tm_em_bytes.pkl, étendue par les paires ptr vérifiées)
Sortie : $TMP/em_cand.pkl {msgid: [(méthode, octets_fr, preuve)]}, $TMP/em_occ.pkl {msgid: [adresses US]},
         $TMP/tm_em_bytes_v2.pkl (table octets EN -> FR étendue)
"""
import os, sys, pickle, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from em_commun import roms, TMP, MEM, G, charger_po, deja_emeraude
import ahocorasick

us, fr = roms(); N = len(us)
d = pickle.load(open(os.path.join(TMP, 'em_ptr.pkl'), 'rb'))
pairs = d['ptr']
dl = np.load(os.path.join(TMP, 'em_delta.npz'))['dl']
NONE = np.iinfo(np.int32).min
po = charger_po()
LETTRES = set(range(0xA1, 0xEF))


def chaine(rom, a, lim=1200):
    e = rom.find(b'\xff', a, a + lim)
    return rom[a:e] if e >= 0 else None


def debut_texte(rom, a):
    """début de chaîne : précédé d'un FF, d'un octet non texte, ou d'un 00 qui n'est pas une espace dans un mot"""
    if a == 0 or rom[a - 1] == 0xFF: return True
    if rom[a - 1] == 0x00: return a < 2 or rom[a - 2] in (0x00, 0xFF) or rom[a - 2] not in LETTRES
    return rom[a - 1] not in LETTRES


# ---------------------------------------------------------------- table octets EN -> FR étendue
tm = pickle.load(open(os.path.join(MEM, 'tm_em_bytes.pkl'), 'rb'))
tm2 = collections.defaultdict(collections.Counter)
for k, v in tm.items(): tm2[k][v] += 1
for pu, c in pairs.items():
    if not debut_texte(us, pu): continue
    eb = chaine(us, pu)
    if not eb or len(eb) < 2 or G.decode(eb) is None: continue
    for pf, n in c.items():
        if not (pf == 0 or fr[pf - 1] in (0x00, 0xFF) or pf % 4 == 0): continue
        fb = chaine(fr, pf)
        if fb is None or G.decode(fb) is None: continue
        tm2[eb][fb] += n
tm2 = {k: c for k, c in tm2.items()}
pickle.dump({k: c.most_common(1)[0][0] for k, c in tm2.items() if c.most_common(1)[0][1] >= 0.6 * sum(c.values())},
            open(os.path.join(TMP, 'tm_em_bytes_v2.pkl'), 'wb'))
print('table octets EN->FR :', len(tm), '->', len(tm2), file=sys.stderr)

# ---------------------------------------------------------------- occurrences US des msgid
A = ahocorasick.Automaton(); enc = {}
for (c, m), info in po.items():
    if c or deja_emeraude(info): continue
    b = G.encode(m)
    if b and len(b) >= 1:
        enc[m] = b; A.add_word((b + b'\xff').decode('latin1'), m)
A.make_automaton()
occ = collections.defaultdict(list)
for e, m in A.iter(us.decode('latin1')):
    a = e - len(enc[m])
    occ[m].append(a)

cand = collections.defaultdict(list)
for m, al in occ.items():
    b = enc[m]
    for a in al:
        if a in pairs and debut_texte(us, a):
            for pf, n in pairs[a].items():
                fb = chaine(fr, pf)
                if fb is not None:
                    cand[m].append(('ptr', fb, 'US %06X -> FR %06X (pointeur x%d)' % (a, pf, n)))
            continue
        D = int(dl[a])
        if D == NONE or not debut_texte(us, a): continue
        e = a + len(b)                      # position du FF en US
        q = a + D
        if q <= 0 or q >= N: continue
        if not (us[a - 1] == fr[q - 1] or (us[a - 1] in (0, 0xFF) and fr[q - 1] in (0, 0xFF))): continue
        if dl[a - 1] != D and us[a - 1] not in (0, 0xFF): continue
        fb = chaine(fr, q, 400)
        if fb is None or not debut_texte(fr, q): continue
        # resynchronisation après les deux textes : 4 octets identiques au même décalage, parcourus
        M = max(e, q + len(fb) - D)
        if not any(dl[y] == D and us[y:y + 4] == fr[y + D:y + D + 4] for y in range(M + 1, M + 25)): continue
        cand[m].append(('delta', fb, 'US %06X -> FR %06X (zone parallèle, décalage %+d)' % (a, q, D)))
    if b in tm2:
        for fb, n in tm2[b].items():
            cand[m].append(('tm', fb, 'table octets EN->FR (x%d)' % n))

# ---------------------------------------------------------------- tables à champs fixes (index)
import bisect
TG = sorted(pairs)


def depart(rom, p):
    """début de texte probable : précédé d'un FF, d'un remplissage 00 (lui-même après FF/00) ou d'un octet non texte"""
    if rom[p] not in LETTRES: return False
    x = rom[p - 1]
    if x == 0xFF: return True
    if x == 0: return rom[p - 2] in (0, 0xFF)
    return x not in LETTRES and not (0x01 <= x <= 0x1F or x in (0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB8, 0xBA))


def voisins_ok(a, b, la):
    """les débuts de texte voisins en US (±96 octets) sont aussi des débuts de texte en FR au même écart"""
    vs = [p for p in range(max(1, a - 96), min(N - 1, a + la + 97)) if p != a and depart(us, p)]
    if len(vs) < 2: return False, 0
    ok = sum(1 for p in vs if 0 < b + (p - a) < N - 1 and depart(fr, b + (p - a)))
    return ok >= 0.85 * len(vs), len(vs)


for m, al in occ.items():
    deja = {int(x[2][3:9], 16) for x in cand.get(m, []) if x[0] in ('ptr', 'delta')}
    b = enc[m]
    for a in al:
        if a in deja: continue
        if not debut_texte(us, a) or us[a] not in LETTRES and us[a] < 0xF7 and len(b) < 2: continue
        k = bisect.bisect_right(TG, a) - 1
        for T in TG[max(0, k - 2):k + 1][::-1]:
            if a - T > 0x10000: break
            Tf = pairs[T].most_common(1)[0][0]
            q = Tf + (a - T)
            if not (0 < q < N) or not debut_texte(fr, q): continue
            Ds = dl[max(T, a - 64):a + 64]; Ds = Ds[Ds != NONE]
            if len(Ds) and (Ds != Tf - T).any(): continue
            fb = chaine(fr, q, 200)
            if fb is None or G.decode(fb) is None: continue
            ok, nv = voisins_ok(a, q, len(b))
            if not ok: continue
            cand[m].append(('table', fb, 'US %06X -> FR %06X (table de base US %06X / FR %06X, index +%d, %d voisins)' % (a, q, T, Tf, a - T, nv)))
            break
# ---------------------------------------------------------------- séquences de chaînes voisines (même bloc, même ordre)
K = {}
for pu, c in pairs.items():
    pf, n = c.most_common(1)[0]
    if n < 0.6 * sum(c.values()): continue
    if us[pu - 1] in (0, 0xFF) and fr[pf - 1] in (0, 0xFF) and chaine(us, pu) is not None and chaine(fr, pf) is not None:
        K[pu] = pf
for m, l in cand.items():
    for meth, fb, pr in l:
        if meth in ('delta', 'table'):
            a, q = int(pr[3:9], 16), int(pr[15:21], 16)
            K.setdefault(a, q)


def precedente(rom, a):
    """début de la chaîne qui précède a (a doit suivre un FF)"""
    if rom[a - 1] != 0xFF: return None
    x = rom.rfind(b'\xff', max(0, a - 1200), a - 1)
    if x < 0: return None
    seg = rom[x + 1:a - 1]
    if not seg or G.decode(seg) is None: return None
    return x + 1


def suivante(rom, a):
    e = rom.find(b'\xff', a, a + 1200)
    if e < 0: return None
    n = e + 1
    if rom[n] == 0xFF or chaine(rom, n) is None or not chaine(rom, n) or G.decode(chaine(rom, n)) is None: return None
    return n


def seq(a, sens, lim=30):
    """remonte (sens=-1) ou descend (+1) jusqu'à une chaîne connue ; renvoie (cible FR, pas) ou None"""
    x = a
    for k in range(1, lim + 1):
        x = precedente(us, x) if sens < 0 else suivante(us, x)
        if x is None: return None
        if x in K:
            y = K[x]
            for _ in range(k):
                y = suivante(fr, y) if sens < 0 else precedente(fr, y)
                if y is None: return None
            return y, k, x
    return None


for m, al in occ.items():
    if m in cand: continue
    for a in al:
        if us[a - 1] != 0xFF: continue
        r1, r2 = seq(a, -1), seq(a, +1)
        if r1 and r2 and r1[0] == r2[0]:
            fb = chaine(fr, r1[0])
            if fb is not None and G.decode(fb) is not None:
                cand[m].append(('seq', fb, 'US %06X -> FR %06X (séquence : %d chaîne(s) après US %06X, %d avant US %06X)' % (a, r1[0], r1[1], r1[2], r2[1], r2[2])))
                break
        elif r1 or r2:
            r = r1 or r2
            fb = chaine(fr, r[0])
            if fb is not None and G.decode(fb) is not None:
                cand[m].append(('seq1', fb, 'US %06X -> FR %06X (séquence d’un seul côté : %d chaîne(s) %s US %06X)' % (a, r[0], r[1], 'après' if r is r1 else 'avant', r[2])))
for m, b in enc.items():
    if m not in cand and b in tm2:
        for fb, n in tm2[b].items():
            cand[m].append(('tm', fb, 'table octets EN->FR (x%d)' % n))
pickle.dump(dict(cand), open(os.path.join(TMP, 'em_cand.pkl'), 'wb'))
pickle.dump(dict(occ), open(os.path.join(TMP, 'em_occ.pkl'), 'wb'))
st = collections.Counter()
for m, l in cand.items():
    st[tuple(sorted({x[0] for x in l}))] += 1
print('msgid trouvés dans Émeraude US :', len(occ), ' avec candidat :', len(cand), dict(st), file=sys.stderr)
