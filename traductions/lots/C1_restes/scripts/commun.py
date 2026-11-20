import sys, os, re, json, collections
P='/Users/tfournier/projets/gitlab.com/tfournier/PokemonHnS-FR'
S='/private/tmp/claude-501/-Users-tfournier-projets-gitlab-com-tfournier-PokemonHnS-FR/d65695bd-6542-4bbf-9aff-f39c55206823/scratchpad/c1'
sys.path.insert(0, P+'/outils')
import polib
R=P+'/build/upstream_orig'
def src_of(e): return (re.search(r'source : ([^\n]*)', e.comment or '') or [None, ''])[1]
def load_po():
    idx={}
    for d in ['dialogues','menus','donnees','contextes']:
        for e in polib.pofile(f'{P}/traductions/{d}.po'):
            if not e.obsolete: idx[(e.msgctxt or '', e.msgid)]=(d,e)
    return idx
def files(e): return sorted(set(f for f,l in e.occurrences))
A=json.load(open(P+'/traductions/lots/A_emeraude/douteux.json'))
B=json.load(open(P+'/traductions/lots/B_soulsilver/douteux.json'))
for i,x in enumerate(A): x['_id']='A:%d'%i
for i,x in enumerate(B): x['_id']='B:%d'%i
NAMEF=('.party','battle_frontier_trainers.h','battle_tent.h','contest_opponents.h','trade.h','apprentice.h','trainer_hill.h','trainer_tower_sets.c')
