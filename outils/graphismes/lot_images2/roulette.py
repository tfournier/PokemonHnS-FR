import sys; sys.path.insert(0,'outils/graphismes'); from pnglike import *; import numpy as np
U='build/upstream_orig/graphics/roulette/'
O=sys.argv[1]
c=load(U+'credit.png'); w=load(U+'window.png')
def mask(arr,y0,x0): return [''.join('#' if arr[y0+y,x0+x] not in (0,1) else '.' for x in range(7)) for y in range(7)]
# glyphes existants
G={}
for i,ch in enumerate('CREDIT'): pass
G['E']=mask(c,8,24); G['T']=mask(w,48,0); G['I']=mask(w,48,8); G['M']=mask(w,48,16)
G['J']=["..#####","....##.","....##.","....##.","##..##.","###.##.",".####.."]
G['O']=[".#####.","###..##","##...##","##...##","##...##","###..##",".#####."]
G['N']=["##...##","###..##","####.##","##.####","##..###","##...##","##...##"]
G['S']=[".#####.","###..##","###....",".#####.","....###","##..###",".#####."]
for k,v in G.items(): print(k); print('\n'.join(v))
def draw(arr,x,y,text,rowcol,keep=None):
    pts=[]
    for ch in text:
        g=G[ch]
        for gy,row in enumerate(g):
            for gx,ch2 in enumerate(row):
                if ch2=='#': pts.append((x+gx,y+gy))
        x+=8
    P=set(pts)
    for (px,py) in pts:
        for dx,dy in ((1,0),(0,1),(1,1)):
            q=(px+dx,py+dy)
            if q not in P: arr[q[1],q[0]]=1
    for (px,py) in pts: arr[py,px]=rowcol[py-y]
# credit : zone texte x 8..55, y 8..15
o=c.copy(); o[8:16,8:56]=0
draw(o,8,8,'JETONS',[0xd,0xd,0xf,0xf,0xf,0xf,0xe])
save_like(U+'credit.png',o,O+'/credit.png')
# window : tuiles 96..103 (y 48..55, x 0..63) ; on garde M, I, E d'origine
o=w.copy(); o[48:56,0:64]=0
draw(o,0,48,'MISEJTON',[0xd,0xd,0xd,0xf,0xe,0xe,0xe])
o[48:56,0:8]=w[48:56,16:24]; o[48:56,8:16]=w[48:56,8:16]; o[48:56,24:32]=w[48:56,24:32]
save_like(U+'window.png',o,O+'/window.png')
