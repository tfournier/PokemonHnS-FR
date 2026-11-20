import sys,polib,glob,re,json; sys.path.insert(0,'/home/claude/pokehns-fr/outils')
from gen3 import Gen3
g=Gen3('/home/claude/pokehns-fr/build/upstream')
fr=open('/home/claude/pokehns-fr/memoires/hns_fr_patch.gba','rb').read()
sus=[]
for f in glob.glob('/home/claude/pokehns-fr/traductions/*.po'):
    for e in polib.pofile(f):
        if not e.msgstr or 'patch FR actuel' not in (e.comment or ''): continue
        try: b=g.encode(e.msgstr)
        except Exception: continue
        if not b: continue
        pat=b+b'\xff'; i=fr.find(pat); occ=[]; 
        while i>=0 and len(occ)<50:
            occ.append(i); i=fr.find(pat,i+1)
        if not occ: continue
        starts=[o for o in occ if o==0 or fr[o-1] in (0xFF,0x00) or o%4==0]
        if not starts: sus.append({'f':f.split('/')[-1],'id':e.msgid,'fr':e.msgstr,'src':e.occurrences[0][0]})
print(len(sus))
json.dump(sus,open('/tmp/suspects.json','w'),ensure_ascii=False,indent=0)
for s in sus[:400]: print('%s|%s|%s'%(s['f'][:3],s['id'],s['fr']))
