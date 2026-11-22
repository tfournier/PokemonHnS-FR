#!/usr/bin/env python3
"""pokehns-fr : extraction / application des textes de Pokémon Heart & Soul.

Les textes sont identifiés par la phrase anglaise elle-même (msgid des fichiers .po),
écrite dans la syntaxe du code source (\\n, \\l, \\p, {PLAYER}…).

  hnsfr.py extraire <source_upstream> <sortie.pot>
  hnsfr.py appliquer <source_upstream> <traductions/> [--rapport fichier]
"""
import os, re, sys, collections

EXCLUDE_DIRS = ('/tools', '/test', '/build', '/.git', '/docs', '/migration_scripts', '/dev_scripts')
EXCLUDE_FILES = ('src/text_input_strings.c',)  # claviers : la disposition affichée doit suivre celle du code
# fichiers texte non C : noms de Dresseurs (.party, convertis en .h à la compilation) et noms de lieux
PARTY_NAME = re.compile(r'^(Name:[ \t]*)(.*?)[ \t]*$', re.M)
JSON_FILES = ('src/data/region_map/region_map_sections.json',)
JSON_NAME = re.compile(r'("name"\s*:\s*")((?:[^"\\]|\\.)*)"')
LIT = r'"(?:[^"\\\n]|\\.)*"'
# une macro du code peut s'intercaler entre deux littéraux ("for "BINDING_TURNS" turns.") : elle devient
# le code {C:BINDING_TURNS}, à garder tel quel dans la traduction
C_RE = re.compile(r'(?<![A-Za-z0-9_])(_|COMPOUND_STRING|ITEM_NAME|ITEM_PLURAL_NAME)\(\s*((?:' + LIT + r'\s*)+(?:[A-Z][A-Z0-9_]*\s*(?:' + LIT + r'\s*)+)*)\)')
C_TOK = re.compile(LIT + r'|[A-Z][A-Z0-9_]*')
DEFINE_RE = re.compile(r'^[ \t]*#[ \t]*define[ \t]+\w+[ \t]+(' + LIT + r')[ \t]*$', re.M)
LIT_RE = re.compile(LIT)
STR_LINE = re.compile(r'^([ \t]*)\.string[ \t]+(' + LIT + r')(.*)$')
# inscriptions en braille (data/text/braille.inc) : même découpage que .string, autre directive ; les octets
# codent les points (table anglaise de preproc), d'où des entrées propres au fichier (msgctxt)
BRL_LINE = re.compile(r'^([ \t]*)\.braille[ \t]+(' + LIT + r')(.*)$')


class Occ:
    __slots__ = ('path', 'kind', 'start', 'end', 'text', 'indent', 'line', 'term', 'bloc')

    def __init__(self, path, kind, start, end, text, indent='', line=0, term=True, bloc=None):
        self.path, self.kind, self.start, self.end = path, kind, start, end
        self.text, self.indent, self.line, self.term = text, indent, line, term
        self.bloc = bloc   # 'cif' : (structure du bloc, n° de la variante)


# Texte C coupé par le préprocesseur, par exemple :
#     .description = COMPOUND_STRING(          .description = COMPOUND_STRING(
#         "Crunches with sharp fangs.\n"       #if B_MENTAL_HERB >= GEN_5
#     #if B_UPDATED_MOVE_DATA >= GEN_4             "Snaps Pokémon out\n" ... "effects."),
#         "May lower Defense."),               #else
#     #else                                        "A hold item that\n" ... "of infatuation."),
#         "May lower Sp. Def."),               #endif
#     #endif
# Chaque variante (début commun + branche) est un texte complet ; à l'écriture, le début commun
# est déplacé dans chaque branche (le nombre de lignes du fichier ne change pas).
CIF_OPEN = re.compile(r'(?<![A-Za-z0-9_])(?:_|COMPOUND_STRING|ITEM_NAME|ITEM_PLURAL_NAME)\([ \t]*\n')
CIF_LIT = re.compile(r'^([ \t]*)((?:' + LIT + r'[ \t]*)+)(.*)$')
CIF_DIR = re.compile(r'^[ \t]*#[ \t]*(if|ifdef|ifndef|elif|else|endif)\b')


def scan_cif(txt, rel):
    occ = []; spans = []
    for m in CIF_OPEN.finditer(txt):
        start = m.end()                      # début de la ligne qui suit « ( »
        lines = []; pos = start
        while pos < len(txt) and len(lines) < 60:
            e = txt.find('\n', pos); e = len(txt) if e < 0 else e
            lines.append((pos, e, txt[pos:e])); pos = e + 1
        prefixe = []; branches = []; suffixe = []; ok = False; profondeur = 0; apres = False; end = None
        for (a, b, l) in lines:
            d = CIF_DIR.match(l)
            if d:
                k = d.group(1)
                if apres: break
                if k in ('if', 'ifdef', 'ifndef'):
                    profondeur += 1
                    if profondeur > 1: break
                    branches.append({'dir': (a, b), 'lits': [], 'tail': None})
                elif k in ('elif', 'else'):
                    if profondeur != 1 or not branches: break
                    branches.append({'dir': (a, b), 'lits': [], 'tail': None})
                else:                                   # endif
                    if profondeur != 1 or not branches: break
                    fermees = [br['tail'] is not None for br in branches]
                    if all(fermees): ok = True; end = b; break      # chaque branche finit le texte
                    if any(fermees): break
                    apres = True; endif = (a, b)                   # partie commune après #endif
                continue
            lm = CIF_LIT.match(l)
            if not lm: break
            rest = lm.group(3).strip()
            lit = (a, b, lm.group(1), LIT_RE.findall(lm.group(2)))
            if apres:
                suffixe.append(lit)
                if rest:
                    if not rest.startswith(')'): break
                    for br in branches: br['tail'] = rest
                    ok = True; end = b; break
                continue
            cible = branches[-1] if branches else None
            if cible is None:
                if rest: break                          # « ) » avant tout #if : texte ordinaire
                prefixe.append(lit)
            else:
                if cible['tail'] is not None: break
                cible['lits'].append(lit)
                if rest:
                    if not rest.startswith(')'): break
                    cible['tail'] = rest
        if not ok or len(branches) < 2 or any(not br['lits'] for br in branches):
            continue
        bloc = {'start': start, 'end': end, 'prefixe': prefixe, 'branches': branches, 'suffixe': suffixe,
                'endif': endif if suffixe else None}
        debut = ''.join(unq(x) for p in prefixe for x in p[3])
        fin = ''.join(unq(x) for p in suffixe for x in p[3])
        ligne = txt.count('\n', 0, start) + 1
        for i, br in enumerate(branches):
            texte = debut + ''.join(unq(x) for p in br['lits'] for x in p[3]) + fin
            occ.append(Occ(rel, 'cif', start, end, texte, '', ligne, True, (bloc, i)))
        spans.append((start, end))
    return occ, spans


def render_cif(txt, bloc, frs):
    """Réécrit tout le bloc : lignes du début commun vidées, chaque branche reçoit son texte complet."""
    out = []
    for (a, b, ind, lits) in bloc['prefixe']:
        out.append('')
    for br, fr in zip(bloc['branches'], frs):
        a, b = br['dir']; out.append(txt[a:b])
        n = len(br['lits']); ind = br['lits'][0][2]
        pieces = [p for p in re.split(r'(?<=\\[nlp])', fr) if p != ''] or ['']
        while len(pieces) > n:
            pieces[-2] += pieces[-1]; pieces.pop()
        while len(pieces) < n:
            pieces.append('')
        for k, p in enumerate(pieces):
            out.append('%s"%s"%s' % (ind, p, br['tail'] if k == n - 1 else ''))
    if bloc.get('suffixe'):
        a, b = bloc['endif']; out.append(txt[a:b])      # ligne #endif, puis lignes de la partie commune vidées
        out += [''] * len(bloc['suffixe'])
    else:
        fin = txt.rfind('\n', 0, bloc['end']) + 1
        out.append(txt[fin:bloc['end']])            # ligne #endif
    return '\n'.join(out)


def unq(lit):
    return lit[1:-1]


def scan_file(root, rel):
    p = os.path.join(root, rel)
    try:
        txt = open(p, encoding='utf-8').read()
    except (UnicodeDecodeError, FileNotFoundError):
        return []
    occ = []
    if rel.endswith('.party'):
        for m in PARTY_NAME.finditer(txt):
            if m.group(2):
                occ.append(Occ(rel, 'party', m.start(2), m.end(2), m.group(2), '', txt.count('\n', 0, m.start()) + 1))
        return occ
    if rel.endswith('.json'):
        for m in JSON_NAME.finditer(txt):
            occ.append(Occ(rel, 'json', m.start(2), m.end(2), m.group(2), '', txt.count('\n', 0, m.start()) + 1))
        return occ
    if rel.endswith(('.inc', '.s')):
        pos = 0; lines = txt.split('\n'); offs = []
        for l in lines:
            offs.append(pos); pos += len(l) + 1
        i = 0
        while i < len(lines):
            m = STR_LINE.match(lines[i]); kind, RX = 'inc', STR_LINE
            if not m:
                m = BRL_LINE.match(lines[i]); kind, RX = 'braille', BRL_LINE
            if not m:
                i += 1; continue
            j = i; parts = []; indent = m.group(1)
            while j < len(lines):
                mm = RX.match(lines[j])
                if not mm or mm.group(3).strip() and not mm.group(3).strip().startswith('@'):
                    break
                parts.append(unq(mm.group(2)))
                j += 1
                if parts[-1].endswith('$'):
                    break
            if not parts:
                i += 1; continue
            text = ''.join(parts)
            term = text.endswith('$')
            if term: text = text[:-1]
            start = offs[i]; end = offs[j - 1] + len(lines[j - 1])
            occ.append(Occ(rel, kind, start, end, text, indent, i + 1, term))
            i = j
    else:
        cif, spans = scan_cif(txt, rel)
        occ += cif
        for m in C_RE.finditer(txt):
            if any(a <= m.start() < b for a, b in spans): continue
            toks = C_TOK.findall(m.group(2))
            text = ''.join(unq(t) if t.startswith('"') else '{C:%s}' % t for t in toks)
            s, e = m.span(2)
            occ.append(Occ(rel, 'c', s, e, text, '', txt.count('\n', 0, m.start()) + 1))
        if rel.startswith('src/'):   # valeur textuelle d'une macro : #define BINDING_TURNS "4 or 5"
            for m in DEFINE_RE.finditer(txt):
                s, e = m.span(1)
                occ.append(Occ(rel, 'c', s, e, unq(m.group(1)), '', txt.count('\n', 0, m.start()) + 1))
    return occ


def fichiers_suivis(root):
    """Fichiers suivis par git (les .h générés à la compilation sont exclus)."""
    import subprocess
    try:
        top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(root): raise ValueError('pas un dépôt git')
        r = subprocess.run(['git', 'ls-files', '-z'], cwd=root, capture_output=True, check=True)
        return sorted(f.decode('utf-8') for f in r.stdout.split(b'\0') if f)
    except Exception:
        out = []
        for dp, dn, fn in os.walk(root):
            for f in fn: out.append(os.path.relpath(os.path.join(dp, f), root))
        return sorted(out)


def scan(root):
    out = []
    for rel in fichiers_suivis(root):
        rd = '/' + os.path.dirname(rel)
        if any(rd.startswith(x) for x in EXCLUDE_DIRS):
            continue
        if rel in EXCLUDE_FILES:
            continue
        if rel.endswith(('.inc', '.s', '.c', '.h', '.party')) or rel in JSON_FILES:
            out += scan_file(root, rel)
    return out


def wanted(text):
    """Tout texte qui contient une lettre (latine ou japonaise) est à traduire, même d'une lettre
    (« A », « I » du langage Easy Chat, « 1F », « 's », restes japonais du code)."""
    t = re.sub(r'\{[^}]*\}|\\[nlp]', '', text)
    return re.search(r'[A-Za-z぀-ヿ一-鿿]', t) is not None


def domain(path):
    if path.startswith('data/maps/') or path.startswith('data/scripts') or path.startswith('data/event_scripts') or path.startswith('data/text'):
        return 'dialogues'
    if path.startswith('src/data/') or path.endswith('.party'):
        return 'donnees'
    return 'menus'


# ------------------------------------------------------------------ charmap
class Charmap:
    def __init__(self, root):
        self.chars, self.names = set(), set()
        for line in open(os.path.join(root, 'charmap.txt'), encoding='utf-8'):
            line = line.split('@')[0].strip()
            if '=' not in line: continue
            k = line.rsplit('=', 1)[0].strip()
            if k.startswith("'") and k.endswith("'"):
                c = k[1:-1]
                if len(c) == 2 and c[0] == '\\':
                    c = '\\' + c[1] if c[1] in 'nlp' else c[1]
                self.chars.add(c)
            else:
                self.names.add(k)

    def invalid(self, s):
        """Return the list of characters/tokens that the build cannot encode."""
        bad = []; i = 0
        while i < len(s):
            c = s[i]
            if c == '{':
                j = s.find('}', i)
                if j < 0: bad.append(s[i:]); break
                tok = s[i+1:j].split()
                if not tok or (tok[0] not in self.names and not re.fullmatch(r'0x[0-9A-Fa-f]{1,2}', tok[0])
                               and not re.fullmatch(r'C:[A-Z][A-Z0-9_]*', tok[0])): bad.append(s[i:j+1])
                i = j + 1; continue
            if c == '\\':
                if s[i:i+2] in ('\\n', '\\l', '\\p', '\\"', "\\'", '\\\\'): i += 2; continue
                bad.append(s[i:i+2]); i += 2; continue
            if c not in self.chars and c != '"': bad.append(c)
            i += 1
        return bad


# ------------------------------------------------------------------ write back
def render(occ, fr, orig=''):
    if occ.kind in ('party', 'json'):
        return fr
    if occ.kind == 'c':
        # keep the same number of lines (assertions use __LINE__)
        nl = orig.count('\n')
        if nl == 0:
            return re.sub(r'\{C:([A-Z][A-Z0-9_]*)\}', r'" \1 "', '"' + fr + '"')
        m = re.search(r'\n([ \t]*)"', orig)
        ind = m.group(1) if m else ''
        pieces = [p for p in re.split(r'(?<=\\[nlp])', fr) if p != ''] or ['']
        while len(pieces) > nl + 1:
            pieces[-2] += pieces[-1]; pieces.pop()
        while len(pieces) < nl + 1:
            pieces.append('')
        out = ('\n' + ind).join('"%s"' % p for p in pieces)
        return re.sub(r'\{C:([A-Z][A-Z0-9_]*)\}', r'" \1 "', out)
    # .inc : one .string per line break, last one with $
    pieces = re.split(r'(?<=\\[nlp])', fr)
    pieces = [p for p in pieces if p != ''] or ['']
    if occ.term: pieces[-1] += '$'
    directive = '.braille' if occ.kind == 'braille' else '.string'
    return '\n'.join('%s%s "%s"' % (occ.indent, directive, p) for p in pieces)


def load_po(dirpath):
    import polib
    tr = {}
    for f in sorted(os.listdir(dirpath)):
        if not f.endswith('.po'): continue
        for e in polib.pofile(os.path.join(dirpath, f)):
            if e.msgstr and 'fuzzy' not in e.flags and not e.obsolete:
                tr[(e.msgctxt or '', e.msgid)] = e.msgstr
    return tr


def apply(root, podir, report=None):
    cm = Charmap(root)
    tr = load_po(podir)
    occs = scan(root)
    byfile = collections.defaultdict(list)
    for o in occs: byfile[o.path].append(o)
    stats = collections.Counter(); problems = []
    for path, lst in byfile.items():
        p = os.path.join(root, path)
        txt = open(p, encoding='utf-8').read()
        changed = False
        faits = set()
        for o in sorted(lst, key=lambda o: -o.start):
            if o.kind == 'cif':
                bloc = o.bloc[0]
                if id(bloc) in faits: continue
                faits.add(id(bloc))
                variantes = sorted((x for x in lst if x.kind == 'cif' and x.bloc[0] is bloc), key=lambda x: x.bloc[1])
                frs = []
                for v in variantes:
                    fr = (tr.get((path, v.text)) or tr.get(('', v.text))) if wanted(v.text) else None
                    if fr and cm.invalid(fr):
                        stats['caractère invalide'] += 1
                        problems.append('%s:%d caractères inconnus %r : %s' % (path, v.line, sorted(set(cm.invalid(fr)))[:5], fr[:60])); fr = None
                    if fr: stats['traduit'] += 1
                    elif wanted(v.text): stats['non traduit'] += 1
                    frs.append(fr or v.text)
                txt = txt[:bloc['start']] + render_cif(txt, bloc, frs) + txt[bloc['end']:]
                changed = True
                continue
            if not wanted(o.text): continue
            fr = tr.get((path, o.text)) or tr.get(('', o.text))
            if not fr:
                stats['non traduit'] += 1; continue
            bad = cm.invalid(fr)
            if bad:
                stats['caractère invalide'] += 1
                problems.append('%s:%d caractères inconnus %r : %s' % (path, o.line, sorted(set(bad))[:5], fr[:60])); continue
            txt = txt[:o.start] + render(o, fr, txt[o.start:o.end]) + txt[o.end:]
            stats['traduit'] += 1; changed = True
        if changed:
            open(p, 'w', encoding='utf-8').write(txt)
    if report:
        with open(report, 'w', encoding='utf-8') as f:
            for k, v in stats.most_common(): f.write('%s: %d\n' % (k, v))
            f.write('\n'.join(problems) + '\n')
    return stats, problems


def extract(root, out):
    import polib
    occs = scan(root)
    pot = polib.POFile(); pot.metadata = {'Content-Type': 'text/plain; charset=UTF-8', 'Language': 'fr'}
    seen = {}
    for o in occs:
        if not wanted(o.text): continue
        e = seen.get(o.text)
        if e is None:
            e = polib.POEntry(msgid=o.text, msgstr='', occurrences=[])
            seen[o.text] = e; pot.append(e)
        e.occurrences.append((o.path, str(o.line)))
    pot.save(out)
    return len(pot)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'extraire':
        print(extract(sys.argv[2], sys.argv[3]), 'textes')
    elif cmd == 'appliquer':
        rep = sys.argv[sys.argv.index('--rapport') + 1] if '--rapport' in sys.argv else None
        st, pb = apply(sys.argv[2], sys.argv[3], rep)
        for k, v in st.most_common(): print('%-20s %d' % (k, v))
        if pb: print(len(pb), 'problèmes (voir rapport)')
