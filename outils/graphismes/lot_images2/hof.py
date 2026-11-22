import sys; sys.path.insert(0,'outils/graphismes'); from pnglike import *; import numpy as np
import police3x5 as P
O=sys.argv[1]; U='build/upstream_orig/graphics/misc/'
def stream(a,W): return [a[(k//W)*8:(k//W)*8+8,(k%W)*8:(k%W)*8+8].copy() for k in range((a.shape[0]//8)*W)]
def unstream(ts,W,shape):
    a=np.zeros(shape,np.uint8)
    for k,t in enumerate(ts): a[(k//W)*8:(k//W)*8+8,(k%W)*8:(k%W)*8+8]=t
    return a
j=load(U+'japanese_hof.png'); h=load(U+'hall_of_fame.png')
sj=stream(j,13); sh=stream(h,8)
print('flux identiques', all((sj[k]==sh[k]).all() for k in range(29)), [k for k in range(32) if not (sj[k]==sh[k]).all()])
s=np.vstack([np.hstack(sj[3:16]),np.hstack(sj[16:29])])
for (x0,x1),word in [((11,33),'CHOIX'),((45,67),'SUITE'),((79,102),'RETOUR')]:
    reg=s[:,x0:x1]; reg[(reg==0xf)|(reg==0xe)]=1
    w=P.width(word); P.draw(s, x0+(x1-x0-w)//2, 4, word, 0xf, 0xe)
for k in range(13): sj[3+k]=s[0:8,k*8:k*8+8]; sj[16+k]=s[8:16,k*8:k*8+8]
oj=unstream(sj,13,j.shape)
save_like(U+'japanese_hof.png',oj,O+'/japanese_hof.png')
save_like(U+'japanese_hof_hns.png',oj,O+'/japanese_hof_hns.png')
for k in range(32): sh[k]=sj[k] if k<29 else sh[k]
save_like(U+'hall_of_fame.png',unstream(sh,8,h.shape),O+'/hall_of_fame.png')
