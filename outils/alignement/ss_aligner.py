#!/usr/bin/env python3
"""Lot B : ré-alignement des textes Heart & Soul sur SoulSilver FR officiel.

  ss_aligner.py --travail <dossier de ss_paires.py> [--sortie traductions/lots/B_soulsilver]

Lit les .po (entrées qui ne viennent pas d'un officiel), les paires HGSS EN ↔ SS FR (ss_paires.json)
et écrit exact.json, adapte.json, douteux.json (+ candidats_*.json de travail dans --travail).
Les noms (Dresseurs, classes, lieux…) sont traités par ss_noms.py.

Méthodes :
  exact   anglais normalisé identique à un message HGSS entier → français SS converti ;
  adapté  même texte à l'interlocuteur près (« ELM: » ajouté/retiré), extrait de pages d'un message
          (même nombre de pages EN/FR), ou approché (rapidfuzz) avec substitution de noms/nombres ;
  douteux tout le reste au-dessus du seuil, avec la raison.
"""
import os, re, sys, json, random, difflib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ss_commun import *   # noqa

EXCL_TEXTE = {802, 440, 812, 813, 814, 815, 729, 27, 310, 246}
SEUIL_FLOU = 80
SEUIL_DOUTEUX = 88

G = None
CM = None
VALIDES = set()
EXCLUS = {}


def opt(args, n, d=None):
    if n in args:
        i = args.index(n); v = args[i + 1]; del args[i:i + 2]; return v
    return d


def brut(s):
    return s.replace('\n', '\\n').replace('\r', '\\r').replace('\f', '\\f')


# ------------------------------------------------------------ dictionnaire de termes EN → FR
def termes(en, fr):
    """noms propres et termes : clé = anglais normalisé → (français, type). Ambigus exclus."""
    cand = collections.defaultdict(collections.Counter)
    kinds = {}
    banks = {222: 'objet', 237: 'espèce', 750: 'capacité', 720: 'talent', 279: 'lieu', 730: 'classe',
             729: 'personnage'}
    for b, kind in banks.items():
        for e, f in zip(en[str(b)], fr[str(b)]):
            e = e.replace('{TRNAME}', '').strip(); f = f.replace('{TRNAME}', '').strip()
            if not e or not f or '{' in e: continue
            k = norm(e)
            if not k: continue
            cand[k][f] += 1; kinds.setdefault(k, kind)
    # interlocuteurs des dialogues HGSS (« Professor Elm: » ↔ « Prof. Orme: »)
    for b in en:
        if int(b) in EXCL_TEXTE: continue
        for e, f in zip(en[b], fr[b] or []):
            me = re.match(r"^([A-Z][\w.’' -]{1,22}): ", e); mf = re.match(r"^([A-ZÉ][\w.’' -]{1,22}): ", f or '')
            if me and mf:
                k = norm(me.group(1))
                cand[k][mf.group(1)] += 1; kinds.setdefault(k, 'interlocuteur')
    out = {}
    for k, c in cand.items():
        (f, n), = c.most_common(1)
        if len(c) == 1 or n >= 0.8 * sum(c.values()):
            out[k] = (f, kinds[k])
    return out


# ------------------------------------------------------------ unités HGSS
def unites(paires):
    """[(norm, b, i, sorte, en, fr, détail)] : messages entiers, extraits de pages, paires consécutives."""
    U = []
    parb = collections.defaultdict(dict)
    for b, i, e, f in paires:
        if b in EXCL_TEXTE: continue
        parb[b][i] = (e, f)
        U.append((norm(e), b, i, 'msg', e, f, ''))
        pe = [x for x in re.split(r'\r', e)]; pf = [x for x in re.split(r'\r', f)]
        if pe and pe[-1] == '': pe.pop()
        if pf and pf[-1] == '': pf.pop()
        if len(pe) == len(pf) and 1 < len(pe) <= 30:
            for a in range(len(pe)):
                for z in range(a, len(pe)):
                    if a == 0 and z == len(pe) - 1: continue
                    ee = '\r'.join(pe[a:z + 1]); ff = '\r'.join(pf[a:z + 1])
                    U.append((norm(ee), b, i, 'pages', ee, ff, 'pages %d-%d/%d' % (a + 1, z + 1, len(pe))))
    for b, d in parb.items():
        for i in d:
            if i + 1 in d:
                (e1, f1), (e2, f2) = d[i], d[i + 1]
                U.append((norm(e1 + ' ' + e2), b, i, 'concat', e1.rstrip('\r') + '\r' + e2, f1.rstrip('\r') + '\r' + f2,
                          'messages %d+%d' % (i, i + 1)))
    def plausible(u):
        e, f = u[4], u[5]
        if re.fullmatch(r'\s*(Non utilisé|Inutilisé|Pas utilisé|Dummy|-+)\s*\.?', CODE.sub('', f), re.I): return False
        le, lf = len(CODE.sub('', e)), len(CODE.sub('', f))
        if le >= 15 and not (0.4 <= lf / max(le, 1) <= 2.6): return False
        if u[3] != 'msg' and len(u[0].split()) < 5: return False
        return True
    return [u for u in U if u[0] and plausible(u)]


# ------------------------------------------------------------ interlocuteurs
PRE_HNS = re.compile(r"^((?:\{(?:COLOR|SHADOW|COLOR_HIGHLIGHT_SHADOW)[^}]*\})*)([A-Z][A-Z0-9.’'é& -]{0,20}[A-Z.]|\{PLAYER\}|\{RIVAL\}|\{STR_VAR_\d\}): ")
PRE_HGSS = re.compile(r"^([A-Z][\w.’' -]{0,22}[\w.]|\{STRVAR_1 \d+, \d+, \d+\}): ")
PRE_FR = re.compile(r"^([A-ZÉ][\w.’' -]{0,22}[\w.]|\{STRVAR_1 \d+, \d+, \d+\}) ?: ")


def couper_hns(h):
    m = PRE_HNS.match(h)
    if not m: return '', '', h
    return m.group(1), m.group(2), h[m.end():]


def couper(s, rx):
    m = rx.match(s)
    if not m: return '', s
    return m.group(1), s[m.end():]


# ------------------------------------------------------------ substitutions
FR_TERME = None


LEGER = {'the', 'a', 'an', 'type', 'city', 'town'}          # mots qu'on peut ajouter/retirer
EQUIV = {frozenset(x) for x in (('s', 'is'), ('s', 'has'), ('re', 'are'), ('ll', 'will'), ('ve', 'have'), ('m', 'am'),
                                ('d', 'would'), ('d', 'had'), ('t', 'not'), ('nt', 'not'), ('a', 'the'), ('an', 'the'))}
ABREV = {'professor': 'prof', 'mister': 'mr', 'department': 'dept', 'okay': 'ok', 'rt': 'route'}


def compact(s):
    return ''.join(ABREV.get(w, w) for w in norm(s).split())


def norm_v(s):
    """comme norm, mais chaque variable (HnS ou HGSS) devient le mot « zv »."""
    s = STRV.sub(' zv ', s)
    s = VARIABLE_HNS.sub(' zv ', s)
    return [ABREV.get(w, w) for w in norm(s).split()]


VOY = re.compile(r"^[AEIOUYÉÈÊÂÎÔaeiouyéèêâîôhH]")


def elision_ok(avant, ancien, nouveau):
    """le mot qui précède reste correct (de/d’, le/l’, ce/cet, du/de l’…) après la substitution."""
    if bool(VOY.match(ancien)) == bool(VOY.match(nouveau)): return True
    if re.search(r"(?:^|[\s(“])(de|le|la|que|ce|je|ne|me|te|se|du|au|jusque|lorsque|puisque)\s+$", avant, re.I): return False
    if re.search(r"(?:^|[\s(“])(d|l|qu|j|n|m|t|s|jusqu|lorsqu|puisqu)[’']\s*$", avant, re.I): return False
    return True


def substituer(hc, ec, fc, T):
    """rend (ec', fc', notes) : même sens que hc après retouche de noms, nombres, variables, ou None."""
    if compact(hc) == compact(ec):
        return ec, fc, ['anglais identique aux espaces/abréviations près']
    ht, et = norm_v(hc), norm_v(ec)
    sm = difflib.SequenceMatcher(None, et, ht, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
    if not ops or len(ops) > 3: return None
    notes = []; fc2 = fc; ec2 = ec
    strv = list(STRV.finditer(ec))
    for tag, i1, i2, j1, j2 in ops:
        eo_t, hn_t = et[i1:i2], ht[j1:j2]
        if (tag in ('insert', 'delete') and set(eo_t) | set(hn_t) <= LEGER) or (
                tag == 'replace' and len(eo_t) == len(hn_t) and all(x == y or frozenset((x, y)) in EQUIV for x, y in zip(eo_t, hn_t))):
            notes.append('formulation anglaise : « %s » / « %s »' % (' '.join(eo_t), ' '.join(hn_t))); continue
        if tag != 'replace': return None
        # variable HGSS ↔ texte en dur dans HnS
        if eo_t == ['zv'] and 'zv' not in hn_t:
            k = et[:i1].count('zv')
            if k >= len(strv): return None
            m = strv[k]; key = (m.group(1), m.group(3))
            occ = [x for x in STRV.finditer(fc2) if (x.group(1), x.group(3)) == key]
            hn = ' '.join(hn_t)
            if len(occ) != 1: return None
            if hn.replace(' ', '').isdigit():
                mm = re.search(r'(?<![\w])%s(?![\w])' % r'[ ,]?'.join(hn_t), CODE.sub(' ', hc))
                lit = mm.group(0).replace(',', ' ') if mm else hn
            elif hn in T and T[hn][1] in ('lieu', 'objet', 'personnage', 'espèce'):
                lit = T[hn][0]
                if T[hn][1] == 'espèce': lit = lit.upper()
            else:
                return None
            fc2 = fc2.replace(occ[0].group(0), lit)
            ec2 = ec2.replace(m.group(0), ' '.join(hn_t))
            notes.append('variable SS %s → « %s »' % (m.group(0), lit)); continue
        if 'zv' in eo_t or 'zv' in hn_t: return None
        ok = False
        for kl in range(0, 3):
            for kr in range(0, 3):
                a1, a2, b1, b2 = i1 - kl, i2 + kr, j1 - kl, j2 + kr
                if a1 < 0 or b1 < 0 or a2 > len(et) or b2 > len(ht): continue
                eo, hn = ' '.join(et[a1:a2]), ' '.join(ht[b1:b2])
                if 'zv' in eo or 'zv' in hn: continue
                if eo.isdigit() and hn.isdigit():
                    rx = r'(?<![\d,.])%s(?![\d,.])' % eo
                    occ = re.findall(rx, CODE.sub('', fc2))
                    if len(occ) != 1: continue
                    fc2 = re.sub(rx, hn, fc2, count=1)
                    notes.append('nombre %s → %s' % (eo, hn)); ok = True; break
                if eo in T and hn in T:
                    (fo, ko), (fn, kn) = T[eo], T[hn]
                    # personnes : genre, épithètes et pronoms risquent de ne plus s'accorder → pas de substitution
                    if ko != kn or ko in ('personnage', 'interlocuteur', 'classe'): continue
                    if ko == 'lieu':
                        w1, w2 = fo.split(), fn.split()
                        if not (w1[0] == w2[0] or (len(w1) == 1 and len(w2) == 1)): continue
                    rx = re.compile(r'(?<![\wÀ-ÿ])%s(?![\wÀ-ÿ])' % re.escape(fo), re.I)
                    occ = rx.findall(fc2)
                    if len(occ) != 1: continue
                    rep = fn.upper() if occ[0].isupper() and len(occ[0]) > 1 else fn
                    mpos = rx.search(fc2)
                    if not elision_ok(fc2[:mpos.start()], occ[0], rep): continue
                    fc2 = rx.sub(lambda m: rep, fc2, count=1)
                    notes.append('%s → %s' % (occ[0], rep)); ok = True; break
            if ok: break
        if not ok: return None
    return ec2, fc2, notes


# ------------------------------------------------------------ mise en page
def mise_en_page(fr, h, dom):
    """fr : français déjà en syntaxe HnS (\\n \\p). Renvoie (texte, problème)."""
    fragment = h.endswith(('\\n', '\\p', '\\l')) or re.search(r'\{(DYNAMIC|CLEAR_TO)', h)
    une_ligne = not re.search(r'\\[nlp]', h)
    if une_ligne and dom != 'dialogues':
        t = re.sub(r'\\[nlp]', ' ', fr); t = re.sub(r'  +', ' ', t).strip()
        we = G.largeur(h); wf = G.largeur(t)
        if wf > max(we * 1.25, we + 18) and wf > 60:
            return t, 'libellé d’une ligne nettement plus large que l’anglais (%d px > %d px)' % (wf, we)
        return t, None
    if fragment:
        t = fr
        for l in re.split(r'\\[nlp]', t):
            if G.largeur(l) > 198: return t, 'fragment : ligne de plus de 198 px'
        return t, None
    if dom != 'dialogues' and not re.search(r'\\[pl]', h):
        # description à lignes fixes : même nombre de lignes au plus, largeur de l'anglais
        nl = h.count('\\n') + 1
        W = max(G.largeur(l) for l in h.split('\\n'))
        t = G.reformater(re.sub(r'\\[nlp]', ' ', fr), max(W, 100))
        t = t.replace('\\l', '\\n')
        if t.count('\\n') + 1 > nl:
            return t, 'description : %d lignes au lieu de %d' % (t.count('\\n') + 1, nl)
        return t, None
    # mise en page officielle conservée si elle tient en 198 px ; sinon remise en page
    pages = []
    for pg in re.split(r'\\p', fr):
        ls = [l.strip() for l in re.split(r'\\[nl]', pg) if l.strip()]
        pages.append(ls)
    if all(G.largeur(l) <= 198 for ls in pages for l in ls) and all(pages):
        t = '\\p'.join(ls[0] + ''.join(('\\n' if k == 1 else '\\l') + l for k, l in enumerate(ls[1:], 1)) for ls in pages)
        return t, None
    # remise en page : on ne fusionne pas une ligne SS qui finit une phrase ou un titre court
    out = []
    for ls in pages:
        blocs, cur = [], []
        for l in ls:
            cur.append(l)
            if re.search(r'[.!?:…”]$', l) or G.largeur(l) < 100:
                blocs.append(' '.join(cur)); cur = []
        if cur: blocs.append(' '.join(cur))
        lignes = []
        for b in blocs:
            lignes += re.split(r'\\[nl]', G.reformater(b, 198))
        out.append(lignes[0] + ''.join(('\\n' if k == 1 else '\\l') + l for k, l in enumerate(lignes[1:], 1)) if lignes else '')
    return '\\p'.join(out), None


def convertir(h, e, f):
    """h anglais HnS, e anglais HGSS (même sens), f français SS → (msgstr, problème)."""
    t = table_codes(h, e)
    if t is None:
        return None, 'variables différentes (%s / %s)' % (re.findall(VARIABLE_HNS, h), STRV.findall(e))
    s = convertir_fr(f, t)
    if s is None:
        return None, 'code SS sans équivalent'
    return s, None


def finir(h, fr, dom):
    """codes non variables HnS en tête/queue, mise en page, espaces de bord. → (msgstr, problème)."""
    m1 = re.match(r'^((?:\{[^}]*\})*)', h); pre = m1.group(1)
    m2 = re.search(r'((?:\{[^}]*\}|\\[nlp])*)$', h[len(pre):]); suf = m2.group(1)
    milieu = h[len(pre):len(h) - len(suf)]
    if [c for c in autres_codes(milieu)]:
        return None, 'codes de mise en forme au milieu du texte : %s' % autres_codes(milieu)[:3]
    pre_v = [c for c in codes_hns(pre) if VARIABLE_HNS.fullmatch(c)]
    if pre_v:   # une variable en tête fait partie du texte : on ne garde en tête que les codes de forme
        pre = ''.join(c for c in codes_hns(pre) if not VARIABLE_HNS.fullmatch(c))
        if not h.startswith(pre): return None, 'codes de tête mêlés'
    suf_codes = re.sub(r'\\[nlp]', '', suf)
    if [c for c in codes_hns(suf_codes) if VARIABLE_HNS.fullmatch(c)]:
        return None, 'variable en fin de texte'
    corps_h = h[len(pre):len(h) - len(suf)] if suf else h[len(pre):]
    fr = fr.strip()
    fr = re.sub(r'(\\[pn])+$', '', fr)
    t, pb = mise_en_page(fr, corps_h + re.sub(r'\{[^}]*\}', '', suf), dom)
    if t is None: return None, pb
    if corps_h.startswith(' ') and not t.startswith(' '): t = ' ' + t
    if corps_h.endswith(' ') and not t.endswith(' '): t = t + ' '
    return pre + t + suf, pb


def controler(h, s):
    import collections as C
    def cc(x):
        out = C.Counter()
        for c in CODE.findall(x):
            b = G.encode(c)
            if b is None or not b or b[0] >= 0xF7: out[c] += 1
        return out
    if cc(h) != cc(s): return 'codes différents'
    if CM.invalid(s): return 'caractères hors charmap %r' % CM.invalid(s)[:4]
    if nombres(h) != nombres(s): return 'nombres différents (%s / %s)' % (nombres(h), nombres(s))
    for fin in ('\\n', '\\p', '\\l', ' '):
        if h.endswith(fin) and not s.endswith(fin): return 'fin %s non conservée' % fin
    if h.startswith(' ') != s.startswith(' '): return 'espace initiale'
    return None


# ------------------------------------------------------------ alignement d'une entrée sur une unité
def essayer(h, dom, u, T, flou=False, force=False):
    """→ dict(msgstr, sorte, notes, pb) ; sorte ∈ exact, adapte."""
    _, b, i, kind, e, f, det = u
    col, hp, hc = couper_hns(h)
    ep, ec = couper(e, PRE_HGSS)
    fp, fc = couper(f, PRE_FR) if ep else ('', f)
    notes = []
    if det: notes.append(det)
    if norm(hc) != norm(ec):
        if norm(h) == norm(e) and not hp:
            hc, ec, fc, ep, fp = h, e, f, '', ''
        else:
            r = substituer(hc, ec, fc, T)
            if r is None and not force: return None
            if r is None: notes.append('relu à la main : anglais HnS proche, texte SS repris tel quel')
            else:
                ec, fc, nn = r; notes += nn
    # interlocuteur
    pref = ''
    if hp:
        if VARIABLE_HNS.fullmatch(hp):
            if ep and not STRV.fullmatch(ep): return None
            pref = hp
            if not ep: notes.append('interlocuteur %s ajouté' % hp)
        elif ep and fp and (norm(ep) == norm(hp) or norm(hp) in norm(ep).split() or norm(hp).replace('prof ', 'professor ') == norm(ep)
                            or T.get(norm(hp), (None,))[0] == fp):
            pref = fp
        else:
            k = norm(hp)
            nm = T.get(k) or T.get(re.sub(r'^prof ', 'professor ', k))
            if nm and nm[1] not in ('personnage', 'interlocuteur', 'classe'): nm = None
            if not nm: return {'pb': 'interlocuteur %s sans équivalent SS' % hp, 'u': u}
            pref = nm[0]
            notes.append('interlocuteur %s → %s' % (hp, pref))
    elif ep:
        notes.append('interlocuteur SS « %s » retiré' % (fp or ep))
    s, pb = convertir(hc, ec, fc)
    if s is None: return {'pb': pb, 'u': u}
    if pref: s = pref + ': ' + s
    s, pb = finir(h, s, dom)
    if s is None: return {'pb': pb, 'u': u}
    pb2 = controler(h, s)
    adapte = bool(notes) or kind != 'msg' or flou
    return {'msgstr': s, 'sorte': 'adapte' if adapte else 'exact', 'notes': notes, 'pb': pb or pb2, 'u': u}


# ------------------------------------------------------------ contexte des entrées courtes
CONTEXTE_COURT = [
    (re.compile(r'items\.h$|battle_debug\.c$'), {222, 223}),
    (re.compile(r'moves_info\.h$'), {750, 751}),
    (re.compile(r'abilities\.h$'), {720, 721}),
    (re.compile(r'region_map'), {279}),
    (re.compile(r'battle_message\.c$|battle_script'), {197, 368}),
    (re.compile(r'follower_(messages|helper)'), {265}),
]


GENRE = re.compile(r"^(il|elle|ils|elles|le|la|un|une|lui|petit|petite|mon|ma|garçon|fille|monsieur|madame|mademoiselle)$", re.I)


def lettres(s):
    return ' '.join(re.findall(r"[a-zà-ÿœ]+", CODE.sub(' ', s).lower()))


def fuzz_ratio(a, b):
    from rapidfuzz import fuzz
    return fuzz.ratio(a, b)


def registre(s):
    t = bool(re.search(r"(?<![\wÀ-ÿ])(tu|te|t’|toi|ton|ta|tes)(?![\wÀ-ÿ])", s, re.I))
    v = bool(re.search(r"(?<![\wÀ-ÿ])(vous|votre|vos)(?![\wÀ-ÿ])", s, re.I))
    return (t, v)


def genre(a, b):
    """deux variantes qui ne diffèrent que par l'accord masculin/féminin."""
    wa, wb = re.findall(r"[\wÀ-ÿ]+", a), re.findall(r"[\wÀ-ÿ]+", b)
    sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
    for t, i1, i2, j1, j2 in sm.get_opcodes():
        if t == 'equal': continue
        for x, y in zip(wa[i1:i2], wb[j1:j2]):
            if x + 'e' == y or y + 'e' == x or x + 'se' == y[:len(x) + 2] or GENRE.match(x) or GENRE.match(y):
                return True
    return False


def contexte_ok(e, bank):
    for path, _ in e.occurrences:
        for rx, banks in CONTEXTE_COURT:
            if rx.search(path) and bank in banks: return True
    return False


def est_nom(e):
    if all('easy_chat' in path for path, _ in e.occurrences): return True   # mots du Livret (Émeraude)
    for path, line in e.occurrences:
        if path.endswith('.party') or path.endswith('region_map_sections.json'): return True
        if path == 'src/battle_main.c': return True
    return False


def ligne_src(path, line, cache={}):
    if path not in cache:
        try: cache[path] = open(os.path.join(P, 'build', 'upstream_orig', path), encoding='utf-8', errors='replace').read().split('\n')
        except FileNotFoundError: cache[path] = []
    L = cache[path]
    return L[line - 1] if 0 < line <= len(L) else ''


def est_champ_nom(e):
    """nom d'objet/capacité/talent/espèce : traité par ss_noms.py."""
    for path, line in e.occurrences:
        try: src = ligne_src(path, int(line))
        except ValueError: continue
        if re.search(r'\.(name|speciesName)\s*=', src) and re.search(r'items\.h|moves_info\.h|abilities\.h|species_info', path):
            return True
    return False


def entree(d, e, msgstr, source, preuve, note):
    o = {'msgid': e.msgid}
    if e.msgctxt: o['msgctxt'] = e.msgctxt
    o.update({'msgstr': msgstr, 'source': source,
              'fichier': e.occurrences[0][0] if e.occurrences else '',
              'ligne': int(e.occurrences[0][1]) if e.occurrences and str(e.occurrences[0][1]).isdigit() else 0})
    if e.msgstr: o['ancien'] = e.msgstr
    o['preuve'] = preuve
    if note: o['note'] = note
    o['_domaine'] = d
    o['_source_po'] = source_po(e.comment) or 'non traduit'
    return o


def main():
    global G, CM
    args = sys.argv[1:]
    trav = opt(args, '--travail')
    sortie = opt(args, '--sortie', os.path.join(P, 'traductions', 'lots', 'B_soulsilver'))
    os.makedirs(sortie, exist_ok=True)
    G = gen3()
    import hnsfr
    CM = hnsfr.Charmap(os.path.join(P, 'build', 'upstream_orig'))
    en = json.load(open(os.path.join(trav, 'ss_en.json'), encoding='utf-8'))
    fr = json.load(open(os.path.join(trav, 'ss_fr.json'), encoding='utf-8'))
    paires = json.load(open(os.path.join(trav, 'ss_paires.json'), encoding='utf-8'))
    global VALIDES
    fv = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ss_valides.json')
    jv = json.load(open(fv, encoding='utf-8')) if os.path.exists(fv) else {}
    VALIDES = set(jv.get('msgids', [])); EXCLUS.update(jv.get('exclus', {}))
    T = termes(en, fr)
    U = unites(paires)
    idx = collections.defaultdict(list)
    for k, u in enumerate(U): idx[u[0]].append(k)
    print('unités', len(U), 'termes', len(T))
    ents = [(d, e) for d, e in charger_po() if dans_perimetre(e) and not est_nom(e) and not est_champ_nom(e)]
    print('entrées examinées', len(ents))
    exact, adapte, douteux = [], [], []
    reste = []
    stats = collections.Counter()

    def ranger(d, e, res_list, flou=False):
        if e.msgid in EXCLUS:
            r = next((r for r in res_list if r and r.get('msgstr')), None)
            if r:
                u = r['u']
                douteux.append(entree(d, e, r['msgstr'], 'SoulSilver FR officiel', '%d:%d — %s' % (u[1], u[2], brut(u[5])),
                                      'écarté à la relecture : ' + EXCLUS[e.msgid]))
                stats['exclu_relecture'] += 1; return True
        ok = [r for r in res_list if r and 'msgstr' in r and not r['pb']]
        if ok:
            # préférence : exact > adapté ; message entier > pages > concaténation
            rang = {'msg': 0, 'pages': 1, 'concat': 2}
            ok.sort(key=lambda r: (r['sorte'] != 'exact', rang[r['u'][3]], len(r['notes'])))
            best = ok[0]
            vals = collections.Counter(r['msgstr'] for r in ok if r['sorte'] == best['sorte'] and r['u'][3] == best['u'][3])
            u = best['u']
            preuve = '%d:%d — %s' % (u[1], u[2], brut(u[5]))
            note = '; '.join(best['notes'])
            if len(vals) > 1:
                top = vals.most_common(2)
                v1, v2 = top[0][0], top[1][0]
                if v1.lower() == v2.lower():
                    # mêmes mots, casse différente (BRUME / Brume) : graphie SoulSilver en casse normale
                    top = sorted(top, key=lambda x: sum(c.isupper() for c in x[0]))
                    top = [(top[0][0], top[0][1] + top[1][1] + 1)] + top[1:]
                elif genre(v1, v2) or registre(v1) != registre(v2):
                    top = [(v1, 1), (v2, 1)]
                elif len({r['u'][1] for r in ok}) > 1 and fuzz_ratio(lettres(v1), lettres(v2)) < 80:
                    top = [(v1, 1), (v2, 1)]
                else:
                    # même banque, même contexte : variantes équivalentes, on garde la première
                    top = sorted(top, key=lambda x: min(r['u'][2] for r in ok if r['msgstr'] == x[0]))
                    top = [(top[0][0], top[0][1] + 1)] + top[1:]
                if top[0][1] == top[1][1]:
                    alts = ' | '.join('%s' % v for v, _ in top)
                    douteux.append(entree(d, e, best['msgstr'], 'SoulSilver FR officiel (adapté)' if best['sorte'] == 'adapte' else 'SoulSilver FR officiel', preuve,
                                          'même anglais, plusieurs français SS : ' + alts))
                    stats['douteux_ambigu'] += 1; return True
                best = next(r for r in ok if r['msgstr'] == top[0][0]); u = best['u']
                preuve = '%d:%d — %s' % (u[1], u[2], brut(u[5]))
                autres = [v for v in vals if v != top[0][0]]
                note = ('; '.join(best['notes']) + '; ' if best['notes'] else '') + 'autre(s) variante(s) SS : ' + ' | '.join(autres[:2])
            court = len(norm(e.msgid).split()) <= 2
            if court and not contexte_ok(e, u[1]):
                stats['rejet_court_sans_contexte'] += 1; return True
            src = 'SoulSilver FR officiel' if best['sorte'] == 'exact' else 'SoulSilver FR officiel (adapté)'
            (exact if best['sorte'] == 'exact' else adapte).append(entree(d, e, best['msgstr'], src, preuve, note))
            stats[best['sorte'] + ('_flou' if flou else '')] += 1
            return True
        avec_pb = [r for r in res_list if r and r.get('pb')]
        if avec_pb:
            r = avec_pb[0]; u = r['u']
            douteux.append(entree(d, e, r.get('msgstr') or '', 'SoulSilver FR officiel (adapté)',
                                  '%d:%d — %s' % (u[1], u[2], brut(u[5])), 'correspondance trouvée mais ' + r['pb']))
            stats['douteux_pb'] += 1
            return True
        return False

    for d, e in ents:
        n = norm(e.msgid)
        if not n: continue
        ks = idx.get(n, [])
        if not ks:
            # sans l'interlocuteur HnS
            col, hp, hc = couper_hns(e.msgid)
            if hp: ks = idx.get(norm(hc), [])
        if ks:
            res = [essayer(e.msgid, d, U[k], T) for k in ks[:40]]
            if ranger(d, e, res): continue
        reste.append((d, e))
    print('après exact :', dict(stats), 'reste', len(reste))

    # ---------------------------------------------------------------- approché
    from rapidfuzz import process, fuzz
    import numpy as np
    cand_k = [k for k, u in enumerate(U) if u[3] in ('msg', 'pages') and len(u[0].split()) >= 3]
    # pages : seulement les pages simples et les messages entiers pour limiter la taille
    cand_k = [k for k in cand_k if U[k][3] == 'msg' or re.match(r'pages (\d+)-\1/', U[k][6])]
    choix = [U[k][0] for k in cand_k]
    q = [(d, e) for d, e in reste if len(norm(e.msgid).split()) >= 4]
    qn = []
    for d, e in q:
        col, hp, hc = couper_hns(e.msgid)
        qn.append(norm(hc))
    for a in range(0, len(q), 1500):
        M = process.cdist(qn[a:a + 1500], choix, scorer=fuzz.ratio, workers=-1, score_cutoff=SEUIL_FLOU, dtype=np.uint8)
        for r in range(M.shape[0]):
            row = M[r]
            top = np.argsort(row)[::-1][:6]
            top = [t for t in top if row[t] >= SEUIL_FLOU]
            if not top: continue
            d, e = q[a + r]
            res = [essayer(e.msgid, d, U[cand_k[t]], T, flou=True) for t in top]
            if ranger(d, e, res, flou=True): continue
            if e.msgid in VALIDES:
                res = [essayer(e.msgid, d, U[cand_k[top[0]]], T, flou=True, force=True)]
                if ranger(d, e, res, flou=True):
                    stats['valide_main'] += 1; continue
            t = top[0]
            if row[t] >= SEUIL_DOUTEUX:
                u = U[cand_k[t]]
                douteux.append(entree(d, e, '', 'SoulSilver FR officiel (adapté)', '%d:%d — %s' % (u[1], u[2], brut(u[5])),
                                      'proche (%d %%) mais non adaptable automatiquement ; anglais HGSS : %s' % (row[t], brut(u[4]))))
                stats['douteux_flou'] += 1
    print('fin :', dict(stats))
    for nom, L in (('exact', exact), ('adapte', adapte), ('douteux_textes', douteux)):
        json.dump(L, open(os.path.join(trav, 'cand_%s.json' % nom), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump({k: list(v) for k, v in T.items()}, open(os.path.join(trav, 'termes.json'), 'w', encoding='utf-8'), ensure_ascii=False)


if __name__ == '__main__':
    main()
