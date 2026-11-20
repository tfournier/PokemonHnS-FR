# Lot H : défauts de texte et de mise en page vus en jeu

## Résultat

- `H_textes.json` : **175 entrées** (142 traductions nouvelles, 21 « Émeraude FR officiel (adapté) »,
  12 « Émeraude FR officiel » : texte officiel exact rétabli après un passage de style qui l'avait mis en
  casse mixte). 11 entrées avec `msgctxt`, 10 avec `alignement_faux: true`. `verifier.py` : 0 problème.
- Deux correctifs de code nouveaux : `code/categorie-pokemon.patch`, `code/virgule-decimale.patch`.
- Captures avant / après (240×160) : `rapport/captures_H/<n° du défaut>_<écran>_{avant,apres}.png` (35 écrans).
- Script de travail (reproductible) : `build/lot_H/corrections.py` (écrit le JSON et une copie corrigée des
  .po dans `build/lot_H/traductions/`, jamais les .po principaux).

**Vérification en jeu** : ROM construite avec `construire.py --traductions build/lot_H/traductions`
(les 4 correctifs s'appliquent, aucune de mes chaînes n'est remise en anglais pour cause de longueur), puis
les 9 scénarios rejoués (`lancer_tests.sh`, tous OK, mêmes écrans qu'avant). « Avant » = ROM construite au
début du lot avec les .po de ce moment ; « après » = .po principaux du dernier commit + mes corrections.

### À savoir pour l'intégration

35 entrées remplacent un texte noté « officiel » exact (Émeraude FR / SoulSilver FR). `integrer_lot.py`
les **garde** même avec `--corriger` (essai fait) : elles portent le champ `"retouche_officiel"` :
- `"casse"` (31) : seule la casse change (le passage de style avait écrit « INFOS Pokémon »,
  « ANIMAT. Combat », « DEPLACER Pokémon », « Retour », « Sac »…) ; c'est autorisé par le brief ;
- `"place"` (4) : contrainte démontrée par le code d'affichage (surnom, CRI DE, NºID /, classe Prof.).

Il faut donc un passage d'intégration qui accepte ce champ (ou les forcer à la main). Attention aussi : si le
passage de style (`style.appliquer`) est relancé sur ces entrées, il remettra « Pokémon », « Combat »,
« Sac », « Retour » en casse mixte dans des libellés en capitales : il faudrait qu'il ignore les chaînes
entièrement en capitales (menus).

## Défaut par défaut

| n° | Cause | Correction | En jeu |
|---|---|---|---|
| 3 | `DrawMonTextEntryBox()` écrit le nom de l'espèce puis **ajoute** le titre ; `{STR_VAR_1}` n'est pas affiché. « Surnom de {STR_VAR_1}? » donnait « HERICENDRESurnom de ? ». | Texte : « {STR_VAR_1}: surnom? » → « HERICENDRE: surnom? » | vérifié (03) |
| 4 | Infos de capacité : colonne PREC à x=108 (code), FONT_NARROW, fenêtre de 144 px ; « PREC: 100 » = 41 px. | « PRE: » (36 px, comme « ACC: 100 ») | vérifié : « PRE: 100 » (04) |
| 5, 6 (Lv) | Glyphe 0x34 de la police (pas une chaîne). | Rien à faire côté texte : **déjà corrigé par le lot F** (polices) — « N.6 » s'affiche dans l'équipe, le résumé et le Pokédex EVO avec la ROM actuelle. | vérifié (05, 06) |
| 6 (Sinjoh) | « out of » traduit « sur » : TYPHLOSION évolue **hors** de Sinjoh (IF_NOT_REGION). | « hors de » | vérifié : « N.↑36, hors de Sinjoh. » (06) |
| 7 | Résumé : étiquettes de droite centrées sur 36 px dans une fenêtre de 40 px (`PrintPageNamesAndStats`). | `msgctxt src/strings.c` : ATQ.SP. / DEF.SP. / VIT. (battle_message.c garde « ATQ. SPE. », « VITESSE » dans les messages). Concerne aussi la fenêtre de montée de niveau (même fichier). Titres : INFOS POKéMON, APTITU. POKéMON. « POUVOIR » tronqué par l'icône (résumé et Pokédex) → `msgctxt src/strings.c` « PUIS. » (le mot Easy Chat garde POUVOIR). | vérifié (07, 07b) |
| 8, 9 | Réglages de partie : 3 valeurs dans 94 px (x=104 à 198, `GetMiddleX`) ; « NON FACILE NORMAL » = 90 px, « NON ECHELLE DIFFICILE » = 114 px. | `msgctxt src/challenge_menu.c` : EASY → LEGER, HARD → DUR ; SCALE → BADGES (IV/EV qui montent avec les Badges), EXTREM → MAX (252 EV). Toutes les combinaisons affichées ≤ 84 px (comme l'anglais). | vérifié (08, 08b, 09) |
| 10 | METRIQUE + IMPERIAL = 96 px pour 94. | IMPERIAL → « IMPER. » ; « Turbo » → TURBO | vérifié (10) |
| 13 | « Field » : ligne anglaise de SoulSilver prise pour une traduction (faux alignement). | TERRESTRE ; EAU ①②③ en capitales | vérifié (13) |
| 14 | Abréviations du patch FR. | `msgctxt` Pokédex : PV AT DF VI AS DS (consignes). « CATCH% » était déjà « CAPT.% ». « POUVOI » : voir 7. | vérifié (14) |
| 15 | `CopyMonCategoryText()` colle « catégorie » + espace + `gText_Pokemon`. | **Correctif `code/categorie-pokemon.patch`** : l'ordre vient d'une chaîne traduisible `"{STR_VAR_1} POKéMON"` (rendu anglais identique octet pour octet) ; entrée `msgctxt src/international_string_util.c` → « Pokémon {STR_VAR_1} ». | vérifié : « Pokémon Souris Feu » (15) |
| 16 | `{PKMN}BALLS` (glyphe collé, déjà dans l'anglais). | « {R_BUTTON} en combat: lancer une Poké Ball. / Maintenez …: changer de Ball. » ; autre description idem | vérifié (16) |
| 17 | POKéDEX / POKéMON sans `msgctxt` START : l'entrée générale (passage de style) s'appliquait. | Texte officiel exact rétabli dans l'entrée générale : POKéDEX, POKéMON (menu START, carte Dresseur, sauvegarde, invite du résumé, mots Easy Chat). | vérifié (17, 36) |
| 18 | Patch FR « Sac », « Fuite ». | « ATTAQUE / SAC / POKéMON / FUITE » | vérifié (18) |
| 26 | Info horloge, CENTRE ᴾᴷᴹᴺ. | Phrase en casse normale (« Centre Pokémon », « Objets Rares du Sac », « menu Options ») ; libellé « CENTRE POKéMON » ; descriptions « Centres Pokémon ». | vérifié (26, 26b) |
| 27 | Le professeur tutoie juste avant. | « Quel défi te / tente? » (et `{COLOR 4}` réécrit `{COLOR RED}`, décision 5) | vérifié (27) |
| 28 | Passage de style dans des libellés en capitales. | ANIMAT. COMBAT, STYLE COMBAT (officiels exacts), SURF AUTO, SOIN RAPIDE, COMBAT RAPIDE, DECORS COMBAT, AIDE FUITE, MUSIQUE SURF ; bandeaux OPTIONS / OPTIONS DE COMBAT ; « L’INFIRMIERE », « VELO » dans les descriptions → « L’infirmière », « Bicyclette ». | vérifié (10, 16, 28, 28b, 28c) |
| 29 | Classe `{PKMN} PROF.` traduite « Prof.{PKMN} ». | « Prof. » → « Prof. Orme » (Pokématos et combat) ; « Nb Dresseurs: » ; boutons du Pokématos « {B_BUTTON}RETOUR ». | vérifié (29) |
| 30 | Le nom de l'espèce est imprimé à part, ligne suivante (`pokedex_plus_hgss.c:7446`) : élision impossible sans code. | « CRI: » / « HERICENDRE » | vérifié (30) |
| 31 | Casse des poches. | SOINS, POKé BALLS, BAIES (OBJETS, CT & CS, OBJ. RARES inchangés) ; menu d'objet « RETOUR » (CANCEL, EXIT → RETOUR, BAG → SAC). | vérifié (31, 31b) |
| 32 | « TOMBE » : `nuzlocke.c` copie le Pokémon K.O. au PC (`CopyMonToPC`) au lieu de le relâcher. | « PC » / « RELACHER » (la description dit « vont au PC… sans retour possible ») | vérifié (32) |
| 33 | `DrawTopBar()` place « SAUVE » à la position calculée pour la largeur de « SUIV. » : un libellé plus long déborde. | « {R_BUTTON}SUIVANT » / « {R_BUTTON}SAUVER » (SAUVER ≤ SUIVANT) ; dernier choix « SAUVER » (officiel exact). | vérifié (33) |
| 35 | `CHAR_DEC_SEPARATOR` (config upstream) et « kg. » écrit par le code. | **Correctif `code/virgule-decimale.patch`** : `CHAR_DEC_SEPARATOR` = `CHAR_COMMA` (réglage prévu par upstream pour les pays hors UK/US ; Pokédex, temps de course à vélo) et suppression du point après « kg ». | vérifié : « 0,5 m », « 7,9 kg » (15) |
| 36 | « NºID / » : le « / » d'Émeraude FR est parasite dans cette mise en page. | « NºID » + espace (carte Dresseur, Panthéon) ; fenêtre de sauvegarde « BADGES », « POKéDEX ». | vérifié (36, 36b) |
| 37 | Casse mixte « DEPLACER Pokémon ». | DEPLACER / DEPOSER / RETIRER POKéMON, STOCKAGE OBJ., METTRE DANS SAC | vérifié (37, 37b) |
| 43 | « PHYSIQUE ou SPECIALE … CAPACITE » en capitales dans une phrase. | « Catégorie physique ou spéciale / selon la capacité. » (et « selon le type du Pokémon ») | vérifié (43) |
| 44 | — | Rien : décision 14 précisée (aucune majuscule accentuée, « A la prochaine! » reste). | — |
| accents | Décision 14. | Déjà fait par l'agent principal dans les .po (GEN. 3, STEREO, RECOMMANDE, DEFIS…) : rien à ajouter. | vérifié (mode, 28c) |

Autres corrections faites au passage, sur les mêmes écrans :
- Glyphe ᴾᴷᴹᴺ → « Pokémon » dans les descriptions des Options et des réglages de partie (65 phrases ; chaque
  ligne mesurée ≤ 198 px pour une fenêtre de 200 px ; 13 phrases raccourcies à la main) et dans les libellés
  POKéMON DEPART, POKéMON SAUV., POKéMON FIXES, CAPA. POKéMON.
- Pokédex EVO : Male, Female, Morning, Evening, Night, « Weather », « Nature » étaient des lignes anglaises de
  SoulSilver (faux alignements) → Mâle, Femelle, Matin, Soir, Nuit, « météo », « (nature) » ; « Atq > Déf »,
  « Att < Déf » incohérents → AT > DF… ; taux de capture « Médium » (classe de Dresseur) → MOYEN, RELAXED →
  ABORDABLE (`msgctxt`, la nature Relax ne change pas).
- `GOLD` (nom proposé au garçon, `src/oak_speech_hns.c`) valait « or » (mot Easy Chat) → `msgctxt` « GOLD ».
- Menu principal « Cadeau MYST. » → CADEAU MYST.

## Ce qui reste (hors périmètre ou non corrigeable par le texte)

- **Carte Dresseur « ₽3000/0 »** : ce n'est pas un défaut de traduction : `trainer_card.c` (`#if IS_HNS`)
  affiche « argent / épargne de Maman » ; l'anglais affiche pareil. Un correctif serait un choix de jeu.
- **Casse mixte dans les noms de données** (lot E / glossaire, non touchés) : environ 400 noms d'objets,
  capacités, talents, lieux, badges en casse mixte après le passage de style : « JOYAU Feu », « Pierre FOUDRE »,
  « Tunnel MERAZON », « Badge PRISME », « EPINE DE Fer », « TOURNOI DE Combat », « POINTS DE Combat » dans les
  dialogues… Liste reproductible avec `build/lot_H/scanner_casse_mixte.py` (msgid tout en capitales, msgstr
  mêlant mots en capitales et mots en minuscules). Même cause que les défauts 26/28/31/37.
- Dialogues (audit global) : « A la prochaine » reste (décision 14) ; `data/maps/FallarborTown/scripts.inc:93`
  « MOVE TUTOR'S HOUSE… » a reçu le texte du Centre Pokémon (faux alignement du patch FR) ;
  `src/data/union_room.h:340` « Oh… A la prochaine alors. » a perdu le `\p` final de l'anglais.
- Pokédex : le glyphe « % » de `CAPT.{0x5B}` s'affiche « × » dans cette police (même chose en anglais).
- Écran de stockage du PC : « EQUIPE ᴾᴷᴹᴺ » (bouton) n'a pas été traité (texte ou image non identifié).

## Propositions pour le glossaire / DECISIONS

- Réglages de partie : LEGER / NORMAL / DUR (Nuzlocke), BADGES (IV/EV progressifs), MAX, PC (K.O. Nuzlocke).
- Stats abrégées partout où la place manque : AT DF AS DS VI (Pokédex) ; ATQ.SP. / DEF.SP. / VIT. (résumé,
  montée de niveau) ; PUIS. (puissance), PRE: (précision, combat).
- Classe `{PKMN} PROF.` = « Prof. » (« Prof. Orme »).
- Groupe d'œufs FIELD = TERRESTRE.
