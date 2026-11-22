"""Police capitale 3x5 (+ ombre) pour les petits textes redessinés (restes japonais, légendes)."""
import numpy as np
G = {
 'A': ".#.|#.#|###|#.#|#.#", 'B': "##.|#.#|##.|#.#|##.", 'C': ".##|#..|#..|#..|.##", 'D': "##.|#.#|#.#|#.#|##.",
 'E': "###|#..|##.|#..|###", 'F': "###|#..|##.|#..|#..", 'G': ".##|#..|#.#|#.#|.##", 'H': "#.#|#.#|###|#.#|#.#",
 'I': "###|.#.|.#.|.#.|###", 'J': "..#|..#|..#|#.#|.#.", 'K': "#.#|#.#|##.|#.#|#.#", 'L': "#..|#..|#..|#..|###",
 'M': "#.#|###|###|#.#|#.#", 'N': "##.|#.#|#.#|#.#|#.#", 'O': ".#.|#.#|#.#|#.#|.#.", 'P': "##.|#.#|##.|#..|#..",
 'Q': ".#.|#.#|#.#|##.|.##", 'R': "##.|#.#|##.|#.#|#.#", 'S': ".##|#..|.#.|..#|##.", 'T': "###|.#.|.#.|.#.|.#.",
 'U': "#.#|#.#|#.#|#.#|###", 'V': "#.#|#.#|#.#|#.#|.#.", 'W': "#.#|#.#|###|###|#.#", 'X': "#.#|#.#|.#.|#.#|#.#",
 'Y': "#.#|#.#|.#.|.#.|.#.", 'Z': "###|..#|.#.|#..|###", 'é': "..#|.#.|###|#..|.##", '.': ".|.|.|.|#",
 '!': "#|#|#|.|#", '+': "...|.#.|###|.#.|...", '-': "...|...|###|...|...", '?': "##.|..#|.#.|...|.#.",
 '1': ".#|##|.#|.#|.#", '2': "##.|..#|.#.|#..|###", '3': "##.|..#|.#.|..#|##.", '4': "#.#|#.#|###|..#|..#",
 'e': "...|.#.|###|#..|.##", 'r': "...|...|.##|#..|#..",
}
def glyph(c): return [r for r in G[c].split('|')]
def width(text, gap=1, space=2):
    w = 0
    for i, c in enumerate(text):
        w += space if c == ' ' else len(glyph(c)[0])
        if i + 1 < len(text) and c != ' ' and text[i + 1] != ' ': w += gap
    return w
def draw(a, x, y, text, fg, sh=None, gap=1, space=2, shadow=((1, 0), (0, 1), (1, 1))):
    """dessine text (coin haut-gauche x,y) dans le tableau d'indices a ; ombre sh en bas/à droite"""
    pts = []
    for i, c in enumerate(text):
        if c == ' ': x += space; continue
        g = glyph(c)
        for gy, row in enumerate(g):
            for gx, v in enumerate(row):
                if v == '#': pts.append((x + gx, y + gy))
        x += len(g[0])
        if i + 1 < len(text) and text[i + 1] != ' ': x += gap
    P = set(pts)
    if sh is not None:
        for px, py in pts:
            for dx, dy in shadow:
                q = (px + dx, py + dy)
                if q not in P and 0 <= q[1] < a.shape[0] and 0 <= q[0] < a.shape[1]: a[q[1], q[0]] = sh
    for px, py in pts: a[py, px] = fg
    return x
