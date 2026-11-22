import sys; sys.path.insert(0,'outils/graphismes'); sys.path.insert(0,'outils/graphismes')
from pnglike import *; from dexgfx import load_tiles, read_bin, compose; from glyphs import *; from writeback import writeback
import numpy as np
U='build/upstream_orig/graphics/dexnav/'; O=sys.argv[1]
_,t=load_tiles(U+'gui_tiles.png'); e=read_bin(U+'gui_tilemap.bin')
C=compose(t,e)&15
L=[((13,22,10,40),'WATER'),((55,63,2,30),'LAND'),((119,127,35,72),"HIDDEN")]
R=[((37,45,162,240),'SPECIES'),((61,69,162,240),'TYPE'),((85,93,162,240),'SEARCH LEVEL'),((109,117,162,240),'HIDDEN ABILITY'),((133,141,162,240),'CURRENT CHAIN')]
for b,tx in R:
    m=(C[b[0]:b[1],b[2]:b[3]]==1); 
libL=build_lib2([(C,b,1,tx) for b,tx in L]); libR=build_lib2([(C,b,1,tx) for b,tx in R])
for c in 'CSU':
    if c not in libL: libL[c]=libR[c]
m,dy=libR['I']; libR['.']=(np.ones((1,1),bool),0)
print(gapstats([(C,b,1,tx) for b,tx in L])); print(gapstats([(C,b,1,tx) for b,tx in R]))
def drawx(S,box,fg,sh,bgfun,lib,text,x,base,gap,space):
    y0,y1,x0,x1=box
    for yy in range(y0,y1+1):
        for xx in range(x0,x1):
            if S[yy,xx] in ((fg,sh) if sh is not None else (fg,)): S[yy,xx]=bgfun(yy,xx)
    pts=[]
    for i,c in enumerate(text):
        if c==' ': x+=space; continue
        mm,d=lib[c]; ys,xs=np.nonzero(mm); pts+=[(x+a,base+d+bb) for bb,a in zip(ys,xs)]
        x+=mm.shape[1]+(gap if i+1<len(text) and text[i+1]!=' ' else 0)
    P=set(pts)
    if sh is not None:
        for px,py in pts:
            for dx,dy2 in ((1,0),(0,1),(1,1)):
                if (px+dx,py+dy2) not in P: S[py+dy2,px+dx]=sh
    for px,py in pts: S[py,px]=fg
N=C.copy()
FRL=['EAU','TERRE','CACHES']; FRR=['ESPECE','TYPE','NIV. RECH.','TALENT CACHE','CHAINE ACT.']
for (b,tx),fr in zip(L,FRL):
    base,out=baseline(C,b,1,tx); x0=out[0][2]; xend=out[-1][2]+out[-1][1].shape[1]+2
    def bg(y,x,b=b,xend=xend):
        xx=x
        while xx<xend: xx+=16
        return C[y,xx]
    drawx(N,b,1,7,bg,libL,fr,x0,base,1,3)
for (b,tx),fr in zip(R,FRR):
    base,out=baseline(C,b,1,tx); x0=out[0][2]
    drawx(N,b,1,None,lambda y,x:2,libR,fr,x0,base,1,3)
# bouton SEARCH (gras) -> RECH.
bb=(19,28,168,219)
sub=C[bb[0]:bb[1],bb[2]:bb[3]]
out,_=segment(C,bb,1,'SEARCH'); base=bb[0]+max(np.nonzero(m.any(1))[0].max() for c,m,x in out)
libS={}
for c,m,x in out:
    r=np.nonzero(m.any(1))[0]; libS[c]=(m[r.min():r.max()+1],r.min()-(base-bb[0]))
libS['.']=(np.ones((2,2),bool),-1)
x0=out[0][2]; x1=out[-1][2]+out[-1][1].shape[1]
w=sum(libS[c][0].shape[1] for c in 'RECH.')+4*1
reg=N[bb[0]:bb[1]+1,bb[2]:bb[3]]
drawx(N,bb,1,None,lambda y,x:6,libS,'RECH.',x0+(x1-x0-w)//2,base,1,3)
np.save(O+'/comp.npy',np.stack([C,N]))
import struct
A=load(U+'gui_tiles.png').copy(); W=A.shape[1]//8; NT=(A.shape[0]//8)*W
def T(k): r,c=divmod(k,W); return A[r*8:r*8+8,c*8:c*8+8]
ref=set(x&0x3ff for x in e)
free=[k for k in range(NT) if k not in ref]
ents=list(e); tiles_new={}; moved=[]
# 1er passage : contenu voulu par position
want={}
for k,x in enumerate(e):
    t=x&0x3ff; y=(k//32)*8; xx=(k%32)*8
    p=N[y:y+8,xx:xx+8].copy()
    if x&0x400: p=p[:,::-1]
    if x&0x800: p=p[::-1,:]
    want.setdefault(t,[]).append((k,p))
for t,lst in want.items():
    # contenu majoritaire garde l'indice ; les autres positions reçoivent une tuile libre
    from collections import Counter
    cnt=Counter(p.tobytes() for k,p in lst); keep=cnt.most_common(1)[0][0]
    # si l'original (C) est inchangé pour la majorité, on garde
    tiles_new[t]=np.frombuffer(keep,np.uint8).reshape(8,8)
    extra={}
    for k,p in lst:
        b=p.tobytes()
        if b==keep: continue
        if b not in extra: extra[b]=free.pop(0)
        nt=extra[b]; tiles_new[nt]=p; ents[k]=(e[k]&0xFC00)|nt; moved.append((k,t,nt))
print('entrées déplacées', len(moved), 'tuiles libres utilisées', sorted(set(m[2] for m in moved)))
for k,p in tiles_new.items():
    r,c=divmod(k,W); A[r*8:r*8+8,c*8:c*8+8]=(A[r*8:r*8+8,c*8:c*8+8]&0xF0)|p
save_like(U+'gui_tiles.png',A,O+'/gui_tiles.png')
open(O+'/gui_tilemap.bin','wb').write(b''.join(struct.pack('<H',x) for x in ents))
_,t2=load_tiles(O+'/gui_tiles.png'); C2=compose(t2,ents)&15
print('rendu conforme', (C2==N).all())
