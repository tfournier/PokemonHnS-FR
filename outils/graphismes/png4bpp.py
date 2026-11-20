from PIL import Image
def to4bpp(path):
    im=Image.open(path)
    if im.mode!='P': return None
    w,h=im.size
    if w%8 or h%8: return None
    px=im.load(); out=bytearray()
    for ty in range(h//8):
        for tx in range(w//8):
            for y in range(8):
                for x in range(0,8,2):
                    a=px[tx*8+x,ty*8+y]&15; b=px[tx*8+x+1,ty*8+y]&15
                    out.append(a|(b<<4))
    return bytes(out)
