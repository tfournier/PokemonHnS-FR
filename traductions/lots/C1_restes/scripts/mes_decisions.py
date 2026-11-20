# Décisions manuelles du lot C1 (hors noms de Dresseurs et hors lots délégués)
exec(open('/private/tmp/claude-501/-Users-tfournier-projets-gitlab-com-tfournier-PokemonHnS-FR/d65695bd-6542-4bbf-9aff-f39c55206823/scratchpad/c1/commun.py').read())
sys.path.insert(0, P + '/outils/alignement')
import em_commun as E
idx = load_po()
nd = {x['_id']: x for x in json.load(open(S + '/douteux_nonnoms.json'))}
OUT = []      # entrées C1
EXC = []      # exceptions (texte gardé)
DEC = {}      # _id -> (decision, raison)
TN = 'traduction nouvelle'; EM = 'Émeraude FR officiel'; EMA = 'Émeraude FR officiel (adapté)'; SS = 'SoulSilver FR officiel'


def first_occ(m, ctx=''):
    k = (ctx, m) if (ctx, m) in idx else ('', m)
    e = idx[k][1]
    oc = [o for o in e.occurrences if not ctx or o[0] == ctx] or e.occurrences or [(ctx, '0')]
    return oc[0][0], int(oc[0][1]) if str(oc[0][1]).isdigit() else 0


def cur(m, ctx=''):
    k = (ctx, m)
    return idx[k][1].msgstr if k in idx else ''


def add(m, s, src, preuve='', note='', ctx='', ids=(), dec='retenu', lst=None, **kw):
    f, l = first_occ(m, ctx)
    d = dict(msgid=m, msgstr=s, source=src, fichier=f, ligne=l, ancien=cur(m, ctx), preuve=preuve, note=note)
    if ctx: d['msgctxt'] = ctx
    d.update(kw)
    (OUT if lst is None else lst).append(d)
    for i in ids: DEC[i] = (dec, note)


def rej(i, raison):
    DEC[i] = ('rejeté', raison)

# ---------------------------------------------------------------- A_ctx
EC_ST = 'src/data/easy_chat/easy_chat_group_status.h'
ident = []
for i, x in nd.items():
    if x['_cat'] != 'A_ctx': continue
    b = (x['po_base'] or ['', ''])[0]
    if x['msgstr'] == b:
        ident.append(i)
for i in ident:
    rej(i, 'inutile : l’entrée générale du .po a déjà exactement ce texte (pas besoin de msgctxt)')
# retenus avec msgctxt (texte Émeraude FR exact de ce fichier, différent de l'entrée générale)
for i in ['A:49', 'A:51', 'A:52', 'A:53', 'A:54', 'A:58', 'A:79', 'A:59', 'A:88', 'A:109', 'A:162', 'A:571', 'A:845', 'A:848']:
    x = nd[i]
    add(x['msgid'], x['msgstr'], EM, x['preuve'], 'même anglais, texte Émeraude FR propre à ce fichier : entrée à contexte (msgctxt vérifié parmi les fichiers du texte)', ctx=x['msgctxt'], ids=[i])
DEC['A:572'] = ('retenu', 'doublon de A:571 (même proposition, même fichier)')
# A:50 (Route104) devient l'entrée générale : convient aussi à RustboroCity (A:75 sans {PLAYER} : codes différents)
x = nd['A:50']
add(x['msgid'], x['msgstr'], EM, x['preuve'], 'texte Émeraude FR exact de Route104, repris comme entrée générale : il vaut aussi pour RustboroCity, dont le texte FR officiel omet {PLAYER} (A:75, codes différents) ; remplace un texte du patch qui omettait aussi {PLAYER}', ids=['A:50'])
rej('A:75', 'le texte Émeraude FR de RustboroCity omet {PLAYER}{KUN} (codes différents) ; l’entrée générale reprend celui de Route104 (A:50)')
# entrées générales (un seul fichier) : texte Émeraude FR exact plutôt que patch/traduction manuelle
for i in ['A:515', 'A:523', 'A:526']:
    x = nd[i]
    add(x['msgid'], x['msgstr'], EM, x['preuve'], 'description officielle Émeraude FR (le texte n’apparaît que dans moves_info.h : entrée générale, pas de msgctxt) ; remplace le patch FR', ids=[i])
for i in ['A:129', 'A:131', 'A:133', 'A:135', 'A:138']:
    x = nd[i]
    s = x['msgstr'].replace('ZONE DE\\nCombat', 'Zone de\\nCombat').replace('ZONE DE\\lCombat', 'Zone de\\lCombat')
    src = EM if s == x['msgstr'] else EMA
    add(x['msgid'], s, src, x['preuve'] + ('' if s == x['msgstr'] else ' ; FR officiel : « %s »' % x['msgstr']),
        'appel PokéNav Émeraude FR (match_call.inc seul : entrée générale) ; remplace une traduction manuelle' + ('' if s == x['msgstr'] else ' ; « ZONE DE Combat » homogénéisé en « Zone de Combat »'),
        ids=[i], dec='retenu' if src == EM else 'adapté')
# entrées générales corrigées
add('BERRY MASTER\'S HOUSE', 'MAISON DU MAITRE DES BAIES', EMA, nd['A:61']['preuve'] + ' ; FR officiel : « MAISON DU MAITRE DES BAIES »',
    'panneau de Route123 : texte Émeraude FR en capitales comme les autres panneaux de maison (MAISON D’ANNETTE) ; la casse mixte « MAISON DU Maître DES Baies » venait du passage de style ; remplace « MAISON Maître Baies » (patch)', ids=['A:61'], dec='adapté')
add('BERRY MASTER\'S HOUSE', 'MAITRE DES BAIES', EMA, nd['A:844']['preuve'], 'nom de lieu du PokéNav (landmark.c), Émeraude FR en capitales', ctx='src/landmark.c', ids=['A:844'], dec='adapté')
add('RAIN', 'PLUIE', EM, nd['A:872']['preuve'], 'nom de météo de debug (field_weather.c, strings.c) : Émeraude FR « PLUIE » remplace « Rain » (anglais resté dans le .po) ; entrée générale', ids=['A:872'])
add('SUNNY', 'SOLEIL', EM, nd['A:871']['preuve'], 'nom de météo de debug (field_weather.c, strings.c), Émeraude FR ; entrée générale (non traduite)', ids=['A:871'])
add('FOG', 'BROUILLARD', EMA, nd['A:873']['preuve'] + ' ; FR officiel « BROUILLARD » (FOG2 = BROUILLARD2)', 'nom de météo de debug, capitales comme SOLEIL2/BROUILLARD2 ; entrée générale (non traduite)', ids=['A:873'], dec='adapté')
add('SHADE', 'OMBRE', TN, '', 'nom de météo de debug (field_weather.c), capitales comme les autres')
rej('A:163', 'classe Kinésiste en casse normale souhaitable (comme Montagnard, Scout), mais l’entrée générale est un texte Émeraude FR exact (KINESISTE) qu’une simple différence de casse ne permet pas de remplacer ; signalé'); rej('A:164', 'idem A:163')
add('STURDY', 'Fermeté', EMA, nd['A:237']['preuve'], 'talent (abilities.h) en casse normale (style SoulSilver) ; FERMETE reste pour challenge_menu.c et Easy Chat', ctx='src/data/abilities.h', ids=['A:237'], dec='adapté')
add('SYNCHRONIZE', 'Synchro', EMA, nd['A:239']['preuve'], 'talent (abilities.h) en casse normale ; SYNCHRO reste pour challenge_menu.c et Easy Chat', ctx='src/data/abilities.h', ids=['A:239'], dec='adapté')
add('SITRUS BERRY', 'Baie Sitrus', EMA, nd['A:505']['preuve'], 'objet (items.h) en casse normale ; BAIE SITRUS reste pour challenge_menu.c', ctx='src/data/items.h', ids=['A:505'], dec='adapté')
for i, r in {'A:2': 'la proposition supprime la question « OK? » alors que l’anglais attend oui/non ; l’entrée générale (Émeraude FR) convient aux deux fichiers',
             'A:3': 'idem A:2', 'A:5': 'identique', 'A:12': 'codes/mise en page différents (retour à la ligne ajouté à un fragment d’une ligne) ; laissé à l’arbitrage de l’entrée générale (lot délégué)',
             'A:14': 'idem A:12', 'A:16': 'idem A:12', 'A:17': 'idem A:12',
             'A:19': 'variante Émeraude FR équivalente ; l’entrée générale est déjà un texte Émeraude FR exact', 'A:20': 'idem A:19',
             'A:32': 'carte HnS (Johto) : on garde l’entrée générale SoulSilver « Et voilà! »', 'A:42': 'différence minime (« Voici! » / « Et voilà! ») : entrée à contexte inutile',
             'A:56': 'différence minime : entrée à contexte inutile', 'A:240': 'variante Émeraude FR équivalente ; l’entrée générale est déjà un texte Émeraude FR exact',
             'A:456': 'Easy Chat : l’entrée à contexte existante vaut « PSY » (décision du projet)',
             'A:463': 'types : même graphie partout (décision 3, DRAGON)', 'A:785': 'idem', 'A:467': 'idem (FEU)', 'A:783': 'idem', 'A:459': 'idem (SPECTRE ; « SPECTR » était la troncature d’Émeraude)', 'A:782': 'idem',
             'A:458': 'idem (PLANTE)', 'A:784': 'idem', 'A:465': 'idem (VOL)', 'A:781': 'idem', 'A:464': 'idem (NORMAL)', 'A:868': 'idem (libellé en capitales)',
             'A:466': 'Easy Chat : l’entrée générale convient', 'A:460': 'Easy Chat : l’entrée générale convient', 'A:457': 'Easy Chat : FERMETE (entrée générale) convient', 'A:461': 'Easy Chat : SYNCHRO (entrée générale) convient',
             'A:578': 'casse mixte « Combat MULTI » : l’entrée générale COMBAT MULTI convient', 'A:787': 'idem',
             'A:509': 'POKéFLUTE en capitales contraire au style ; l’entrée générale Pokéflûte (Émeraude FR stylé) convient',
             'A:847': 'les natures sont en casse normale dans le .po (Hardi, Relax) : entrée générale conservée',
             'A:581': 'deux fichiers, même proposition : il faudrait changer l’entrée générale, mais les 2es lignes des rubans cadeaux ont été traduites avec « pour le triomphe » ; à arbitrer par l’agent principal (signalé)',
             'A:597': 'idem A:581', 'A:594': 'abréviation officielle « ROBUS. » non nécessaire (cohérence avec le lot délégué A:596)', 'A:595': 'idem', 'A:788': 'identique à l’entrée générale',
             'A:858': 'codes différents ({STR_VAR_2} ajouté)', 'A:503': 'identique', 'A:504': 'identique'}.items():
    if i not in DEC: rej(i, r)

# ---------------------------------------------------------------- A_pco
for i, x in nd.items():
    if x['_cat'] != 'A_pco': continue
    b = (x['po_base'] or ['', ''])[0]
    same = E.G.encode(x['msgstr']) == E.G.encode(b)
    add(x['msgid'], x['msgstr'], EMA, x['preuve'], ('texte identique au .po (seule la graphie de {CLEAR_TO} change : celle de l’anglais) ; ' if same else 'nom complet Émeraude FR au lieu de l’abréviation du patch (largeur vérifiée sous la colonne {CLEAR_TO}) ; ') + 'glyphe 0x64 d’Émeraude FR (Points de Combat) rendu « PCo », comme tout le .po', ids=[i], dec='retenu' if same else 'adapté')

# ---------------------------------------------------------------- Easy Chat
EC = {  # msgid: (valeur, source, ctx-fichier si texte partagé)
    'PLAY': ('JOUER', TN), 'MAGAZINE': ('MAGAZINES', EM), 'RIVAL': ('RIVAL', TN), 'ON': ('SUR', TN), 'NEXT': ('PROCHAIN', EM), 'ALL': ('TOUT', EM),
    'ANTICIPATION': ('ANTICIPATION', TN), 'TEACH': ('ENSEIGNER', EM), 'MAKE': ('FAIRE', EM), 'RUN': ('JE COURS', EM), 'WORKING': ('TRAVAILLER', EM),
    'OWN': ('POSSEDER', TN), 'FIERY': ('FOUGUEUX', EM), 'LOVEY-DOVEY': ('MIMI', EM), 'MATCH UP': ('AFFRONTEMENT', TN), 'TRUMP CARD': ('ATOUT', TN),
    'COME ON': ('ALLEZ', TN), 'ESCAPE': ('ECHAPPER', EM), 'LOSE': ('PERDRE', EM), 'GUARD': ('VIGILANCE', EM), 'HOT': ('CHAUD', EM), 'TASTY': ('DELICIEUX', EM),
    'CLOSE': ('PROCHE', EM), 'NOTHING': ('RIEN', EM), 'BORED': ('JE M’ENNUIE', EM), 'MYSTERY': ('MYSTERE', EM), 'KIND': ('AGREABLE', EM),
    'OR': ('OU', EM), 'IS': ('EST', EM), 'IT': ('CA', TN), 'AT': ('A', TN), 'IN': ('EN', EM), 'OUT': ('DEHORS', EM), 'EVOLUTION': ('EVOLUTION', TN),
    'TOWER': ('TOUR', EM), 'HAPPINESS': ('BONHEUR', EM), 'IMPORTANT': ('IMPORTANT', TN), 'FUNNY': ('DROLE', EM), 'DOWNCAST': ('DECOURAGE', EM),
    'LIKES': ('AIME', TN), 'ALL RIGHT': ('D’ACCORD', TN), 'ADORE': ('J’ADORE', EM), 'DONE': ('FINI', TN), 'THANKS': ('MERCI BIEN!', EM),
    'WELL, THEN': ('HE BIEN', EM), "WHAT'S UP?": ('CA VA BIEN?', EM), 'HI': ('COUCOU', EM), 'YO': ('YO', EM), 'MOVIE': ('CINEMA', EM),
    'GOURMET': ('CUISINE', EM), 'GAME': ('JEUX', EM), 'SOFTWARE': ('LOGICIELS', EM), 'SONGS': ('CHANTER', EM), 'DIET': ('DIETETIQUE', EM),
    'TREASURE': ('TRESORS', EM), 'FLOWERS': ('JARDINAGE', EM), 'BALL': ('BALLON', TN), 'FESTIVAL': ('FESTIVALS', EM), 'LOOK': ('STYLE', TN),
    'HABIT': ('HABITUDES', EM), 'CLASS': ('CLASSE', EM), 'LESSONS': ('LECONS', TN), 'TEACHER': ('PROFESSEUR', EM), 'TEST': ('CONTROLE', EM),
    'LIFE': ('VIE', EM), 'BACK': ('DERRIERE', EM), 'HIGH': ('HAUT', EM), 'DOWN': ('BAS', TN), 'AM': ('SUIS', TN), 'NEAR': ('PRES', EM), 'WHAT': ('QUEL', EM),
    'BROTHER': ('FRERE', EM), 'ME': ('MOI', EM), 'HER': ('ELLE', TN), 'OUR': ('NOTRE', EM), 'AND': ('ET', EM), 'READY': ('PRET', EM),
    'MORNING': ('MATIN', EM), 'STOP': ('STOP', EM), 'SPRING': ('PRINTEMPS', EM), 'NIGHT': ('NUIT', EM), 'HEART': ('COEUR', TN),
    'CRIES': ('PLEURS', EM), 'OH, YEAH': ('AH OUI', EM), 'GWAHAHAHA': ('MOUHAHAHA', TN), 'TCH': ('PSHT', EM), 'HIYAH': ('HIYAAA', TN), 'ARRGH': ('ARRRG', EM),
}
EC_REJ = {'OFF': 'le texte n’apparaît que dans challenge_menu.c (libellé de menu) : ce n’est pas un mot Easy Chat, l’entrée générale convient',
          'MODERN': 'MODERNE (entrée générale) convient aussi au Livret', 'MODE': 'MODE convient aussi au Livret', 'EXCUSE ME': 'mot Émeraude non équivalent ; PARDON (actuel) convient',
          'VIEWING': 'mot Émeraude non équivalent ; VISIONNER (actuel) convient', 'COMPLETE': 'mot Émeraude non équivalent ; COMPLET convient', 'BOARD': 'mot Émeraude non équivalent ; PLANCHE convient',
          'PLANS': 'mot Émeraude non équivalent ; PLANS convient', 'RECOMMEND': 'mot Émeraude non équivalent ; RECOMMANDE convient', 'YES, SIR!': 'mot Émeraude non équivalent ; « Oui, chef! » convient',
          'KNOCKOUT': 'mot Émeraude non équivalent ; K.O. convient', 'BABY': 'mot Émeraude non équivalent ; BEBE convient', 'OLD': 'mot Émeraude non équivalent ; ANCIEN convient',
          'WROOOAAR!': 'GROOOAR (actuel) rend mieux le cri', 'SIGH': 'PFF (actuel) rend mieux le soupir', 'HAHAHA': 'mot Émeraude non équivalent (BEURK) ; HAHAHA convient',
          'AIYEEH': 'mot Émeraude non équivalent ; AYAHHHH convient', 'HUMPH': 'mot Émeraude non équivalent (HOURRA) ; HOUF convient'}
for i, x in nd.items():
    if x['_cat'] != 'A_easychat': continue
    m = x['msgid']
    if m in EC_REJ: rej(i, EC_REJ[m]); continue
    v, src = EC[m]
    ecf = [f for f in x['po_fichiers'] if 'easy_chat' in f]
    ctx = ecf[0] if len(x['po_fichiers']) > 1 and ecf else ''
    if not ctx and cur(m) == v and src == TN: rej(i, 'l’entrée actuelle convient'); continue
    if src == EM:
        d = 'retenu' if v == x['msgstr'] else 'adapté'
        note = 'mot du Livret Émeraude FR (même index EC_WORD) de même sens : gardé'
    else:
        d = 'rejeté'
        note = 'mot Émeraude FR du même index non équivalent (« %s ») : traduction du mot anglais' % x['msgstr']
    if ctx: note += ' ; texte partagé avec %s : entrée à contexte pour le Livret' % ', '.join(f.split('/')[-1] for f in x['po_fichiers'] if f != ctx)
    elif cur(m) and cur(m) != v: note += ' ; remplace « %s »' % cur(m)
    add(m, v, src, x['preuve'] if src == EM else '', note, ctx=ctx, ids=[i], dec=d)

json.dump(dict(OUT=OUT, EXC=EXC, DEC=DEC), open(S + '/mes_decisions_1.json', 'w'), ensure_ascii=False, indent=1)
print(len(OUT), collections.Counter(v[0] for v in DEC.values()), 'sans décision :', [i for i, x in nd.items() if x['_cat'] in ('A_ctx', 'A_pco', 'A_easychat') and i not in DEC])
