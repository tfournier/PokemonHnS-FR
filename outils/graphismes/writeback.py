import numpy as np
from dexgfx import read_bin
def writeback(tiles_new, comps, conflicts):
    """tiles_new: dict t->8x8 ; comps: [(composite S (low nibble), entries)]"""
    for S,ents in comps:
        for k,e in enumerate(ents):
            t=e&0x3ff; y=(k//32)*8; x=(k%32)*8
            p=(S[y:y+8,x:x+8]&15).copy()
            if e&0x400: p=p[:,::-1]
            if e&0x800: p=p[::-1,:]
            if t in tiles_new and (tiles_new[t]!=p).any(): conflicts.append((t,k)); continue
            tiles_new[t]=p
