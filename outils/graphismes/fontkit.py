from PIL import Image
def grid(img, x0, y0, w, h):
    return [[img.getpixel((x0+x, y0+y)) for x in range(w)] for y in range(h)]
def glyph_from(img, x0, y0, w, h, fg):
    return [''.join('1' if img.getpixel((x0+x,y0+y))==fg else '.' for x in range(w)) for y in range(h)]
def draw_text(img, x, y, text, glyphs, fg, sh, adv=1, shadow=True, bg_ok=None):
    pts=[]
    for ch in text:
        g=glyphs[ch]
        for gy,row in enumerate(g):
            for gx,c in enumerate(row):
                if c=='1': pts.append((x+gx,y+gy))
        x+=len(g[0])+adv
    S=set(pts)
    if shadow:
        for (px,py) in pts:
            for dx,dy in ((1,0),(0,1),(1,1)):
                q=(px+dx,py+dy)
                if q not in S: img.putpixel(q, sh)
    for p in pts: img.putpixel(p, fg)
    return x
def width(text, glyphs, adv=1):
    return sum(len(glyphs[c][0])+adv for c in text)-adv
