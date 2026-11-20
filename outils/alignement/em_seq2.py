"""[Ancien script, remplacé par em_pointeurs.py / em_candidats.py (lot A) ; chemins rendus relatifs au projet.]
Sorties dans $LOTA_TMP (défaut memoires/lotA) ; les mémoires historiques de memoires/ ne sont pas écrasées."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from em_commun import P, MEM, TMP, ROOT
os.makedirs(TMP, exist_ok=True)
import pickle,sys,re,bisect,polib,glob; sys.path.insert(0, os.path.join(P, 'outils'))
from gen3 import Gen3
g=Gen3(ROOT)
us=open(os.path.join(MEM, 'emeraude_us.gba'),'rb').read(); fr=open(os.path.join(MEM, 'em_fr.gba'),'rb').read()
m=pickle.load(open(os.path.join(TMP, 'em_ptrmap.pkl'),'rb'))
# keep only mappings whose targets look like text in both
known=sorted(k for k,v in m.items() if 0<k<len(us) and 0<v<len(fr))
prev={}
vals=set(m.values())
def codes(s): return sorted(re.findall(r'\{[A-Z_0-9]+',s))
out=dict(prev); n=0
for f in glob.glob(os.path.join(P, 'traductions', '*.po')):
    for e in polib.pofile(f):
        if (e.msgstr and 'fuzzy' not in e.flags) or e.msgid in out: continue
        try: b=g.encode(e.msgid)
        except Exception: continue
        if not b or len(b)<4: continue
        p=us.find(b+b'\xff')
        if p<0: continue
        res=None; cands=[]
        for direction in (-1,1):
            i=bisect.bisect_left(known,p)+(-1 if direction<0 else 0)
            if direction>0 and i<len(known) and known[i]==p: i+=1
            if not (0<=i<len(known)): continue
            q=known[i]
            if abs(q-p)>3000: continue
            lo,hi=(q,p) if q<p else (p,q)
            seg=us[lo:hi]
            k=seg.count(b'\xff')
            if k>40: continue
            qq=m[q]
            if q<p:
                x=qq
                for _ in range(k): x=fr.index(b'\xff',x)+1
            else:
                x=qq
                for _ in range(k):
                    x=fr.rindex(b'\xff',0,x-1)+1 if x>0 else 0
            end=fr.find(b'\xff',x)
            if end<0 or end-x>1500: continue
            t=g.decode(fr[x:end],e.msgid)
            if not t: continue
            if codes(t)!=codes(e.msgid): continue
            r=len(t)/max(1,len(e.msgid))
            if not 0.6<r<2.0: continue
            cands.append(x)
        if len(cands)==2 and cands[0]==cands[1] and cands[0] not in vals:
            end=fr.find(b'\xff',cands[0]); t=g.decode(fr[cands[0]:end],e.msgid)
            if t and not re.search(r'[\u3040-\u30ff]',t) and t!=e.msgid and re.search(r'[a-zà-ÿ]{2}',t):
                out[e.msgid]=t; n+=1
print('nouveaux',n,'total',len(out))
pickle.dump(out,open(os.path.join(TMP, 'em_seq_pairs.pkl'),'wb'))
