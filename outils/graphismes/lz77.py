def lz77(d, a, maxout=0x40000):
    if d[a] != 0x10: return None
    n = d[a+1] | d[a+2] << 8 | d[a+3] << 16
    if n == 0 or n > maxout: return None
    out = bytearray(); i = a + 4
    try:
        while len(out) < n:
            flags = d[i]; i += 1
            for b in range(8):
                if len(out) >= n: break
                if flags & (0x80 >> b):
                    x = d[i] << 8 | d[i+1]; i += 2
                    ln = (x >> 12) + 3; off = (x & 0xFFF) + 1
                    if off > len(out): return None
                    for _ in range(ln): out.append(out[-off])
                else:
                    out.append(d[i]); i += 1
    except IndexError:
        return None
    return bytes(out[:n])
