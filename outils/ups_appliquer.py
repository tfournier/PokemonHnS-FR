#!/usr/bin/env python3
"""Applique un patch UPS en contrôlant les trois CRC (source, cible, patch).

  ups_appliquer.py <rom_source> <patch.ups> <rom_sortie>
"""
import sys, zlib


def _nombre(d, i):
    v, s = 0, 1
    while True:
        x = d[i]; i += 1; v += (x & 0x7f) * s
        if x & 0x80: return v, i
        s <<= 7; v += s


def appliquer(source, patch):
    if patch[:4] != b'UPS1': raise ValueError('pas un patch UPS')
    if zlib.crc32(patch[:-4]) != int.from_bytes(patch[-4:], 'little'): raise ValueError('CRC du patch incorrect')
    if zlib.crc32(source) != int.from_bytes(patch[-12:-8], 'little'): raise ValueError('ROM source inattendue (CRC)')
    i = 4; _, i = _nombre(patch, i); lb, i = _nombre(patch, i)
    out = bytearray(source.ljust(lb, b'\0'))[:lb]; p = 0
    while i < len(patch) - 12:
        k, i = _nombre(patch, i); p += k
        while patch[i]: out[p] ^= patch[i]; p += 1; i += 1
        i += 1; p += 1
    if zlib.crc32(out) != int.from_bytes(patch[-8:-4], 'little'): raise ValueError('CRC de la ROM obtenue incorrect')
    return bytes(out)


if __name__ == '__main__':
    src, pt, dst = sys.argv[1:4]
    open(dst, 'wb').write(appliquer(open(src, 'rb').read(), open(pt, 'rb').read()))
    print('OK :', dst)
