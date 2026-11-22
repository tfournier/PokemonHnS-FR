import re, os, bisect
P = '/Users/tfournier/projets/github.com/tfournier/PokemonHnS-FR'
UP = P + '/build/upstream_orig'
PE = P + '/build/pokeemerald'
PF = P + '/build/pokefirered'

GROUPS = ['POKEMON', 'TRAINER', 'STATUS', 'BATTLE', 'GREETINGS', 'PEOPLE', 'VOICES', 'SPEECH', 'ENDINGS',
          'FEELINGS', 'CONDITIONS', 'ACTIONS', 'LIFESTYLE', 'HOBBIES', 'TIME', 'MISC', 'ADJECTIVES', 'EVENTS',
          'MOVE_1', 'MOVE_2', 'TRENDY_SAYING', 'POKEMON_NATIONAL']

def defs(path, prefix):
    d = {}; last = None
    for l in open(path):
        m = re.match(r'\s*#define\s+(%s[A-Z0-9_]+)\s+(\d+)\b' % prefix, l)
        if m: d.setdefault(m.group(1), int(m.group(2))); continue
        m = re.match(r'\s+(%s[A-Z0-9_]+)\s*(?:=\s*([A-Za-z0-9_]+))?\s*,' % prefix, l)
        if m:
            v = m.group(2)
            if v is None: val = None if last is None else last + 1
            elif v.isdigit(): val = int(v)
            else: val = d.get(v, None if last is None else last + 1)
            if val is not None: d.setdefault(m.group(1), val); last = val
    return d

def ec_words(root):
    d = {}
    for m in re.finditer(r'#define (EC_WORD_[A-Z0-9_]+)\s+\(\(EC_GROUP_([A-Z0-9_]+) << EC_MASK_BITS\) \| (\d+)\)',
                         open(root + '/include/constants/easy_chat.h').read()):
        d[m.group(1)] = (GROUPS.index(m.group(2)) << 9) | int(m.group(3))
    return d

class Consts:
    def __init__(self, root):
        self.words = ec_words(root)
        self.species = defs(root + '/include/constants/species.h', 'SPECIES_')
        self.moves = defs(root + '/include/constants/moves.h', 'MOVE_')
        self.rwords = {v: k for k, v in self.words.items()}
        self.rspecies = {}
        for k, v in self.species.items():
            self.rspecies.setdefault(v, k)
        self.rmoves = {}
        for k, v in self.moves.items():
            self.rmoves.setdefault(v, k)

    def value(self, tok):
        tok = tok.replace(' ', '')
        if tok in ('EC_EMPTY_WORD', '-1', '0xFFFF'): return 0xFFFF
        if tok.startswith('EC_WORD_'): return self.words.get(tok)
        m = re.match(r'EC_(MOVE2?|POKEMON_NATIONAL|POKEMON2?)\(([A-Z0-9_]+)\)$', tok)
        if not m: return None
        k, n = m.groups()
        if k.startswith('MOVE'):
            v = self.moves.get('MOVE_' + n); g = 18 if k == 'MOVE' else 19
        else:
            v = self.species.get('SPECIES_' + n); g = 0 if k == 'POKEMON' else 21
        return None if v is None else (g << 9) | v

    def name(self, val, natpref=False):
        """token for expansion source from a value expressed in THIS constant set"""
        if val == 0xFFFF: return 'EC_EMPTY_WORD'
        g, i = val >> 9, val & 511
        if g in (18, 19):
            n = self.rmoves.get(i)
            return n and ('EC_MOVE%s(%s)' % ('' if g == 18 else '2', n[5:]))
        if g in (0, 21):
            n = self.rspecies.get(i)
            return n and ('EC_POKEMON%s(%s)' % ('' if g == 0 else '_NATIONAL', n[8:]))
        return self.rwords.get(val)

TOK = re.compile(r'EC_WORD_[A-Z0-9_]+|EC_(?:MOVE2?|POKEMON_NATIONAL|POKEMON2?)\(\s*[A-Z0-9_]+\s*\)|EC_EMPTY_WORD|-1|0xFFFF')

def parse_groups(path):
    """innermost {...} brace groups containing EC tokens. returns list of dict(start,end,line,items=[(s,e,tok)])"""
    txt = open(path, encoding='utf-8').read()
    # mask comments and strings
    mask = list(txt)
    for m in re.finditer(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', txt, re.S):
        for i in range(m.start(), m.end()):
            if mask[i] != '\n': mask[i] = ' '
    mt = ''.join(mask)
    out, stack = [], []
    for i, c in enumerate(mt):
        if c == '{': stack.append(i)
        elif c == '}':
            s = stack.pop()
            body = mt[s+1:i]
            if '{' in body: continue
            items = [(s + 1 + m.start(), s + 1 + m.end(), m.group(0)) for m in TOK.finditer(body)]
            if any(t not in ('-1', '0xFFFF') for _, _, t in items) and any(t.startswith('EC_') for _, _, t in items):
                # all comma-separated elements must be EC tokens
                elems = [re.sub(r'\s+', '', e) for e in body.split(',') if e.strip()]
                if elems != [re.sub(r'\s+', '', t) for _, _, t in items]: continue
                out.append(dict(start=s, end=i, line=txt.count('\n', 0, s) + 1, items=items))
    return txt, out

class Sym:
    def __init__(self, nmfile):
        self.a, self.n, self.sz = [], [], []
        for l in open(nmfile):
            p = l.split()
            if len(p) == 4 and p[2] in 'tTrRdD' and p[0].startswith('08'):
                self.a.append(int(p[0], 16)); self.sz.append(int(p[1], 16)); self.n.append(p[3])
            elif len(p) == 3 and p[1] in 'tTrRdD' and p[0].startswith('08'):
                self.a.append(int(p[0], 16)); self.sz.append(0); self.n.append(p[2])
    def at(self, off):
        a = off + 0x08000000
        i = bisect.bisect_right(self.a, a) - 1
        return self.n[i], a - self.a[i], self.sz[i], self.a[i] - 0x08000000
    def addr(self, name):
        i = self.n.index(name); return self.a[i] - 0x08000000, self.sz[i]
