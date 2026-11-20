import sys, struct
from PIL import Image
def tiles_of(png):
    im=Image.open(png); assert im.mode=='P'
    w,h=im.size; t=[]
    for ty in range(h//8):
        for tx in range(w//8): t.append(im.crop((tx*8,ty*8,tx*8+8,ty*8+8)))
    return im, t
def render(png, binf, cols=32, out=None):
    im,t=tiles_of(png); d=open(binf,'rb').read(); n=len(d)//2
    rows=n//cols; c=Image.new('P',(cols*8,rows*8)); c.putpalette(im.getpalette())
    for k in range(n):
        e=struct.unpack_from('<H',d,2*k)[0]; ti=e&0x3FF
        if ti>=len(t): continue
        tile=t[ti]
        if e&0x400: tile=tile.transpose(Image.FLIP_LEFT_RIGHT)
        if e&0x800: tile=tile.transpose(Image.FLIP_TOP_BOTTOM)
        c.paste(tile,((k%cols)*8,(k//cols)*8))
    return c
if __name__=='__main__':
    c=render(sys.argv[1],sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 32)
    c.save(sys.argv[4] if len(sys.argv)>4 else '/tmp/o.png')
