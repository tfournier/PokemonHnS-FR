#!/usr/bin/env python3
"""Table des textes Rouge Feu : symbole pokefirered -> (adresse US, texte US, adresse FR, texte FR).

Entrée : build/lotF/frlg_ptr.pkl (frlg_pointeurs.py) + build/pokefirered/syms.txt.
L'adresse FR d'un symbole est la cible FR la plus fréquente des pointeurs qui visent son adresse US.
Pour les textes non visés directement (suite d'un tableau), on tente le décalage local de la marche
parallèle (frlg_delta.npz) quand il retombe sur un début de chaîne.
Sortie : build/lotF/frlg_table.pkl = {nom: dict(us, en, fr, fr_txt, mode)}
"""
import os, sys, pickle
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frlg_commun import roms, symboles, lire, G, TMP, SUF

us, fr = roms()
d = pickle.load(open(os.path.join(TMP, 'frlg_ptr%s.pkl' % SUF), 'rb'))
dl = np.load(os.path.join(TMP, 'frlg_delta%s.npz' % SUF))['dl']
NONE = np.iinfo(np.int32).min
syms = symboles()


def texte(rom, a):
    b = lire(rom, a)
    if b is None or len(b) < 1: return None
    s = G.decode(b)
    return s


def debut(rom, a):
    return a > 0 and rom[a - 1] in (0xFF, 0x00)


out = {}
for nom, a in syms.items():
    if a >= len(us) or not (debut(us, a) or 'Text' in nom): continue
    en = texte(us, a)
    if not en or not any(c.isalpha() for c in en): continue
    mode = None; f = None
    c = d['ptr'].get(a)
    if c:
        f, n = c.most_common(1)[0]
        mode = 'ptr' if len(c) == 1 else 'ptr~%d/%d' % (n, sum(c.values()))
    elif dl[a] != NONE and debut(fr, a + int(dl[a])):
        f = a + int(dl[a]); mode = 'delta'
    frt = texte(fr, f) if f is not None else None
    out[nom] = dict(us=a, en=en, fr=f, fr_txt=frt, mode=mode)
# textes contigus (même fichier text.inc, même ordre dans les deux ROM) : on propage l'adresse FR
# depuis le texte précédent (ou suivant) quand le symbole n'est pas visé par un pointeur.
ordre = sorted(out, key=lambda k: out[k]['us'])
def fin(rom, a): return rom.find(b'\xff', a) + 1
for sens in (1, -1):
    seq = ordre if sens == 1 else ordre[::-1]
    for i in range(1, len(seq)):
        a, b = out[seq[i - 1]], out[seq[i]]
        if b['mode'] and b['mode'].startswith('ptr') or a['fr'] is None or not (a['mode'] or '').startswith(('ptr', 'contigu')): continue
        if sens == 1 and fin(us, a['us']) == b['us']:
            f = fin(fr, a['fr'])
        elif sens == -1 and fin(us, b['us']) == a['us'] and fr[a['fr'] - 1] == 0xFF:
            f = fr.rfind(b'\xff', 0, a['fr'] - 1) + 1
        else: continue
        if b['fr'] is not None and b['fr'] != f and b['mode'] == 'delta': b['conflit'] = b['fr']
        if b['mode'] == 'delta' or b['mode'] is None:
            b['fr'] = f; b['fr_txt'] = texte(fr, f); b['mode'] = 'contigu' if sens == 1 else 'contigu-'
pickle.dump(out, open(os.path.join(TMP, 'frlg_table%s.pkl' % SUF), 'wb'))
import collections
print(len(out), collections.Counter((v['mode'] or 'aucun').split('~')[0] for v in out.values()))
