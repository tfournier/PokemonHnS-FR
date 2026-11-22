import sys; sys.path.insert(0,'outils/graphismes')
from lz77 import lz77; from tiles4bpp import from4bpp; from pnglike import *; from dexgfx import load_tiles, read_bin, compose
import numpy as np, struct
O=sys.argv[1]
U='build/upstream_orig/graphics/credits_frlg/'
rf=open('roms/Pokemon - Version Rouge Feu (France).gba','rb').read()
a=from4bpp(lz77(rf,0xeafa74),16)
_,t=load_tiles(U+'the_end.png'); e=read_bin(U+'the_end.bin'); C=compose(t,e)&15
ys,xs=np.nonzero(C[64:88]==15); cx=(xs.min()+xs.max())//2; print('THE END ink x',xs.min(),xs.max(),'rows',ys.min(),ys.max())
g=a[0:22,8:84].copy(); gm=(g==15)|(g==10)
fy,fx=np.nonzero(g==15); print('FIN ink',fx.min(),fx.max(),fy.min(),fy.max())
N=C.copy(); band=N[64:88]; band[:,:240][band[:,:240]!=0]=1
band[:]=np.where(C[64:88]==0,0,1)
w=fx.max()-fx.min()+1; X0=cx-w//2-fx.min()
best=None
for dx in range(-4,5):
  for dy in (0,):
    Nt=C.copy(); bt=Nt[64:88]; bt[:]=np.where(C[64:88]==0,0,1)
    sub=bt[0:22, X0+dx:X0+dx+76]; sub[gm]=g[gm]
    us=set()
    for r in range(8,11):
        for c in range(30):
            p=Nt[r*8:r*8+8,c*8:c*8+8]
            us.add(min(p.tobytes(),p[:,::-1].tobytes(),p[::-1].tobytes(),p[::-1,::-1].tobytes()))
    print(dx,len(us))
    if best is None or len(us)<best[0]: best=(len(us),dx,Nt)
N=best[2]; print('dx',best[1])
# ombre/anticrénelage 'a' déjà dans g ; retuilage des lignes 8-10
tiles=[t[0]&15, t[1]&15]; ents=list(e)
def key(p): return p.tobytes()
def find(p):
    for i,q in enumerate(tiles):
        for fl,qq in ((0,q),(0x400,q[:,::-1]),(0x800,q[::-1,:]),(0xC00,q[::-1,::-1])):
            if (qq==p).all(): return i|fl
    return None
for r in range(8,11):
    for c in range(30):
        p=N[r*8:r*8+8,c*8:c*8+8]
        k=find(p)
        if k is None: tiles.append(p.copy()); k=len(tiles)-1
        ents[r*32+c]=k
print('tuiles', len(tiles))
assert len(tiles)<=14
im=load(U+'the_end.png'); out=np.zeros_like(im)
for i,p in enumerate(tiles): out[:,i*8:i*8+8]=p
save_like(U+'the_end.png',out,O+'/the_end.png')
open(O+'/the_end.bin','wb').write(b''.join(struct.pack('<H',x) for x in ents))
_,t2=load_tiles(O+'/the_end.png'); C2=compose(t2,ents)&15
assert (C2==N).all()
np.save(O+'/the_end_comp.npy',np.stack([C,N]))
