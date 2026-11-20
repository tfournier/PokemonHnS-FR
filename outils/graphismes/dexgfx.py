"""Edition d'écrans composés (tileset + tilemaps) puis re-tuilage sans casser les autres écrans."""
import struct
import numpy as np
from PIL import Image

def load_tiles(png):
    im = Image.open(png)
    a = np.array(im)
    h, w = a.shape
    t = [a[ty*8:ty*8+8, tx*8:tx*8+8].copy() for ty in range(h//8) for tx in range(w//8)]
    return im, t

def read_bin(p):
    d = open(p, 'rb').read()
    return [struct.unpack_from('<H', d, 2*k)[0] for k in range(len(d)//2)]

def compose(tiles, ents, cols=32):
    rows = len(ents)//cols
    S = np.zeros((rows*8, cols*8), np.uint8)
    for k, e in enumerate(ents):
        ti = e & 0x3FF
        if ti >= len(tiles):
            continue
        t = tiles[ti] & 15
        if e & 0x400: t = t[:, ::-1]
        if e & 0x800: t = t[::-1, :]
        S[(k//cols)*8:(k//cols)*8+8, (k % cols)*8:(k % cols)*8+8] = t | ((e >> 12) << 4)
    return S

class Set:
    """Un tileset et les tilemaps qui l'utilisent."""
    def __init__(self, png, bins, cols=32):
        self.png = png; self.bins = bins; self.cols = cols
        self.im, self.tiles = load_tiles(png)
        self.ents = {b: read_bin(b) for b in bins}
        self.screens = {b: compose(self.tiles, self.ents[b], cols) for b in bins}
        self.orig = {b: self.screens[b].copy() for b in bins}

    def save(self, max_tiles=256, reuse_unused=False, compact=False):
        tiles = self.tiles
        free = []
        if reuse_unused:
            used = set()
            for b in self.bins: used |= {e & 0x3FF for e in self.ents[b]}
            free = [i for i in range(1, len(tiles)) if i not in used]
        index = {}
        for i, t in enumerate(tiles):
            k = (t & 15).tobytes()
            index.setdefault(k, (i, 0))
        def find(t):
            for fl, tt in ((0, t), (0x400, t[:, ::-1]), (0x800, t[::-1, :]), (0xC00, t[::-1, ::-1])):
                r = index.get(tt.tobytes())
                if r is not None:
                    return r[0], fl
            return None
        added = 0
        for b in self.bins:
            S = self.screens[b]; O = self.orig[b]; ents = self.ents[b]
            for k, e in enumerate(ents):
                y, x = (k//self.cols)*8, (k % self.cols)*8
                ns = S[y:y+8, x:x+8]
                if np.array_equal(ns, O[y:y+8, x:x+8]):
                    continue
                low = (ns & 15).astype(np.uint8)
                banks = set((ns >> 4).flatten().tolist())
                bank = (e >> 12)
                r = find(low)
                if r is None:
                    if free:
                        i = free.pop(0); index.pop((tiles[i] & 15).tobytes(), None); tiles[i] = low.copy(); r = (i, 0)
                    else:
                        tiles.append(low.copy()); r = (len(tiles)-1, 0)
                    added += 1
                    index[low.tobytes()] = r
                ents[k] = (bank << 12) | r[1] | r[0]
        if compact:
            used = sorted({e & 0x3FF for b in self.bins for e in self.ents[b]} | {0})
            remap = {o: n for n, o in enumerate(used)}
            tiles = [tiles[o] for o in used]
            for b in self.bins:
                self.ents[b] = [(e & ~0x3FF) | remap[e & 0x3FF] for e in self.ents[b]]
            self.tiles = tiles
        assert len(tiles) <= max_tiles, (self.png, len(tiles))
        w = self.im.size[0]; per = w//8
        h = ((len(tiles)+per-1)//per)*8
        a = np.zeros((h, w), np.uint8)
        for i, t in enumerate(tiles):
            ty, tx = divmod(i, per)
            a[ty*8:ty*8+8, tx*8:tx*8+8] = t
        out = Image.fromarray(a, 'P'); out.putpalette(self.im.getpalette())
        kw = {'transparency': self.im.info['transparency']} if 'transparency' in self.im.info else {}
        out.save(self.png, **kw)
        for b in self.bins:
            open(b, 'wb').write(b''.join(struct.pack('<H', e) for e in self.ents[b]))
        return added, len(tiles)

    def _n0(self):
        w, h = self.im.size
        return (w//8)*(h//8)

# ---------- polices ----------
def segment(mask):
    """Découpe un masque (rangées) en lettres selon les colonnes vides."""
    cols = [x for x in range(mask.shape[1]) if mask[:, x].any()]
    runs = []; s = p = cols[0]
    for c in cols[1:]:
        if c != p+1: runs.append((s, p)); s = c
        p = c
    runs.append((s, p))
    return [mask[:, a:b+1] for a, b in runs]

def draw_shadow(S, x, y, word, font, fill, shadow, adv=1):
    pts = []
    for ch in word:
        g = font[ch]
        for gy in range(g.shape[0]):
            for gx in range(g.shape[1]):
                if g[gy, gx]: pts.append((y+gy, x+gx))
        x += g.shape[1]+adv
    P = set(pts)
    for (py, px) in pts:
        for dy, dx in ((0, 1), (1, 0), (1, 1)):
            q = (py+dy, px+dx)
            if q not in P: S[q] = shadow
    for p in pts: S[p] = fill

def draw_outline(S, x, y, word, font, fill, outline, adv=-1, diag=True):
    """Lettres pleines entourées d'un contour 1 px partagé (adv=-1 : contours fusionnés)."""
    pts = []
    for ch in word:
        g = font[ch]
        for gy in range(g.shape[0]):
            for gx in range(g.shape[1]):
                if g[gy, gx]: pts.append((y+gy, x+gx))
        x += g.shape[1]+1+adv+1
    P = set(pts)
    nb = [(-1, 0), (1, 0), (0, -1), (0, 1)] + ([(-1, -1), (-1, 1), (1, -1), (1, 1)] if diag else [])
    for (py, px) in pts:
        for dy, dx in nb:
            q = (py+dy, px+dx)
            if q not in P: S[q] = outline
    for p in pts: S[p] = fill

def wshadow(word, font, adv=1):
    return sum(font[c].shape[1]+adv for c in word)-adv+1
