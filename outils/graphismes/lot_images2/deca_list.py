import sys; sys.path.insert(0,'outils/graphismes'); sys.path.insert(0,'outils/graphismes')
from dexr import *; from glyphs import *; from writeback import writeback
from dexgfx import load_tiles, read_bin
import numpy as np
U='build/upstream_orig/graphics/pokedex/hgss/'; I='images/graphics/pokedex/hgss/'; O=sys.argv[1]
pal=jasc(U+'palette_default.pal')
TD=U+'tileset_menu_list_DECA.png'; TF=I+'tileset_menu_list.png'
D5=render(TD,U+'tilemap_start_menu_search_results.bin',pal); F5=render(TF,I+'tilemap_start_menu_search_results.bin',pal)
F4=render(TF,I+'tilemap_start_menu.bin',pal)
DL=render(TD,U+'tilemap_list_screen.bin',pal); FL=render(TF,I+'tilemap_list_screen.bin',pal)
L5=[11,27,43,59,75]; L4=[11,27,43,59]
def bx(y): return (y,y+11,140,231)
EN=['Back To List','List Top','List Bottom','Back To Pokédex','Close Pokédex']
FRC=['RETOUR LISTE','HAUT DE LISTE','BAS DE LISTE','RETOUR POKéDEX','FERMER POKéDEX']
FRD=['Retour liste','Haut de liste','Bas de liste','Retour Pokédex','Fermer Pokédex']
libM=build_lib([(D5,bx(y),0xf,t) for y,t in zip(L5,EN)])
libMF=build_lib([(F5,bx(y),0xf,t) for y,t in zip(L5,FRC)])
for c in 'RHF': libM[c]=libMF[c]
def g(rows,top=3,h=11): 
    m=np.zeros((h,len(rows[0])),bool)
    for i,r in enumerate(rows): m[top+i]=[c=='#' for c in r]
    return m
libM['u']=g(["#...#","#...#","#...#","#...#","#...#",".####"])
libM['r']=g(["#.##.","##..#","#....","#....","#....","#...."])
BL=(150,160,113,182)
libB=build_lib([(DL,BL,0xf,'Menu Search')]); libBF=build_lib([(FL,BL,0xf,'MENU RECH.')])
for c in 'R.': libB[c]=libBF[c]
def white(y,x): return 1
# fond de la barre du bas : quadrillage (indice 4)
gridrows=[y for y in range(BL[0],BL[1]) if ((FL[y,113:182]&15)==4).sum()>40]
gridcols=[x for x in range(113,182) if ((FL[140:149,x]&15)==4).all()]
print('grid', gridrows, gridcols)
def gridbg(y,x): return 4 if (y in gridrows or x in gridcols) else 1
def redo(Fc, lines, texts):
    S=Fc.copy()
    for y,t in zip(lines,texts):
        out,_=segment(Fc,bx(y),0xf,FRC[FRD.index(t)])
        x0=out[0][2]
        y0,y1,a0,a1=bx(y); reg=S[y0:y1,a0:a1]; reg[(reg&15)==5]=(reg[(reg&15)==5]&0xF0)|1
        draw(S,bx(y),0xf,3,white,libM,t,x0,1,4)
    return S
N5=redo(F5,L5,FRD); N4=redo(F4,L4,[FRD[i] for i in (0,1,2,4)])
NL=FL.copy()
out,_=segment(FL,BL,0xf,'MENU RECH.')
# centre de RECH. conservé
xs=[x for c,m,x in out[4:]]; x0=xs[0]; x1=out[-1][2]+out[-1][1].shape[1]
w=width(libB,'Rech.',1,4); xn=(x0+x1)//2-w//2
# effacer seulement RECH.
draw(NL,(150,160,out[4][2],x1+2),0xf,4,gridbg,libB,'Rech.',xn,1,4)
m0=out[0][2]; m1=out[3][2]+out[3][1].shape[1]
w=width(libB,'Menu',1,4); xm=(m0+m1)//2-w//2
draw(NL,(150,160,m0,m1+2),0xf,4,gridbg,libB,'Menu',xm,1,4)
tiles_new={}; conf=[]
writeback(tiles_new,[(N5,read_bin(I+'tilemap_start_menu_search_results.bin')),(N4,read_bin(I+'tilemap_start_menu.bin')),(NL,read_bin(I+'tilemap_list_screen.bin')),
                     (render(TF,I+'tilemap_list_screen_underlay.bin',pal),read_bin(I+'tilemap_list_screen_underlay.bin'))],conf)
print('conflicts',conf)
# tuileset final
_,to=load_tiles(U+'tileset_menu_list.png'); _,tf=load_tiles(TF); _,td=load_tiles(TD)
A=load(TF).copy(); n=len(tf); cols=16
for t in range(n):
    r,c=divmod(t,cols)
    if t in tiles_new: A[r*8:r*8+8,c*8:c*8+8]=tiles_new[t]
    elif (tf[t]==to[t]).all(): A[r*8:r*8+8,c*8:c*8+8]=td[t]
save_like(TD,A,O+'/tileset_menu_list_DECA.png')
for nm,b in [('sr','tilemap_start_menu_search_results'),('sm','tilemap_start_menu'),('ls','tilemap_list_screen')]:
    pass
