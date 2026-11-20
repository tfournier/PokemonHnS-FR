import struct
from PIL import Image
def retile(composed, orig_bin, orig_png, out_png, out_bin, cols=32):
    d=open(orig_bin,'rb').read(); n=len(d)//2
    op=Image.open(orig_png)
    t0=op.crop((0,0,8,8))
    tiles=[t0.tobytes()]; idx={t0.tobytes():0}
    ents=[]
    for k in range(n):
        e=struct.unpack_from('<H',d,2*k)[0]
        x,y=(k%cols)*8,(k//cols)*8
        tb=composed.crop((x,y,x+8,y+8)).tobytes()
        if tb not in idx: idx[tb]=len(tiles); tiles.append(tb)
        ents.append((e&0xF000)|idx[tb])
    out=Image.new('P',(8*len(tiles),8)); out.putpalette(op.getpalette())
    for i,tb in enumerate(tiles): out.paste(Image.frombytes('P',(8,8),tb),(8*i,0))
    kw={'transparency':op.info['transparency']} if 'transparency' in op.info else {}
    out.save(out_png,**kw)
    open(out_bin,'wb').write(b''.join(struct.pack('<H',e) for e in ents))
    return len(tiles)
