import sys, zlib
def rd(d,i):
    v=0;s=1
    while True:
        x=d[i];i+=1
        if x&0x80: v+=(x&0x7f)*s; break
        v+=(x|0x80)*s; s<<=7
    return v,i
p=open(sys.argv[2],'rb').read(); src=open(sys.argv[1],'rb').read()
assert p[:4]==b'UPS1'
i=4; ins,i=rd(p,i); outs,i=rd(p,i)
out=bytearray(src[:outs]+b'\0'*max(0,outs-len(src)))
pos=0; end=len(p)-12
while i<end:
    skip,i=rd(p,i); pos+=skip
    while p[i]!=0:
        if pos<outs: out[pos]^=p[i]
        pos+=1; i+=1
    i+=1; pos+=1
open(sys.argv[3],'wb').write(out)
print('crc out %08x expected %08x'%(zlib.crc32(out), int.from_bytes(p[-8:-4],'little')))
