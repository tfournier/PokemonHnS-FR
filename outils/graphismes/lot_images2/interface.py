import sys; sys.path.insert(0,'outils/graphismes'); sys.path.insert(0,'outils/graphismes')
from pnglike import *; from spr1d import *; import numpy as np
U='build/upstream_orig/graphics/pokedex/hgss/'; I='images/graphics/pokedex/hgss/'; O=sys.argv[1]
F=load(I+'tileset_interface_hns.png'); H=load(U+'tileset_interface_hns.png')
# vérif : la version FR hns ne change que les tuiles 40-47, 64-127
d=np.nonzero(F!=H); ks=set((y//8)*4+x//8 for y,x in zip(*d)); assert ks<=set(range(40,48))|set(range(64,128)), ks
vus=get(F,64,8,4)
def m(s,y0,y1,x0,x1): return [''.join('#' if s[y,x]==0xf else '.' for x in range(x0,x1)) for y in range(y0,y1)]
caps={'V':m(vus,6,13,16,21),'P':m(get(F,96,8,4),6,13,16,21),'R':m(get(F,96,8,4),6,13,22,27)}
lower={
 'u':["#...#","#...#","#...#","#...#",".####"],
 's':[".####","#....",".###.","....#","####."],
 'r':["#.##.","##..#","#....","#....","#...."],
 'i':["#",".","#","#","#","#","#"],
}
G={}
for k,v in caps.items(): G[k]=v
for k,v in lower.items(): G[k]=v if len(v)==7 else ['.'*len(v[0])]*2+v
print(G)
def word(text, w=64, h=32, x=16, y=6):
    s=np.zeros((h,w),np.uint8); pts=[]
    for ch in text:
        g=G[ch]
        for gy,row in enumerate(g):
            for gx,c in enumerate(row):
                if c=='#': pts.append((x+gx,y+gy))
        x+=len(g[0])+1
    P=set(pts)
    for px,py in pts:
        for dx,dy in ((1,0),(0,1),(1,1)):
            if (px+dx,py+dy) not in P: s[py+dy,px+dx]=4
    for px,py in pts: s[py,px]=0xf
    return s
Vus=word('Vus'); Pris=word('Pris')
for src,deca in [('tileset_interface',False),('tileset_interface_DECA',True),('tileset_interface_DECA_hns',True)]:
    a=load(U+src+'.png'); o=a.copy()
    put(o,40,4,2,get(F,40,4,2))               # SEARCH -> RECH.
    if deca: put(o,64,8,4,Vus); put(o,96,8,4,Pris)
    else: put(o,64,8,4,get(F,64,8,4)); put(o,96,8,4,get(F,96,8,4))
    save_like(U+src+'.png',o,O+'/'+src+'.png')
