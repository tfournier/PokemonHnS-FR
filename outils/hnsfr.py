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
C_RE = re.compile(r'(?<![A-Za-z0-9_])(_|COMPOUND_STRING|ITEM_NAME|ITEM_PLURAL_NAME)\(\s*((?:' + LIT + r'\s*)+)\)')
LIT_RE = re.compile(LIT)
STR_LINE = re.compile(r'^([ \t]*)\.string[ \t]+(' + LIT + r')(.*)$')


class Occ:
    __slots__ = ('path', 'kind', 'start', 'end', 'text', 'indent', 'line', 'term')

    def __init__(self, path, kind, start, end, text, indent='', line=0, term=True):
        self.path, self.kind, self.start, self.end = path, kind, start, end
        self.text, self.indent, self.line, self.term = text, indent, line, term


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
            m = STR_LINE.match(lines[i])
            if not m:
                i += 1; continue
            j = i; parts = []; indent = m.group(1)
            while j < len(lines):
                mm = STR_LINE.match(lines[j])
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
            occ.append(Occ(rel, 'inc', start, end, text, indent, i + 1, term))
            i = j
    else:
        for m in C_RE.finditer(txt):
            lits = LIT_RE.findall(m.group(2))
            text = ''.join(unq(l) for l in lits)
            s, e = m.span(2)
            occ.append(Occ(rel, 'c', s, e, text, '', txt.count('\n', 0, m.start()) + 1))
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
    t = re.sub(r'\{[^}]*\}', '', text)
    return re.search(r'[A-Za-z]{2}', t) is not None


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
                if not tok or tok[0] not in self.names: bad.append(s[i:j+1])
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
            return '"' + fr + '"'
        m = re.search(r'\n([ \t]*)"', orig)
        ind = m.group(1) if m else ''
        pieces = [p for p in re.split(r'(?<=\\[nlp])', fr) if p != ''] or ['']
        while len(pieces) > nl + 1:
            pieces[-2] += pieces[-1]; pieces.pop()
        while len(pieces) < nl + 1:
            pieces.append('')
        return ('\n' + ind).join('"%s"' % p for p in pieces)
    # .inc : one .string per line break, last one with $
    pieces = re.split(r'(?<=\\[nlp])', fr)
    pieces = [p for p in pieces if p != ''] or ['']
    if occ.term: pieces[-1] += '$'
    return '\n'.join('%s.string "%s"' % (occ.indent, p) for p in pieces)


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
        for o in sorted(lst, key=lambda o: -o.start):
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
