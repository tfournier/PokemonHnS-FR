import sys,json,pickle,polib,glob,re,importlib.util; sys.path.insert(0,'/home/claude/pokehns-fr/outils')
import style, hnsfr
from gen3 import Gen3
R='/home/claude/pokehns-fr/'
g=Gen3(R+'build/upstream'); CM=hnsfr.Charmap(R+'build/upstream')
gl=style.charger(R+'traductions/glossaire.tsv')
esp=frozenset(style.cle(x) for x in json.load(open(R+'memoires/ss_fr_msg.json'))['237'] if x.strip())
def load(mode,arg):
    if mode=='em': return {k:(v,'Émeraude FR officiel (contexte de script)') for k,v in pickle.load(open(arg,'rb')).items()}
    o=json.load(open('/tmp/a_trad.json'))
    spec=importlib.util.spec_from_file_location('b',arg); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
    return {o[i]['id']:((t[0],'traduction manuelle (style SoulSilver)','brut') if isinstance(t,tuple) else (t,'traduction manuelle (style SoulSilver)')) for i,t in b.T.items()}
mode,arg=sys.argv[1],sys.argv[2]
D=load(mode,arg); n=bad=0
for f in glob.glob(R+'traductions/*.po'):
    po=polib.pofile(f); ch=False
    for e in po:
        if e.msgid not in D: continue
        if e.msgstr and 'fuzzy' not in e.flags and mode=='em' and not e.comment.startswith('source : traduction manuelle'): continue
        t,src,*brut=D[e.msgid]
        if mode=='em': t=style.appliquer(t,gl,esp)
        frag=re.search(r'\\[nlp]$',e.msgid)
        if re.search(r'\\[nlp]',e.msgid) and not frag and mode!='em' and not brut:
            t=g.reformater(t,198)
        elif '\\n' in t and '\\n' not in e.msgid:
            t=t.replace('\\n',' ')
        if CM.invalid(t): print('INVALIDE',repr(t),CM.invalid(t)); bad+=1; continue
        e.msgstr=t; e.flags=[x for x in e.flags if x!='fuzzy']; e.comment='source : '+src; n+=1; ch=True
    if ch: po.save(f)
print('appliqués',n,'rejetés',bad)
