import numpy as np
def tile(a,k): return a[(k//4)*8:(k//4)*8+8,(k%4)*8:(k%4)*8+8]
def get(a,start,w,h):
    return np.vstack([np.hstack([tile(a,start+r*w+c) for c in range(w)]) for r in range(h)])
def put(a,start,w,h,img):
    for r in range(h):
        for c in range(w):
            k=start+r*w+c; a[(k//4)*8:(k//4)*8+8,(k%4)*8:(k%4)*8+8]=img[r*8:r*8+8,c*8:c*8+8]
