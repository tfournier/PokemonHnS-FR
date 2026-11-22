import sys; sys.path.insert(0,'outils/graphismes'); sys.path.insert(0,'outils/graphismes')
from dexr import *; from glyphs import *; from writeback import writeback
from dexgfx import load_tiles, read_bin
import numpy as np
U='build/upstream_orig/graphics/pokedex/hgss/'; I='images/graphics/pokedex/hgss/'; O=sys.argv[1]
pal=jasc(U+'palette_search_menu.pal')
TD=U+'tileset_menu_search_DECA.png'
HB=O+'/tilemap_search_screen_hoenn.bin'   # hoenn corrigée
# tuile 82 partagée par TYPE (ligne 6) et MODE (ligne 10) : MODE reçoit sa propre copie (rendu non-DECA identique)
import struct
_,tf0=load_tiles(I+'tileset_menu_search.png')
ref=set()
for b in [I+'tilemap_search_screen_national.bin',HB]: ref|=set(x&0x3ff for x in read_bin(b))
FREE=max(i for i in range(len(tf0)) if i not in ref and len(set((tf0[i]&15).flatten()))==1)
print('tuile libre', FREE)
A0=load(I+'tileset_menu_search.png').copy(); r,c=divmod(FREE,16); r2,c2=divmod(82,16)
A0[r*8:r*8+8,c*8:c*8+8]=A0[r2*8:r2*8+8,c2*8:c2*8+8]
save_like(I+'tileset_menu_search.png',A0,O+'/tileset_menu_search.png')
nb=bytearray(open(I+'tilemap_search_screen_national.bin','rb').read())
e=struct.unpack_from('<H',nb,2*(10*32+3))[0]; assert e&0x3ff==82
struct.pack_into('<H',nb,2*(10*32+3),(e&0xFC00)|FREE); open(O+'/tilemap_search_screen_national.bin','wb').write(nb)
NBIN=O+'/tilemap_search_screen_national.bin'
TF=O+'/tileset_menu_search.png'
DN=render(TD,U+'tilemap_search_screen_national.bin',pal); FN=render(TF,NBIN,pal)
FH=render(TF,HB,pal)
TOP=[(3,14,4,37),(3,14,52,85),(3,14,100,135)]
BTN=[(17,30,4,34),(33,46,4,34),(49,62,4,34),(65,78,4,34),(81,94,4,34),(97,110,4,32)]
EN=(['Search','Shift','Cancel'],['Name','Color','Type','Order','Mode','OK'])
FRC=(['RECH.','TRI','RETOUR'],['NOM','COUL.','TYPE','ORDRE','MODE','OK'])
FRD=(['Rech.','Tri','Retour'],['Nom','Coul.','Type','Ordre','Mode','OK'])
eT=[(DN,b,3,t) for b,t in zip(TOP,EN[0])]; eB=[(DN,b,3,t) for b,t in zip(BTN,EN[1])]
fT=[(FN,b,3,t) for b,t in zip(TOP,FRC[0])]; fB=[(FN,b,3,t) for b,t in zip(BTN,FRC[1])]
libT=build_lib2(eT); build_lib2(eB,libT); build_lib2(fT,libT)      # barre du haut : ses glyphes d'abord
libB=build_lib2(eB); build_lib2(eT,libB); build_lib2(fB,libB)
for L in (libT,libB):
    m,dy=L['n']; u=np.zeros_like(m); u[:-1,0]=u[:-1,-1]=True; u[-1,1:]=True; L['u']=(u,dy)
print(gapstats(eT+eB))
def show(m): return '\n'.join(''.join('#' if v else '.' for v in r) for r in m)
print(show(libT['u'][0]))
def redo(Fc, Sx, boxes, frc, frd, sh, bg, lib):
    for b,c,d in zip(boxes,frc,frd):
        base,out=baseline(Fc,b,3,c); x0=out[0][2]; x1=out[-1][2]+out[-1][1].shape[1]
        w=width2(lib,d,1,3); xn=(x0+x1)//2-w//2
        draw2(Sx,b,3,sh,lambda y,x:bg,lib,d,xn,base,1,3)
    return Sx
NN=FN.copy(); redo(FN,NN,TOP,FRC[0],FRD[0],9,8,libT); redo(FN,NN,BTN[:5],FRC[1][:5],FRD[1][:5],0xb,0xa,libB)
NH=FH.copy(); redo(FH,NH,TOP,FRC[0],FRD[0],9,8,libT); redo(FH,NH,BTN[:4],FRC[1][:4],FRD[1][:4],0xb,0xa,libB)
tiles_new={}; conf=[]
writeback(tiles_new,[(NN,read_bin(NBIN)),(NH,read_bin(HB))],conf)
print('conflicts',conf)
_,to=load_tiles(U+'tileset_menu_search.png'); _,tf=load_tiles(TF); to=list(to); to[FREE]=tf[FREE] if False else to[FREE]; _,td=load_tiles(TD)
A=load(TF).copy()
for t in range(len(tf)):
    r,c=divmod(t,16)
    if t in tiles_new: A[r*8:r*8+8,c*8:c*8+8]=tiles_new[t]
    elif (tf[t]==to[t]).all(): A[r*8:r*8+8,c*8:c*8+8]=td[t]
save_like(TD,A,O+'/tileset_menu_search_DECA.png')
