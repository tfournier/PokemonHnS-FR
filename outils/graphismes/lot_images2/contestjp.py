import sys; sys.path.insert(0,'outils/graphismes'); from pnglike import *; import numpy as np
import police3x5 as P
U='build/upstream_orig/graphics/contest/japanese/'; O=sys.argv[1]
def dil(m):
    r=m.copy()
    for dy in (-1,0,1):
        for dx in (-1,0,1): r|=np.roll(np.roll(m,dy,0),dx,1)
    return r
# letters : ランク -> RANG
a=load(U+'letters.png'); o=a.copy()
for c in range(5):
    x0=c*16; o[9:16,x0:x0+16]=0xa
    P.draw(o,x0,10,'RANG',1,5)
save_like(U+'letters.png',o,O+'/letters.png')
# numbers : 位 -> ER / E (encre 2, contour 1)
a=load(U+'numbers.png'); o=a.copy()
for c,suf in enumerate(['ER','E','E','E']):
    x0=c*16
    cell=o[0:16,x0:x0+16]
    dig=np.isin(cell,[5,6,7,8]); keep=dil(dig)
    win=np.zeros_like(dig); win[7:15,8:16]=True
    clear=(win&~keep)|(win&np.isin(cell,[2,3,4])); cell[clear]=0
    t=np.zeros((16,16),np.uint8); P.draw(t,8 if suf=='ER' else 10,8,suf,2)
    ink=(t==2); out=dil(ink)&~ink
    cell[out&~keep&(cell==0)]=1; cell[ink]=2
save_like(U+'numbers.png',o,O+'/numbers.png')
# interface : 大 -> +, アピール!! -> DEMO!!, ぼうがい!! -> BLOCAGE!!, ツギ -> SUIV., バン -> TOUR
a=load(U+'interface.png'); o=a.copy()
reg=o[16:24,0:9]; reg[reg==0xd]=0; P.draw(o,2,18,'+',0xd)
def repl(y0,y1,x0,x1,col,text,bgcol):
    reg=o[y0:y1,x0:x1]; reg[(reg==0xb)|(reg==0xc)]=bgcol
    w=P.width(text); P.draw(o,x0+(x1-x0-w)//2,y0+(y1-y0-5)//2,text,col)
repl(8,16,72,112,0xb,'DEMO!!',0xa)
repl(16,24,72,112,0xc,'BLOCAGE!!',0xa)
reg=o[24:32,0:16]; reg[reg==0xb]=0; P.draw(o,0,26,'SUIV',0xb); o[30,15]=0xb
reg=o[24:32,24:40]; reg[(reg==0xb)|(reg==0xf)]=0; P.draw(o,24,26,'TOUR',0xb)
save_like(U+'interface.png',o,O+'/interface.png')
# voltage : ボルテージ -> AMBIANCE
a=load(U+'voltage.png'); o=a.copy()
reg=o[8:15,23:64]; reg[reg==6]=1; P.draw(o,64-P.width('AMBIANCE')-1,9,'AMBIANCE',6)
save_like(U+'voltage.png',o,O+'/voltage.png')
