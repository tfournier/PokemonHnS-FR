exec(open('/private/tmp/claude-501/-Users-tfournier-projets-gitlab-com-tfournier-PokemonHnS-FR/d65695bd-6542-4bbf-9aff-f39c55206823/scratchpad/c1/commun.py').read())
import unicodedata
L=P+'/traductions/lots/C1_restes'
ent={}
for f in ['C1_001.json','C1_002.json','C1_003.json','C1_004.json']:
    for d in json.load(open(f'{L}/{f}')): ent[(d.get('msgctxt',''),d['msgid'])]=d
exc={(d.get('msgctxt',''),d['msgid']):d for d in json.load(open(L+'/C1_exceptions.json'))}
v=json.load(open(S+'/vides.json'))
print('vides couverts entrées',sum(1 for x in v if ('',x['msgid']) in ent),'exceptions',sum(1 for x in v if ('',x['msgid']) not in ent and ('',x['msgid']) in exc),'restants',sum(1 for x in v if ('',x['msgid']) not in ent and ('',x['msgid']) not in exc))
idx=load_po()
DEC=json.load(open(S+'/DEC_final.json'))
def eff(m,f):
    for k in ((f,m),('',m)):
        if k in ent: return ent[k]['msgstr']
        if k in idx and idx[k][1].msgstr: return idx[k][1].msgstr
    return ''
def sa(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c)).upper()
rej=[]; nd={}
for x in A+B:
    i=x['_id']
    if i in DEC: continue
    f=x.get('msgctxt') or x['fichier']; val=eff(x['msgid'],f); p=x['msgstr']
    d='retenu' if p and val==p else ('adapté' if p and sa(val)==sa(p) else 'rejeté')
    nd[i]=d
    if d=='rejeté': rej.append(dict(_id=i,msgid=x['msgid'],msgctxt=x.get('msgctxt',''),proposition=p,raison='nom de Dresseur/personnage : proposition non retenue pour %s (valeur C1 : « %s ») ; règle par fichier : Hoenn = Émeraude FR par index de table, Johto/Kanto = SoulSilver FR si même Dresseur (équipes comparées), sinon prénom anglais en casse normale'%(f,val),remplacement=val))
R=json.load(open(L+'/C1_rejets.json'))+rej
json.dump(sorted(R,key=lambda r:(r['_id'][0],int(r['_id'].split(':')[1].split('/')[0]))),open(L+'/C1_rejets.json','w'),ensure_ascii=False,indent=1)
tot=collections.Counter((i[0],d) for i,(d,_) in DEC.items()); tot.update((i[0],d) for i,d in nd.items())
print('noms', collections.Counter((i[0],d) for i,d in nd.items()))
print(sorted(tot.items()), 'rejets', len(R))
