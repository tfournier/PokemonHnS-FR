import sys,struct,collections,re,polib,glob,pickle; sys.path.insert(0,'/home/claude/pokehns-fr/outils')
from gen3 import Gen3
import ahocorasick
g=Gen3('/home/claude/pokehns-fr/build/upstream')
en=open('memoires/hns_en.gba','rb').read(); fr=open('memoires/hns_fr_patch.gba','rb').read()
todo={}
for f in glob.glob('traductions/*.po'):
    for e in polib.pofile(f):
        if not e.msgstr or 'fuzzy' in e.flags: todo[e.msgid]=f
A=ahocorasick.Automaton(); enc={}
for m in todo:
    try: b=g.encode(m)
    except Exception: continue
    if b and len(b)>=2: enc[m]=b; A.add_word((b+b'\xff').decode('latin1'),m)
A.make_automaton()
addrs=collections.defaultdict(list)
for endpos,m in A.iter(en.decode('latin1')):
    a=endpos-len(enc[m]); addrs[m].append(a)
tg={a for v in addrs.values() for a in v}
ptrs=collections.defaultdict(list)
for p in range(len(en)-3):
    if en[p+3] in (8,9):
        v=struct.unpack_from('<I',en,p)[0]-0x08000000
        if v in tg: ptrs[v].append(p)
res={}
st=collections.Counter()
for m in todo:
    if m not in enc: st['noenc']+=1; continue
    if m not in addrs: st['absent_rom']+=1; continue
    votes=collections.Counter()
    for a in addrs[m]:
        for p in ptrs.get(a,[]):
            v=struct.unpack_from('<I',fr,p)[0]-0x08000000
            if 0<=v<len(fr):
                e=fr.find(b'\xff',v,v+2000)
                if e>0: votes[fr[v:e]]+=1
        e=fr.find(b'\xff',a,a+2000)
        if e>0: votes[fr[a:e]]+=0.5
    cands=[(n,b) for b,n in votes.items()]
    best=None
    for n,b in sorted(cands,reverse=True):
        t=g.decode(b,m)
        if t and t!=m and re.sub(r'\W','',t.lower())!=re.sub(r'\W','',m.lower()): best=t; break
    if best: res[m]=best; st['ok']+=1
    else: st['same_or_none']+=1
print(st)
pickle.dump(res,open('/tmp/recup.pkl','wb'))
