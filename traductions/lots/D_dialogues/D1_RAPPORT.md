# Lot D1 : dialogues restants de data/text et data/scripts

## Résultat
- **536 / 536 entrées traduites** (toutes celles de `D1_a_traduire.json`, compilées ou non), dans `D1_001.json` (134), `D1_002.json` (135), `D1_003.json` (134), `D1_004.json` (133).
- `D1_verifications.tsv` : **0 problème bloquant** (CODES, KANA, CARACTERE, LONGUEUR, ESPACE, LARGEUR = 0). 8 signalements non bloquants, justifiés plus bas.
- Seules 16 entrées sont compilées (15 de `debug.inc` + `RESEARCH LAB`) ; tout le reste est du code FRLG mort ou des variantes `#else` non HnS.

### Par fichier
| Fichier | Entrées | Compilées | Contenu |
|---|---|---|---|
| data/text/trainers_frlg.inc | 204 | 0 | phrases d’avant-combat des revanches FRLG (Cherche VS) |
| data/text/fame_checker_frlg.inc | 150 | 1 | Mémorydex : fiches, messages finaux, lieux/sources, Journal Pokémon |
| data/text/new_game_intro_frlg.inc | 45 | 0 | intro du Prof. Chen, guide des commandes, noms proposés |
| data/scripts/flavor_text.inc | 27 | 0 | textes d’ambiance FRLG (meubles, panneaux) |
| data/text/trainer_card_frlg.inc | 25 | 0 | imprimante de Carte Dresseur, fillette aux autocollants |
| data/scripts/berry_tree.inc | 16 | 0 | arbres à Baies (mutation, engrais, mauvaises herbes) |
| data/scripts/debug.inc | 15 | 15 | menu de débogage |
| data/scripts/mystery_event_club.inc | 13 | 0 | femme au profil (Club Événement Mystère) |
| data/text/ingame_trade_frlg.inc | 11 | 0 | échanges en jeu FRLG |
| data/scripts/cable_club_frlg.inc | 6 | 0 | Club Câble / sans fil FRLG |
| data/scripts/route23.inc | 5 | 0 | gardes des Badges de la Route 23 |
| data/text/battle_tent.inc | 4 | 0 | fragments `#else` (Tentes de Combat Émeraude) |
| data/text/day_care_frlg.inc | 4 | 0 | Pension FRLG |
| data/scripts/aide.inc | 3 | 0 | assistant du Professeur |
| data/scripts/silphco_doors.inc | 3 | 0 | portes de Sylphe SARL |
| data/text/pc_transfer.inc | 2 | 0 | fragments `#else` (PC d’ANNETTE) |
| pkmn_center_nurse_frlg / pokemon_league / seagallop | 1 + 1 + 1 | 0 | |

### Par source
| Source | Entrées |
|---|---|
| traduction nouvelle | 497 |
| SoulSilver FR officiel (adapté) | 15 (intro du Prof. Chen banque 219, Pension 439:0, panneaux d’Arène, Aldo 525:0) |
| Émeraude FR officiel (adapté) | 15 (Pension, arbres à Baies, Club Câble, PC d’ANNETTE, porte) |
| SoulSilver FR officiel | 6 (boutons A/B banque 219:16, 219:36, noms Nina / Peter / Giovanni) |
| Émeraude FR officiel | 3 (Saut Pokémon, adaptateur sans fil, “Veuillez prendre place…”) |

Le texte officiel d’origine est cité dans `preuve` pour chaque entrée (adapté). Aucune entrée ne vient du patch FR.

## Méthode
- Contexte lu pour chaque entrée dans `build/upstream_orig` : label, script appelant (`data/scripts/trainers_frlg.inc` pour la classe de chaque Dresseur, `data/maps/*_Frlg` pour sa réplique du premier combat, reprise dans la note), interlocuteur, texte suivant pour les fragments.
- Recherche de phrases proches (rapidfuzz, seuil 70-80) dans les quatre .po, dans `tm_ss_pairs.pkl` (sauf banque 802) et `tm_em_bytes.pkl` ; reprise des officiels proches (Pension, intro SS banque 219, panneaux d’Arène SS, berry_tree Émeraude, Club Câble Émeraude).
- Mise en page : reformatage à 198 px, page par page ; pages à sauts manuels, fragments (`\n`/`\p` final) et textes d’une ligne laissés tels quels. Les noms “Prof. X” et “M. X” ne sont jamais coupés en fin de ligne.
- **Bug d’outil signalé** : `Gen3.reformater()` boucle à l’infini quand le texte contient un code avec espace (`{COLOR BLUE}`, `{PAUSE 0x60}`…). `split()` coupe le code et `largeur()` ne trouve plus de `}`, donc `j = -1` et la boucle repart de zéro. Contournement dans mon script : protéger les espaces internes aux codes avant l’appel. À corriger dans `outils/gen3.py` (par exemple, découper les mots en ignorant les espaces entre accolades).

## Décisions de style et de registre
- **Noms Kanto selon SoulSilver FR** : Prof. Chen, Pierre, Ondine, Major Bob, Erika, Koga, Morgane, Auguste, Olga (LORELEI), Aldo (BRUNO, SS 525), Agatha, Peter, Léo (BILL), M. Fuji, Giovanni.
- **DAISY = Nina** (sœur du rival, SoulSilver FR banque 449). Le glossaire n’a que `DAISY = Daisy`, qui vaut pour la Peintre Daisy de FRLG et d’autres Dresseurs : ce n’est pas le même personnage. « DAISY OAK » = « Nina Chen ».
- Noms Hoenn selon Émeraude FR : BASTIEN (BRAWLY), ANNETTE (LANETTE : « PC d’ANNETTE »), AUTEQUIA, VERGAZON, POIVRESSEL.
- **Registre** : tutoiement pour les Dresseurs, enfants, champions, PNJ, l’Hôte de la Pension, les gardes de la Route 23, le Prof. Chen et la femme au profil (comme l’homme au profil d’Émeraude). Vouvoiement pour l’infirmière, l’accueil du Club Câble, l’imprimante, les textes système des arbres à Baies (comme Émeraude) et les deux Mademoiselles distinguées (Jacki, Gillian). Accords au masculin par défaut quand le texte ne varie pas selon le sexe du joueur (comme les officiels Gen 3).
- **Noms des duos de Dresseurs** (Eli & Anne, Jes & Gia, Kiri & Jan, Mya & Ron, Jed, Lia & Luc, Lil & Ian, Kia & Mik, Joy & Meg, Ava & Geb, Miu & Mia, Eve & Jon, Lex & Nya) : noms anglais gardés, en casse SoulSilver (« Eli: … »), car le glossaire a déjà Anne, Ian, Jon et Ron. **À aligner** sur la traduction des noms de `trainers_frlg.party` (vides au .po pour l’instant).
- **Mémorydex (Fame Checker)** : rubriques « Que fait cette personne? », « Quel genre de personne est-ce? », « Famille et amis? », « Pokémon préférés? », « Une rumeur… », « Où est née cette personne? » ; messages finaux « De: X\nÀ: {PLAYER} ». Panneaux d’Arène au format SS « Arène de X\nChampion: Y\lslogan ». Les citations du Mémorydex reprennent des répliques de PNJ des cartes `*_Frlg`, encore non traduites au .po : **à harmoniser** avec le lot qui traduira ces cartes. Les phrases du Journal Pokémon sont déjà identiques entre la fiche et le magazine.
- Sources des fiches en capitales comme celles déjà au .po (VIEILLE DAME, JEUNE HOMME, FILLETTE, PETIT GARÇON, COGNEUR), noms propres en casse SS (Charine, Celio). Lieux en casse SS (« Arène d’Argenta », « Musée d’Argenta », « Centre Commercial », « Arène de Carmin » abrégé).
- Intro FRLG : GARY = REGIS (nom du rival dans l’anime français) ; les autres noms proposés sont conservés.
- Statistiques de débogage : EV/IV + PV, AT, DF, AS, DS, VI ; « Single » = Solo (déjà au .po) donc « Party-wide » = « Toute l’équipe ».

## Termes nouveaux proposés pour le glossaire
| Anglais | Proposition | Origine |
|---|---|---|
| DAISY (Daisy Chen) | Nina | SoulSilver FR (banque 449) ; contexte distinct de DAISY = Daisy |
| LORELEI | Olga | nom FR officiel Gen 1-4 (absent du glossaire) |
| BRUNO | Aldo | SS 525:0 |
| AGATHA / MR. FUJI / KOGA / GIOVANNI | Agatha / M. Fuji / Koga / Giovanni | SS |
| HALL OF FAME | Panthéon | SS (Émeraude au .po : PANTHEON) |
| POKéMON HOUSE (Lavanville) | Bénévolat de Lavanville | SS banque 475 |
| NUGGET BRIDGE | Pont Doré | SS 662:35 |
| CELADON DEPT. STORE | Centre Commercial de Céladopole | SS 491:32 |
| FAME CHECKER | Mémorydex (le .po a MEMORYDEX) | patch FR / FRLG FR |
| POKéMON JOURNAL | Journal Pokémon | glossaire JOURNAL = Journal |
| STICKER | autocollant | traduction nouvelle |
| POKéMON PRINTER | Imprimante Pokémon | traduction nouvelle |
| BIRD BROTHERS | Frères Oiseaux | traduction nouvelle |
| KARATE MASTER | Maître Karaté | traduction nouvelle |
| SPA (Ile 1) | thermes | traduction nouvelle |
| link battle | combat en link | Émeraude FR (COMBATS EN LINK) |
| Mulch / fertilizer | engrais (Fertipousse…) | SS (REPANDRE ENGRAIS) |

## Doutes
- **Noms FRLG sans source officielle disponible** : FOUR ISLAND = « Ile 4 » (forme du .po, tirée du patch), ICEFALL CAVE = « Grotte de Glace », SEAGALLOP HI-SPEED {n} = « Seagallop {n} » (“HI-SPEED” omis), CELIO et CHARINE conservés, CRUSHER = « COGNEUR ». À remplacer si l’on retrouve les noms de Rouge Feu/Vert Feuille FR.
- GARY = REGIS : choix de l’anime, non vérifié dans FRLG FR.
- « mythical POKéMON » (dragons, fiche de Peter) rendu par « légendaires ».
- Les cinq Tentes de Combat (4 fragments `#else`) : majuscules « TENTE DE COMBAT … », comme les entrées sœurs du .po. Le glossaire voudrait « TENTE DE Combat » (passage automatique au style), d’où 3 signalements GLOSSAIRE que je laisse.

## Signalements non bloquants du vérificateur
- ANGLAIS ×5 (JUNE, MOMO, NORIE, SAI, TOSH) : noms proposés par l’intro FRLG, conservés comme les autres.
- GLOSSAIRE ×3 : « TENTE DE COMBAT D’AUTEQUIA / DE VERGAZON / DE POIVRESSEL », gardés pour la cohérence avec « À la TENTE DE COMBAT ARÈNE,\n » déjà au .po (voir ci-dessus).
- Le vérificateur ne lit pas la source des lots JSON : `com` vaut le champ `source` sans le préfixe « source : ». La tolérance de 216 px pour les textes officiels ne s’applique donc jamais aux lots. Toutes mes lignes tiennent malgré tout dans 198 px, ou dans la largeur de l’anglais quand elle est plus grande.

## Anomalies remarquées dans les .po (hors périmètre, non modifiées)
- `battle_tent.inc` : « Do you wish to take the PALACE\n » = « Voulez-vous relever le défi de la\n », suivi de « défi de la TENTE DE COMBAT? ». Le texte affiché dit donc « le défi de la défi de la… ». J’ai évité ce doublon dans l’entrée VERDANTURF.
- `pc_transfer.inc` : « BILL'S PC.\p » = « PC DE LEO » a perdu son `\p` final et ne suit pas le préfixe « … a été transféré dans\n ». « BILL'S PC was full.\p » = « Le PC de Léo était plein.\p » ne s’enchaîne pas avec « la Boîte “{STR_VAR_3}” du\n ». Mes entrées LANETTE donnent « le PC d’ANNETTE.\p » et « PC d’ANNETTE était pleine.\p ».
- `fame_checker_frlg.inc` : les libellés seuls « KOGA » = « KOGA » et « LANCE » = « PETER » sont en capitales, alors que mes en-têtes de messages finaux sont en casse SS (Koga, Peter) : à harmoniser. « AGATHA » et « LORELEI » (lignes 1101 et 1251) sont encore vides au .po.
- Plusieurs fragments du patch dans `battle_tent.inc` commencent au milieu d’un mot (« rganisons… », « ègle… ») : problème FRAGMENT connu du patch.
