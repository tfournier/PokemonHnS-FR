exec(open('/private/tmp/claude-501/-Users-tfournier-projets-gitlab-com-tfournier-PokemonHnS-FR/d65695bd-6542-4bbf-9aff-f39c55206823/scratchpad/c1/commun.py').read())
rows=json.load(open(S+'/noms_rows.json'))
idx=load_po()
ss=json.load(open(S+'/ss_all.json'))
b200en=["Rocky","Muscle","Billy","Doris","Sprints","Rusty","Shuckie","Kenya","Maggie","Paul","Volty","Hornlette","Iron","Rudy","Jose","Richard","Ayana","Stuart","Jasmine","Kirk","Webster","Lorenzo","Mondo","Surge","Brock","Steven"]
B200={n.upper():(i,ss['200'][i]) for i,n in enumerate(b200en)}
HOENN=('src/data/trainers.party','src/data/battle_frontier/battle_frontier_trainers.h','src/data/battle_frontier/battle_tent.h','src/data/contest_opponents.h','src/data/battle_frontier/trainer_hill.h')
def normal(n):
    return re.sub(r"[A-Z]+", lambda m: m.group(0)[0]+m.group(0)[1:].lower(), n)
# corrections manuelles (remplies après revue) : {(msgid, fichier): (valeur, source, preuve, note)}
MAN=json.load(open(S+'/noms_manuel.json')) if os.path.exists(S+'/noms_manuel.json') else {}
SPECIES_FILES=('species_info',)
OTHER_KEEP_BASE=True
out=[]; review=[]
def val_for(r,f,info):
    m=r['msgid']; k=m+'|'+f
    if k in MAN:
        v=list(MAN[k])
        if v[0]=='@normal': v[0]=normal(m)
        return tuple(v)
    if f.endswith('fame_checker_frlg.inc'):
        fr=r['files'].get('src/data/trainers_frlg.party')
        v=val_for(r,'src/data/trainers_frlg.party',fr) if fr else None
        if v and v[1]!='(existant)': return (v[0],v[1],v[2],'Pokédex des célébrités (FRLG) : même nom que le Dresseur de trainers_frlg.party')
        if v: return (v[0],'SoulSilver FR officiel','','Pokédex des célébrités (FRLG) : même nom que le Dresseur de trainers_frlg.party (entrée à contexte existante)')
        return (normal(m),'traduction nouvelle','','Pokédex des célébrités (FRLG), personne de Kanto sans nom officiel connu : prénom anglais en casse normale')
    if f.endswith('new_game_intro_frlg.inc'):
        return (m,'traduction nouvelle','','nom proposé à l’introduction FRLG : gardé tel quel en capitales, comme les autres noms proposés de ce fichier (KAZ, TORU…)')
    if f.endswith('apprentice.h'):
        return (m,'Émeraude FR officiel','gApprentices : table multilingue (JP/EN/FR/IT/DE/ES) présente telle quelle dans Émeraude FR','nom de l’apprenti dans une autre langue (colonne non française de gApprentices) : gardé tel quel')
    if 'em' in info and info['em']:
        vals=[v for v in info['em'] if isinstance(v[0],str) and v[0]]
        if vals:
            ds=collections.Counter(v[0] for v in vals)
            v=ds.most_common(1)[0][0]
            note='nom Émeraude FR du même index'
            if len(ds)>1: note+=' ; plusieurs Dresseurs de ce fichier portent ce nom anglais avec des noms FR différents (%s) : nom le plus fréquent retenu (un seul msgctxt par fichier)'%', '.join(ds)
            return (v,'Émeraude FR officiel',' ; '.join(x[1] for x in vals if x[0]==v)[:300],note)
    if f.endswith('trade.h'):
        if m.upper() in B200:
            i,frn=B200[m.upper()]; return (frn,'SoulSilver FR officiel','200:%d — %s (échanges in-game HGSS : %s)'%(i,frn,b200en[i]),'échange in-game Johto/Kanto : nom SoulSilver FR (banque 200)')
        return (normal(m),'traduction nouvelle','','échange in-game HnS sans équivalent HGSS : prénom anglais en casse normale (comme les autres échanges HnS)')
    if f.endswith(('trainers_hns.party','trainers_frlg.party')):
        if info['ctx']:
            return (info['ctx'][0],'(existant)','','')
        best=None
        for t in info.get('hns',[]):
            for c in t[3]:
                if c[0]>=1 and (best is None or c[0]>best[0]): best=c
        if best:
            return (best[1],'SoulSilver FR officiel','729:%d — %s (%s, équipe %s)'%(best[4],best[1],best[2],'/'.join(best[3])),'même Dresseur que dans HGSS (même nom anglais, %d espèce(s) en commun)'%best[0])
        reg='Johto/Kanto' if 'hns' in f else 'Kanto (FRLG)'
        return (normal(m),'traduction nouvelle','','Dresseur %s sans équivalent dans SoulSilver FR : prénom anglais en casse normale (style SoulSilver)'%reg)
    if f.endswith('trainer_tower_sets.c'):
        return (normal(m),'traduction nouvelle','','Tour des Dresseurs (FRLG) : prénom anglais en casse normale, comme les Dresseurs FRLG sans équivalent SoulSilver')
    if f.endswith('trainer_hill.h') or f in HOENN:
        return (m,'traduction nouvelle','','absent de la table Émeraude (données propres à l’expansion) : prénom anglais en capitales comme Émeraude')
    return None
for r in rows:
    m=r['msgid']
    if any('species_info' in f for f in r['files']) or m.startswith(' '): continue
    vals={}
    for f,info in r['files'].items():
        v=val_for(r,f,info)
        vals[f]=v
    others=[f for f,v in vals.items() if v is None]
    BASE=json.load(open(S+'/noms_base.json'))
    # choix de la base
    if m in BASE:
        base=BASE[m][0]; basefrom='__BASE__'; vals['__BASE__']=tuple(BASE[m]); r['files']['__BASE__']={'lignes':[0],'ctx':None}
    elif others:
        base=r['base'] if r['base'] else None
        basefrom='(existant : autres fichiers)'
    else:
        base=None
        for pref in HOENN+('src/data/trade.h','src/data/trainers_hns.party','src/data/trainers_frlg.party'):
            if pref in vals and vals[pref]: base=vals[pref][0]; basefrom=pref; break
        if base is None:
            f0=sorted(vals)[0]; base=vals[f0][0]; basefrom=f0
    review.append((m,r['base'],base,basefrom,{f.split('/')[-1]:(v[0] if v else None) for f,v in vals.items()},others))
    # entrée de base
    d,e=idx[('',m)]
    if base is not None and base!=r['base'] and (not others or basefrom=='__BASE__'):
        v=vals[basefrom]
        out.append(dict(msgid=m,msgstr=base,source=v[1] if v[1]!='(existant)' else 'SoulSilver FR officiel',fichier=basefrom if basefrom!='__BASE__' else e.occurrences[0][0],ligne=r['files'][basefrom]['lignes'][0] if basefrom!='__BASE__' else int(e.occurrences[0][1]),ancien=r['base'],preuve=v[2],note='entrée générale (fichiers sans msgctxt : %s) ; %s'%(', '.join(sorted(f.split('/')[-1] for f in vals if vals[f] and vals[f][0]==base and f!='__BASE__')),v[3])))
    for f,v in vals.items():
        if v is None or f=='__BASE__': continue
        cur=r['files'][f]['ctx']
        if v[0]==base and not cur: continue
        if cur and cur[0]==v[0]: continue
        if v[1]=='(existant)': continue
        out.append(dict(msgid=m,msgctxt=f,msgstr=v[0],source=v[1],fichier=f,ligne=r['files'][f]['lignes'][0],ancien=cur[0] if cur else '',preuve=v[2],note=v[3]))
json.dump(out,open(S+'/noms_out.json','w'),ensure_ascii=False,indent=1)
with open(S+'/noms_review.txt','w') as fo:
    for x in review: fo.write(repr(x)+'\n')
print(len(out), collections.Counter(x['source'] for x in out))
