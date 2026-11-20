#!/usr/bin/env python3
"""Intègre un lot JSON (format docs/CONSIGNES.md §6) dans les .po, en respectant la priorité des sources.

  integrer_lot.py <nom_du_lot> <fichiers .json…> [--essai] [--corriger] [--exclure ids.txt]

- Une entrée du lot remplace l'entrée du .po si sa source est de rang meilleur (plus petit),
  si le .po est vide ou « fuzzy », ou, avec --corriger, si le rang est égal ou moins bon
  (corrections issues d'un audit ou d'une relecture : il faut alors un champ "note" ou "preuve").
- Les textes officiels exacts (rang 1 et 2) ne sont jamais remplacés par une source de rang
  inférieur, même avec --corriger, sauf si l'entrée porte "alignement_faux": true (le texte
  officiel était associé à la mauvaise phrase) ou "retouche_officiel": true (casse des libellés,
  décision 14, ou contrainte de place démontrée en jeu ; justification obligatoire).
- Contrôles bloquants (outils/verifier.py) : CODES, KANA, CARACTERE, LONGUEUR, ESPACE, FRAGMENT.
  Les autres (LARGEUR, GLOSSAIRE, ANGLAIS) sont signalés dans le journal.
- Journal : rapport/integrations/<lot>.tsv ; --essai n'écrit pas les .po.
"""
import os, sys, re, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import polib, hnsfr
from verifier import Verif

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SANS_ACCENT_MAJ = str.maketrans('ÀÂÄÉÈÊËÎÏÔÖÙÛÜ', 'AAAEEEEIIOOUUU')   # décision 14 (Ç et Œ gardés)
BLOQUANTS = {'CODES', 'KANA', 'CARACTERE', 'LONGUEUR', 'ESPACE', 'FRAGMENT', 'TYPO'}


def rang(source):
    s = (source or '').lower()
    if not s: return 9
    adapte = 'adapt' in s
    if s.startswith('émeraude fr officiel') or s.startswith('emeraude fr officiel'):
        return 1.5 if adapte else 1
    if s.startswith('soulsilver fr officiel'):
        return 2.5 if adapte else 2
    if s.startswith('soulsilver fr, correspondance'):
        return 2.7
    if s.startswith('patch fr'):
        return 3
    return 4   # traduction nouvelle / manuelle / relue


def source_de(e):
    return (re.search(r'source : ([^\n]*)', e.comment or '') or [None, ''])[1]


def main():
    args = sys.argv[1:]
    essai = '--essai' in args; corriger = '--corriger' in args
    excl = set()
    if '--exclure' in args:
        i = args.index('--exclure'); excl = set(l.rstrip('\n') for l in open(args[i + 1], encoding='utf-8')); del args[i:i + 2]
    args = [a for a in args if not a.startswith('--')]
    lot, fichiers = args[0], args[1:]
    root = os.path.join(P, 'build', 'upstream_orig')
    V = Verif(root, os.path.join(P, 'memoires', 'hns_fr_patch.gba'), os.path.join(P, 'traductions', 'glossaire.tsv'))
    pos = {d: polib.pofile(os.path.join(P, 'traductions', d + '.po')) for d in ('dialogues', 'menus', 'donnees', 'contextes')}
    index = {}
    for d, po in pos.items():
        for e in po:
            if not e.obsolete: index[(e.msgctxt or '', e.msgid)] = (d, e)
    st = collections.Counter(); journal = []
    for f in fichiers:
        for it in json.load(open(f, encoding='utf-8')):
            mid, ctx, mstr = it['msgid'], it.get('msgctxt') or '', (it.get('msgstr') or '').translate(SANS_ACCENT_MAJ)
            mstr = re.sub(r'(?<![A-Za-zÀ-ÿ])Ca(?![A-Za-zÀ-ÿ’\'])', 'Ça', mstr)   # la cédille reste (décision 14)
            src = it.get('source') or 'traduction nouvelle'
            if not mstr: st['vide'] += 1; continue
            if mid in excl: st['exclu'] += 1; journal.append(('exclu', mid, mstr, '')); continue
            cle = (ctx, mid)
            if cle not in index:
                if ctx:
                    e = polib.POEntry(msgctxt=ctx, msgid=mid, msgstr='', occurrences=[(ctx, '0')])
                    e.comment = 'même texte anglais qu’ailleurs, sens différent dans ce fichier'
                    if not essai: pos['contextes'].append(e)
                    index[cle] = ('contextes', e)
                else:
                    st['msgid inconnu'] += 1; journal.append(('msgid inconnu', mid, mstr, '')); continue
            d, e = index[cle]
            occ = e.occurrences or ([(it['fichier'], it.get('ligne', 0))] if it.get('fichier') else [])
            if not ctx:   # les fichiers couverts par une entrée à contexte ne comptent pas pour l'entrée générale
                occ = [o for o in occ if (o[0], mid) not in index]
            pbs = V.check(mid, mstr, occ, 'source : ' + src, d)
            bloq = [p for p in pbs if p[0] in BLOQUANTS and not (p[0] == 'FRAGMENT' and not src.lower().startswith('patch'))]
            if bloq:
                st['rejeté (contrôle)'] += 1
                journal.append(('rejeté', mid, mstr, '; '.join('%s %s' % p for p in bloq))); continue
            ancien_src = source_de(e) if e.msgstr and 'fuzzy' not in e.flags else ''
            r_new, r_old = rang(src), rang(ancien_src)
            if e.msgstr == mstr and 'fuzzy' not in e.flags:
                if r_new < r_old and not essai:
                    e.comment = re.sub(r'source : [^\n]*', 'source : ' + src, e.comment or '') if 'source :' in (e.comment or '') else 'source : ' + src
                st['identique'] += 1; continue
            ok = r_new < r_old or not ancien_src
            if not ok and corriger:
                officiel_exact = r_old in (1, 2)
                ok = (not officiel_exact) or it.get('alignement_faux') or it.get('retouche_officiel')
                if ok and not (it.get('note') or it.get('preuve')):
                    ok = False; st['correction sans justification'] += 1
            if not ok:
                st['gardé (source meilleure ou égale)'] += 1
                journal.append(('gardé', mid, mstr, 'ancien [%s] %s' % (ancien_src, e.msgstr))); continue
            avert = '; '.join('%s %s' % p for p in pbs)
            if not essai:
                com = ['source : ' + src, 'lot : ' + lot]
                if it.get('preuve'): com.append('preuve : ' + str(it['preuve'])[:300].replace('\n', ' '))
                if e.msgstr and e.msgstr != mstr: com.append('ancien (%s) : %s' % (ancien_src or '?', e.msgstr[:300].replace('\n', ' ')))
                e.msgstr = mstr; e.comment = '\n'.join(com)
                e.flags = [x for x in e.flags if x != 'fuzzy']
            st['intégré'] += 1
            journal.append(('intégré', mid, mstr, ('remplace [%s] ' % ancien_src if ancien_src else '') + avert))
    if not essai:
        for d, po in pos.items(): po.save(os.path.join(P, 'traductions', d + '.po'))
    os.makedirs(os.path.join(P, 'rapport', 'integrations'), exist_ok=True)
    out = os.path.join(P, 'rapport', 'integrations', lot + ('.essai' if essai else '') + '.tsv')
    with open(out, 'w', encoding='utf-8') as fo:
        fo.write('action\tmsgid\tmsgstr\tdetail\n')
        for r in journal: fo.write('\t'.join(x.replace('\t', ' ').replace('\n', '\\n') for x in r) + '\n')
    print(lot, '(essai)' if essai else '', dict(st)); print('journal :', out)


if __name__ == '__main__':
    main()
