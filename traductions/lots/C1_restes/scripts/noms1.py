exec(open('/private/tmp/claude-501/-Users-tfournier-projets-gitlab-com-tfournier-PokemonHnS-FR/d65695bd-6542-4bbf-9aff-f39c55206823/scratchpad/c1/commun.py').read())
exec(open(S+'/party.py').read())
import hnsfr
idx=load_po()
T=json.load(open(S+'/tables_em.json'))
ss=json.load(open(S+'/ss_all.json'))
tr=json.load(open(S+'/phg/files/poketool/trainer/trainers.json'))['trainers']
SS=[]
for i,t in enumerate(tr):
    SS.append(dict(i=i,en=t['name'].replace('{TRNAME}',''),cls=t['class'].replace('TRAINERCLASS_',''),sp=set(p['species'].replace('SPECIES_','') for p in t['party']),fr=ss['729'][i].replace('{TRNAME}','')))
ssby=collections.defaultdict(list)
for s in SS: ssby[s['en'].upper()].append(s)
H={'src/data/trainers_hns.party':parse_party(R+'/src/data/trainers_hns.party'),'src/data/trainers_frlg.party':parse_party(R+'/src/data/trainers_frlg.party')}
# names in scope
vides={o['msgid'] for o in json.load(open(S+'/vides.json'))}
scope=set()
for (c,m),(d,e) in idx.items():
    if c: continue
    fs=files(e)
    if any(f.endswith(NAMEF) for f in fs) and (m in vides):
        scope.add(m)
for x in A+B:
    if x['fichier'].endswith(NAMEF) or 'nom de table' in x['note'] or 'Dresseur' in x['note'] or 'TRAINER_' in x['note']:
        if re.fullmatch(r"[A-Z0-9 .&'\-é]+", x['msgid']) and len(x['msgid'])<=12: scope.add(x['msgid'])
print(len(scope))
def ssmatch(t):
    c=ssby.get(t['name'].upper(),[])
    sc=[]
    for s in c:
        sp=set(t['species']); ov=len(sp&s['sp'])
        sc.append((ov, s))
    sc.sort(key=lambda z:-z[0])
    return sc
rows=[]
for m in sorted(scope):
    d,e=idx[('',m)]
    occ=collections.defaultdict(list)
    for f,l in e.occurrences: occ[f].append(int(l))
    r=dict(msgid=m,po=d,base=e.msgstr,basesrc=src_of(e),files={})
    for f,lines in occ.items():
        ctx=idx.get((f,m))
        info=dict(lignes=lines, ctx=(ctx[1].msgstr, src_of(ctx[1])) if ctx else None)
        if f in T:
            vals=[(t['fr'],t['adr']) for t in T[f] if t['ligne'] in lines or (f=='src/data/trainers.party' and t['ligne'] in lines)]
            info['em']=vals
        if f in H:
            ts=[t for t in H[f] if t['ligne'] in lines]
            info['hns']=[(t['id'],t['cls'],t['species'],[(ov,s['fr'],s['cls'],sorted(s['sp']),s['i']) for ov,s in ssmatch(t)]) for t in ts]
        r['files'][f]=info
    rows.append(r)
json.dump(rows,open(S+'/noms_rows.json','w'),ensure_ascii=False,indent=0)
