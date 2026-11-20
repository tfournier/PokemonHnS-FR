#!/usr/bin/env python3
"""Lot F : msgid FRLG du hack -> texte pokefirered (même étiquette, sinon même texte) -> texte Rouge Feu FR.

Entrées : build/lotF/frlg_table.pkl (frlg_table.py), traductions/*.po, build/upstream_orig.
Sortie : build/lotF/frlg_paires.pkl = liste de dict(cle, info, occ, label, sym, mode, score, en_pfr, fr_brut, fr_adr)
"""
import os, sys, re, pickle, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frlg_commun import ROOT, TMP
import em_commun
from em_commun import charger_po
import hnsfr
from rapidfuzz import fuzz, process

TABLES = {'fr': pickle.load(open(os.path.join(TMP, 'frlg_table.pkl'), 'rb')),
          'lg': pickle.load(open(os.path.join(TMP, 'frlg_table_lg.pkl'), 'rb'))}
po = charger_po()


def frlg(p):
    return '_Frlg' in p or 'frlg' in p.lower() or 'trainer_tower' in p


PLACE = re.compile(r'\{(PLAYER|RIVAL|STR_VAR_\d|B_[A-Z_0-9]+|KUN)\}')


def norm(s):
    """texte comparé sans les codes de mise en forme (police, couleur, musique : leurs noms et valeurs
    diffèrent entre pokefirered et pokeemerald-expansion) ; les variables ({PLAYER}…) sont gardées."""
    s = re.sub(r'\{[^}]*\}', lambda m: m.group(0) if PLACE.fullmatch(m.group(0)) else ' ', s)
    s = s.replace('’', "'").replace('$', '')
    s = re.sub(r'\\[nlp]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip().lower()
    return s


# --- étiquettes du hack
_cache = {}
def occs(path):
    if path not in _cache:
        lst = hnsfr.scan_file(ROOT, path)
        txt = open(os.path.join(ROOT, path), encoding='utf-8').read()
        lines = txt.split('\n')
        res = {}
        for o in lst:
            lab = None
            if o.kind == 'inc':
                for i in range(o.line - 1, max(-1, o.line - 400), -1):
                    m = re.match(r'^(\w+):{1,2}\s*(@.*)?$', lines[i])
                    if m: lab = m.group(1); break
            elif o.kind == 'c':
                avant = txt[max(0, o.start - 300):o.start]
                m = re.search(r'(\w+)\s*\[[^\]]*\]\s*=\s*_?\(?\s*"?$', avant.rstrip(' \t"(_'))
                m = re.search(r'(\w+)\s*\[[^\]]*\]\s*=\s*_\(\s*$', avant)
                if m: lab = m.group(1)
            res.setdefault(o.line, []).append((o, lab))
        _cache[path] = res
    return _cache[path]


idx = collections.defaultdict(list)
for ver, table in TABLES.items():
    for nom, v in table.items():
        if v['fr_txt']: idx[norm(v['en'])].append((ver, nom))
cles_norm = list(idx)


def table_texte(msgid):
    """pas de recherche par texte pour les noms (Dresseurs) : traités par table"""
    return len(msgid.split()) >= 2 or len(msgid) >= 12


paires = []; stats = collections.Counter()
for cle, info in po.items():
    occ = [(p, l) for p, l in info['occ'] if frlg(p)]
    if not occ: continue
    src = info['source']
    if src in ('Émeraude FR officiel', 'SoulSilver FR officiel'): continue
    if src.endswith('(adapté)') and not all(frlg(p) for p, l in info['occ']): continue
    msgid = cle[1]
    if all(p.endswith('.party') or 'trainer_tower' in p for p, l in occ):
        continue   # noms de Dresseurs : frlg_noms.py
    labs = []
    for p, l in occ:
        cands = occs(p).get(l, []) if l else [x for v in occs(p).values() for x in v]   # ligne 0 : toutes
        for o, lab in cands:
            if o.text == msgid and lab and lab not in labs: labs.append(lab)
    n = norm(msgid)
    res = None
    for lab in labs:
        for ver, table in TABLES.items():
            v = table.get(lab)
            if v and v['fr_txt']:
                sc = fuzz.ratio(n, norm(v['en']))
                if res is None or sc > res['score']:
                    res = dict(label=lab, sym=lab, ver=ver, mode='étiquette', score=sc)
    if (res is None or res['score'] < 100) and table_texte(msgid):
        if n in idx:
            noms = idx[n]
            frs = sorted({TABLES[v][x]['fr_txt'] for v, x in noms})
            ver, nom = noms[0]
            res = dict(label=labs[0] if labs else None, sym=nom, ver=ver, mode='texte' if len(frs) == 1 else 'texte~%d' % len(frs),
                       score=100, variantes=frs if len(frs) > 1 else None)
        elif len(n) >= 12:
            r = process.extractOne(n, cles_norm, scorer=fuzz.ratio, score_cutoff=85)
            if r and (res is None or r[1] > res['score']):
                ver, nom = idx[r[0]][0]
                res = dict(label=labs[0] if labs else None, sym=nom, ver=ver, mode='approché', score=r[1])
    if res is None:
        stats['non trouvé'] += 1
        paires.append(dict(cle=cle, info=info, occ=occ, label=labs[0] if labs else None, mode=None)); continue
    v = TABLES[res['ver']][res['sym']]
    res.update(cle=cle, info=info, occ=occ, en_pfr=v['en'], fr_brut=v['fr_txt'], fr_adr=v['fr'], us_adr=v['us'], tmode=v['mode'])
    paires.append(res); stats[res['mode'].split('~')[0] + (' exact' if res['score'] == 100 else ' ≥90' if res['score'] >= 90 else ' <90')] += 1
pickle.dump(paires, open(os.path.join(TMP, 'frlg_paires.pkl'), 'wb'))
print(len(paires), stats.most_common())
