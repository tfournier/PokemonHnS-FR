#!/usr/bin/env python3
"""Arbitre les remarques de ChatGPT sur un lot et produit le lot corrigé.

  arbitrer_relecture.py <nom_du_lot> <fichiers .json du lot…> [--decisions decisions.json]

Règles automatiques (dans l'ordre) :
  0. texte officiel adapté : seules les retouches minimales sont admises (orthographe, codes, ou
     correction à plus de 85 % identique) ; « autre_phrase » → à vérifier ;
  1. texte officiel exact (Émeraude FR / SoulSilver FR) : jamais modifié ; une remarque
     « autre_phrase » est mise de côté pour vérification d'alignement (à_vérifier) ;
  2. correction vide ou identique à la mise en page près : refusée (« mise en page seulement ») ;
  3. correction qui casse un contrôle bloquant (codes, kana, caractères, longueur, espaces) : refusée ;
  4. typographie contraire aux conventions (espace avant ! ? : ;) : refusée ;
  5. terminologie : acceptée seulement si le terme proposé est la graphie du glossaire ou du lexique
     officiel, sinon à arbitrer ;
  6. sinon : acceptée, la correction est remise en page (198 px) si c'est un dialogue.
Le fichier --decisions ({"msgid": "accepter"|"refuser"|"texte imposé"}) permet à l'agent principal
d'imposer son arbitrage sur les cas « à arbitrer ».
Sorties dans rapport/relectures/<lot>/ : bilan.md, arbitrage.tsv, lot_corrige.json.
"""
import os, sys, re, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier import Verif
from gen3 import Gen3
import style

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOQ = {'CODES', 'KANA', 'CARACTERE', 'LONGUEUR', 'ESPACE', 'TYPO'}


def plat(s):
    return re.sub(r'\s+', ' ', re.sub(r'\\[nlp]', ' ', s or '')).strip()


def officiel_adapte(src):
    s = (src or '').lower()
    return (s.startswith('émeraude fr officiel') or s.startswith('soulsilver fr officiel')) and 'adapt' in s


def ratio(a, b):
    from rapidfuzz import fuzz
    return fuzz.ratio(a, b) / 100


def officiel_exact(src):
    s = (src or '').lower()
    return (s.startswith('émeraude fr officiel') or s.startswith('soulsilver fr officiel')) and 'adapt' not in s


def main():
    args = sys.argv[1:]
    dec = {}
    if '--decisions' in args:
        i = args.index('--decisions'); dec = json.load(open(args[i + 1], encoding='utf-8')); del args[i:i + 2]
    lot, fichiers = args[0], args[1:]
    root = os.path.join(P, 'build', 'upstream_orig')
    V = Verif(root); g = Gen3(root)
    gl = style.charger(os.path.join(P, 'traductions', 'glossaire.tsv'))
    graphies = set(gl.values())
    dossier = os.path.join(P, 'rapport', 'relectures', lot)
    rem = json.load(open(os.path.join(dossier, 'remarques.json'), encoding='utf-8'))
    entrees = []
    for f in fichiers: entrees += json.load(open(f, encoding='utf-8'))
    par_id = {(it.get('msgctxt') or '', it['msgid']): it for it in entrees}
    st = collections.Counter(); lignes = []
    for r in rem:
        cle = (r.get('msgctxt') or '', r['msgid'])
        it = par_id.get(cle)
        if it is None: st['entrée introuvable'] += 1; continue
        cat = r.get('categorie', ''); corr = (r.get('correction') or '').strip()
        verdict, raison = 'accepté', ''
        imp = dec.get(r['msgid'])
        if imp:
            if imp == 'accepter': verdict, raison = 'accepté', 'décision de l’agent principal'
            elif imp == 'refuser': verdict, raison = 'refusé', 'décision de l’agent principal'
            else: verdict, raison, corr = 'accepté', 'texte imposé par l’agent principal', imp
        elif officiel_exact(it.get('source')):
            verdict, raison = ('à_vérifier', 'texte officiel : vérifier l’alignement') if cat == 'autre_phrase' else ('refusé', 'texte officiel non modifiable')
        elif officiel_adapte(it.get('source')) and cat not in ('codes', 'autre_phrase') and \
                ratio(plat(corr), plat(it['msgstr'])) < 0.85:
            verdict, raison = 'refusé', 'texte officiel adapté : on garde la formulation officielle (seule une retouche minimale est admise)'
        elif officiel_adapte(it.get('source')) and cat == 'autre_phrase':
            verdict, raison = 'à_vérifier', 'texte officiel adapté : vérifier l’alignement'
        elif not corr or plat(corr) == plat(it['msgstr']):
            verdict, raison = 'refusé', 'mise en page seulement ou pas de correction'
        elif re.search(r' [!?:;]', corr) and not re.search(r' [!?:;]', it['msgstr']):
            verdict, raison = 'refusé', 'typographie contraire aux conventions (pas d’espace avant ! ? : ;)'
        elif cat == 'terminologie':
            nouveaux = set(re.findall(r"[A-ZÀ-Þ][\w’'\-]+(?: [A-ZÀ-Þ][\w’'\-]+)*", corr)) - set(re.findall(r"[A-ZÀ-Þ][\w’'\-]+(?: [A-ZÀ-Þ][\w’'\-]+)*", it['msgstr']))
            if nouveaux and not all(n in graphies or n.upper() == n for n in nouveaux):
                verdict, raison = 'à_arbitrer', 'terme hors glossaire : %s' % sorted(nouveaux)[:3]
        if verdict == 'accepté':
            if re.search(r'\\[nlp]', it['msgid']) and not re.search(r'\\[np]$', it['msgid']) and not re.search(r'\{(DYNAMIC|CLEAR_TO)', corr):
                corr = g.reformater(corr, 198)
            pb = [p for p in V.check(it['msgid'], corr, [(it.get('fichier', ''), it.get('ligne', 0))] if it.get('fichier') else [], '', '') if p[0] in BLOQ]
            if pb:
                verdict, raison = 'refusé', 'la correction casse : ' + '; '.join('%s %s' % p for p in pb)
            else:
                it['msgstr'] = corr
                it['note'] = ((it.get('note') or '') + ' | corrigé après relecture ChatGPT (%s)' % cat).strip(' |')
        st[verdict] += 1
        lignes.append((verdict, cat, r['msgid'], r['msgstr'], corr, r.get('probleme', ''), r.get('justification', ''), raison))
    with open(os.path.join(dossier, 'arbitrage.tsv'), 'w', encoding='utf-8') as fo:
        fo.write('verdict\tcategorie\tmsgid\tavant\tcorrection\tprobleme\tjustification\traison\n')
        for l in lignes: fo.write('\t'.join(str(x).replace('\t', ' ').replace('\n', '\\n') for x in l) + '\n')
    json.dump(entrees, open(os.path.join(dossier, 'lot_corrige.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    cats = collections.Counter((l[0], l[1]) for l in lignes)
    with open(os.path.join(dossier, 'bilan.md'), 'w', encoding='utf-8') as fo:
        fo.write('# Relecture ChatGPT — lot %s\n\n' % lot)
        fo.write('- entrées du lot : %d\n- remarques : %d\n' % (len(entrees), len(rem)))
        for k, v in st.most_common(): fo.write('- %s : %d\n' % (k, v))
        fo.write('\n| verdict | catégorie | nombre |\n|---|---|---|\n')
        for (v, c), n in sorted(cats.items()): fo.write('| %s | %s | %d |\n' % (v, c, n))
        fo.write('\nDétail : arbitrage.tsv. Lot corrigé : lot_corrige.json.\n')
    print(lot, dict(st))


if __name__ == '__main__':
    main()
