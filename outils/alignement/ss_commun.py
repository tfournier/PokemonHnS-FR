"""Lot B : fonctions communes (chargement des .po, normalisation, conversion des codes HGSS → HnS)."""
import os, re, sys, json, unicodedata, collections

P = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(P, 'outils'))

DOMAINES = ('dialogues', 'menus', 'donnees', 'contextes')
CODE = re.compile(r'\{[^}]*\}')
STRV = re.compile(r'\{STRVAR_(\w+) (\d+), (\d+)(?:, (\d+))?\}')


def source_po(comment):
    m = re.search(r'source : ([^\n]*)', comment or '')
    return m.group(1).strip() if m else ''


def dans_perimetre(e):
    """entrée qui ne vient pas déjà d'un officiel : non traduite, patch FR, traduction manuelle, relue."""
    s = source_po(e.comment)
    if 'officiel' in s or s.startswith('SoulSilver FR'):
        return False
    return True


def charger_po(domaines=DOMAINES):
    import polib
    out = []
    for d in domaines:
        for e in polib.pofile(os.path.join(P, 'traductions', d + '.po')):
            if e.obsolete or not e.msgid: continue
            out.append((d, e))
    return out


def sans_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))


def norm(s):
    """anglais normalisé : sans codes, sans casse, sans ponctuation ni retours."""
    s = CODE.sub(' ', s)
    s = re.sub(r'\\[nlpr]', ' ', s)
    s = s.replace('\n', ' ').replace('\r', ' ').replace('\f', ' ')
    s = sans_accents(s).lower().replace('’', "'").replace('‘', "'")
    s = s.replace('…', ' ')
    s = re.sub(r"[^a-z0-9]+", ' ', s)
    return ' '.join(s.split())


def nombres(s):
    s = CODE.sub(' ', s)
    return sorted(re.findall(r'\d+', s))


# ---------------------------------------------------------------- codes HnS
VARIABLE_HNS = re.compile(r'\{(STR_VAR_\d|PLAYER|RIVAL|B_[A-Z_0-9]+|KUN|STRING \d+)\}')


def codes_hns(s):
    return [m.group(0) for m in CODE.finditer(s)]


def cle_hgss(m):
    return (m.group(1), m.group(3))      # (STRVAR_x, emplacement)


def table_codes(en_hns, en_hgss):
    """associe chaque variable HGSS ({STRVAR_1 t, i, 0}) à la variable HnS de même rang.
    Renvoie (table {clé: code HnS}, autres codes HnS non variables) ou None si incohérent."""
    vh = [m.group(0) for m in VARIABLE_HNS.finditer(en_hns)]
    vg = list(STRV.finditer(en_hgss))
    if len(vh) != len(vg):
        return None
    t = {}
    for g, h in zip(vg, vh):
        k = cle_hgss(g)
        if t.get(k, h) != h:
            return None
        t[k] = h
    if len(set(t.values())) != len(t):
        return None
    return t


def autres_codes(s):
    """codes HnS qui ne sont pas des variables (couleurs, pauses, sons…) ni des glyphes."""
    return [c for c in codes_hns(s) if not VARIABLE_HNS.fullmatch(c) and not GLYPHE.fullmatch(c)]


GLYPHE = re.compile(r'\{(PKMN|POKE|POKEBLOCK|SUPER_E|SUPER_ER|SUPER_RE|UP_ARROW|DOWN_ARROW|LEFT_ARROW|RIGHT_ARROW|PK|MN|LV|LV_2|ID|NO|EMOJI_[A-Z_]+|[A-Z]_BUTTON|DPAD_[A-Z]+|START_BUTTON|SELECT_BUTTON|L_BUTTON|R_BUTTON)\}')


def convertir_fr(fr, table):
    """français SS (format pret) → syntaxe HnS. Renvoie None si une variable n'a pas d'équivalent."""
    manque = []

    def rep(m):
        k = cle_hgss(m)
        if k not in table:
            manque.append(m.group(0)); return ''
        return table[k]
    s = STRV.sub(rep, fr)
    if manque:
        return None
    # codes HGSS sans équivalent HnS (couleurs, OUI/NON, alignement, pauses) : supprimés
    s = re.sub(r'\{(COLOR|YESNO|ALN_CENTER|ALN_RIGHT|PAUSE|WAIT|SIZE|CURSOR_X|CURSOR_Y|UNK_[0-9A-F]+|TRNAME)[^}]*\}', '', s)
    if CODE.sub('', s).count('{') or re.search(r'\{(?!STR_VAR|PLAYER|RIVAL|B_|KUN|STRING)', s):
        return None
    s = s.replace('«\u00a0', '“').replace('\u00a0»', '”').replace('« ', '“').replace(' »', '”')
    s = s.replace('«', '“').replace('»', '”')
    s = s.replace('\u2009', '').replace('\u202f', '').replace('\u00a0', ' ')
    s = s.replace('\r', '\\p').replace('\f', '\\p').replace('\n', '\\n')
    s = s.replace('...', '…')
    s = re.sub(r' +([!?:;])', r'\1', s)
    s = re.sub(r'  +', ' ', s)
    return s.strip(' ')


def charger_glossaire():
    import style
    return style.charger(os.path.join(P, 'traductions', 'glossaire.tsv'))


def gen3():
    from gen3 import Gen3
    return Gen3(os.path.join(P, 'build', 'upstream_orig'))
