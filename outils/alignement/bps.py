import sys, json, zlib

def rd(d, i):
    v, s = 0, 1
    while True:
        x = d[i]; i += 1
        v += (x & 0x7f) * s
        if x & 0x80: break
        s <<= 7
        v += s
    return v, i

d = open(sys.argv[1], 'rb').read()
assert d[:4] == b'BPS1'
i = 4
src, i = rd(d, i); tgt, i = rd(d, i); ml, i = rd(d, i)
meta = d[i:i+ml]; i += ml
print('source', src, hex(src), 'target', tgt, hex(tgt), 'meta', meta[:200])
print('crc src %08x tgt %08x' % tuple(int.from_bytes(d[-12+k*4:-8+k*4], 'little') for k in range(2)))
end = len(d) - 12
out = 0
chunks = []  # (target_offset, bytes) for TargetRead
stats = [0, 0, 0, 0]
while i < end:
    v, i = rd(d, i)
    cmd, ln = v & 3, (v >> 2) + 1
    stats[cmd] += ln
    if cmd == 1:
        chunks.append((out, d[i:i+ln])); i += ln
    elif cmd in (2, 3):
        o, i = rd(d, i)
    out += ln
print('stats SourceRead/TargetRead/SourceCopy/TargetCopy', stats)
import pickle
pickle.dump(chunks, open(sys.argv[2], 'wb'))
print('chunks', len(chunks), sum(len(c) for _, c in chunks))
