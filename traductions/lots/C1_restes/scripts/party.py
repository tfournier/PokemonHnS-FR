# parse .party files : liste de dresseurs {id, name, class, species, ligne}
import re
def parse_party(path):
    L=open(path,encoding='utf-8').read().split('\n')
    out=[]; cur=None; inmon=False
    for i,l in enumerate(L):
        if l.startswith('=== ') and l.endswith(' ==='):
            cur=dict(id=l[4:-4],name='',cls='',species=[],ligne=0); out.append(cur); inmon=False; continue
        if cur is None: continue
        m=re.match(r'^Name:\s*(.*?)\s*$',l)
        if m and not inmon: cur['name']=m.group(1); cur['ligne']=i+1; continue
        m=re.match(r'^Class:\s*(.*?)\s*$',l)
        if m and not inmon: cur['cls']=m.group(1); continue
        if l.strip()=='' : inmon=True; continue
        if inmon and l and not l.startswith(('-',' ','Level','Ability','IVs','EVs','Ball','Happiness','Nature','Shiny','Dynamax','Gigantamax','Tera','/*','*')) and ':' not in l.split('@')[0]:
            sp=l.split('@')[0].strip()
            mm=re.search(r'\(([^()]+)\)\s*(\((M|F)\))?\s*$',sp)
            if mm and mm.group(1) not in ('M','F'): sp=mm.group(1)
            else: sp=re.sub(r'\s*\((M|F)\)\s*$','',sp)
            cur['species'].append(sp.upper().replace('SPECIES_','').replace(' ','_').replace('-','_').replace('.','').replace("'",''))
    return out
