#!/usr/bin/env python3
"""Relecture indépendante d'un lot par ChatGPT (via la CLI Codex, connectée au compte ChatGPT).

  relecture_chatgpt.py <nom_du_lot> <fichiers .json…> [--taille 100] [--paralleles 4] [--alignement]

- Les textes officiels exacts (Émeraude FR / SoulSilver FR, non adaptés) ne sont pas relus,
  sauf avec --alignement : on demande alors seulement si c'est bien la bonne phrase.
- Paquets de 50 à 150 entrées : anglais, traduction, source, contexte, contraintes, plus un
  extrait de lexique officiel (termes présents dans le paquet).
- ChatGPT ne réécrit pas librement : il signale et propose une correction motivée.
- Sorties : rapport/relectures/<lot>/paquet_NNN.json (remarques brutes) et remarques.json
  (toutes les remarques, avec id → msgid). L'arbitrage se fait ensuite (arbitrer_relecture.py).
"""
import os, sys, re, json, pickle, subprocess, collections, concurrent.futures, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODEX = os.environ.get('CODEX', 'codex')

REGLES = """Tu es relecteur professionnel de la traduction française d'un jeu Pokémon (hack GBA « Heart & Soul » : Johto/Kanto façon HeartGold/SoulSilver, moteur Pokémon Émeraude).
Tu relis des entrées (anglais → français). Tu NE réécris PAS librement : pour chaque entrée qui pose un vrai problème, tu proposes une correction minimale et motivée. Si une entrée est correcte, tu ne la cites pas.

Signale uniquement :
- contresens, oubli ou ajout de sens (« contresens », « oubli ») ;
- non-respect de la terminologie officielle française (Pokémon Émeraude FR, Pokémon SoulSilver FR ; lexique fourni) (« terminologie ») ;
- incohérence de registre tu/vous (le personnel des Centres, Boutiques, Frontier, accueils vouvoie le joueur ; enfants, rivaux, Dresseurs, amis le tutoient en général) (« registre ») ;
- fautes d'orthographe, de grammaire, d'accord (« orthographe ») ; typographie française (« typographie ») ;
- codes entre accolades modifiés, ajoutés ou supprimés ({PLAYER}, {STR_VAR_1}, {COLOR …}, {PAUSE …}…) (« codes ») ;
- traduction qui semble appartenir à une autre phrase (texte décalé, morceau d'une autre réplique) (« autre_phrase »).

Conventions du projet (à respecter, ne PAS les signaler comme fautes) :
- Style SoulSilver : « Pokémon », « Dresseur », « Pokématos », « Prof. Orme », « Prof. Chen » ; lieux, objets, capacités avec majuscule initiale (« Bourg Geon », « Super Ball ») ; noms d'espèces en CAPITALES (PTITARD) ; noms de personnages de Hoenn en capitales comme dans Émeraude FR (FLORA, BRICE, Prof. SEKO).
- Pas d'espace avant ! ? : ; (contrainte de place, comme les jeux officiels de l'époque). Apostrophe ’, points de suspension …, guillemets “ ”.
- \\n = 2e ligne, \\l = ligne suivante, \\p = nouvelle page : ce sont des sauts de ligne, ne les commente pas sauf s'ils coupent un mot.
- Libellés de menus en capitales (SAC, SAUVER, RETOUR…), abréviations officielles (PV, AT, DF, AS, DS, VI ; PSN, PAR, SOM, GEL, BRU, GLR ; N. pour le niveau).
- « … sauvage », « … ennemi » après le nom, sans article.
- « Team Rocket » pour l'organisation (jamais « les Rocket » seul), « Sbire de la Team Rocket » ou « Sbire Rocket » ; noms communs sans majuscule (un gamin, un combat), les classes de Dresseurs avec majuscule seulement quand elles désignent la classe (Gamin Joey).
- Majuscules jamais accentuées (Ile, Iles Ecume, A bientôt, ELECTRIK), cédille gardée (Ça).
- Respecte les longueurs maximales indiquées ; une correction ne doit pas les dépasser ni changer les codes.

Réponds UNIQUEMENT par un tableau JSON (éventuellement vide []), sans texte autour :
[{"id": <id>, "categorie": "contresens|oubli|terminologie|registre|orthographe|typographie|codes|autre_phrase", "probleme": "explication courte", "correction": "texte français complet corrigé (mêmes codes, mêmes \\\\n \\\\l \\\\p sauf nécessité)", "justification": "pourquoi, avec la référence officielle si terminologie"}]"""

REGLES_ALIGN = """Tu vérifies l'alignement de textes officiels français (Pokémon Émeraude FR ou SoulSilver FR) avec des phrases anglaises d'un hack Pokémon. Le français est officiel : ne corrige PAS son style ni sa traduction. Dis seulement si le français correspond bien à cette phrase anglaise (même réplique, même sens général), ou s'il s'agit d'une autre phrase (décalage d'alignement).
Réponds UNIQUEMENT par un tableau JSON des entrées MAL alignées (éventuellement vide []) :
[{"id": <id>, "categorie": "autre_phrase", "probleme": "explication courte", "correction": "", "justification": "ce que dit réellement le français"}]"""


def sans_acc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))


def lexique():
    """anglais HGSS → français SS pour les banques de noms officielles."""
    lx = {}
    try:
        pairs = pickle.load(open(os.path.join(P, 'memoires', 'tm_ss_pairs.pkl'), 'rb'))
    except Exception:
        return lx
    for b, i, e, f in pairs:
        if b in (222, 237, 750, 720, 279, 730) and e and f and len(e) < 30 and '{' not in e:
            lx.setdefault(e.strip().upper(), f.strip())
    return lx


def officiel_exact(src):
    s = (src or '').lower()
    return (s.startswith('émeraude fr officiel') or s.startswith('soulsilver fr officiel')) and 'adapt' not in s


def contraintes(it):
    c = []
    mid = it['msgid']
    if re.search(r'\\[nlp]', mid): c.append('dialogue : 198 px par ligne (~34 caractères)')
    else: c.append('une seule ligne')
    if it.get('max'): c.append('longueur max %s caractères' % it['max'])
    if mid.startswith(' '): c.append('commence par une espace (suffixe)')
    return ', '.join(c)


def appel(prompt, sortie):
    r = subprocess.run([CODEX, 'exec', '--skip-git-repo-check', '-s', 'read-only', '--ephemeral', '-o', sortie, '-'],
                       input=prompt, capture_output=True, text=True, timeout=1800)
    txt = open(sortie, encoding='utf-8').read() if os.path.exists(sortie) else ''
    m = re.search(r'\[.*\]', txt, re.S)
    if not m:
        raise RuntimeError('réponse sans JSON : ' + (txt or r.stderr)[-500:])
    return json.loads(m.group(0))


def main():
    args = sys.argv[1:]
    def opt(n, d):
        if n in args:
            i = args.index(n); v = args[i + 1]; del args[i:i + 2]; return v
        return d
    taille = int(opt('--taille', '100')); par = int(opt('--paralleles', '4'))
    align = '--alignement' in args; args = [a for a in args if not a.startswith('--')]
    lot, fichiers = args[0], args[1:]
    entrees = []
    for f in fichiers:
        for it in json.load(open(f, encoding='utf-8')):
            if not it.get('msgstr'): continue
            if officiel_exact(it.get('source')) != align: continue
            entrees.append(it)
    lx = lexique()
    gl = {}
    for l in open(os.path.join(P, 'traductions', 'glossaire.tsv'), encoding='utf-8'):
        if l.startswith('#') or not l.strip(): continue
        k, v, *_ = l.rstrip('\n').split('\t'); gl[k] = v
    dossier = os.path.join(P, 'rapport', 'relectures', lot); os.makedirs(dossier, exist_ok=True)
    paquets = [entrees[i:i + taille] for i in range(0, len(entrees), taille)]
    print('%s : %d entrées à relire, %d paquets' % (lot, len(entrees), len(paquets)))

    def traiter(k):
        sortie = os.path.join(dossier, 'paquet_%03d.json' % k)
        if os.path.exists(sortie):
            return k, json.load(open(sortie, encoding='utf-8'))
        pq = paquets[k]
        items = []; termes = {}
        for j, it in enumerate(pq):
            items.append({'id': j, 'anglais': it['msgid'], 'francais': it['msgstr'], 'source': it.get('source', ''),
                          'contexte': '%s:%s' % (it.get('fichier', '?'), it.get('ligne', '')) + (' — ' + it['note'] if it.get('note') else ''),
                          'contraintes': contraintes(it)})
            up = it['msgid'].upper()
            for en, fr in lx.items():
                if len(en) >= 4 and re.search(r'(?<![A-Z])' + re.escape(en) + r'(?![A-Z])', up): termes[en] = fr
            for w in re.findall(r"[A-ZÀ-Þa-zà-ÿ’' .\-]{3,}", it['msgstr']):
                kk = sans_acc(w.strip()).upper().replace('’', "'")
                if kk in gl: termes[w.strip()] = gl[kk]
        lex = '\n'.join('%s → %s' % (a, b) for a, b in sorted(termes.items())[:200])
        prompt = (REGLES_ALIGN if align else REGLES) + '\n\nLexique officiel utile (anglais ou graphie → graphie officielle) :\n' + (lex or '(aucun)') + \
            '\n\nEntrées :\n' + json.dumps(items, ensure_ascii=False, indent=0)
        tmp = sortie + '.tmp'
        for essai in range(3):
            try:
                res = appel(prompt, tmp); break
            except Exception as ex:
                err = ex
        else:
            return k, {'erreur': str(err)}
        for r in res:
            try: r['msgid'] = pq[int(r['id'])]['msgid']; r['msgstr'] = pq[int(r['id'])]['msgstr']; r['msgctxt'] = pq[int(r['id'])].get('msgctxt', '')
            except Exception: r['msgid'] = None
        json.dump(res, open(sortie, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        if os.path.exists(tmp): os.remove(tmp)
        return k, res

    tout = []; erreurs = 0
    with concurrent.futures.ThreadPoolExecutor(par) as ex:
        for k, res in ex.map(traiter, range(len(paquets))):
            if isinstance(res, dict): erreurs += 1; print('paquet %d : %s' % (k, res['erreur'][:200])); continue
            tout += [r for r in res if r.get('msgid')]
            print('paquet %d/%d : %d remarques' % (k + 1, len(paquets), len(res)), flush=True)
    json.dump(tout, open(os.path.join(dossier, 'remarques.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    c = collections.Counter(r.get('categorie') for r in tout)
    print('remarques : %d %s ; paquets en erreur : %d' % (len(tout), dict(c), erreurs))


if __name__ == '__main__':
    main()
