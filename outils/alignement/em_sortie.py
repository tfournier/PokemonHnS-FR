#!/usr/bin/env python3
"""Décision, contrôles, passage au style et écriture des sorties du lot A.

Entrées : $TMP/em_cand.pkl (em_candidats.py), $TMP/em_tables.pkl (em_tables.py), $TMP/em_approche.pkl (em_approche.py, facultatif)
Sorties : traductions/lots/A_emeraude/{exact,contexte,tables,adapte,douteux}.json, $TMP/em_stats.pkl, $TMP/echantillons/*.tsv
"""
import os, sys, re, pickle, collections, random, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from em_commun import (mise_en_page, vocabulaire, proteges, gl_esp, style, TMP, G, ROOT, CODE, charger_po, deja_emeraude, officiel, controle, codes_octets, nombres,
                       zone, ecrire, entree, hnsfr, roms, LOT)
import verifier
VERIF = verifier.Verif(ROOT)

us, fr = roms()
cand = pickle.load(open(os.path.join(TMP, 'em_cand.pkl'), 'rb'))
_t = pickle.load(open(os.path.join(TMP, 'em_tables.pkl'), 'rb'))
tabs, PLAGES = _t['res'], _t['plages']
PERSONNES = ('gTrainers', 'gBattleFrontierTrainers', 'gBattleTent', 'gContestOpponents.trainerName', 'gDefaultContestWinners.trainerName',
             'sIngameTrades.otName', 'gApprentices')
SURNOMS = ('gContestOpponents.nickname', 'gDefaultContestWinners.monName', 'sIngameTrades.nickname')
FICHIERS_NOMS = {'src/data/trainers.party', 'src/data/battle_frontier/battle_frontier_trainers.h', 'src/data/battle_frontier/battle_tent.h',
                 'src/data/battle_frontier/trainer_hill.h', 'src/data/contest_opponents.h', 'src/data/battle_frontier/apprentice.h',
                 'src/data/trade.h'}


_DICO = None
def copie_anglaise(m):
    """le texte (identique en FR) est de l'anglais : mot en minuscules, ou mots du dictionnaire anglais"""
    global _DICO
    if _DICO is None:
        _DICO = {l.strip() for l in open('/usr/share/dict/words', errors='ignore') if l.strip().islower()} if os.path.exists('/usr/share/dict/words') else set()
    t = re.sub(r'\{[^}]*\}|\\[nlp]', ' ', m)
    mots = [w.lower() for w in re.findall(r'[A-Za-z]{2,}', t)]
    # phrase en minuscules restée identique : texte non traduit de la ROM FR
    if re.search(r'\b[a-z]{2,}', t) and any(w in _DICO for w in mots): return True
    # libellé : un mot anglais qui n'existe pas en français (CONTROLS, Button, NEXT, RANK…) ; NORMAL, ROUTE… restent
    voc = vocabulaire()
    def base(w):
        for suf in ('ing', 'ers', 'ed', 'es', 's', 'er'):
            if w.endswith(suf) and len(w) - len(suf) >= 3 and w[:-len(suf)] in _DICO: return w[:-len(suf)]
            if w.endswith(suf) and len(w) - len(suf) >= 3 and w[:-len(suf)] + 'e' in _DICO: return w[:-len(suf)] + 'e'
        return w
    return any((w in _DICO or base(w) in _DICO) and (w not in voc or w in ('button', 'buttons')) for w in mots if len(w) >= 3)


def genre_nom(m):
    """msgid utilisé seulement comme nom propre (tables de noms, .party, FRLG)"""
    fm = {p for p, _ in occs.get(m, [])}
    return nom_court(m) and fm and all(p in FICHIERS_NOMS or p.endswith('.party') or 'frlg' in p.lower() or 'trainer_tower' in p for p in fm)


def genre_preuve(pr):
    """'easychat', 'personne', 'surnom' ou '' d'après le libellé de table ou l'adresse US"""
    if pr.startswith('EasyChat'): return 'easychat'
    for x in PERSONNES:
        if pr.startswith(x): return 'personne'
    for x in SURNOMS:
        if pr.startswith(x): return 'surnom'
    mm = re.match(r'US ([0-9A-F]{6})', pr)
    if mm:
        a = int(mm.group(1), 16)
        for lab, b, e in PLAGES:
            if b <= a < e:
                if lab == 'EasyChat': return 'easychat'
                if lab.startswith(PERSONNES): return 'personne'
                if lab.startswith(SURNOMS): return 'surnom'
                if lab.startswith('gPokedexEntries'): return 'categorie'
    return ''
appr = {}
if os.path.exists(os.path.join(TMP, 'em_approche.pkl')):
    appr = pickle.load(open(os.path.join(TMP, 'em_approche.pkl'), 'rb'))
po = charger_po()
occs = collections.defaultdict(list)
for o in hnsfr.scan(ROOT):
    if hnsfr.wanted(o.text): occs[o.text].append((o.path, o.line))

POIDS = {'ptr': 1, 'delta': 1, 'table': 1, 'tidx': 3, 'tm': 1, 'seq': 1, 'seq1': 0.5}
FICHIER = {'ptr': 'exact', 'tm': 'exact', 'delta': 'exact', 'table': 'tables', 'tidx': 'tables', 'seq': 'contexte', 'seq1': 'contexte'}
NUM_EN = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
          'ten': '10', 'first': '1', 'second': '2', 'third': '3', 'fourth': '4', 'fifth': '5', 'once': '1', 'twice': '2',
          'single': '1', 'double': '2', 'triple': '3', 'half': '2'}
NUM_FR = {'un': '1', 'une': '1', 'deux': '2', 'trois': '3', 'quatre': '4', 'cinq': '5', 'six': '6', 'sept': '7', 'huit': '8',
          'neuf': '9', 'dix': '10', 'premier': '1', 'première': '1', 'premiere': '1', 'deuxième': '2', 'deuxieme': '2', 'second': '2', 'seconde': '2',
          'troisième': '3', 'troisieme': '3', 'quatrième': '4', 'cinquième': '5', 'double': '2', 'moitié': '2', 'triple': '3',
          'ile': '', 'île': ''}


def nb_norm(s, table):
    s = CODE.sub(' ', s)
    s = re.sub(r'(\d+)\s*(?:st|nd|rd|th|er|e|re|ème|ᵉ)\b', r'\1', s)
    out = re.findall(r'\d+', s.replace(',', ''))
    for w in re.findall(r"[A-Za-zÀ-ÿ]+", s):
        v = table.get(w.lower())
        if v: out.append(v)
    return sorted(out)


def norm(s):
    return re.sub(r'[^a-z0-9]', '', re.sub(r'\{[^}]*\}|\\[nlp]', '', s.lower().replace('’', "'")))


def textlike(t):
    t2 = re.sub(r'\{[^}]*\}|\\[nlp]', '', t)
    return len(re.findall(r'[A-Za-zÀ-ÿ]', t2)) >= max(1, 0.4 * len(t2.replace(' ', '')))


MOTS_EN = set('''the you your you're you've you'll with and that that's this what have has had will are was were please let
here there would could should been from they them their we our it's don't i'm i've i'll isn't can't won't my is of to in
for be not all one just so if at who how when why where now up out about get got go did can no yes any some
very much more than then too also only well right back over into after before again want know think see look come make hello hi
take give used using battle battles trainer trainers it its she his her him us am do does doesn't didn't'''.split())


def anglais_residuel(en, t):
    """le « français » est de l'anglais (texte resté en anglais dans la ROM FR, souvent inutilisé)"""
    mots = [w.lower() for w in re.findall(r"[A-Za-z’']+", re.sub(r'\{[^}]*\}|\\[nlp]', ' ', t))]
    if len(mots) < 2: return False
    n = sum(1 for w in mots if w.replace('’', "'") in MOTS_EN)
    return n >= 2 and n >= 0.25 * len(mots) or (norm(en) == norm(t) and n >= 1)


def nom_court(en):
    t = CODE.sub('', en).strip()
    return bool(re.fullmatch(r"[A-Z0-9][A-Z0-9 .'’&\-é]{0,14}", t)) and len(t.split()) <= 2


def adapter_codes(en, t):
    """Les CLEAR_TO diffèrent (alignement FR) : on garde les codes anglais. Renvoie (texte, note) ou None."""
    ce = re.findall(r'\{CLEAR_TO [^}]*\}', en); cf = re.findall(r'\{CLEAR_TO [^}]*\}', t)
    if len(ce) != len(cf) or not ce: return None
    it = iter(ce)
    t2 = re.sub(r'\{CLEAR_TO [^}]*\}', lambda m: next(it), t)
    if codes_octets(t2) != codes_octets(en): return None
    return t2, 'code(s) CLEAR_TO d’Émeraude FR (%s) remplacé(s) par ceux de l’anglais' % ', '.join(cf)


# ---------------------------------------------------------------- adresses US de tous les msgid (contexte des noms courts)
import ahocorasick
AC = ahocorasick.Automaton(); encs = {}
for (c, m) in po:
    b = G.encode(m)
    if b and len(b) >= 3: encs[m] = b; AC.add_word((b + b'\xff').decode('latin1'), m)
AC.make_automaton()
addr = []
for e, m in AC.iter(us.decode('latin1')):
    a = e - len(encs[m])
    if us[a - 1] in (0, 0xFF) or not 0xA1 <= us[a - 1] <= 0xEE: addr.append((a, m))
addr.sort()
import bisect
AD = [a for a, _ in addr]


def fichiers_voisins(a, m, r=1500):
    """Counter des fichiers HnS des msgid voisins (adresse US ± r), un vote par msgid voisin"""
    i, j = bisect.bisect_left(AD, a - r), bisect.bisect_right(AD, a + r)
    out = collections.Counter()
    for _, x in addr[i:j]:
        if x != m: out.update({p for p, _ in occs.get(x, [])})
    return out


LARGES = {'src/data', 'src', 'data/text', 'data/scripts', 'data', 'src/data/text'}


def meme_contexte(m, preuves, seuil=0.15):
    """vrai si un fichier HnS du msgid (ou son dossier précis) représente au moins `seuil` des fichiers HnS
    des textes voisins dans Émeraude US ; None si aucun voisin connu"""
    mine = {p for p, _ in occs.get(m, [])}
    dirs = {os.path.dirname(p) for p in mine} - LARGES
    vus = set()
    for pr in preuves:
        mm = re.match(r'US ([0-9A-F]{6})', pr)
        if not mm: continue
        v = fichiers_voisins(int(mm.group(1), 16), m)
        tot = sum(v.values())
        if not tot: continue
        part = sum(n for f, n in v.items() if f in mine or os.path.dirname(f) in dirs) / tot
        if part >= seuil: return True, set(v)
        vus |= set(v)
    return (None if not vus else False), vus


# ---------------------------------------------------------------- décision
sorties = collections.defaultdict(list)
stats = collections.Counter(); par_zone = collections.Counter(); remplace = []
meme_anglais = []; rejets = collections.Counter()
for (c, m), info in po.items():
    if c or deja_emeraude(info): continue
    L = list(cand.get(m, [])) + [(x[0], x[1], x[2]) for x in tabs.get(m, [])]
    tabfiles = {x[2]: x[3] for x in tabs.get(m, [])}
    if not L: continue
    groupes = collections.defaultdict(lambda: {'w': 0, 'meth': set(), 'preuves': [], 'brut': None})
    for meth, fb, pr in L:
        t = G.decode(fb, m)
        if t is None or not t.strip(): rejets['indécodable'] += 1; continue
        if anglais_residuel(m, t): rejets['anglais resté dans la ROM FR'] += 1; continue
        if norm(t) == norm(m) and copie_anglaise(m) and not genre_nom(m):
            rejets['anglais resté dans la ROM FR'] += 1; continue
        if not textlike(t) and textlike(m): rejets['pas du texte'] += 1; continue
        w = POIDS[meth]
        if meth == 'ptr':
            n = re.search(r'x(\d+)', pr); w = int(n.group(1)) if n else 1
        if meth == 'tidx':
            mine = {p for p, _ in occs.get(m, [])}
            if tabfiles.get(pr) not in mine: w = 0.5
        g = groupes[t]; g['w'] += w; g['meth'].add(meth); g['preuves'].append(pr); g['brut'] = t
    if not groupes: stats['candidats rejetés'] += 1; continue
    for g in groupes.values():
        gs = {genre_preuve(pr) for pr in g['preuves'] if not pr.startswith('table octets')}
        g['genre'] = gs.pop() if len(gs) == 1 else ''
    fm0 = {p for p, _ in occs.get(m, [])}
    if fm0 and all(p.startswith('src/data/easy_chat/') for p in fm0):
        for g in groupes.values(): g['genre'] = 'easychat'
    # catégorie du Pokédex d'Émeraude : autre sens (les catégories HnS sont en casse mixte)
    for k in [k for k, g in groupes.items() if g['genre'] == 'categorie']: del groupes[k]
    if not groupes: stats['catégorie Pokédex (autre sens)'] += 1; continue
    if any(g['genre'] != 'easychat' for g in groupes.values()):
        for k in [k for k, g in groupes.items() if g['genre'] == 'easychat']: del groupes[k]
    # une table par index (fichier de la table = fichier du msgid) prime sur les autres correspondances
    ordre = sorted(groupes.items(), key=lambda kv: (-(('tidx' in kv[1]['meth']) and kv[1]['w'] >= 3), -kv[1]['w']))
    t, g = ordre[0]
    tot = sum(x['w'] for _, x in ordre)
    meths = g['meth']
    notes = []; douteux = []
    autres = [(x, y) for x, y in ordre[1:]]
    if autres:
        alt = ' | '.join('« %s » (%s)' % (x.replace('\n', ' ')[:80], '+'.join(sorted(y['meth']))) for x, y in autres[:3])
        def regions(y):
            return {int(r.group(1), 16) >> 15 for pr in y['preuves'] for r in [re.match(r'US ([0-9A-F]{6})', pr)] if r}
        r0 = regions(ordre[0][1])
        autre_table = any(regions(y) - r0 and meme_contexte(m, y['preuves'])[0] for x, y in ordre[1:])
        if 'tidx' in ordre[0][1]['meth'] and ordre[0][1]['w'] >= 3 and not ('tidx' in ordre[1][1]['meth'] and ordre[1][1]['w'] >= 3):
            notes.append('table par index retenue ; autre(s) correspondance(s) : ' + alt)
        elif ordre[1][1]['w'] >= 0.34 * tot or autre_table:
            ctx = [(x, y) for x, y in ordre if meme_contexte(m, y['preuves'])[0]]
            if len(ctx) == 1:
                t, g = ctx[0]; meths = g['meth']
                notes.append('plusieurs textes Émeraude FR pour le même anglais ; retenu celui du même contexte (fichier HnS voisin) ; autres : '
                             + ' | '.join('« %s »' % x.replace('\n', ' ')[:80] for x, y in ordre if x != t)[:300])
                meme_anglais.append((m, [(x, sorted(y['meth']), y['w']) for x, y in ordre[:4]], 'contexte'))
                autres = []
            else:
                douteux.append('plusieurs textes Émeraude FR pour le même anglais : ' + alt)
                meme_anglais.append((m, [(x, sorted(y['meth']), y['w']) for x, y in ordre[:4]], 'douteux'))
                # même anglais, sens différents : une proposition par fichier HnS (msgctxt = chemin du fichier)
                mine = {p for p, _ in occs.get(m, [])}
                def compte(y):
                    c = collections.Counter()
                    for pr in y['preuves']:
                        r = re.match(r'US ([0-9A-F]{6})', pr)
                        if not r: continue
                        a = int(r.group(1), 16)
                        i, j = bisect.bisect_left(AD, a - 1500), bisect.bisect_right(AD, a + 1500)
                        for _, xx in addr[i:j]:
                            if xx != m: c.update({p for p, _ in occs.get(xx, [])})
                    tot_ = sum(c.values()) or 1
                    return {f: c[f] / tot_ for f in c}
                scores = [compte(y) for x, y in ctx]
                attrib = collections.defaultdict(list)
                for f in mine:
                    best = max(range(len(ctx)), key=lambda k: scores[k].get(f, 0))
                    if scores[best].get(f, 0) > 0: attrib[best].append(f)
                for k, (x, y) in enumerate(ctx):
                    fs = sorted(attrib.get(k, []))
                    for f in fs[:3]:
                        dc = entree(m, officiel(x, m) if g.get('genre') not in ('personne', 'surnom') else x, 'Émeraude FR officiel', info,
                                    ' ; '.join(sorted(set(y['preuves']))[:2]),
                                    'même anglais, sens différents : proposition avec msgctxt = fichier (%s)' % '+'.join(sorted(y['meth'])), ctx=f)
                        dc['fichier'] = f; dc['ligne'] = next((l for p, l in occs[m] if p == f), 0); dc['methode'] = 'ctx'
                        sorties['douteux'].append(dc)
        else:
            notes.append('autre(s) texte(s) FR minoritaire(s) : ' + alt)
    if 'ptr' in meths or 'delta' in meths or 'tm' in meths: cat = 'exact'
    elif meths & {'tidx', 'table'}: cat = 'tables'
    else: cat = 'contexte'
    meth_princ = next(x for x in ('ptr', 'delta', 'tm', 'tidx', 'table', 'seq', 'seq1') if x in meths)
    if meths <= {'seq1'}: douteux.append('séquence vérifiée d’un seul côté')
    # contrôles
    pb = controle(m, t)
    brut = t
    if any(p.startswith('codes') for p in pb):
        r = adapter_codes(m, t)
        if r: t, n = r; notes.append(n); pb = controle(m, t); cat_adapt = True
        else: douteux.append('codes de contrôle différents de l’anglais')
    if any(p.startswith('nombres') for p in pb):
        if nb_norm(m, NUM_EN) != nb_norm(t, NUM_FR):
            douteux.append('nombres différents (%s / %s)' % (nombres(m), nombres(t)))
    for p in pb:
        if p.startswith('ratio'): douteux.append('rapport de longueur ' + p[6:])
        if p.startswith('fin') or p.startswith('debut'): douteux.append('début/fin de fragment différent (%s)' % p)
        if p == 'kana': douteux.append('caractère japonais dans le texte FR (glyphe propre à Émeraude FR)')
    if nom_court(m) and meths & {'ptr', 'delta', 'table', 'seq', 'seq1', 'tm'} and not ('tidx' in meths and g['w'] >= 3):
        ok, v = meme_contexte(m, g['preuves'])
        if ok is False:
            douteux.append('nom/libellé court : contexte Émeraude différent (fichiers HnS des textes voisins dans Émeraude US : %s)'
                           % ', '.join(sorted(v)[:3] or ['aucun']))
    # style et mise en page
    genre = g['genre']
    # nom/libellé dont l'anglais sert dans des fichiers de natures différentes (objet / catégorie Pokédex…) :
    # la correspondance Émeraude ne couvre que les fichiers voisins -> msgctxt proposé, entrée douteuse
    fm_ = sorted({p for p, _ in occs.get(m, [])})
    if nom_court(m) and len(fm_) >= 2 and genre not in ('personne', 'surnom', 'easychat') and any(pr.startswith('US ') for pr in g['preuves']):
        c_ = collections.Counter()
        for pr in g['preuves']:
            r = re.match(r'US ([0-9A-F]{6})', pr)
            if not r: continue
            a_ = int(r.group(1), 16)
            i_, j_ = bisect.bisect_left(AD, a_ - 1500), bisect.bisect_right(AD, a_ + 1500)
            for _, xx in addr[i_:j_]:
                if xx != m: c_.update({p for p, _ in occs.get(xx, [])})
        tot_ = sum(c_.values()) or 1
        couverts = [f for f in fm_ if c_[f] / tot_ >= 0.05]
        def nature(f):
            if f.endswith('.party') or f in FICHIERS_NOMS: return 'noms'
            if '/species_info/' in f: return 'especes'
            if f.startswith('data/maps/'): return 'cartes'
            return f
        nat_c = {nature(f) for f in couverts}
        autres_n = sorted(f for f in fm_ if f not in couverts and nature(f) not in nat_c and not f.startswith('src/data/easy_chat/'))
        if couverts and autres_n:
            douteux.append('même anglais, sens différents : texte Émeraude trouvé pour %s, pas pour %s (msgctxt proposé)'
                           % (', '.join(couverts[:2]), ', '.join(autres_n[:3])))
            for f in couverts[:2]:
                txc = officiel(t, m)
                dc = entree(m, txc, 'Émeraude FR officiel', info, ' ; '.join(sorted(set(g['preuves']))[:2]),
                            'même anglais, sens différents : proposition pour ce fichier seulement (msgctxt)', ctx=f)
                dc['fichier'] = f; dc['ligne'] = next((l for p, l in occs[m] if p == f), 0); dc['methode'] = 'ctx'
                sorties['douteux'].append(dc)
    fm = {p for p, _ in occs.get(m, [])}
    if not genre and nom_court(m) and fm & FICHIERS_NOMS and all(p in FICHIERS_NOMS or p.endswith('.party') or 'frlg' in p.lower() for p in fm):
        genre = 'personne'
    if genre == 'easychat':
        douteux.append('mot Easy Chat : mot FR officiel au même index EC_WORD (les listes FR/EN sont localisées, pas traduites mot à mot)')
    if genre in ('personne', 'surnom') and nom_court(m):
        autres_f = sorted({p for p, _ in occs.get(m, [])} - FICHIERS_NOMS)
        hns = [f for f in autres_f if 'frlg' not in f.lower() and 'trainer_tower' not in f]
        if hns:
            douteux.append('nom de table Émeraude aussi porté dans HnS par : %s (personnage Johto/Kanto : nom SoulSilver prioritaire)' % ', '.join(hns[:4]))
        elif autres_f:
            notes.append('même nom aussi utilisé dans les données FRLG (%s) : nom Émeraude FR proposé faute de FRLG FR' % ', '.join(autres_f[:3]))
        # nom propre Hoenn / surnom : graphie officielle conservée (pas de passage au glossaire)
        from em_commun import graphie_codes, nettoyer_kana
        txt = nettoyer_kana(graphie_codes(t, m))
    else:
        txt = officiel(t, m)
    txt, n2 = mise_en_page(txt, m); notes += n2
    gardes = [n for n in proteges() if re.search(r"(?<![A-Za-zÀ-ÿ])%s(?![A-Za-zÀ-ÿ])" % re.escape(n), re.sub(r'\\[nlp]', ' ', txt))]
    if gardes and genre != 'personne':
        gl_, esp_ = gl_esp()
        notes.append('nom(s) de personnage Hoenn gardé(s) en capitales d’Émeraude FR malgré le glossaire : %s'
                     % ', '.join('%s (glossaire : %s)' % (n, gl_.get(style.cle(n), '?')) for n in gardes))
    ch = VERIF.champ(occs.get(m, [])[:12])
    if ch and G.encode(txt) is not None and len(G.encode(txt)) > ch[0]:
        douteux.append('trop long pour le champ « %s » (%d > %d octets) : abréviation à choisir' % (ch[1], len(G.encode(txt)), ch[0]))
    if 'ト' in txt and re.search(r'BP', m):
        txt = txt.replace('ト', 'PCo')
        douteux.append('glyphe 0x64 propre à Émeraude FR (abréviation des Points de Combat) remplacé par « PCo » (graphie du patch actuel)')
        douteux = [x for x in douteux if 'japonais' not in x]
    if re.search(r'[぀-ヿ]', txt) and not any('japonais' in x for x in douteux):
        douteux.append('caractère japonais après nettoyage')
    adapte = any('CLEAR_TO' in n for n in notes)
    source = 'Émeraude FR officiel (adapté)' if adapte else 'Émeraude FR officiel'
    preuve = ' ; '.join(sorted(set(g['preuves']))[:3])
    if adapte: preuve += ' ; texte officiel : ' + brut
    d = entree(m, txt, source, info, preuve, ' ; '.join(douteux + notes))
    d['fichier'], d['ligne'] = occs[m][0] if occs.get(m) else (d['fichier'], d['ligne'])
    ka, kt = style.cle(info['msgstr'] or '').replace('’', "'"), style.cle(txt).replace('’', "'")
    if info['msgstr'] and info['msgstr'] != txt and len(re.findall(r'[A-Za-zé]+', m)) <= 3 and \
            (ka == kt or (nom_court(m) and len(kt) >= 3 and ka.startswith(kt) and len(ka) > len(kt))):
        # même terme, seule la casse/les accents diffèrent : la graphie actuelle (glossaire/SoulSilver) est gardée
        stats['même terme, casse différente (actuel gardé)'] += 1
        d['methode'] = meth_princ; d['msgstr'] = info['msgstr']
        d['note'] = 'texte Émeraude FR « %s » : même terme que l’actuel à la casse/aux accents près ou abrégé (source actuelle : %s)' % (txt, info['source'] or '?')
        sorties['confirmes'].append(d)
        continue
    if info['msgstr'] == txt:
        stats['identique à l’actuel'] += 1
        d['methode'] = meth_princ; d['note'] = ('texte actuel identique au texte Émeraude FR officiel (source actuelle : %s)' % (info['source'] or '?'))
        if douteux: d['note'] += ' ; réserve : ' + ' ; '.join(douteux)
        sorties['confirmes'].append(d)
        continue
    if douteux:
        d['methode'] = meth_princ
        sorties['douteux'].append(d); stats['douteux:' + meth_princ] += 1
    else:
        dest = 'adapte' if adapte else cat
        d['methode'] = meth_princ
        sorties[dest].append(d); stats[dest + ':' + meth_princ] += 1
        par_zone[(dest, info['po'], zone(d['fichier']))] += 1
        if info['msgstr']:
            remplace.append((info['source'].split(' (')[0] or '(sans source)', m, info['msgstr'], txt, d['fichier']))

# ---------------------------------------------------------------- approché (em_approche.py)
for m, d in appr.items():
    if any(m == x['msgid'] for k in sorties for x in sorties[k]): continue
    info = po.get(('', m))
    if not info or deja_emeraude(info): continue
    d = dict(d); d['fichier'], d['ligne'] = occs[m][0] if occs.get(m) else (d.get('fichier', ''), d.get('ligne', 0))
    if info['msgstr']: d['ancien'] = info['msgstr']
    dest = d.pop('_dest', 'adapte')
    if info['msgstr'] == d['msgstr']:
        stats['identique à l’actuel (approché)'] += 1; continue
    d['methode'] = 'approche'
    sorties[dest].append(d); stats[dest + ':approche'] += 1
    if dest == 'adapte':
        par_zone[(dest, info['po'], zone(d['fichier']))] += 1
        if info['msgstr']: remplace.append((info['source'].split(' (')[0] or '(sans source)', m, info['msgstr'], d['msgstr'], d['fichier']))

import copy
pickle.dump(copy.deepcopy(dict(sorties)), open(os.path.join(TMP, 'em_sorties.pkl'), 'wb'))
for k in ('exact', 'contexte', 'tables', 'adapte', 'douteux', 'confirmes'):
    for d in sorties[k]: d.pop('methode', None) if k != 'douteux' else None
    print('%-10s %d' % (k, ecrire(k + '.json', sorties[k])), file=sys.stderr)
for k, v in sorted(stats.items()): print('  %-28s %d' % (k, v), file=sys.stderr)
print('rejets de candidats :', dict(rejets), file=sys.stderr)
pickle.dump({'stats': stats, 'zone': par_zone, 'remplace': remplace, 'meme_anglais': meme_anglais, 'rejets': rejets},
            open(os.path.join(TMP, 'em_stats.pkl'), 'wb'))
