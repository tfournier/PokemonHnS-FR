#!/usr/bin/env python3
"""Lot B : assemble les sorties (exact.json, adapte.json, noms.json, douteux.json, confirmations.json).

  ss_sorties.py --travail <dossier> [--sortie traductions/lots/B_soulsilver]

Une entrée par (msgctxt, msgid) ; priorité exact > noms > adapté > douteux. Les entrées dont la
proposition est identique au msgstr actuel vont dans confirmations.json (source à requalifier seulement).
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ss_commun import P

def opt(args, n, d=None):
    if n in args:
        i = args.index(n); v = args[i + 1]; del args[i:i + 2]; return v
    return d

def main():
    args = sys.argv[1:]
    trav = opt(args, '--travail')
    sortie = opt(args, '--sortie', os.path.join(P, 'traductions', 'lots', 'B_soulsilver'))
    os.makedirs(sortie, exist_ok=True)
    lire = lambda n: json.load(open(os.path.join(trav, n), encoding='utf-8')) if os.path.exists(os.path.join(trav, n)) else []
    groupes = [('exact', lire('cand_exact.json')), ('noms', lire('cand_noms.json')), ('adapte', lire('cand_adapte.json')),
               ('douteux', lire('cand_douteux_textes.json') + lire('cand_douteux_noms.json'))]
    vus = set(); out = collections.defaultdict(list); conf = []
    for nom, L in groupes:
        for o in L:
            k = (o.get('msgctxt', ''), o['msgid'])
            if k in vus: continue
            vus.add(k)
            o = {a: b for a, b in o.items() if not a.startswith('_')}
            if nom != 'douteux' and o.get('ancien') == o['msgstr'] and 'msgctxt' not in o:
                o['note'] = (o.get('note', '') + ' ; ' if o.get('note') else '') + 'identique au msgstr actuel : seule la source change'
                conf.append(o); continue
            out[nom].append(o)
    for nom in ('exact', 'adapte', 'noms', 'douteux'):
        json.dump(out[nom], open(os.path.join(sortie, nom + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print(nom, len(out[nom]))
    json.dump(conf, open(os.path.join(sortie, 'confirmations.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('confirmations', len(conf))

if __name__ == '__main__':
    main()
