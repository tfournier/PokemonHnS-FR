#!/usr/bin/env python3
"""Prépare memoires/ à partir des fichiers fournis par l'utilisateur, identifiés par leur contenu.

  preparer_roms.py <dossier_des_roms> <memoires/>

Reconnaît, quel que soit leur nom : Émeraude US (BPEE), Émeraude FR (BPEF), SoulSilver FR (NDS, IPGF),
le patch officiel HnS (UPS dont la source est Émeraude US) et le patch HnS FR (BPS dont la source est
la ROM anglaise de HnS). Produit : emeraude_us.gba, em_fr.gba, hns_en.gba (contrôle du CRC 0x01713508),
hns_fr_patch.gba (ROM anglaise + patch FR) et patch_fr.bps. Rien n'est jamais distribué.
"""
import os, sys, zlib

CRC_HNS_EN = 0x01713508


def rd(d, i):
    v, s = 0, 1
    while True:
        x = d[i]; i += 1; v += (x & 0x7f) * s
        if x & 0x80: return v, i
        s <<= 7; v += s


def ups(src, p):
    i = 4; a, i = rd(p, i); b, i = rd(p, i)
    if len(src) != a or zlib.crc32(src) != int.from_bytes(p[-12:-8], 'little'): raise ValueError('source UPS')
    out = bytearray(src + b'\0' * max(0, b - a))[:b]; pos = 0; end = len(p) - 12
    while i < end:
        n, i = rd(p, i); pos += n
        while p[i] != 0:
            if pos < b: out[pos] ^= p[i]
            pos += 1; i += 1
        i += 1; pos += 1
    if zlib.crc32(out) != int.from_bytes(p[-8:-4], 'little'): raise ValueError('cible UPS')
    return bytes(out)


def bps(src, d):
    i = 4; _, i = rd(d, i); ts, i = rd(d, i); ml, i = rd(d, i); i += ml
    if zlib.crc32(src) != int.from_bytes(d[-12:-8], 'little'): raise ValueError('source BPS')
    out = bytearray(ts); o = so = to = 0; end = len(d) - 12
    while i < end:
        v, i = rd(d, i); c, n = v & 3, (v >> 2) + 1
        if c == 0: out[o:o + n] = src[o:o + n]; o += n
        elif c == 1: out[o:o + n] = d[i:i + n]; i += n; o += n
        else:
            x, i = rd(d, i); x = (-1 if x & 1 else 1) * (x >> 1)
            if c == 2: so += x; out[o:o + n] = src[so:so + n]; so += n; o += n
            else:
                to += x
                for _ in range(n): out[o] = out[to]; o += 1; to += 1
    if zlib.crc32(out) != int.from_bytes(d[-8:-4], 'little'): raise ValueError('cible BPS')
    return bytes(out)


def main():
    src_dir, mem = sys.argv[1], sys.argv[2]
    os.makedirs(mem, exist_ok=True)
    gba, upss, bpss = {}, [], []
    for f in sorted(os.listdir(src_dir)):
        p = os.path.join(src_dir, f)
        if not os.path.isfile(p): continue
        with open(p, 'rb') as fh: head = fh.read(0x200)
        if head[:4] == b'UPS1': upss.append(p); continue
        if head[:4] == b'BPS1': bpss.append(p); continue
        code = head[0xAC:0xB0]
        if head[0x0C:0x10] == b'IPGF': print('SoulSilver FR (NDS) :', f); continue
        if code in (b'BPEE', b'BPEF'):
            d = open(p, 'rb').read()
            if code == b'BPEE' and len(d) == 16 * 1024 * 1024: gba['us'] = d; print('Émeraude US :', f, '%08X' % zlib.crc32(d))
            elif code == b'BPEF': gba['fr'] = d; print('Émeraude FR :', f, '%08X' % zlib.crc32(d))
            else: print('autre ROM BPEE (ignorée) :', f, '%08X' % zlib.crc32(d))
    if 'us' not in gba: sys.exit('Émeraude US introuvable')
    open(os.path.join(mem, 'emeraude_us.gba'), 'wb').write(gba['us'])
    if 'fr' in gba: open(os.path.join(mem, 'em_fr.gba'), 'wb').write(gba['fr'])
    en = None
    for p in upss:
        try: en = ups(gba['us'], open(p, 'rb').read()); print('patch officiel HnS (UPS) :', os.path.basename(p)); break
        except ValueError: pass
    if en is None: sys.exit('patch officiel HnS (UPS sur Émeraude US) introuvable')
    if zlib.crc32(en) != CRC_HNS_EN: print('ATTENTION : ROM anglaise CRC %08X (attendu %08X)' % (zlib.crc32(en), CRC_HNS_EN))
    else: print('ROM anglaise HnS : CRC %08X conforme' % zlib.crc32(en))
    open(os.path.join(mem, 'hns_en.gba'), 'wb').write(en)
    for p in bpss:
        d = open(p, 'rb').read()
        try: fr = bps(en, d)
        except ValueError: continue
        print('patch HnS FR (BPS) :', os.path.basename(p), '→ CRC %08X' % zlib.crc32(fr))
        open(os.path.join(mem, 'hns_fr_patch.gba'), 'wb').write(fr)
        open(os.path.join(mem, 'patch_fr.bps'), 'wb').write(d)
        break


if __name__ == '__main__':
    main()
