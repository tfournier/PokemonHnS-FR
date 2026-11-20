"""Passage au style d'écriture de SoulSilver FR.

Les textes Gen 3 écrivent les noms propres en capitales (POKéMON, DOUBLONVILLE, POTION…).
SoulSilver FR écrit « Pokémon », « Doublonville », « Potion », mais garde les noms d'espèces
en capitales (BULBIZARRE). Le glossaire (traductions/glossaire.tsv) donne la graphie officielle
de chaque terme ; il est éditable à la main.
"""
import re, unicodedata, os

def sans_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))

def cle(s):
    return sans_accents(s).upper().replace('’', "'")

FIXES = {
    'POKéMON': 'Pokémon', 'POKéDEX': 'Pokédex', 'POKé BALL': 'Poké Ball', 'POKé BALLS': 'Poké Balls',
    'POKéMATOS': 'Pokématos', 'POKéNAV': 'PokéNav', 'POKéBLOC': 'PokéBloc',
    'DRESSEUR': 'Dresseur', 'DRESSEURS': 'Dresseurs', 'DRESSEUSE': 'Dresseuse', 'PROF.': 'Prof.',
    'OEUF': 'Œuf', 'OEUFS': 'Œufs', 'ARENE': 'Arène', 'ARENES': 'Arènes',
    "CHAMPION D'ARENE": "Champion d'Arène", 'CHAMPION': 'Champion', 'CHAMPIONNE': 'Championne',
    'MAITRE': 'Maître', 'LIGUE': 'Ligue', 'LIGUE POKéMON': 'Ligue Pokémon', 'CONSEIL 4': 'Conseil 4',
    'CENTRE POKéMON': 'Centre Pokémon', 'BOUTIQUE': 'Boutique', 'TEAM ROCKET': 'Team Rocket',
    'BADGE': 'Badge', 'BADGES': 'Badges', 'SAC': 'Sac', 'PENSION': 'Pension', 'RADIO': 'Radio',
    'TOUR RADIO': 'Tour Radio', 'CARTE': 'Carte', 'BAIE': 'Baie', 'BAIES': 'Baies',
    'CT': 'CT', 'CS': 'CS', 'PC': 'PC', 'PV': 'PV', 'PP': 'PP', 'K.O.': 'K.O.', 'EXP.': 'Exp.',
    'NORMAL': 'Normal', 'FEU': 'Feu', 'EAU': 'Eau', 'PLANTE': 'Plante', 'ELECTRIK': 'Électrik',
    'GLACE': 'Glace', 'COMBAT': 'Combat', 'POISON': 'Poison', 'SOL': 'Sol', 'VOL': 'Vol', 'PSY': 'Psy',
    'INSECTE': 'Insecte', 'ROCHE': 'Roche', 'SPECTRE': 'Spectre', 'DRAGON': 'Dragon',
    'TENEBRES': 'Ténèbres', 'ACIER': 'Acier', 'FEE': 'Fée',
}

def construire(ss_json, sortie):
    import json
    fr = json.load(open(ss_json, encoding='utf-8'))
    banks = {'222': 'objet', '279': 'lieu', '720': 'talent', '730': 'classe', '750': 'capacité',
             '27': 'personnage', '310': 'personnage'}
    for b in range(600, 720):  # banques des appels : 1re ligne = nom du correspondant
        l = fr.get(str(b)) or []
        if l and re.fullmatch(r"[A-ZÉ][a-zà-ÿ’' -]{1,15}", l[0].strip()):
            banks.setdefault(str(b) + ':0', 'personnage')
    rows = {}
    for b, kind in banks.items():
        src = (fr.get(b.split(':')[0]) or [])[:1] if ':' in b else (fr.get(b) or [])
        for n in src:
            n = n.strip()
            if not n or '{' in n or '\\' in n or not re.search('[a-zà-ÿ]', n): continue
            rows.setdefault(cle(n), (n, kind))
    for k, v in FIXES.items():
        rows[cle(k)] = (v, 'terme')
    with open(sortie, 'w', encoding='utf-8') as f:
        f.write('# CLE (sans accents, majuscules)\tGRAPHIE SOULSILVER\tTYPE\n')
        for k in sorted(rows):
            f.write('%s\t%s\t%s\n' % (k, rows[k][0], rows[k][1]))
    return len(rows)

def charger(path):
    g = {}
    for line in open(path, encoding='utf-8'):
        if line.startswith('#') or not line.strip(): continue
        k, v, *_ = line.rstrip('\n').split('\t')
        g[k] = v
    return g

# a run of "capitalised" words: letters, digits, accents, é in POKéMON, apostrophes, dots, hyphens
WORD = r"[A-ZÀ-ÖØ-Þé0-9][A-ZÀ-ÖØ-Þé0-9'’.\-]*"
RUN = re.compile(r"(?<![A-Za-zÀ-ÿ0-9{])(" + WORD + r"(?: " + WORD + r"){0,3})(?![A-Za-zÀ-ÿ0-9}])")

def appliquer(text, gl, especes=frozenset()):
    """Remplace chaque suite de mots en capitales par sa graphie du glossaire (plus long d'abord)."""
    if not text: return text
    def repl(m):
        words = m.group(1).split(' ')
        out = []; i = 0
        while i < len(words):
            for n in range(min(4, len(words) - i), 0, -1):
                chunk = ' '.join(words[i:i+n])
                core = chunk.rstrip('.!?,;:')
                tail = chunk[len(core):]
                k = cle(core)
                if k in especes: continue
                # only touch real capitalised words (at least 2 capitals), not ordinary words
                if k in gl and sum(c.isupper() for c in core) >= 2 and core != gl[k]:
                    out.append(gl[k] + tail); i += n; break
            else:
                out.append(words[i]); i += 1
        return ' '.join(out)
    # don't touch {CODES}
    parts = re.split(r'(\{[^}]*\})', text)
    return ''.join(p if p.startswith('{') else RUN.sub(repl, p) for p in parts)

# ---------------------------------------------------------------- casse homogène
_ACCENTS = None
def accents(ss_json):
    """mot sans accents (minuscules) -> graphie accentuée la plus fréquente dans SoulSilver FR."""
    global _ACCENTS
    if _ACCENTS is None:
        import json, collections
        c = collections.defaultdict(collections.Counter)
        for lines in json.load(open(ss_json, encoding='utf-8')).values():
            for l in lines:
                for w in re.findall(r"[a-zà-ÿœ]+", l):
                    c[sans_accents(w)][w] += 1
        _ACCENTS = {k: (k if k in v else v.most_common(1)[0][0]) for k, v in c.items()}
    return _ACCENTS

SIGLES = re.compile(r"^(?:[A-Z]{1,3}\.?|[IVX]+|K\.O\.|N°|Nº|\d.*)$")
MOTS_COURTS = {'LE', 'LA', 'LES', 'DE', 'DU', 'DES', 'EN', 'ET', 'UN', 'UNE', 'AU', 'AUX', 'SUR', 'PAR',
               'POUR', 'AVEC', 'SANS', 'MON', 'TON', 'SON', 'MA', 'TA', 'SA', 'MES', 'TES', 'SES', 'OU', 'EST'}

def homogeneiser(text, avant, acc, especes=frozenset()):
    """Dans une suite de mots en capitales où le glossaire a remis certains mots en casse normale
    (« FERMER LE Sac »), passe aussi les autres en minuscules accentuées (« Fermer le Sac »)."""
    if not text: return text
    def fix_run(m):
        words = m.group(0).split(' ')
        if not any(re.search(r'[a-zà-ÿ]', w) for w in words): return m.group(0)
        if not any((sum(ch.isupper() for ch in w) >= 2 and not SIGLES.match(w)) or w in MOTS_COURTS for w in words): return m.group(0)
        out = []
        for i, w in enumerate(words):
            core = w.rstrip('.!?,;:'); tail = w[len(core):]
            plain = sans_accents(core.lower())
            if core in MOTS_COURTS or (sum(ch.isupper() for ch in core) >= 2 and not SIGLES.match(core)
                    and cle(core) not in especes and plain in acc
                    and not re.search(r'[a-zà-ÿ]', core.replace('é', ''))):
                low = core.lower()
                parts = re.split(r"([’'\-])", low)
                low = ''.join(acc.get(p, p) if p.isalpha() else p for p in parts)
                if i == 0 and m.start() == 0: low = low[:1].upper() + low[1:]
                out.append(low + tail)
            else:
                out.append(w)
        return ' '.join(out)
    RUNX = re.compile(r"(?<![A-Za-zÀ-ÿ0-9{])[A-Za-zÀ-ÿé0-9'’.\-]+(?: [A-Za-zÀ-ÿé0-9'’.\-]+){1,6}")
    parts = re.split(r'(\{[^}]*\}|\\[nlp])', text)
    return ''.join(p if (p.startswith('{') or p.startswith('\\')) else RUNX.sub(fix_run, p) for p in parts)
