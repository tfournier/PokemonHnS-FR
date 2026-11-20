#!/usr/bin/env python3
"""Lot F : écrit traductions/lots/F_frlg/{lot,douteux}.json depuis build/lotF/frlg_paires.pkl.

Texte Rouge Feu FR -> style SoulSilver (em_commun.officiel : glossaire, espèces en capitales) ->
codes de mise en forme du hack remis à la place de ceux de Rouge Feu (police, couleur, musique : même
ordre) -> capitales restantes (termes propres à Rouge Feu absents du glossaire) en casse normale ->
mise en page (em_commun.mise_en_page) -> contrôles (em_commun.controle).
"""
import os, sys, re, json, pickle, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frlg_commun import TMP, LOT, G, P
import em_commun
from em_commun import officiel, mise_en_page, controle, codes_octets, entree, CODE
import style

em_commun._PROT = []          # pas de protection des noms Hoenn (PIERRE = Pierre, Champion d'Argenta)
GL, ESP = em_commun.gl_esp()
ACC = style.accents(os.path.join(P, 'memoires', 'ss_fr_msg.json'))


def _acc2():
    """comme style.accents, mais en comptant aussi les mots à initiale majuscule (Sélénite, Appât)"""
    c = collections.defaultdict(collections.Counter)
    for lines in json.load(open(os.path.join(P, 'memoires', 'ss_fr_msg.json'), encoding='utf-8')).values():
        for l in lines or []:
            for w in re.findall(r"[A-Za-zÀ-ÿœ]+", l):
                if w.isupper() and len(w) > 1: continue
                w = w.lower(); c[style.sans_accents(w)][w] += 1
    return {k: v.most_common(1)[0][0] for k, v in c.items()}


ACC = {**ACC, **_acc2()}
PLACE = re.compile(r'\{(PLAYER|RIVAL|STR_VAR_\d|B_[A-Z_0-9]+|KUN)\}')


def runs_forme(s):
    """suites de codes de mise en forme (hors variables), dans l'ordre, avec leurs positions"""
    out = []
    for m in re.finditer(r'(?:\{[^}]*\})+', s):
        toks = re.findall(r'\{[^}]*\}', m.group(0))
        if all(PLACE.fullmatch(t) or not em_commun.est_code(t) for t in toks): continue
        out.append(m)
    return out


def adapter_codes(fr, en):
    """Remplace, dans l'ordre, chaque suite de codes de mise en forme du texte FR par celle du msgid.
    Les variables ({PLAYER}, {STR_VAR_1}…) d'une suite sont conservées à leur place relative."""
    if codes_octets(fr) == codes_octets(en): return fr, False
    # musique : {PLAY_BGM 86 1} (pokefirered) <-> {PLAY_BGM}{MUS_RG_…} (pokeemerald-expansion), dans l'ordre
    mus_fr = re.findall(r'\{PLAY_(?:BGM|SE) \d+ \d+\}', fr); mus_en = re.findall(r'\{PLAY_(?:BGM|SE)\}\{[A-Z_0-9]+\}', en)
    if mus_fr and len(mus_fr) == len(mus_en):
        it = iter(mus_en); fr = re.sub(r'\{PLAY_(?:BGM|SE) \d+ \d+\}', lambda m: next(it), fr)
        if codes_octets(fr) == codes_octets(en): return fr, True
    rf, re_ = runs_forme(fr), runs_forme(en)
    if len(rf) + 1 == len(re_) and re_[-1].end() == len(en) and not (rf and rf[-1].end() == len(fr)):
        # suite finale du hack ({PLAY_BGM}{MUS_…} en fin de réplique) absente du texte FR : ajoutée en fin
        fr = fr + re_[-1].group(0); rf = runs_forme(fr)
        if len(rf) == len(re_) and codes_octets(fr) == codes_octets(en): return fr, True
    if len(rf) != len(re_): return fr, False
    out = []; pos = 0
    for a, b in zip(rf, re_):
        va = [t for t in re.findall(r'\{[^}]*\}', a.group(0)) if PLACE.fullmatch(t) or not em_commun.est_code(t)]
        vb = [t for t in re.findall(r'\{[^}]*\}', b.group(0)) if PLACE.fullmatch(t) or not em_commun.est_code(t)]
        if va != vb: return fr, False
        out.append(fr[pos:a.start()]); out.append(b.group(0)); pos = a.end()
    out.append(fr[pos:])
    return ''.join(out), True


SIGLES = re.compile(r"^(?:[A-Z]|[IVX]+|K\.O\.|PC|CT|CS|PV|PP|KO|OK|SS|TV|ID|EV|PS|CD|N°|GBA|RPG|VTT|PDG|NCL|SARL|DS|PNJ|ADN|QG|NES|ABC|VS|SNES|\d.*)$")
# noms propres sans accent dans le vocabulaire SoulSilver (Rouge Feu FR n'a pas de capitales accentuées)
ACC_NOMS = {'oceane': 'océane', 'pantheon': 'panthéon', 'celadon': 'céladon', 'azuree': 'azurée', 'dome': 'dôme',
            'romeo': 'roméo', 'noe': 'noé', 'entrepot': 'entrepôt', 'teleporteur': 'téléporteur', 'polo': 'polo',
            'mael': 'maël', 'gedeon': 'gédéon', 'secrete': 'secrète', 'special': 'spécial', 'seminaire': 'séminaire',
            'appats': 'appâts', 'flute': 'flûte', 'def': 'déf', 'attrape': 'attrape'}
COURTS = {w.lower() for w in style.MOTS_COURTS} | {'à', 'a', 'l', 'd', 'aux', 'dans'}
WORD = r"[A-ZÀ-Þ][A-ZÀ-Þ\-]+"
# cris et interjections en capitales de Rouge Feu FR : gardés tels quels (effet voulu)
CRIS = {'HAHAHA', 'RHAA', 'YAHA', 'PAF', 'NAN', 'NON', 'QUOI', 'YO', 'STOP', 'IMPOSSIBLE', 'DEGAGE', 'CONZEIL',
        'FIGHT', 'COOL', 'DANGER', 'ALERTE', 'OUI', 'HEIN', 'AAAH', 'OH', 'AH', 'HE', 'HO', 'GRR'}
# suite de capitales qui est une phrase (panneau, mot de passe) : casse de phrase, pas de majuscule à chaque mot
VERBAUX = {'JE', 'TU', 'IL', 'ELLE', 'NOUS', 'VOUS', 'ILS', 'QUI', 'QUE', 'EST', 'SONT', 'DIS-MOI', 'EN', 'PARTI', 'LA', 'LE', 'LES'}


def cri(x):
    return x in CRIS or re.search(r'([A-Z])\1\1', x) is not None


def mot(w, debut):
    low = w.lower()
    low = '-'.join(ACC_NOMS.get(p, ACC.get(p, p)) for p in low.split('-'))
    if not debut and low in COURTS: return low
    c = low[:1].upper()
    c = style.sans_accents(c) if c != low[:1] else c
    return c + low[1:]


def casse_restante(t):
    """capitales qui restent après le glossaire (termes de Rouge Feu FR) -> casse normale, sans majuscule accentuée"""
    vus = []
    ctx = {'avant': ''}
    def run(m, part):
        mots = m.group(0).split(' ')
        if all(SIGLES.match(x) or style.cle(x) in ESP or cri(x) for x in mots): return m.group(0)
        avant = (ctx['avant'] + part[:m.start()]).rstrip()
        debut_phrase = not avant or avant[-1] in '.!?…:“'
        phrase = len(mots) >= 3 and any(x in VERBAUX for x in mots)
        out = []
        for i, x in enumerate(mots):
            if SIGLES.match(x) or style.cle(x) in ESP or len(x) < 2 or cri(x): out.append(x); continue
            if x.lower() in COURTS and (i or not debut_phrase): out.append(x.lower()); continue
            w = mot(x, True)
            if phrase and (i or not debut_phrase): w = w.lower()
            out.append(w)
        r = ' '.join(out)
        if r != m.group(0): vus.append('%s → %s' % (m.group(0), r))
        return r
    t = re.sub(r'\bBADGE([A-Z]{3,})\b', r'BADGE \1', t)          # BADGEFOUDRE -> Badge Foudre (SoulSilver)
    t = re.sub(r'\bMR\. ', 'M. ', t)                                # MR. FUJI -> M. Fuji
    parts = re.split(r'(\{[^}]*\}|\\[nlp])', t)
    rx = re.compile(r"(?<![A-Za-zÀ-ÿ0-9{])" + WORD + r"(?: " + WORD + r"){0,5}(?![A-Za-zà-ÿ0-9}])")
    out = []
    for p in parts:
        if p.startswith('{') or p.startswith('\\'):
            out.append(p)
            if p == '\\p': ctx['avant'] += ' .'   # nouvelle page : souvent une nouvelle phrase si la précédente est finie
            continue
        q = rx.sub(lambda m: run(m, p), p)
        out.append(q); ctx['avant'] += q
    return ''.join(out), vus


def preuve(p):
    ver = 'BPRF' if p['ver'] == 'fr' else 'BPGF'
    return '%s 0x%06X (pokefirered %s, %s 0x%06X, %s) : %s' % (
        ver, p['fr_adr'], p['sym'], 'BPRE' if p['ver'] == 'fr' else 'BPGE', p['us_adr'], p['tmode'], p['fr_brut'])


def traiter(p):
    msgid = p['cle'][1]
    notes = []; adapte = False
    t = officiel(p['fr_brut'], msgid)
    t, ch = adapter_codes(t, msgid)
    if ch: adapte = True; notes.append('codes de mise en forme du hack remis (police/couleur/musique)')
    t, vus = casse_restante(t)
    t1 = re.sub(r'(?<=\S) +([!?:;])', r'\1', t)
    if t1 != t: adapte = True; notes.append('espace avant ! ? : ; retirée'); t = t1
    if vus: adapte = True; notes.append('casse : ' + ' ; '.join(vus))
    t2, n2 = mise_en_page(t, msgid)
    if t2 != t: adapte = True; notes += [x.replace('Émeraude FR', 'Rouge Feu FR') for x in n2]
    t = t2
    pb = controle(msgid, t)
    import hnsfr
    if '$' in t: pb.append('$')
    if hnsfr.Charmap(em_commun.ROOT).invalid(t): pb.append('hors charmap')
    if any(G.largeur(l) > 216 for l in re.split(r'\\[nlp]', t)) and not re.search(r'\{(DYNAMIC|CLEAR_TO)', t):
        pb.append('ligne > 216 px')
    return t, adapte, notes, pb


po_ctx = {}
lot = []; douteux = []; stats = collections.Counter(); deja = 0
for p in pickle.load(open(os.path.join(TMP, 'frlg_paires.pkl'), 'rb')):
    if not p['mode']:
        stats['non trouvé'] += 1; continue
    msgid = p['cle'][1]; ctx = p['cle'][0]; info = p['info']
    t, adapte, notes, pb = traiter(p)
    raison = []
    if p['score'] < 100: raison.append('le hack a modifié la phrase (ressemblance %d %%) ; anglais Rouge Feu : %s' % (p['score'], p['en_pfr']))
    if p['mode'].startswith('texte~'): raison.append('même anglais, plusieurs textes FR : ' + ' | '.join(p['variantes']))
    if p['mode'] == 'approché': raison.append('correspondance approchée')
    # alignement par étiquette + pointeur : un écart de longueur ou de nombres (« 1F » -> « Rdc », « fifty » -> « 50 »)
    # vient de la traduction libre de Rouge Feu FR ; on le note sans écarter l'entrée
    sur = p['mode'] == 'étiquette' and p['tmode'] and p['tmode'].startswith(('ptr', 'contigu'))
    leger = [x for x in pb if x == 'nombres' or x.startswith('ratio')] if sur else []
    if leger: notes.append('écart signalé par les contrôles (%s) : traduction libre de Rouge Feu FR' % ', '.join(leger))
    pb = [x for x in pb if x not in leger]
    if pb: raison.append('contrôles : ' + ', '.join(pb))
    if p['mode'].startswith('texte'): notes.append('trouvé par le texte anglais (étiquette %s absente de pokefirered)' % p.get('label'))
    if p['ver'] == 'lg': notes.append('texte de Vert Feuille')
    autres = sorted({x for x, l in info['occ'] if not ('_Frlg' in x or 'frlg' in x.lower() or 'trainer_tower' in x)})
    if autres and len(re.findall(r'[A-Za-z]+', msgid)) < 6:
        # réplique courte partagée avec une carte HnS : la traduction libre de Rouge Feu peut ne pas convenir
        raison.append('réplique courte partagée avec : ' + ', '.join(autres))
    elif autres:
        notes.append('entrée partagée avec : ' + ', '.join(autres))
    if raison:
        d = entree(msgid, t, 'Rouge Feu FR officiel (adapté)', info, preuve(p), ' ; '.join(raison + notes), ctx)
        douteux.append(d); stats['douteux'] += 1; continue
    if t == info['msgstr']:
        deja += 1; continue
    src = 'Rouge Feu FR officiel' + (' (adapté)' if adapte else '')
    lot.append(entree(msgid, t, src, info, preuve(p), ' ; '.join(notes), ctx))
    stats['adapté' if adapte else 'exact'] += 1
em_commun.LOT = LOT
print('lot', em_commun.ecrire('lot.json', lot), 'douteux', em_commun.ecrire('douteux.json', douteux), 'identiques', deja, dict(stats))


# ------------------------------------------------------------------ noms de Dresseurs (frlg_noms.py)
ACC_PRENOMS = dict(x.split('=') for x in (
    'AIMEE=Aimée ANGELIQUE=Angélique BENOIT=Benoît CEDRIC=Cédric CELESTIN=Célestin CELIA=Célia CELINA=Célina '
    'CLEMENT=Clément CLEO=Cléo FREDERIC=Frédéric GAELLE=Gaëlle GENEVIEVE=Geneviève GERALD=Gérald GERARD=Gérard '
    'GWENAELLE=Gwenaëlle HERVE=Hervé IRENE=Irène JEAN-LOIC=Jean-Loïc JEROME=Jérôme JEREMY=Jérémy JOELLE=Joëlle '
    'LEA=Léa LEO=Léo LEON=Léon LEONARD=Léonard MAELLE=Maëlle MATHEO=Mathéo MYLENE=Mylène NOE=Noé NOEL=Noël '
    'PACOME=Pacôme RAPHAEL=Raphaël REGIS=Régis REMI=Rémi ROMEO=Roméo SEBASTIEN=Sébastien SOLENE=Solène '
    'STEPHANE=Stéphane TEO=Téo THEO=Théo THEMIS=Thémis JOSE=José').split())


def nom_casse(n):
    def w(m):
        x = m.group(0)
        if x in ACC_PRENOMS: return ACC_PRENOMS[x]
        if x in ('PROF', 'SBIRE'): return x.capitalize()
        return '-'.join(p.capitalize() for p in x.split('-'))
    t = officiel(n, n)
    return re.sub(r"[A-ZÀ-Þ][A-ZÀ-Þ\-]+", w, t)


po = em_commun.charger_po()
noms = pickle.load(open(os.path.join(TMP, 'frlg_noms.pkl'), 'rb'))
groupes = collections.defaultdict(list)
for o in noms:
    if not o['fr']: continue
    cles = [k for k in po if k[1] == o['msgid'] and any(p == o['fichier'] for p, l in po[k]['occ'])]
    k = next((k for k in cles if k[0] == o['fichier']), cles[0] if cles else None)
    if k: groupes[k].append(o)
ln = []; ld = []
for k, os_ in groupes.items():
    info = po[k]; src = info['source']
    if src in ('Émeraude FR officiel', 'SoulSilver FR officiel'): continue
    frs = sorted({o['fr'] for o in os_})
    autres = sorted({p for p, l in info['occ'] if not ('_Frlg' in p or 'frlg' in p.lower() or 'trainer_tower' in p)})
    t = nom_casse(frs[0])
    pr = ' ; '.join('BPRF 0x%06X (%s) : %s' % (o['adr_fr'], o['cle'], o['fr']) for o in os_[:6]) + (' …' if len(os_) > 6 else '')
    nb = len(G.encode(t) or b'') + 1
    raison = []
    if len(frs) > 1: raison.append('même nom anglais, plusieurs noms FR : ' + ', '.join(frs))
    if autres: raison.append('l’entrée du .po sert aussi à : ' + ', '.join(autres))
    if nb > 11: raison.append('trop long (%d octets)' % nb)
    note = 'nom de Dresseur ; casse SoulSilver' + (' ; accent restitué' if any(c in t for c in 'éèêëïôûç') else '')
    src_f = 'Rouge Feu FR officiel' + ('' if t == frs[0] else ' (adapté)')
    e = entree(k[1], t, src_f, info, pr, ' ; '.join(raison + [note]), k[0])
    if raison: ld.append(e)
    elif t != info['msgstr']: ln.append(e)
lot += ln; douteux += ld
print('noms : lot', len(ln), 'douteux', len(ld))
print('lot', em_commun.ecrire('lot.json', lot), 'douteux', em_commun.ecrire('douteux.json', douteux))
