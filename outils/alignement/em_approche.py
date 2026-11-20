#!/usr/bin/env python3
"""Correspondance approchée HnS -> Émeraude US -> Émeraude FR, avec adaptation minimale (lot A).

Pour les msgid (3 mots ou plus) sans correspondance exacte : texte Émeraude US le plus proche (rapidfuzz)
parmi ceux dont le FR officiel est connu (table octets EN->FR étendue d'em_candidats.py).
  - identique à la casse, la ponctuation et la mise en page près : FR officiel repris tel quel ;
  - sinon, différences limitées à des noms propres (FR connu des deux côtés), des nombres ou des codes :
    FR officiel retouché sur ces seuls points ;
  - sinon (phrase ajoutée, sens différent) : douteux (score >= 88) ou ignoré.
Sortie : $TMP/em_approche.pkl {msgid: entrée JSON + '_dest' ('adapte' ou 'douteux')}
"""
import os, sys, re, pickle, collections, difflib, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from em_commun import (TMP, MEM, G, CODE, charger_po, deja_emeraude, officiel, controle, codes_octets, mise_en_page)
from rapidfuzz import process, fuzz

tm = pickle.load(open(os.path.join(TMP, 'tm_em_bytes_v2.pkl'), 'rb'))
cand = pickle.load(open(os.path.join(TMP, 'em_cand.pkl'), 'rb'))
tabs = pickle.load(open(os.path.join(TMP, 'em_tables.pkl'), 'rb'))['res']
po = charger_po()


def sans_acc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))


def norm(s):
    s = re.sub(r'\{[^}]*\}|\\[nlp]', ' ', sans_acc(s.lower()))
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', s)).strip()


MOTS_EN = set('the you your with and that this what have will are was please let here there would could should from they them their we our is of to in for be not all one just if at who how when why where now up out about get got did can no yes'.split())


def anglais(t):
    mots = [w.lower() for w in re.findall(r"[A-Za-z]+", CODE.sub(' ', t))]
    return len(mots) >= 2 and sum(w in MOTS_EN for w in mots) >= max(2, 0.25 * len(mots))


# ---------------------------------------------------------------- sources Émeraude (EN -> FR officiel)
src = {}
for eb, fb in tm.items():
    e = G.decode(eb)
    if not e or len(re.findall('[A-Za-z]+', CODE.sub('', e))) < 3: continue
    f = G.decode(fb, e)
    if not f or anglais(f) or controle(e, f): continue
    src.setdefault(norm(e), (e, f, eb))
keys = list(src)

# dictionnaires de noms : Émeraude (EN -> FR, capitales) et SoulSilver (EN -> FR)
D_em = {}
for eb, fb in tm.items():
    e = G.decode(eb); f = G.decode(fb, e or '')
    if e and f and re.fullmatch(r"[A-Z][A-Z .'’&\-é]{1,20}", e) and len(e.split()) <= 3 and re.fullmatch(r"[A-ZÀ-Ý][A-ZÀ-Ýé .'’&\-]{1,24}", f):
        D_em.setdefault(e.upper(), f)
D_ss = {}
for b, i, e, f in pickle.load(open(os.path.join(MEM, 'tm_ss_pairs.pkl'), 'rb')):
    if b in (279, 27, 310, 730, 222, 750, 720, 237) and e and f and len(e.split()) <= 3 and '{' not in e and '\\' not in e:
        D_ss.setdefault(sans_acc(e).upper().replace('’', "'"), f.strip())
D_ss.update({'PROF. OAK': 'Prof. Chen', 'OAK': 'Chen', 'PROF. ELM': 'Prof. Orme', 'ELM': 'Orme'})

TOK = re.compile(r"\{[^}]*\}|[A-Za-zÀ-ÿé0-9]+(?:['’][A-Za-z]+)?|[^\sA-Za-z0-9]")


def toks(s):
    return TOK.findall(re.sub(r'\\[nlp]', ' ', s))


def est_nom(ts):
    t = ' '.join(ts)
    return bool(ts) and all(re.fullmatch(r"[A-Z][A-Z'’\-é]*|[.&]", x) for x in ts) and len(t) >= 2 and ts[0] not in '.&'


def remplace_ci(texte, ancien, nouveau):
    """remplace `ancien` (insensible à la casse et aux accents) dans `texte` ; None si absent"""
    nt = sans_acc(texte).upper(); na = sans_acc(ancien).upper().replace('’', "'")
    nt2 = nt.replace('’', "'")
    i = nt2.find(na)
    if i < 0: return None
    return texte[:i] + nouveau + texte[i + len(ancien):]


def adapter(en_h, en_e, fr_e):
    """renvoie (fr_adapté, [modifs]) ou (None, raison)"""
    a, b = toks(en_e), toks(en_h)
    sm = difflib.SequenceMatcher(None, [x.lower().replace('’', "'") for x in a], [x.lower().replace('’', "'") for x in b], autojunk=False)
    fr = fr_e; mods = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal': continue
        old, new = a[i1:i2], b[j1:j2]
        if all(not re.search(r'[A-Za-z0-9{]', x) for x in old + new):
            continue                                   # ponctuation seulement
        if op == 'replace' and len(old) == 1 and len(new) == 1 and old[0].isdigit() and new[0].isdigit():
            if fr.count(old[0]) != 1: return None, 'nombre %s introuvable/ambigu dans le FR' % old[0]
            fr = fr.replace(old[0], new[0]); mods.append('%s→%s' % (old[0], new[0])); continue
        if op == 'replace' and len(old) == 1 and len(new) == 1 and old[0].startswith('{') and new[0].startswith('{'):
            if fr.count(old[0]) < 1: return None, 'code %s absent du FR' % old[0]
            fr = fr.replace(old[0], new[0]); mods.append('%s→%s' % (old[0], new[0])); continue
        if op == 'replace' and est_nom(old) and est_nom(new):
            o, n = ' '.join(old).replace(' .', '.').rstrip('.'), ' '.join(new).replace(' .', '.').rstrip('.')
            fo = D_em.get(o.upper()) or D_em.get(o.upper() + '.')
            fn = D_ss.get(sans_acc(n).upper()) or D_em.get(n.upper())
            if not fo: return None, 'FR Émeraude de « %s » inconnu' % o
            if not fn: return None, 'FR de « %s » inconnu' % n
            r = remplace_ci(fr, fo, fn)
            if r is None: return None, '« %s » absent du FR officiel' % fo
            fr = r; mods.append('%s→%s' % (fo, fn)); continue
        if all(x.lower() in ('pokémon', 'pokemon', 'the', 'a', 'an') or not re.search(r'[A-Za-z0-9{]', x) for x in old + new):
            continue
        return None, 'différence de texte : « %s » / « %s »' % (' '.join(old), ' '.join(new))
    return fr, mods


out = {}
st = collections.Counter()
for (c, m), info in po.items():
    if c or deja_emeraude(info) or m in cand or m in tabs: continue
    if len(re.findall('[A-Za-z]+', CODE.sub('', m))) < 3: continue
    n = norm(m)
    if n in src:
        score = 100; key = n
    else:
        r = process.extractOne(n, keys, scorer=fuzz.ratio, score_cutoff=85)
        if not r: continue
        key, score = r[0], r[1]
    en_e, fr_e, eb = src[key]
    if en_e == m: continue
    fr2, mods = adapter(m, en_e, fr_e)
    preuve = 'anglais Émeraude : « %s » ; FR officiel : « %s »' % (en_e, fr_e)
    note = 'correspondance approchée (%d %%)' % score
    if fr2 is None:
        if score >= 88:
            out[m] = {'msgid': m, 'msgstr': officiel(fr_e, m), 'source': 'Émeraude FR officiel (adapté)', 'preuve': preuve,
                      'note': note + ' ; adaptation automatique impossible : ' + mods + ' (FR officiel non retouché, à adapter à la main)', '_dest': 'douteux'}
            st['douteux'] += 1
        else:
            st['ignoré'] += 1
        continue
    # codes : si le FR n'a pas les mêmes codes, essayer la correspondance 1:1 des codes anglais
    if codes_octets(fr2) != codes_octets(m):
        ce, ch = CODE.findall(en_e), CODE.findall(m)
        if len(ce) == len(ch) and all(fr2.count(x) >= 1 for x in set(ce)):
            mp = dict(zip(ce, ch))
            if len({mp[x] for x in ce}) == len(set(ce)):
                fr2 = CODE.sub(lambda mm: mp.get(mm.group(0), mm.group(0)), fr2)
                mods.append('codes ' + ', '.join('%s→%s' % kv for kv in mp.items() if kv[0] != kv[1]))
    pb = controle(m, fr2)
    txt = officiel(fr2, m)
    txt, n2 = mise_en_page(txt, m)
    d = {'msgid': m, 'msgstr': txt, 'source': 'Émeraude FR officiel (adapté)' if mods else 'Émeraude FR officiel', 'preuve': preuve}
    notes = [note]
    if mods: notes.append('adapté : ' + ' ; '.join(mods))
    else: notes.append('même texte que dans Émeraude à la casse, ponctuation ou mise en page près')
    notes += n2
    if pb:
        d['note'] = ' ; '.join(notes + ['contrôle : ' + ', '.join(pb)]); d['_dest'] = 'douteux'; st['douteux (contrôle)'] += 1
    else:
        d['note'] = ' ; '.join(notes); d['_dest'] = 'adapte'; st['adapté' if mods else 'identique (casse/ponctuation)'] += 1
    out[m] = d
pickle.dump(out, open(os.path.join(TMP, 'em_approche.pkl'), 'wb'))
print(dict(st), file=sys.stderr)
