# Décisions manuelles, partie 2 : textes non traduits hors noms de Dresseurs, corrections trouvées au passage
exec(open('/private/tmp/claude-501/-Users-tfournier-projets-gitlab-com-tfournier-PokemonHnS-FR/d65695bd-6542-4bbf-9aff-f39c55206823/scratchpad/c1/mes_decisions.py').read().split('# ---------------------------------------------------------------- A_ctx')[0])
prev = json.load(open(S + '/mes_decisions_1.json'))
OUT = prev['OUT']; EXC = prev['EXC']; DEC = prev['DEC']
DEC['A:520'] = ('rejeté', 'identique à l’entrée à contexte existante (moves_info.h : Psyko)')
fr = open(P + '/memoires/em_fr.gba', 'rb').read()


def emfr(s):
    b = E.G.encode(s)
    p = fr.find(b + b'\xff')
    return 'texte identique présent dans Émeraude FR (FR %X)' % p if p >= 0 else 'absent de la ROM Émeraude FR'

# --- Pokédex des célébrités (FRLG) : noms SoulSilver FR
CB = '{COLOR BLUE}{SHADOW LIGHT_BLUE}'
for en, frn in [('PROF. OAK', 'Prof. Chen'), ('BROCK', 'Pierre'), ('MISTY', 'Ondine'), ('LT. SURGE', 'Major Bob'), ('ERIKA', 'Erika'),
                ('SABRINA', 'Morgane'), ('BLAINE', 'Auguste'), ('BILL', 'Léo')]:
    add(CB + en, CB + frn, SS, 'glossaire / .po : %s = %s' % (en, frn), 'nom du Pokédex des célébrités (FRLG) : nom SoulSilver FR, comme les entrées sœurs déjà traduites (Koga, Aldo, Peter, M. Fuji)')
# --- noms proposés de l'introduction FRLG
for n in ['OMI', 'REY', 'MAX']:
    add(n, n, TN, '', 'nom proposé à l’introduction FRLG : gardé tel quel en capitales, comme les autres noms de ce fichier (KAZ, TORU, JODI…)', lst=EXC)
# --- dialogues
add('Do you want to return to LILYCOVE?', 'Voulez-vous retourner à NENUCRIQUE?', TN, 'cf. « On retourne à NENUCRIQUE? » (Émeraude FR, event_ticket_1.inc)',
    'capitaine du bateau du Ticket (Hoenn) : NENUCRIQUE comme Émeraude FR ; vouvoiement du personnel')
add('{PLAYER} planted one {STR_VAR_1} in\\nthe soft, loamy soil.', '{PLAYER} plante une {STR_VAR_1}\\ndans le sol meuble et fertile.', TN, 'cf. « sol meuble et fertile » (entrée sœur)',
    '{STR_VAR_1} = nom de Baie (féminin) ; même tournure que « {PLAYER} répand le {STR_VAR_1} sur le sol meuble et fertile. »')
add('Thank you for using the STAMP CARD\\nSystem.\\pYou have {STR_VAR_1} more to collect to\\nfill your STAMP CARD.',
    'Merci d’utiliser le système de\\nCarte à tampons.\\pIl vous reste {STR_VAR_1} tampons à\\nobtenir pour remplir votre Carte.', TN, '', 'Cadeau Mystère (carte à tampons) ; vouvoiement')
add('the LILYCOVE CONTEST HALL.', 'la SALLE DES CONCOURS DE NENUCRIQUE.', TN, '', 'suite de « You may obtain a {POKEBLOCK} CASE from\\n » (variante non-HnS de safari_zone.inc) ; noms Hoenn en capitales comme Émeraude FR')
add('{B_OPPONENT_MON1_NAME} appeared!\\p', '{B_OPPONENT_MON1_NAME} apparaît!\\p', TN, 'cf. « {B_OPPONENT_MON1_NAME} sauvage apparaît! »', 'message de combat (même tournure que les apparitions de Pokémon sauvages)')
add('Search {STR_VAR_1}', 'Chercher {STR_VAR_1}', TN, '', 'DexNav')
add('{START_BUTTON} EXIT', '{START_BUTTON} QUITTER', TN, '', 'DexNav : libellé de bouton (capitales comme l’anglais)')
add('{R_BUTTON} FLY', '{R_BUTTON} VOL', TN, 'capacité Vol', 'carte de la région : bouton R pour voler')
add('{DPAD_UPDOWN} MORNING', '{DPAD_UPDOWN} MATIN', TN, 'cf. {DPAD_UPDOWN} JOUR / NUIT', 'zones du Pokédex : périodes')
add('{DPAD_UPDOWN} EVENING', '{DPAD_UPDOWN} SOIR', TN, 'cf. {DPAD_UPDOWN} JOUR / NUIT', 'zones du Pokédex : périodes')
add('LR', 'LR', EM, 'option MODE BOUTONS d’Émeraude FR : NORMAL / LR / L=A', 'nom du mode des boutons L et R, identique dans Émeraude FR', lst=EXC)
# environnements de combat / visualiseur
for en, f_ in [('Ice', 'Glace'), ('Sky', 'Ciel'), ('Mountain', 'Montagne'), ('Frontier', 'Zone de Combat'), ('Gym', 'Arène'), ('Puddle', 'Flaque')]:
    add(en, f_, TN, '', 'nom d’environnement de combat / décor du visualiseur (casse normale comme Herbe, Plaine, Etang)')
# scrcmd
add('KENYA', 'Piou Piou', SS, '200:7 — Piou Piou (Kenya)', 'surnom du ROUCOOL du facteur (scrcmd.c) : nom SoulSilver FR (banque 200)')
add('Chad', 'Chad', TN, '', 'pseudonyme (nom de dresseur d’origine dans scrcmd.c) : gardé tel quel', lst=EXC)
# strings.c inutilisés
add('                       POKéMON', '                       Pokémon', TN, '', 'texte inutilisé (catégorie vide du Pokédex) : espaces conservées')
add('        .   lbs.', '        .   kg', TN, 'cf. « ???.? kg. »', 'texte inutilisé (poids vide du Pokédex) : unité métrique comme le reste du Pokédex')
add('BATTLE ITEMS', 'OBJ. COMBAT', TN, '', 'poche du Sac (si les poches ne sont pas fusionnées), capitales comme SOINS')
# battle_debug
BD = {'Ability': 'Talent', 'Held Item': 'Objet tenu', 'Moves': 'Capacités', 'PP': 'PP', 'AI': 'IA', 'Attack': 'Attaque', 'Defense': 'Défense',
      'Speed': 'Vitesse', 'Sp. Atk': 'Atq. Spé.', 'Sp. Def': 'Déf. Spé.', 'Confusion': 'Confusion', 'Flinched': 'Apeuré', 'Torment': 'Tourmente',
      'Rage': 'Frénésie', 'Foresight': 'Clairvoyance', 'Leech Seed': 'Vampigraine', 'Lock On': 'Verrouillage', 'Perish Song': 'Requiem',
      'Minimize': 'Lilliput', 'Charge': 'Chargeur', 'Yawn': 'Bâillement', 'Imprison': 'Possessif', 'Gastro Acid': 'Suc Digestif', 'Embargo': 'Embargo',
      'Miracle Eye': 'Œil Miracle', 'Magnet Rise': 'Vol Magnétik', 'Heal Block': 'Anti-Soin', 'Aqua Ring': 'Anneau Hydro', 'Power Trick': 'Astuce Force',
      'Toxic Spikes': 'Pics Toxik', 'Stealth Rock': 'Piège de Roc', 'Reflect': 'Protection', 'Light Screen': 'Mur Lumière', 'Safeguard': 'Rune Protect',
      'Mist': 'Brume', 'Tailwind': 'Vent Arrière', 'Lucky Chant': 'Air Veinard', 'Double Battle': 'Combat Duo', 'Stall': 'Temporiser', 'Safari': 'Safari',
      'Restore Hp': 'Soin PV', 'Restore Pp': 'Soin PP', 'Grip Claw': 'Accro Griffe', 'Big Root': 'Grosseracine'}
for en, f_ in BD.items():
    note = 'menu de debug des combats (comme le lot E)'
    if en in ('Torment', 'Rage', 'Foresight', 'Leech Seed', 'Lock On', 'Perish Song', 'Minimize', 'Charge', 'Yawn', 'Imprison', 'Gastro Acid', 'Embargo', 'Miracle Eye',
              'Magnet Rise', 'Heal Block', 'Aqua Ring', 'Power Trick', 'Toxic Spikes', 'Stealth Rock', 'Reflect', 'Light Screen', 'Safeguard', 'Mist', 'Tailwind', 'Lucky Chant'):
        note += ' : nom officiel de la capacité (.po, moves_info.h)'
    if en in ('Grip Claw', 'Big Root'): note += ' : nom officiel de l’objet (.po, items.h)'
    if en == 'Confusion': note += ' : état « confusion » (pas la capacité Choc Mental)'
    if en in ('PP', 'Embargo', 'Safari', 'Confusion'):
        add(en, f_, TN, '', note + ' ; identique en français', lst=EXC if en == 'PP' else None)
    else:
        add(en, f_, TN, '', note)
# debug.c
add('Continue…', 'Continuer…', TN, '', 'menu de debug')
add('Group: {STR_VAR_1}{CLEAR_TO 90}\\n{CLEAR_TO 90}\\n\\n{STR_VAR_3}{CLEAR_TO 90}', 'Groupe: {STR_VAR_1}{CLEAR_TO 90}\\n{CLEAR_TO 90}\\n\\n{STR_VAR_3}{CLEAR_TO 90}', TN, '', 'menu de debug (téléportation) : codes et colonnes {CLEAR_TO} de l’anglais')
add('May', 'FLORA', EM, 'Émeraude FR : FLORA', 'debug : PNJ suiveur (Brendan = BRICE, Wally = TIMMY déjà traduits)')
add('Steven', 'PIERRE', EM, 'Émeraude FR : PIERRE', 'debug : PNJ suiveur, nom Émeraude FR')
add('Red', 'Red', SS, 'SoulSilver FR : Red', 'debug : PNJ suiveur ; nom SoulSilver FR identique à l’anglais', lst=EXC)
add('Partner: {STR_VAR_1}', 'Partenaire: {STR_VAR_1}', TN, '', 'menu de debug')
add('Double Battle: {STR_VAR_1}', 'Combat Duo: {STR_VAR_1}', TN, '', 'menu de debug')
add('Music…', 'Musique…', TN, '', 'menu de debug')
add('Party…', 'Equipe…', TN, '', 'menu de debug')
add('Player…', 'Joueur…', TN, '', 'menu de debug')
add('Sound…', 'Son…', TN, '', 'menu de debug')
add('ID: {STR_VAR_3}\\n{STR_VAR_1}{CLEAR_TO 90}\\n\\n{STR_VAR_2}{CLEAR_TO 90}', 'ID: {STR_VAR_3}\\n{STR_VAR_1}{CLEAR_TO 90}\\n\\n{STR_VAR_2}{CLEAR_TO 90}', TN, '', 'menu de debug : « ID » identique en français', lst=EXC)
add('Flag: {STR_VAR_1}{CLEAR_TO 90}\\n{STR_VAR_2}{CLEAR_TO 90}\\n{STR_VAR_3}', 'Drapeau: {STR_VAR_1}{CLEAR_TO 90}\\n{STR_VAR_2}{CLEAR_TO 90}\\n{STR_VAR_3}', TN, '', 'menu de debug : colonnes de l’anglais')
add(' None', ' Aucune', TN, '', 'menu de debug (capacité d’une CT/CS absente) : espace initiale conservée')
add('Level:{CLEAR_TO 90}\\n{STR_VAR_1}{CLEAR_TO 90}\\n{CLEAR_TO 90}\\n{STR_VAR_2}{CLEAR_TO 90}', 'Niveau:{CLEAR_TO 90}\\n{STR_VAR_1}{CLEAR_TO 90}\\n{CLEAR_TO 90}\\n{STR_VAR_2}{CLEAR_TO 90}', TN, '', 'menu de debug : colonnes de l’anglais')
add('Default', 'Par défaut', TN, '', 'menu de debug (capacité par défaut)')
add('Move ', 'Cap. ', TN, '', 'menu de debug : suivi d’un numéro (« Cap. 1 ») ; espace finale conservée')
add('Player', 'Joueur', TN, '', 'nom du Dresseur de debug (debug_trainers.party ; « Debugger » = Débogueur)')
add('PORYGON{CLEAR_TO 0x4B}{FONT_SMALL} 9,999 COINS', 'PORYGON{CLEAR_TO 0x4B}{FONT_SMALL} 9 999 JETONS', TN, 'cf. « MINIDRACO{CLEAR_TO 0x4B}{FONT_SMALL} 2 800 JETONS »', 'menu des lots du Casino : même format que les entrées sœurs')
# union_room.h
UR = [('Awaiting communication\\nfrom another player.', 'Attente de la connexion\\nd’un autre joueur.'),
      ('4 players\\nneeded.', 'Il faut\\n4 joueurs.'),
      ('Communicating…\\nPlease wait.', 'Transmission…\\nVeuillez patienter.'),
      ('{STR_VAR_1}: Want to do anything else?', '{STR_VAR_1}: On fait autre chose?'),
      ('We have registered your POKéMON for\\ntrade on the TRADING BOARD.\\pThank you for using this service!\\p', 'Votre Pokémon a été inscrit au\\nPANNEAU D’ECHANGE.\\pMerci d’avoir utilisé ce service!\\p'),
      ('Nobody has registered any POKéMON\\nfor trade on the TRADING BOARD.\\p\\n', 'Personne n’a inscrit de Pokémon\\nau PANNEAU D’ECHANGE.\\p\\n'),
      ('TRAINERS wishing to make a trade\\nwill be listed.', 'Les Dresseurs souhaitant faire un\\néchange vont s’afficher.'),
      ('Please choose the TRAINER with whom\\nyou would like to trade POKéMON.', 'Veuillez choisir le Dresseur avec\\nqui vous voulez échanger un Pokémon.'),
      ('You have not registered a POKéMON\\nfor trading.\\p', 'Vous n’avez inscrit aucun Pokémon\\npour un échange.\\p'),
      ("{STR_VAR_1} can't make a trade for\\nyour POKéMON right now.\\p", '{STR_VAR_1} ne peut pas échanger\\nvotre Pokémon pour le moment.\\p'),
      ("You can't make a trade for\\n{STR_VAR_1}'s POKéMON right now.\\p", 'Impossible d’échanger le Pokémon\\nde {STR_VAR_1} pour le moment.\\p'),
      ('Please wait for other TRAINERS to\\ngather and get ready.', 'Veuillez attendre que les autres\\nDresseurs soient prêts.')]
for en, f_ in UR:
    add(en, f_, TN, 'cf. entrées Émeraude FR voisines (« Veuillez choisir le Dresseur avec\\nqui faire l’échange. », « Transmission… »)', 'Club Union / panneau d’échange : vouvoiement et vocabulaire des textes Émeraude FR voisins (PANNEAU D’ECHANGE en capitales, sans accent)')
# Match Call (profils du PokéNav, Émeraude FR exact ; l'anglais HnS n'a qu'une apostrophe droite au lieu de ’)
MC = [("Married 50 years, we've", 'On élève des PKMN', '0x624FBD'), ('devotedly raised POKéMON.', 'ensemble depuis 50 ans.', '0x624FCF'),
      ('students into POKéMON!', 'les PKMN!', '0x62526D'), ('I must swim over 6 miles', 'Tous les jours, je nage au', '0x62566E'),
      ('strongest one day!', 'fort!', '0x6257A0'), ('that I may become a ninja.', 'un ninja.', '0x625851'),
      ('BUG POKéMON are number 1!', 'Les PKMN INSECTE, oui!', '0x625D74'), ('I walk the 30 minutes from', 'Je marche tous les jours', '0x6260B3'),
      ('home to here every day.', '30 minutes pour venir ici!', '0x6260CC'), ("I'm one of the ELITE FOUR!", 'je fais partie du CONSEIL 4!', '0x626248')]
for en, f_, a in MC:
    s = E.officiel(f_, en)
    add(en, s, EM, 'FR %s (table des profils PokéNav, même entrée que l’anglais d’Émeraude US à l’apostrophe près) ; FR brut : « %s »' % (a, f_),
        'profil Match Call : moitié de phrase officielle Émeraude FR (la phrase FR se répartit autrement entre les deux lignes, cf. ligne voisine)')
add('every day.', 'moins 10 km.', EM, 'FR 0x625689 (2e ligne du profil de KATELYN, après « Tous les jours, je nage au »)',
    'profil Match Call de KATELYN : 2e moitié de la phrase officielle ; l’actuel « tous les jours. » donnait « Tous les jours, je nage au / tous les jours. » (texte présent dans match_call_messages.h seulement)')
# région / Easy Chat
add('LITTLEROOT TOWN', 'BOURG-EN-VOL', EM, 'Émeraude FR : BOURG-EN-VOL', 'nom de lieu Hoenn (region_map_sections.json), capitales comme AUTEQUIA')
add('SPECIAL AREA', 'ZONE SPECIALE', TN, '', 'nom de section de carte générique (region_map_sections.json), capitales comme les lieux d’Émeraude')
add('Joey', 'Joey', TN, '', 'générique HnS : pseudonyme d’une personne, gardé tel quel', lst=EXC)
# berry_blender.c : textes japonais inutilisés
for en in ['\\nいいTVができました ', '\\nダメTVができました ']:
    add(en, en, TN, 'src/berry_blender.c : « static const u8 sJPText_…TvReady[] … // Unused »', 'texte japonais jamais affiché (tableau marqué Unused, aucune référence) : gardé tel quel ; il contient des kana mais la charmap HnS les encode (la ROM anglaise les contient déjà)', lst=EXC)

# --- crédits
CR = {'credits_frlg': [('\\n\\nDirector\\n\\n\\n\\n', '\\n\\nDirection\\n\\n\\n\\n'), ('\\nMusic Composition\\n\\n\\n\\n\\n', '\\nComposition musicale\\n\\n\\n\\n\\n'),
                       ('\\n\\nSound Effects\\n\\n\\n\\n', '\\n\\nEffets sonores\\n\\n\\n\\n'), ('\\nGame Scenario\\n\\n\\n\\n\\n', '\\nScénario\\n\\n\\n\\n\\n'),
                       ('\\n\\nPOKéDEX Text\\n\\n\\n\\n', '\\n\\nTextes du Pokédex\\n\\n\\n\\n'), ('\\n\\nNCL Product Testing\\n\\n\\n\\n', '\\n\\nTests produit NCL\\n\\n\\n\\n'),
                       ('Special Thanks\\n\\n\\n\\n\\n\\n', 'Remerciements\\n\\n\\n\\n\\n\\n'), ('Information Supervisors\\n\\n\\n\\n\\n\\n', 'Supervision des informations\\n\\n\\n\\n\\n\\n'),
                       ('Coordinators\\n\\n\\n\\n\\n\\n', 'Coordination\\n\\n\\n\\n\\n\\n'), ('\\nProducers\\n\\n\\n\\n\\n', '\\nProducteurs\\n\\n\\n\\n\\n'),
                       ('\\n\\nExecutive Producer\\n\\n\\n\\n', '\\n\\nProducteur exécutif\\n\\n\\n\\n'), ('NOA Product Testing\\n\\n\\n\\n\\n\\n', 'Tests produit NOA\\n\\n\\n\\n\\n\\n')]}
for en, f_ in CR['credits_frlg']:
    add(en, f_, TN, '', 'générique FRLG : rubrique traduite comme les rubriques sœurs déjà traduites de credits_frlg.c (Direction artistique, Programmeurs…), mise en page \\n de l’anglais')
for en in ['\\n\\n\\nJunichi Masuda\\n\\n\\n', '\\n\\n\\nAkira Kinashi\\n\\n\\n']:
    add(en, en, TN, '', 'générique FRLG : nom de personne gardé tel quel (mise en page de l’anglais)', lst=EXC)
for en, old in [('\\n\\n\\nSatoshi Tajiri\\n\\n\\n', 'nom faux (« Shusaku Egami ») et mise en page perdue'), ('\\n\\n\\nSatoru Iwata\\n\\n\\n', 'nom faux (« Hiroaki Tsuru ») et mise en page perdue'),
                ('\\n\\n\\nGo Ichinose\\n\\n\\n', 'mise en page perdue (les \\n de l’anglais manquaient)'), ('\\n\\n\\nKenji Matsushima\\n\\n\\n', 'mise en page perdue')]:
    add(en, en, TN, 'banque 440 (générique SoulSilver) exclue de l’alignement : noms sans lien d’identité', 'corrige l’entrée actuelle « SoulSilver FR officiel » : %s ; nom de personne gardé tel quel (alignement_faux : le texte SS venait d’une banque mal alignée)' % old, alignement_faux=True)
credits_h = [o for o in json.load(open(S + '/vides.json')) if o['occ'][0][0] == 'src/data/credits.h']
for o in credits_h:
    m = o['msgid']; pr = emfr(m)
    if pr.startswith('texte identique'):
        add(m, m, EM, pr, 'générique d’Émeraude : Émeraude FR garde cette ligne en anglais (rubriques et noms) ; gardé tel quel, comme « French Version Coordinators »', lst=EXC)
    else:
        add(m, m, TN, pr, 'générique d’Émeraude : nom propre (personne ou organisme anglophone, propre à la version anglaise) gardé tel quel', lst=EXC)

# --- corrections trouvées au passage (échanges in-game : surnoms SoulSilver FR, banque 200)
for en, i, f_, old in [('MUSCLE', 1, 'Gonflor', 'LE MUSCLE (texte de lilycove_lady.h)'), ('IRON', 12, 'Pôlo', 'Fer (nom de l’objet)'),
                       ('LORENZO', 21, 'Quantin', 'LUIS (Dresseur d’Émeraude)'), ('STEVEN', 25, 'Rochard', 'Pierre (Pierre Rochard d’Émeraude)')]:
    add(en, f_, SS, '200:%d — %s' % (i, f_), 'trouvé au passage : échange in-game Johto/Kanto de trade.h, nom/surnom SoulSilver FR (banque 200, échanges HGSS) ; l’entrée générale donnait %s' % old, ctx='src/data/trade.h')

json.dump(dict(OUT=OUT, EXC=EXC, DEC=DEC), open(S + '/mes_decisions_2.json', 'w'), ensure_ascii=False, indent=1)
print(len(OUT), len(EXC))
