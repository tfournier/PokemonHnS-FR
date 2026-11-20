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
dl = np.load(os.path.join(TMP, 'em_delta.npy'))
NONE = np.iinfo(np.int32).min
po = charger_po()
LETTRES = set(range(0xA1, 0xEF))


def chaine(rom, a, lim=1200):
    e = rom.find(b'\xff', a, a + lim)
    return rom[a:e] if e >= 0 else None


def debut_texte(rom, a):
    return a == 0 or rom[a - 1] in (0x00, 0xFF) or rom[a - 1] not in LETTRES


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
        # resynchronisation après le champ : une position parcourue au même décalage dans les 64 octets
        after = dl[e + 1:e + 65]
        if not (after == D).any(): continue
        fb = chaine(fr, q, 400)
        if fb is None or not debut_texte(fr, q): continue
        # le texte FR doit se terminer avant la reprise de la marche
        k = int(np.argmax(after == D)) + e + 1
        if q + len(fb) >= k + D + 1 and fb != b: continue
        cand[m].append(('delta', fb, 'US %06X -> FR %06X (zone parallèle, décalage %+d)' % (a, q, D)))
    if b in tm2:
        for fb, n in tm2[b].items():
            cand[m].append(('tm', fb, 'table octets EN->FR (x%d)' % n))

# ---------------------------------------------------------------- tables à champs fixes (index)
import bisect
TG = sorted(pairs)


def depart(rom, p):
    return rom[p] in LETTRES and rom[p - 1] not in LETTRES


def voisins_ok(a, b, la):
    """les débuts de texte voisins en US (±96 octets) sont aussi des débuts de texte en FR au même écart"""
    vs = [p for p in range(max(1, a - 96), min(N - 1, a + la + 97)) if p != a and depart(us, p)]
    if len(vs) < 2: return False, 0
    ok = sum(1 for p in vs if 0 < b + (p - a) < N - 1 and depart(fr, b + (p - a)))
    return ok >= 0.85 * len(vs), len(vs)


for m, al in occ.items():
    if any(x[0] in ('ptr', 'delta') for x in cand.get(m, [])): continue
    b = enc[m]
    for a in al:
        if not debut_texte(us, a) or us[a] not in LETTRES and us[a] < 0xF7 and len(b) < 2: continue
        k = bisect.bisect_right(TG, a) - 1
        for T in TG[max(0, k - 2):k + 1][::-1]:
            if a - T > 0x10000: break
            Tf = pairs[T].most_common(1)[0][0]
            q = Tf + (a - T)
            if not (0 < q < N) or not debut_texte(fr, q): continue
            Ds = dl[T:a]; Ds = Ds[Ds != NONE]
            if len(Ds) and (Ds != Tf - T).any(): continue
            fb = chaine(fr, q, 200)
            if fb is None or G.decode(fb) is None: continue
            ok, nv = voisins_ok(a, q, len(b))
            if not ok: continue
            cand[m].append(('table', fb, 'US %06X -> FR %06X (table de base US %06X / FR %06X, index +%d, %d voisins)' % (a, q, T, Tf, a - T, nv)))
            break
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
