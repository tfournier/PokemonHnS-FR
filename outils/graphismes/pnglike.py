"""Lecture/écriture de PNG indexés en conservant tous les chunks de l'original
(IHDR, PLTE, tRNS...) : seuls les pixels (IDAT) changent. Plus vignettes avant/après."""
import struct, zlib
import numpy as np
from PIL import Image, ImageDraw

def chunks(p):
    d = open(p, 'rb').read(); assert d[:8] == b'\x89PNG\r\n\x1a\n'
    i = 8; out = []
    while i < len(d):
        n, = struct.unpack('>I', d[i:i+4]); t = d[i+4:i+8]
        out.append((t, d[i+8:i+8+n])); i += 12 + n
    return out

def info(p):
    c = dict((t, b) for t, b in chunks(p) if t != b'IDAT')
    w, h, bd, ct = struct.unpack('>IIBB', c[b'IHDR'][:10])
    npal = len(c.get(b'PLTE', b'')) // 3
    return w, h, bd, ct, npal

def load(p):
    im = Image.open(p); assert im.mode == 'P', p
    return np.array(im)

def palette(p):
    c = dict((t, b) for t, b in chunks(p) if t != b'IDAT')
    pl = c[b'PLTE']; return [tuple(pl[3*k:3*k+3]) for k in range(len(pl)//3)]

def _chunk(t, b):
    return struct.pack('>I', len(b)) + t + b + struct.pack('>I', zlib.crc32(t + b) & 0xffffffff)

def save_like(orig, arr, out):
    w, h, bd, ct, npal = info(orig)
    arr = np.asarray(arr, np.uint8)
    assert arr.shape == (h, w), (arr.shape, (h, w))
    assert ct == 3
    assert int(arr.max()) < min(npal, 1 << bd), 'indice hors palette'
    raw = bytearray()
    for row in arr:
        raw.append(0)
        if bd == 8:
            raw += bytes(row)
        else:
            per = 8 // bd; r = list(row) + [0] * ((-len(row)) % per)
            for k in range(0, len(r), per):
                v = 0
                for j in range(per): v = (v << bd) | r[k+j]
                raw.append(v)
    data = b'\x89PNG\r\n\x1a\n'; done = False
    for t, b in chunks(orig):
        if t == b'IDAT':
            if not done: data += _chunk(b'IDAT', zlib.compress(bytes(raw), 9)); done = True
            continue
        data += _chunk(t, b)
    open(out, 'wb').write(data)

def rgb(arr, pal):
    pal = list(pal) + [(255, 0, 255)] * (256 - len(pal))
    P = np.array(pal, np.uint8)
    return Image.fromarray(P[np.asarray(arr)], 'RGB')

def vignette(before, after, pal_before, pal_after, out, scale=3):
    """EN à gauche, FR à droite, agrandis, séparés par une bande magenta (format des vignettes existantes)."""
    a = rgb(before, pal_before); b = rgb(after, pal_after)
    w, h = a.size; W = w * scale; H = h * scale
    c = Image.new('RGB', (2 * W + 12, H + 14), (0, 0, 0))
    c.paste(a.resize((W, H), Image.NEAREST), (0, 14))
    c.paste(b.resize((W, H), Image.NEAREST), (W + 12, 14))
    d = ImageDraw.Draw(c)
    d.rectangle([W + 2, 0, W + 9, H + 13], fill=(255, 0, 255))
    d.text((2, 1), 'EN', fill=(255, 255, 255)); d.text((W + 14, 1), 'FR', fill=(255, 255, 255))
    c.save(out)
