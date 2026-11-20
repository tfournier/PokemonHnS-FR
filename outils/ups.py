import sys, zlib
def enc(v):
    out=bytearray()
    while True:
        x=v&0x7f; v>>=7
        if v==0: out.append(0x80|x); break
        out.append(x); v-=1
    return bytes(out)
a=open(sys.argv[1],'rb').read(); b=open(sys.argv[2],'rb').read()
n=max(len(a),len(b)); A=a.ljust(n,b'\0'); B=b.ljust(n,b'\0')
p=bytearray(b'UPS1'+enc(len(a))+enc(len(b)))
i=0; last=0
while i<n:
    if A[i]==B[i]: i+=1; continue
    p+=enc(i-last)
    j=i
    while j<n and A[j]!=B[j]: p.append(A[j]^B[j]); j+=1
    p.append(0); last=j+1; i=j+1
p+=zlib.crc32(a).to_bytes(4,'little')+zlib.crc32(b).to_bytes(4,'little')
p+=zlib.crc32(bytes(p)).to_bytes(4,'little')
open(sys.argv[3],'wb').write(p); print(len(p))
