import numpy as np
def inkbox(S, box, fg):
    y0,y1,x0,x1=box; m=((S[y0:y1,x0:x1]&15)==fg)
    return m
def segment(S, box, fg, text):
    """découpe les glyphes (encre fg) d'une ligne ; renvoie [(car, masque, x_abs)]"""
    y0,y1,x0,x1=box; m=inkbox(S,box,fg)
    cols=m.any(0); segs=[]; x=0
    while x<len(cols):
        if cols[x]:
            s=x
            while x<len(cols) and cols[x]: x+=1
            segs.append((s,x))
        else: x+=1
    chars=[c for c in text if c!=' ']
    assert len(segs)==len(chars), (text, len(segs), len(chars), segs)
    out=[]
    for c,(s,e) in zip(chars,segs): out.append((c, m[:,s:e].copy(), x0+s))
    # espaces : largeur entre mots
    gaps=[segs[i+1][0]-segs[i][1] for i in range(len(segs)-1)]
    return out, gaps
def build_lib(entries):
    lib={}
    for S,box,fg,text in entries:
        out,_=segment(S,box,fg,text)
        for c,m,x in out:
            if c in lib and (lib[c].shape!=m.shape or (lib[c]!=m).any()):
                print('glyph conflict', c, text)
            lib.setdefault(c,m)
    return lib
def gapstats(entries):
    from collections import Counter
    C=Counter()
    for S,box,fg,text in entries:
        out,gaps=segment(S,box,fg,text)
        # associe chaque gap à espace ou non
        k=0; i=0
        chars=text
        idx=[j for j,c in enumerate(text) if c!=' ']
        for g,(a,b) in zip(gaps,zip(idx,idx[1:])):
            C[('space' if b-a>1 else 'gap',g)]+=1
    return C
def width(lib, text, gap, space):
    w=0
    for i,c in enumerate(text):
        if c==' ': w+=space; continue
        w+=lib[c].shape[1]
        if i+1<len(text) and text[i+1]!=' ': w+=gap
    return w
def draw(S, box, fg, sh, bgfun, lib, text, x, gap, space, clear=True):
    y0,y1,x0,x1=box
    if clear:
        for yy in range(y0,y1):
            for xx in range(x0,x1):
                v=S[yy,xx]&15
                if v in (fg,sh): S[yy,xx]=(S[yy,xx]&0xF0)|bgfun(yy,xx)
    pts=[]
    for i,c in enumerate(text):
        if c==' ': x+=space; continue
        m=lib[c]
        ys,xs=np.nonzero(m)
        pts+= [(x+a,y0+b) for b,a in zip(ys,xs)]
        x+=m.shape[1]
        if i+1<len(text) and text[i+1]!=' ': x+=gap
    P=set(pts)
    for px,py in pts:
        for dx,dy in ((1,0),(0,1),(1,1)):
            q=(px+dx,py+dy)
            if q not in P: S[q[1],q[0]]=(S[q[1],q[0]]&0xF0)|sh
    for px,py in pts: S[py,px]=(S[py,px]&0xF0)|fg
    return x

def _base(out):
    from collections import Counter
    bots=[np.nonzero(m.any(1))[0].max() for c,m,x in out]
    return Counter(bots).most_common(1)[0][0]
def build_lib2(entries, lib=None):
    """glyphes rognés + décalage vertical par rapport à la ligne de base"""
    lib={} if lib is None else lib
    for S,box,fg,text in entries:
        out,_=segment(S,box,fg,text); b=_base(out)
        for c,m,x in out:
            r=np.nonzero(m.any(1))[0]
            lib.setdefault(c,(m[r.min():r.max()+1].copy(), r.min()-b))
    return lib
def baseline(S,box,fg,text):
    out,_=segment(S,box,fg,text); return box[0]+_base(out), out
def width2(lib,text,gap,space):
    w=0
    for i,c in enumerate(text):
        if c==' ': w+=space; continue
        w+=lib[c][0].shape[1]
        if i+1<len(text) and text[i+1]!=' ': w+=gap
    return w
def draw2(S, box, fg, sh, bgfun, lib, text, x, base, gap, space):
    y0,y1,x0,x1=box
    for yy in range(y0,y1):
        for xx in range(x0,x1):
            if S[yy,xx]&15 in (fg,sh): S[yy,xx]=(S[yy,xx]&0xF0)|bgfun(yy,xx)
    pts=[]
    for i,c in enumerate(text):
        if c==' ': x+=space; continue
        m,dy=lib[c]; ys,xs=np.nonzero(m)
        pts+=[(x+a,base+dy+b) for b,a in zip(ys,xs)]
        x+=m.shape[1]
        if i+1<len(text) and text[i+1]!=' ': x+=gap
    P=set(pts)
    for px,py in pts:
        for dx,dy in ((1,0),(0,1),(1,1)):
            q=(px+dx,py+dy)
            if q not in P: S[q[1],q[0]]=(S[q[1],q[0]]&0xF0)|sh
    for px,py in pts: S[py,px]=(S[py,px]&0xF0)|fg
