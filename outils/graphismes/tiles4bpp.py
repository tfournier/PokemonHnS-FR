import numpy as np
def from4bpp(d, wtiles):
    n = len(d) // 32; h = (n + wtiles - 1) // wtiles
    a = np.zeros((h * 8, wtiles * 8), np.uint8)
    for t in range(n):
        ty, tx = divmod(t, wtiles)
        for y in range(8):
            for x in range(0, 8, 2):
                b = d[t * 32 + y * 4 + x // 2]
                a[ty * 8 + y, tx * 8 + x] = b & 15; a[ty * 8 + y, tx * 8 + x + 1] = b >> 4
    return a
