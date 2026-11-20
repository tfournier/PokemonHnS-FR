# noms par index : fichier HnS -> [(ligne, EN, FR Émeraude, adresse US, adresse FR)]
import sys, re, json, collections
P='/Users/tfournier/projets/gitlab.com/tfournier/PokemonHnS-FR'
sys.path.insert(0, P+'/outils')
from gen3 import Gen3
import hnsfr
R=P+'/build/upstream_orig'
g=Gen3(R)
us=open(P+'/memoires/emeraude_us.gba','rb').read(); fr=open(P+'/memoires/em_fr.gba','rb').read()
def rd(rom,a,n=12):
    b=rom[a:a+n]; i=b.find(b'\xff'); return g.decode(b[:i] if i>=0 else b)
occs=hnsfr.scan_file(R,'src/data/trainers.party')
out={}
# gTrainers
L=[]
src=open(R+'/src/data/trainers.party').read().split('\n')
idx=0; ids=[]
for i,l in enumerate(src):
    if l.startswith('=== TRAINER_'): ids.append((i+1,l[4:-4]))
names={o.line:o.text for o in occs}
# each trainer: Name line follows header
res=[]
for k,(ln,tid) in enumerate(ids):
    nm=None
    for j in range(ln, ln+3):
        if j+1 in names: nm=(j+1,names[j+1]); break
        if src[j].startswith('Name:'): nm=(j+1,''); break
    a=0x310034+k*40; b=a+31536
    res.append(dict(ligne=nm[0] if nm else 0,id=tid,en=nm[1] if nm else '',us=rd(us,a),fr=rd(fr,b),adr='gTrainers[%d] US %X -> FR %X'%(k,a,b)))
bad=[r for r in res if r['en']!=r['us']]
print('trainers.party',len(res),'diff EN/US',len(bad),bad[:5])
out['src/data/trainers.party']=res
def table(path, attr, delta, step):
    txt=open(R+'/'+path).read()
    lst=[]
    for m in re.finditer(r'\.'+attr+r'\s*=\s*_\("((?:[^"\\]|\\.)*)"\)', txt):
        lst.append((txt.count('\n',0,m.start())+1, m.group(1)))
    # trouver base
    first=g.encode(lst[0][1])+b'\xff'
    best=None
    p=us.find(first)
    while p>=0:
        ok=sum(1 for i,(ln,n) in enumerate(lst) if rd(us,p+i*step,8 if step==52 else 12)==n)
        if not best or ok>best[0]: best=(ok,p)
        p=us.find(first,p+1)
    ok,p=best
    res=[]
    for i,(ln,n) in enumerate(lst):
        a=p+i*step
        res.append(dict(ligne=ln,en=n,us=rd(us,a,8 if step==52 else 12),fr=rd(fr,a+delta,8 if step==52 else 12),adr='%s[%d] US %X -> FR %X'%(path.split('/')[-1],i,a,a+delta)))
    print(path,attr,len(lst),'match',ok)
    return res
out['src/data/battle_frontier/battle_frontier_trainers.h']=table('src/data/battle_frontier/battle_frontier_trainers.h','trainerName',17660,52)
# tentes : 3 tables de 30 dans le même fichier, à traiter par blocs
txt=open(R+'/src/data/battle_frontier/battle_tent.h').read()
lst=[(txt.count('\n',0,m.start())+1,m.group(1)) for m in re.finditer(r'\.trainerName\s*=\s*_\("([^"]*)"\)',txt)]
res=[]
for blk in range(0,len(lst),30):
    sub=lst[blk:blk+30]
    first=g.encode(sub[0][1])+b'\xff'; best=None; p=us.find(first)
    while p>=0:
        ok=sum(1 for i,(ln,n) in enumerate(sub) if rd(us,p+i*52,8)==n)
        if not best or ok>best[0]: best=(ok,p)
        p=us.find(first,p+1)
    ok,p=best; print('tent blk',blk,'match',ok)
    for i,(ln,n) in enumerate(sub):
        a=p+i*52; res.append(dict(ligne=ln,en=n,us=rd(us,a,8),fr=rd(fr,a+17660,8),adr='battle_tent[%d] US %X -> FR %X'%(blk+i,a,a+17660)))
out['src/data/battle_frontier/battle_tent.h']=res
out['src/data/contest_opponents.h']=table('src/data/contest_opponents.h','trainerName',17356,64)
json.dump(out,open(sys.argv[1],'w'),ensure_ascii=False,indent=0)
for k,v in out.items():
    print(k, sum(1 for r in v if r['en']!=r['us']), 'diff')
