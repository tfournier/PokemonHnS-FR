"""[Ancien script, remplacé par em_pointeurs.py / em_candidats.py (lot A) ; chemins rendus relatifs au projet.]
Sorties dans $LOTA_TMP (défaut memoires/lotA) ; les mémoires historiques de memoires/ ne sont pas écrasées."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from em_commun import P, MEM, TMP, ROOT
os.makedirs(TMP, exist_ok=True)
import pickle,sys,struct,re; sys.path.insert(0, os.path.join(P, 'outils'))
from gen3 import Gen3
import polib,glob
g=Gen3(ROOT)
us=open(os.path.join(MEM, 'emeraude_us.gba'),'rb').read(); fr=open(os.path.join(MEM, 'em_fr.gba'),'rb').read()
def mask(rom):
    b=bytearray(rom)
    for i in range(len(b)-3):
        if b[i+3] in (8,9): b[i:i+4]=b'\0\0\0\0'
    return bytes(b)
mu,mf=mask(us),mask(fr)
# index of pointers in US: target -> list of positions
refs={}
for p in range(len(us)-3):
    if us[p+3]==8:
        v=struct.unpack_from('<I',us,p)[0]-0x08000000
        refs.setdefault(v,[]).append(p)
m=pickle.load(open(os.path.join(TMP, 'em_ptrmap.pkl'),'rb'))
out={}
stats={'cand':0,'map':0,'ctx':0}
for f in glob.glob(os.path.join(P, 'traductions', '*.po')):
    for e in polib.pofile(f):
        if e.msgstr and 'fuzzy' not in e.flags: continue
        try: b=g.encode(e.msgid)
        except Exception: continue
        if not b or len(b)<4: continue
        p=us.find(b+b'\xff')
        if p<0: continue
        stats['cand']+=1
        q=m.get(p)
        if q is None:
            for r in refs.get(p,[]):
                for L,R in ((16,16),(24,8),(8,24),(32,32)):
                    ctx=mu[r-L:r+4+R]
                    j=mf.find(ctx)
                    if j>=0 and mf.find(ctx,j+1)<0:
                        w=struct.unpack_from('<I',fr,j+L)[0]
                        if 0x08000000<=w<0x09000000: q=w-0x08000000; stats['ctx']+=1
                        break
                if q is not None: break
        else: stats['map']+=1
        if q is None: continue
        end=fr.find(b'\xff',q)
        if end<0 or end-q>1500: continue
        d=g.decode(fr[q:end+1],e.msgid)
        if d: out[e.msgid]=d
print(stats,len(out))
pickle.dump(out,open(os.path.join(TMP, 'em_ctx_pairs.pkl'),'wb'))
