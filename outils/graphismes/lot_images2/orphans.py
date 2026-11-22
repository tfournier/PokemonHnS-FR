import sys; sys.path.insert(0,'outils/graphismes'); from dexgfx import load_tiles, read_bin
from pnglike import *
from collections import defaultdict
import numpy as np
U='build/upstream_orig/graphics/pokedex/hgss/'; I='images/graphics/pokedex/hgss/'; O=sys.argv[1]
sets={'tileset_menu1':['tilemap_info_screen','tilemap_stats_screen'],
      'tileset_menu2':['tilemap_evo_screen','tilemap_evo_screen_PE','tilemap_forms_screen'],
      'tileset_menu3':['tilemap_cry_screen','tilemap_size_screen']}
for ts,bins in sets.items():
    _,o=load_tiles(U+ts+'.png'); a=load(I+ts+'.png'); out=a.copy()
    refo=set(); reff=set(); mp=defaultdict(set)
    for b in bins:
        eo=read_bin(U+b+'.bin'); ef=read_bin(I+b+'.bin')
        for x,c in zip(eo,ef):
            refo.add(x&0x3ff); reff.add(c&0x3ff)
            if x!=c: mp[x&0x3ff].add((c&0x3ff,(x^c)&0xC00))
    done=[]
    for t in sorted(refo-reff):
        (j,fl),=mp[t]; assert fl==0
        r,c=divmod(t,16); rj,cj=divmod(j,16)
        out[r*8:r*8+8,c*8:c*8+8]=a[rj*8:rj*8+8,cj*8:cj*8+8]; done.append((t,j))
    print(ts,len(done),done)
    save_like(I+ts+'.png',out,O+'/'+ts+'.png')
