import re
import vocab as VV
from eclib import *
rom=open(PF+'/pokefirered.gba','rb').read(); frl=open(P+'/roms/Pokemon - Version Rouge Feu (France).gba','rb').read()
s=Sym('pfr.nm'); a,_=s.addr('sEasyChatGroups')
pat=b''.join(b'(?:.{3}[\x08\x09])'+re.escape(rom[a+8*i+4:a+8*i+8]) for i in range(22))
hits=[m.start() for m in re.finditer(pat,frl,re.S)]
def table(base):
    T={}
    for g in range(22):
        ptr=VV.rd(frl,base+8*g)-0x08000000; n=VV.rd(frl,base+8*g+4,2)
        if g in (0,18,19,21): T[g]=('list',ptr,[VV.rd(frl,ptr+2*i,2) for i in range(n)])
        else: T[g]=('words',ptr,[(ptr+12*i,VV.text(frl,VV.rd(frl,ptr+12*i)-0x08000000)) for i in range(n)])
    return T
if __name__=='__main__':
    print(hits); TL=table(hits[0]); _,TE=VV.tables(VV.fr); diff=0
    for g in range(22):
        if TL[g][0]=='list':
            if TL[g][2]!=TE[g][2]: print('list differs',g,len(TL[g][2]),len(TE[g][2]))
            continue
        for i,(p,t) in enumerate(TL[g][2]):
            e=TE[g][2][i][1] if i<len(TE[g][2]) else None
            if t!=e: diff+=1; print(GROUPS[g],i,repr(t),repr(e))
    print('diff',diff)
