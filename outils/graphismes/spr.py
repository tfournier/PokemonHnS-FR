import numpy as np
from PIL import Image
P='graphics/pokedex/hgss/tileset_interface_hns.png'
def load():
    im=Image.open(P); a=np.array(im); return im,a
def tiles(a): return [a[(i//4)*8:(i//4)*8+8,(i%4)*8:(i%4)*8+8] for i in range(a.shape[0]//8*4)]
def get(a,start,w,h):
    t=tiles(a); return np.vstack([np.hstack([t[start+r*w+c] for c in range(w)]) for r in range(h)])
def put(a,start,w,h,img):
    for r in range(h):
        for c in range(w):
            i=start+r*w+c; a[(i//4)*8:(i//4)*8+8,(i%4)*8:(i%4)*8+8]=img[r*8:r*8+8,c*8:c*8+8]
def save(im,a):
    out=Image.fromarray(a,'P'); out.putpalette(im.getpalette())
    kw={'transparency':im.info['transparency']} if 'transparency' in im.info else {}
    out.save(P,**kw)
