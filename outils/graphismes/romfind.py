"""Recherche d'une image (4bpp, brute ou LZ77) dans une ROM GBA."""
import re, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from lz77 import lz77

def find_lz(rom, data, align=4):
    n = len(data); hdr = bytes([0x10, n & 255, (n >> 8) & 255, n >> 16]); res = []
    for m in re.finditer(re.escape(hdr), rom):
        a = m.start()
        if a % align: continue
        if lz77(rom, a) == data: res.append(a)
    return res

def lz_blocks(rom, size, align=4):
    """Tous les blocs LZ77 valides d'une taille décompressée donnée."""
    hdr = bytes([0x10, size & 255, (size >> 8) & 255, size >> 16]); res = []
    for m in re.finditer(re.escape(hdr), rom):
        a = m.start()
        if a % align: continue
        d = lz77(rom, a)
        if d is not None: res.append((a, d))
    return res
