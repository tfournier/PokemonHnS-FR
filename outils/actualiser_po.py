#!/usr/bin/env python3
"""Met les .po à jour avec les textes du code upstream (nouvelle version, nouveaux types de fichiers).

  actualiser_po.py <source_upstream_vierge> <traductions/> [--appliquer [--purger]]

- ajoute les textes absents des .po (non traduits) dans le .po de leur domaine ;
- met à jour les références (fichier:ligne) de toutes les entrées ;
- liste (sans les supprimer) les entrées qui n'existent plus dans le code.
Sans --appliquer, n'écrit rien et affiche seulement le bilan.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hnsfr, polib

root, podir = sys.argv[1], sys.argv[2]
ecrire = '--appliquer' in sys.argv
purger = '--purger' in sys.argv   # retire les entrées sans occurrence dans le code
occ = collections.defaultdict(list)
for o in hnsfr.scan(root):
    if hnsfr.wanted(o.text): occ[o.text].append(o)
pos = {d: polib.pofile(os.path.join(podir, d + '.po')) for d in ('dialogues', 'menus', 'donnees')}
connus = {}
for d, po in pos.items():
    for e in po:
        if not e.obsolete: connus[e.msgid] = (d, e)
ajouts = collections.Counter(); disparus = []
for m, lst in occ.items():
    refs = [(o.path, str(o.line)) for o in lst[:6]]
    if m in connus:
        connus[m][1].occurrences = refs
        continue
    d = hnsfr.domain(lst[0].path)
    pos[d].append(polib.POEntry(msgid=m, msgstr='', occurrences=refs))
    ajouts[d + ' : ' + lst[0].path.split('/')[-1]] += 1
for m, (d, e) in connus.items():
    if m not in occ: disparus.append((d, m))
print('textes ajoutés :', sum(ajouts.values()))
for k, v in ajouts.most_common(40): print('  %-60s %d' % (k, v))
print('entrées sans occurrence dans le code :', len(disparus))
for d, m in disparus[:20]: print('  %s : %r' % (d, m[:70]))
if ecrire:
    if purger:
        for d, m in disparus:
            po = pos[d]; e = po.find(m)
            if e is not None: po.remove(e)
        print('purgées :', len(disparus))
    for d, po in pos.items(): po.save(os.path.join(podir, d + '.po'))
    print('écrit.')
