"""Codec texte Gen 3 basé sur charmap.txt du projet upstream.

encode(texte_source) -> bytes          (sans 0xFF final)
decode(bytes, indices) -> texte_source (préfère les noms de codes présents dans `indices`)
largeur(texte_source) -> pixels (police normale)
reformater(texte, largeur_max) -> texte avec \\n (2e ligne), \\l (lignes suivantes), \\p (nouvelle page)
"""
import os, re

ARGS = {0x01: 1, 0x02: 1, 0x03: 1, 0x04: 3, 0x05: 1, 0x06: 1, 0x08: 1, 0x0B: 2, 0x0C: 1, 0x0D: 1,
        0x0E: 1, 0x10: 2, 0x11: 1, 0x12: 1, 0x13: 1, 0x14: 1}


# Octets que la charmap nomme aussi en kana : on garde le nom lisible.
MULTI = {bytes([0x55, 0x56, 0x57, 0x58, 0x59]): ('POKEBLOCK', 5), bytes([0x53, 0x54]): ('PKMN', 2)}
SINGLE = {0x2C: 'SUPER_ER', 0x84: 'SUPER_E', 0x7B: 'LEFT_ARROW', 0x7C: 'RIGHT_ARROW', 0x53: 'PK', 0x79: 'UP_ARROW', 0x7A: 'DOWN_ARROW'}
KANA_FIX = [('オカキクケ', '{POKEBLOCK}'), ('ウエ', '{PKMN}'), ('わ', '{SUPER_ER}'), ('ャ', '{SUPER_E}'),
            ('ロ', '{LEFT_ARROW}'), ('ワ', '{RIGHT_ARROW}'), ('ウ', '{PK}'), ('ル', '{UP_ARROW}'), ('レ', '{DOWN_ARROW}')]

def nettoyer_kana(s):
    for k, v in KANA_FIX:
        s = s.replace(k, v)
    return s

class Gen3:
    def __init__(self, root):
        self.c2b, self.n2b = {}, {}
        self.b2c, self.b2names = {}, {}
        for line in open(os.path.join(root, 'charmap.txt'), encoding='utf-8'):
            line = line.split('@')[0].strip()
            if '=' not in line: continue
            k, v = line.rsplit('=', 1); k = k.strip()
            try: vb = bytes(int(x, 16) for x in v.split())
            except ValueError: continue
            if k.startswith("'") and k.endswith("'"):
                c = k[1:-1]
                if len(c) == 2 and c[0] == '\\':
                    c = '\\' + c[1] if c[1] in 'nlp' else c[1]
                self.c2b.setdefault(c, vb)
                if len(vb) == 1: self.b2c.setdefault(vb[0], c)
            else:
                self.n2b.setdefault(k, vb)
                if len(vb) == 2: self.b2names.setdefault(vb, []).append(k)
        self.widths = self._widths(root)

    def _widths(self, root):
        txt = open(os.path.join(root, 'src/fonts.c'), encoding='utf-8').read()
        m = re.search(r'gFontNormalLatinGlyphWidths\[\] = \{([^}]*)\}', txt)
        return [int(x) for x in re.findall(r'\d+', m.group(1))] if m else [6] * 256

    # ---------------------------------------------------------------- encode
    def encode(self, s):
        out = bytearray(); i = 0
        while i < len(s):
            c = s[i]
            if c == '\\' and i + 1 < len(s):
                e = s[i:i+2]
                if e in self.c2b: out += self.c2b[e]
                elif s[i+1] in self.c2b: out += self.c2b[s[i+1]]
                else: return None
                i += 2; continue
            if c == '{':
                j = s.find('}', i)
                if j < 0: return None
                tok = s[i+1:j].split()
                if not tok or tok[0] not in self.n2b: return None
                out += self.n2b[tok[0]]
                for a in tok[1:]:
                    try: out.append(int(a, 0) & 0xFF)
                    except ValueError:
                        if a in self.n2b: out += self.n2b[a]
                        else: return None
                i = j + 1; continue
            if c not in self.c2b: return None
            out += self.c2b[c]; i += 1
        return bytes(out)

    # ---------------------------------------------------------------- decode
    def decode(self, b, hint=''):
        b = bytes(b)
        pref = set(re.findall(r'\{(\w+)', hint))
        out = []; i = 0
        while i < len(b):
            x = b[i]
            if x == 0xFF: break
            if x in (0xFC, 0xFD) and i + 1 < len(b):
                names = self.b2names.get(b[i:i+2], [])
                name = next((n for n in names if n in pref), names[0] if names else None)
                if name is None: return None
                k = ARGS.get(b[i+1], 0) if x == 0xFC else 0
                args = ' '.join(str(y) for y in b[i+2:i+2+k])
                out.append('{%s%s}' % (name, ' ' + args if args else '')); i += 2 + k; continue
            if x in (0xF8, 0xF9) and i + 1 < len(b):
                names = self.b2names.get(b[i:i+2], [])
                if not names: return None
                name = next((n for n in names if n in pref), None) or next((n for n in names if n.endswith('_BUTTON') or 'ARROW' in n), names[0])
                out.append('{%s}' % name); i += 2; continue
            multi = MULTI.get(bytes(b[i:i+5])) or MULTI.get(bytes(b[i:i+2]))
            if multi:
                out.append('{%s}' % multi[0]); i += multi[1]; continue
            if x in SINGLE:
                out.append('{%s}' % SINGLE[x]); i += 1; continue
            c = self.b2c.get(x)
            if c is None: return None
            out.append(c); i += 1
        return ''.join(out)

    # ---------------------------------------------------------------- width
    def largeur(self, s):
        w = 0; i = 0
        while i < len(s):
            if s[i] == '{':
                j = s.find('}', i); tok = s[i+1:j]
                w += 7 * 6 if tok.split()[0] in ('PLAYER', 'RIVAL') else (10 * 6 if 'VAR' in tok or 'B_' in tok else 0)
                i = j + 1; continue
            b = self.c2b.get(s[i])
            w += self.widths[b[0]] if b and len(b) == 1 and b[0] < len(self.widths) else 6
            i += 1
        return w

    def reformater(self, s, maxw=200):
        pages = re.split(r'\\p', s)
        out_pages = []
        for pg in pages:
            words = re.sub(r'\\[nl]', ' ', pg).split()
            lines, cur = [], ''
            for w in words:
                t = (cur + ' ' + w) if cur else w
                if cur and self.largeur(t) > maxw:
                    lines.append(cur); cur = w
                else:
                    cur = t
            if cur or not lines: lines.append(cur)
            txt = lines[0]
            for k, l in enumerate(lines[1:], 1):
                txt += ('\\n' if k == 1 else '\\l') + l
            out_pages.append(txt)
        return '\\p'.join(out_pages)
