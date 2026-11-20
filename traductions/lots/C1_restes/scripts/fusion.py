exec(open('/private/tmp/claude-501/-Users-tfournier-projets-gitlab-com-tfournier-PokemonHnS-FR/d65695bd-6542-4bbf-9aff-f39c55206823/scratchpad/c1/commun.py').read())
import hnsfr, unicodedata
sys.path.insert(0, P + '/outils')
from integrer_lot import rang, SANS_ACCENT_MAJ
idx = load_po()
L = P + '/traductions/lots/C1_restes'
# fichiers où apparaît chaque texte (clé msgctxt)
occ = collections.defaultdict(set)
for o in hnsfr.scan(R):
    occ[o.text].add(o.path)

mine = json.load(open(S + '/mes_decisions_2.json'))
noms = json.load(open(S + '/noms_out.json'))
ag = {}
for k in ('lot1', 'lot2', 'lot3', 'lot4'):
    ag[k] = json.load(open('%s/agents/%s/%s_sortie.json' % (S, k, k)))
douteux = {x['_id']: x for x in A + B}

def norm(d):
    d = {k: v for k, v in d.items() if not k.startswith('_') and k != 'decision' and v not in (None,)}
    if not d.get('msgctxt'): d.pop('msgctxt', None)
    if d.get('msgstr') and d['msgstr'] != d['msgid']:
        s = d['msgstr'].translate(SANS_ACCENT_MAJ)
        d['msgstr'] = s
    return d

groupes = collections.OrderedDict((k, []) for k in ('noms', 'non_traduits', 'douteux_A', 'douteux_B'))
for d in noms: groupes['noms'].append(norm(d))
mA = {x['msgid'] for x in A}
for d in mine['OUT']:
    groupes['douteux_A' if d['msgid'] in mA else 'non_traduits'].append(norm(d))
DEC = dict(mine['DEC'])
REJ = []
for k, lst in ag.items():
    for it in lst:
        DEC[it['_id'].split('/')[0]] = (it['decision'], it.get('note', ''))
        if it.get('msgstr'):
            groupes['douteux_A' if it['_id'].startswith('A') else 'douteux_B'].append(dict(norm(it), _id=it['_id']))
        if it['decision'] == 'rejeté':
            REJ.append(dict(_id=it['_id'], msgid=it['msgid'], msgctxt=it.get('msgctxt', ''), proposition=douteux.get(it['_id'].split('/')[0], {}).get('msgstr', ''),
                            raison=it.get('note', ''), remplacement=it.get('msgstr', '')))
for i, (d, r) in mine['DEC'].items():
    if d == 'rejeté':
        x = douteux[i]
        REJ.append(dict(_id=i, msgid=x['msgid'], msgctxt=x.get('msgctxt', ''), proposition=x['msgstr'], raison=r, remplacement=''))

JP = {'\\nいいTVができました ', '\\nダメTVができました '}
for g in groupes:
    for d in groupes[g]:
        if d['msgid'] in JP and d.get('_id'):
            DEC[d['_id']] = ('rejeté', 'texte japonais jamais affiché (sJPText_…TvReady, marqué Unused dans berry_blender.c) : gardé tel quel (voir C1_exceptions.json)')
            REJ.append(dict(_id=d['_id'], msgid=d['msgid'], msgctxt='', proposition=douteux[d['_id']]['msgstr'], raison=DEC[d['_id']][1], remplacement=''))
    groupes[g] = [d for d in groupes[g] if d['msgid'] not in JP]
# dédoublonnage
vu = {}; conflits = []
for g, lst in groupes.items():
    keep = []
    for d in lst:
        k = (d.get('msgctxt', ''), d['msgid'])
        if k in vu:
            if vu[k]['msgstr'] != d['msgstr']: conflits.append((k, vu[k]['msgstr'], d['msgstr'], g))
            continue
        vu[k] = d; keep.append(d)
    groupes[g] = keep
# contrôles : msgctxt = chemin réel ; retirer les entrées sans changement
retires = []
for g, lst in groupes.items():
    keep = []
    for d in lst:
        ctx = d.get('msgctxt', '')
        if ctx and ctx not in occ.get(d['msgid'], ()):
            print('MSGCTXT INVALIDE', ctx, d['msgid']); continue
        if ('', d['msgid']) not in idx and not ctx:
            print('MSGID INCONNU', repr(d['msgid'])); continue
        e = idx.get((ctx, d['msgid']))
        if e and e[1].msgstr == d['msgstr']:
            if rang(d['source']) >= rang(src_of(e[1])):
                retires.append(d); continue
        if e and e[1].msgstr and not d.get('ancien'): d['ancien'] = e[1].msgstr
        keep.append({k: v for k, v in d.items() if k != '_id'})
    groupes[g] = keep
print('conflits', len(conflits))
for c in conflits: print('  ', c)
print('retirés (identiques, source pas meilleure)', len(retires))
FAUX = {('', 'DAN'): 'l’entrée générale « JOE » est le nom Émeraude d’un autre Dresseur (DAN n’apparaît que dans trainers_frlg.party)',
        ('', 'FRANK'): 'l’entrée générale « Mikail » (SoulSilver) est un homonyme sans rapport : les Montagnards FRANK de HnS ne sont pas dans HGSS',
        ('', 'NATHAN'): 'le Kinésiste Nathan de HGSS s’appelle « Jason » dans SoulSilver FR (729, même classe, GIRAFARIG) ; « Nathan » était un alignement faux (signalé par le lot B)',
        ('', 'OMAR'): 'l’entrée générale « Omar » ne vaut que pour le Concours (gardé en msgctxt) ; la Zone de Combat a MALCOLM (même index Émeraude)'}
for g in groupes:
    for d in groupes[g]:
        k = (d.get('msgctxt', ''), d['msgid'])
        e = idx.get(k)
        old = src_of(e[1]) if e and e[1].msgstr else ''
        if k in FAUX:
            d['alignement_faux'] = True; d['note'] += ' ; alignement faux de l’actuel : ' + FAUX[k]
        elif old.startswith('SoulSilver FR officiel') and rang(old) == 2 and rang(d['source']) >= 2 and 'easy_chat' in (d.get('fichier', '') + d.get('msgctxt', '')):
            d['alignement_faux'] = True; d['note'] += ' ; l’actuel « %s » venait d’une banque SoulSilver d’un autre contexte (mot du Livret mal aligné)' % e[1].msgstr
        elif old == 'SoulSilver FR officiel' and rang(d['source']) >= 2 and d['msgid'].startswith(('NAME RATER\\p', '{B_TRAINER1_NAME_WITH_CLASS} sent out')):
            d['alignement_faux'] = True; d['note'] += ' ; texte officiel inchangé, seule la mise en page est corrigée (drapeau alignement_faux pour lever le blocage d’integrer_lot)'
os.makedirs(L, exist_ok=True)
n = 0
for g, lst in groupes.items():
    if not lst: continue
    n += 1
    json.dump(lst, open('%s/C1_%03d.json' % (L, n), 'w'), ensure_ascii=False, indent=1)
    print('C1_%03d.json' % n, g, len(lst), dict(collections.Counter(d['source'] for d in lst)))
exc = []
seen = set()
for d in mine['EXC']:
    k = (d.get('msgctxt', ''), d['msgid'])
    if k in seen or k in vu: continue
    seen.add(k); exc.append(norm(d) if d['msgstr'] != d['msgid'] else {k2: v for k2, v in d.items() if v is not None})
json.dump(exc, open(L + '/C1_exceptions.json', 'w'), ensure_ascii=False, indent=1)
json.dump(sorted(REJ, key=lambda r: (r['_id'][0], int(r['_id'].split(':')[1].split('/')[0]))), open(L + '/C1_rejets.json', 'w'), ensure_ascii=False, indent=1)
json.dump(DEC, open(S + '/DEC_final.json', 'w'), ensure_ascii=False, indent=1)
print('exceptions', len(exc), 'rejets (hors noms)', len(REJ))
