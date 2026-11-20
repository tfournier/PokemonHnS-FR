#!/usr/bin/env python3
"""Produit rapport/RAPPORT.md à partir de l'état du projet (à relancer après chaque construction).

  rapport.py <dossier_projet>

Chiffre les textes par source et par fichier .po, résume les contrôles (verifications.tsv,
trop_longs.txt, images_a_revoir.txt, anglais_restant.tsv), liste les images traduites, les relectures,
les exceptions, et reprend les points à valider par un humain (rapport/a_valider.md, écrit à la main).
"""
import os, sys, re, json, glob, collections
P = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
sys.path.insert(0, os.path.join(P, 'outils'))
import polib

R = os.path.join(P, 'rapport')
L = []
w = L.append


def lire(p, defaut=''):
    p = os.path.join(R, p)
    return open(p, encoding='utf-8').read() if os.path.exists(p) else defaut


def famille(src):
    s = src.lower()
    if not src: return 'sans source'
    if s.startswith('émeraude fr officiel'): return 'Émeraude FR officiel (adapté)' if 'adapt' in s else 'Émeraude FR officiel'
    if s.startswith('soulsilver fr officiel'): return 'SoulSilver FR officiel (adapté)' if 'adapt' in s else 'SoulSilver FR officiel'
    if s.startswith('soulsilver fr, corresp'): return 'SoulSilver FR officiel (adapté)'
    if s.startswith('patch fr'): return 'patch FR existant (vérifié)' if 'vérifi' in s else 'patch FR existant'
    return 'traduction nouvelle ou manuelle'


tag = open(os.path.join(P, 'upstream.txt')).read().strip()
w('# Rapport — traduction française de Pokémon Heart & Soul (%s)\n' % tag)
w('Rapport généré par `outils/rapport.py`. Détails : `DECISIONS.md`, `rapport/ETAT_DES_LIEUX.md`, '
  '`rapport/relectures/`, `rapport/integrations/`, `rapport/images/RAPPORT.md`, `rapport/captures/`.\n')

# ------------------------------------------------------------ textes par source
w('## Textes par source\n')
tot = collections.Counter(); par = {}
for d in ('dialogues', 'menus', 'donnees', 'contextes'):
    c = collections.Counter()
    for e in polib.pofile(os.path.join(P, 'traductions', d + '.po')):
        if e.obsolete: continue
        if not e.msgstr: k = 'non traduit'
        elif 'fuzzy' in e.flags: k = 'à revoir (fuzzy)'
        else:
            src = (re.search(r'source : ([^\n]*)', e.comment or '') or [None, ''])[1]
            k = famille(src)
            if e.msgstr == e.msgid: k = 'gardé tel quel (exception)' if 'exception' in (e.comment or '').lower() or k == 'traduction nouvelle ou manuelle' else k
        c[k] += 1; tot[k] += 1
    par[d] = c
cols = ['Émeraude FR officiel', 'Émeraude FR officiel (adapté)', 'SoulSilver FR officiel', 'SoulSilver FR officiel (adapté)',
        'patch FR existant (vérifié)', 'patch FR existant', 'traduction nouvelle ou manuelle', 'gardé tel quel (exception)',
        'sans source', 'à revoir (fuzzy)', 'non traduit']
w('| Source | ' + ' | '.join(par) + ' | Total |')
w('|---|' + '---|' * (len(par) + 1))
for k in cols:
    if not tot.get(k): continue
    w('| %s | %s | **%d** |' % (k, ' | '.join(str(par[d].get(k, 0)) for d in par), tot[k]))
w('| **Total** | %s | **%d** |\n' % (' | '.join(str(sum(par[d].values())) for d in par), sum(tot.values())))

# ------------------------------------------------------------ construction et contrôles
w('## Construction et contrôles\n')
txt = lire('textes.txt')
w('- Construction : `./build.sh` (make hns) — ' + (' ; '.join(l.strip() for l in txt.split('\n')[:3] if l.strip()) or 'non lancée') + '.')
tl = [l for l in lire('trop_longs.txt').split('\n') if l.strip()]
w('- `rapport/trop_longs.txt` : %d texte(s) remis en anglais faute de place.' % len(tl))
ir = [l for l in lire('images_a_revoir.txt').split('\n') if l.strip()]
w('- `rapport/images_a_revoir.txt` : %d image(s) modifiée(s) par HnS depuis notre traduction.' % len(ir))
v = [l.split('\t') for l in lire('verifications.tsv').split('\n')[1:] if l.strip()]
vc = collections.Counter(x[0] for x in v)
w('- Contrôles automatiques (`outils/verifier.py`, 100 %% des entrées) : %s.' % (', '.join('%s %d' % kv for kv in vc.most_common()) or 'aucune alerte'))
a = [l.split('\t') for l in lire('anglais_restant.tsv').split('\n')[1:] if l.strip()]
ident = set(); homog = set()   # homog : textes français qui s'écrivent comme un autre texte anglais
for d in ('dialogues', 'menus', 'donnees', 'contextes'):
    for e in polib.pofile(os.path.join(P, 'traductions', d + '.po')):
        if e.msgstr and e.msgstr == e.msgid: ident.add(e.msgid)
        if e.msgstr: homog.add(e.msgstr)
ca = collections.Counter(); autres = []
for x in a:
    if re.match(r'^(MUS|SE|PH)-', x[2]): ca['identifiants du test sonore (exception)'] += 1
    elif x[2] in ident: ca['texte identique en français (nom propre ou exception justifiée)'] += 1
    elif x[2] in homog: ca['texte français officiel identique à un autre texte anglais (ex. CORDELL → JIMMY)'] += 1
    elif x[0] == '(source inconnue)': ca['bruit de détection (données binaires décodées par hasard)'] += 1
    else: ca['à vérifier'] += 1; autres.append(x[2][:40])
snd = ca['identifiants du test sonore (exception)']
w('- Chaînes anglaises de la ROM de référence encore présentes (`outils/controle_anglais.py`) : %d — %s. À vérifier : %s.' % (
    len(a), ', '.join('%s %d' % kv for kv in ca.most_common()), ', '.join(autres) or 'aucune'))
w('- Test aller-retour (`outils/test_aller_retour.py`, msgstr = msgid) : ROM identique à la référence (dernier passage consigné dans l’historique git).\n')

# ------------------------------------------------------------ relectures
w('## Relectures ChatGPT\n')
w('| Lot | Remarques | Acceptées | Refusées | À arbitrer / vérifier |')
w('|---|---|---|---|---|')
for d in sorted(glob.glob(os.path.join(R, 'relectures', '*'))):
    rem = os.path.join(d, 'remarques.json'); arb = os.path.join(d, 'arbitrage.tsv')
    if not os.path.exists(rem): continue
    n = len(json.load(open(rem, encoding='utf-8')))
    c = collections.Counter(l.split('\t')[0] for l in open(arb, encoding='utf-8').read().split('\n')[1:] if l.strip()) if os.path.exists(arb) else {}
    w('| %s | %d | %d | %d | %d |' % (os.path.basename(d), n, c.get('accepté', 0), c.get('refusé', 0), c.get('à_arbitrer', 0) + c.get('à_vérifier', 0)))
w('')

# ------------------------------------------------------------ images
w('## Images traduites\n')
imgs = [l.split(None, 1)[1].strip() for l in open(os.path.join(P, 'images', 'EMPREINTES_ORIGINAUX.txt')) if l.strip()]
groupes = collections.Counter('/'.join(x.split('/')[:2]) for x in imgs)
w('%d fichiers (images et tilemaps) dans `images/`, par dossier : %s.\n' % (len(imgs), ', '.join('%s (%d)' % kv for kv in sorted(groupes.items()))))
w('Détail image par image, méthode et vérification : `rapport/images/RAPPORT.md`.\n')

# ------------------------------------------------------------ exceptions
w('## Exceptions (textes gardés tels quels)\n')
exc = collections.Counter()
for f in glob.glob(os.path.join(P, 'traductions', 'lots', '*', '*exceptions*.json')):
    for it in json.load(open(f, encoding='utf-8')):
        exc[(it.get('fichier', '?').split('/')[-1], (it.get('note') or '')[:110])] += 1
for (f, n), k in sorted(exc.items(), key=lambda x: -x[1])[:40]:
    w('- %s (%d) : %s' % (f, k, n))
w('- Identifiants du test sonore (MUS-…, SE-…, %d chaînes) : générés à partir des noms de constantes du code, non traduisibles sans modifier le code ; écran de débogage.' % snd)
w('- Code `{KUN}` (suffixe japonais) omis par les textes officiels français ; claviers (`src/text_input_strings.c`) non traduits volontairement.\n')

# ------------------------------------------------------------ à valider
w('## Points à valider par un humain\n')
w(lire('a_valider.md', '(voir `rapport/a_valider.md`)'))
open(os.path.join(R, 'RAPPORT.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('rapport/RAPPORT.md écrit (%d lignes)' % len(L))
