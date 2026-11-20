"""Align Emerald US and FR ROMs, map every pointer target in US to its FR counterpart.
Output: pickle {us_target: fr_target} for targets that look like text."""
import struct, collections, pickle, sys
us = open('/home/claude/roms/em_us.gba', 'rb').read()
fr = open('/home/claude/roms/em_fr.gba', 'rb').read()
N = len(us)

def mask(rom):
    b = bytearray(rom)
    # mask aligned pointer words
    for i in range(0, len(b) - 3, 4):
        if b[i+3] in (0x08, 0x09) :
            b[i:i+4] = b'\0\0\0\0'
    # mask thumb BL pairs
    for i in range(0, len(b) - 3, 2):
        h = b[i+1]
        if 0xF0 <= h <= 0xF7 and 0xF8 <= b[i+3] <= 0xFF:
            b[i:i+4] = b'\0\0\0\0'
    return bytes(b)

W = 24
mu, mf = mask(us), mask(fr)
print('masked', file=sys.stderr)
idx = {}
dup = set()
for i in range(0, N - W, 4):
    w = mu[i:i+W]
    if w.count(0) > W // 2 or w.count(0xFF) > W // 2: continue
    if w in idx: dup.add(w)
    else: idx[w] = i
for w in dup: idx.pop(w, None)
print('us windows', len(idx), file=sys.stderr)
anch = []
for j in range(0, N - W, 2):
    i = idx.get(mf[j:j+W])
    if i is not None: anch.append((i, j))
anch.sort()
print('anchors', len(anch), file=sys.stderr)
ai = [a for a, _ in anch]
import bisect
mp = collections.defaultdict(collections.Counter)
for p in range(0, N - 3):
    if us[p+3] != 0x08: continue
    v = struct.unpack_from('<I', us, p)[0]
    if not (0x08000000 <= v < 0x09000000): continue
    k = bisect.bisect_right(ai, p) - 1
    if k < 0: continue
    a, b = anch[k]
    if p - a > 512: continue
    q = b + (p - a)
    if q + 4 > N: continue
    w = struct.unpack_from('<I', fr, q)[0]
    if not (0x08000000 <= w < 0x09000000): continue
    mp[v - 0x08000000][w - 0x08000000] += 1
best = {u: c.most_common(1)[0][0] for u, c in mp.items()}
pickle.dump(best, open('/home/claude/em_ptrmap.pkl', 'wb'))
print('mapped targets', len(best), file=sys.stderr)
