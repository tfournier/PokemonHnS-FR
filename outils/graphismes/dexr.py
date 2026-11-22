import sys; sys.path.insert(0,'outils/graphismes'); from pnglike import *; from dexgfx import load_tiles, read_bin, compose
from PIL import Image
import numpy as np
def jasc(p):
    L=open(p).read().split('\n')[3:]; return [tuple(int(v) for v in l.split()) for l in L if l.strip()]
def render(png, binf, pal, out=None, s=2):
    im,t=load_tiles(png); S=compose(t, read_bin(binf))
    img=rgb(S,pal)
    if out: img.resize((img.size[0]*s,img.size[1]*s),Image.NEAREST).save(out)
    return S
if __name__=='__main__':
    U='build/upstream_orig/graphics/pokedex/hgss/'; I='images/graphics/pokedex/hgss/'
    pal=jasc(U+sys.argv[1]); outs=[]
    for png,b in zip(sys.argv[3::2],sys.argv[4::2]):
        outs.append(rgb(render(png,b,pal),pal))
    W=sum(o.size[0]+4 for o in outs); H=max(o.size[1] for o in outs)
    c=Image.new('RGB',(W,H)); x=0
    for o in outs: c.paste(o,(x,0)); x+=o.size[0]+4
    c=c.resize((c.size[0]*2,c.size[1]*2),Image.NEAREST); c.save(sys.argv[2])
