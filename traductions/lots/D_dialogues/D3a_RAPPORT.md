# Lot D3a : dialogues des cartes FRLG (Céladopole → Route 13)

## Résultat
- **682 / 682 entrées traduites** (toutes celles de `D3a_a_traduire.json`), dans `D3a_001.json` (137), `D3a_002.json` (137), `D3a_003.json` (137), `D3a_004.json` (137), `D3a_005.json` (134), classées par carte puis par ligne.
- `D3a_verifications.tsv` : **0 problème bloquant** (CODES, KANA, CARACTERE, LONGUEUR, ESPACE, LARGEUR = 0). Un seul signalement non bloquant (GLOSSAIRE « COIN ECHANGE », voir Doutes).
- `D3a_douteux.json` : 10 entrées traduites mais à arbitrer (noms sans source officielle, graphies).
- Toutes les cartes `*_Frlg` sont non compilées dans HnS : chaque note se termine par `[non compilé]`.

### Par carte
| Groupe | Entrées | Détail |
|---|---|---|
| Céladopole | 175 | ville 18, Résidence (Condominiums) 1F 5 / 2F 1 / 3F 8 / toit 1 / salle du toit 7, Centre Commercial 1F 3 / 2F 4 / 3F 15 / 4F 3 / 5F 3 / toit 19, Casino 35, Boutique des Lots 6, Arène 29, Hôtel 4, Maison 1 3, Centre Pokémon 3, Restaurant 8 |
| Cramois’Ile | 81 | île 11, Arène 40, Boutique 2, Centre Pokémon 6, Laboratoire : entrée 6 / salle d’expériences 12 / salon 1 / salle de recherche 3 |
| Parmanie | 90 | ville 21, Arène 27, Maisons 3 + 6 + 3, Boutique 2, Centre Pokémon 3, Parc Safari : entrée 10 / bureau 4, Maison du Gardien 11 |
| Plateau Indigo | 5 | Centre Pokémon 5 |
| Lavanville | 31 | ville 8, Maison 1 3, Boutique 3, Centre Pokémon 3, Bénévolat 14 |
| Ligue Pokémon | 23 | Olga 4, Aldo 2, Agatha 4, Peter 4, salle du Maître 8, Panthéon 1 |
| Manoir Pokémon | 27 | 1F 5, 2F 8, 3F 7, B1F 7 |
| Tour Pokémon | 62 | 1F 6, 2F 4, 3F 9, 4F 8, 5F 14, 6F 12, 7F 9 |
| Grotte (Rock Tunnel) | 44 | 1F 20, B1F 24 |
| Repaire Rocket | 33 | B1F 14, B2F 2, B3F 6, B4F 10, ascenseur 1 |
| Route 10 | 26 | route 19, Centre Pokémon 7 |
| Route 12 | 54 | route 35, Maison du pêcheur 13, poste nord 1F 1 / 2F 5 |
| Route 13 | 31 | route 31 |

### Par source
| Source | Entrées |
|---|---|
| traduction nouvelle | 676 |
| SoulSilver FR officiel (adapté) | 5 (défaite d’Erika 492:1, panneau 2F du Centre Commercial 495:2, « Aiyah! » 728:563, « Quoi? Perdu? » 728:1208, « Impossible... ») |
| Émeraude FR officiel (adapté) | 1 (« As-tu visité le PARC SAFARI? » → Jeu Safari) |

Le texte officiel d’origine est dans `preuve` pour chaque entrée « (adapté) ». Aucune entrée ne vient du patch FR. Les traductions proches au .po des cartes HnS de Kanto (Résidence Céladon 3F, Centre Commercial, Effaceur de Capacités, panneaux de villes) viennent toutes du patch FR ou d’une traduction manuelle : je ne les ai pas reprises telles quelles (casse, sens ou anglais différents), mais j’en ai gardé le vocabulaire quand il était correct (« La ville aux rêves arc-en-ciel », « La noble ville pourpre », « Admirez! C’est le rose passion! », « Le programme du jeu… un bug! »).

## Méthode
- Pour chaque entrée : label et script appelant lus dans `build/upstream_orig/data/maps/*_Frlg/scripts.inc` et `data/scripts/trainers_frlg.inc` (classe et rôle du Dresseur : intro / défaite / après-combat, panneau, PNJ, message système). L’interlocuteur et le registre sont repris dans `note`.
- Recherche rapidfuzz (seuil 72, revue à partir de 78) dans les quatre .po, dans `tm_ss_pairs.pkl` (sans la banque 802) et dans `tm_em_bytes.pkl`.
- **Harmonisation avec le lot D1** : 28 répliques sont citées dans les fiches du Mémorydex (`fame_checker_frlg.inc`, traduites en D1). J’ai repris mot pour mot la traduction D1 du passage cité (Auguste, Erika, Koga, Aldo, Agatha, Olga, Peter, Giovanni, M. Fuji, Léo, Nina…), éventuellement rewrappée. Les deux répliques de revanche de D1 (Pokémaniac Mark, Rockeur Luca) restent alignées sur mes intros.
- Mise en page : `Gen3.reformater(texte, 198)` page par page ; panneaux, statues, lignes de deux phrases et messages d’objet à sauts de ligne manuels. Aucune ligne au-delà de 198 px. Les codes `{PLAY_BGM …}`, `{FONT_NORMAL}`, `{STR_VAR_n}`, `{PLAYER}`, `{RIVAL}` sont conservés tels quels.
- 5 répliques d’une seule ligne en anglais (msgbox de dialogue) passent sur deux lignes en français faute de place (#260 Boutique des Lots, intros/après-combat de Lucas, Ashton, Susie, Lola). Ce sont des boîtes de dialogue, pas des libellés de menu.

## Noms officiels relevés
| Anglais | Français retenu | Source |
|---|---|---|
| SILPH SCOPE | Scope Sylphe | Poképédia, page « Scope Sylphe » (le .po a SCOPE SYLPHE, patch) |
| LIFT KEY | Clé Ascenseur | Poképédia, page « Clé Ascenseur (Kanto) » (le .po a CLE ASCENSEUR, patch) |
| GOLD TEETH | Dentier en Or | Poképédia, page « Dentier en Or » (le .po a DENTIER EN OR, patch) |
| ONE ISLAND | Île 1 | Poképédia, page « Île 1 » (confirme la forme « Ile 4 » de D1) |
| TRI-PASS | Tri-Passe | Poképédia, page « Tri-Passe » |
| CELIO | **Ciléo** | Poképédia, page « Tri-Passe » (D1 avait gardé « Celio » : à corriger dans `fame_checker_frlg.inc` et le glossaire) |
| ROCKET HIDEOUT | Repaire Rocket | SS banque 279 + Poképédia « Repaire Rocket » |
| CELADON MANSION | Résidence Céladon | SS banques 491, 507 |
| POKéMON MANSION | Manoir Pokémon | SS 279, glossaire |
| POKéMON HOUSE (M. Fuji) | Bénévolat de Lavanville | SS 475 |
| GAME CORNER | Casino (« Casino Rocket ») | SS 279, glossaire |
| CELADON DEPT. STORE | Centre Commercial de Céladopole | SS 494 |
| TRAINER'S MARKET | Marché du Dresseur | SS 495:2 |
| ROCK TUNNEL | Grotte | SS 279, CONSIGNES_FRLG |
| Badges | Badge Prisme, Badge Âme, Badge Volcan | SS 492 (Prisme), banque des Badges (« Ame », « Volcan ») |
| COIN(S) / COIN CASE | Jetons / Boîte Jetons | SS, .po |
| POKé FLUTE, EVERSTONE, GOOD/SUPER ROD | Pokéflûte, Pierre Stase, Super Canne / Méga Canne | donnees.po (SS) |
| SOFTBOILED, COUNTER, METRONOME, SUBSTITUTE, TOXIC, RETURN, GIGA DRAIN, FIRE BLAST… | E-Coque, Riposte, Métronome, Clonage, Toxik, Retour, Giga-Sangsue, Déflagration… | donnees.po (SS) |
| Personnages | Erika, Koga, Auguste, Olga, Aldo, Agatha, Peter, Giovanni, Léo, M. Fuji, Nina, Prof. Chen | SS, CONSIGNES_FRLG |

## Décisions de registre et de style
- **Vouvoiement** : personnel du Casino et de la Boutique des Lots, accueil du Parc Safari, réceptionniste du Plateau Indigo, panneaux publicitaires (« Échangez vos Jetons… », « Rendez l’invisible visible! »), message de la zone purifiée de la Tour Pokémon (« Vous entrez… », comme les messages système officiels).
- **Tutoiement** : Dresseurs, Champions d’Arène (Erika comprise, comme SS 492), Conseil 4, rival, Prof. Chen, Léo, M. Fuji, le Gardien, les frères du Maître Pêcheur, les guides d’Arène, enfants et PNJ. Les Sbires Rocket tutoient et rudoient (« morveux », « gamin »).
- Le Gardien du Parc Safari sans son dentier parle en « f » (« F’ai ferfu fes fents fans fe Farc Fafari ») ; le docteur du Laboratoire parle un français approximatif (« Moi être docteur important ») pour garder le décalage de l’anglais.
- Statues d’Arène : « Arène Pokémon de X\nChampion(ne): Y\pVainqueurs:\n{RIVAL} » ; panneaux de ville sur deux lignes, nom + slogan.
- Étages du Centre Commercial à la française : RDC, 1{SUPER_ER}, 2{SUPER_E}… (l’anglais 2F = 1{SUPER_ER}), comme SS 495:2.
- « Smell ya later! » = « Allez, à la revoyure! ». « LANCE the dragon TRAINER » = « Peter, le Dresseur de dragons ». « POKéMON LEAGUE CHAMPION » = « Maître de la Ligue Pokémon » ; « HALL OF FAME » = « Panthéon » (décision D1).
- Accord au masculin par défaut ; les deux variantes sexuées de l’anglais (Tour Pokémon 1F « son / girl », Gardien « son / lassie ») sont accordées.

## Termes nouveaux proposés pour le glossaire
| Anglais | Proposition |
|---|---|
| CELIO | Ciléo (officiel FRLG FR) |
| GOLD TEETH | Dentier en Or (casse SS du nom officiel) |
| LIFT KEY | Clé Ascenseur |
| SILPH SCOPE | Scope Sylphe |
| CELADON MANSION | Résidence Céladon |
| SAFARI GAME | Jeu Safari |
| SAFARI ZONE WARDEN | Gardien (du Parc Safari) |
| FISHING GURU | Maître Pêcheur |
| CHANNELER | Exorciste (classe déjà traduite ailleurs ? à vérifier) |
| PRIZE EXCHANGE / PRIZE ROOM | Boutique des Lots |
| TRAINER TIPS | Conseil aux Dresseurs |
| SOULBADGE / VOLCANOBADGE | Badge Âme / Badge Volcan |

## Doutes (détail dans `D3a_douteux.json`)
- **Cramois’Ile ou Cramois’Île** : CONSIGNES_FRLG écrit « Cramois’Île », mais le glossaire, les .po et SS (banque 279) ont « Cramois’Ile ». J’ai suivi le glossaire ; à harmoniser avec D2, D3b, D4. Même question pour « Badge Âme » (SS : « Ame »).
- FISHING GURU, WARDEN, noms d’étages et rayons du Centre Commercial : pas de nom officiel FRLG FR trouvé.
- TOMBSTONY (fausse capacité du quiz d’Auguste) = « Tomberoche ».
- « inches » = « pouces » (valeur calculée par le code, non convertie).
- Signalement GLOSSAIRE non bloquant : « COIN ECHANGE » laissé en capitales, comme COIN DIRECT / SALLE UNION / COLISEE déjà au .po.

## Anomalies remarquées hors périmètre (non modifiées)
- Les entrées du .po des cartes HnS de Kanto (Céladopole, Cramois’Ile, Lavanville, Parmanie) viennent du patch : « Arène Pokémon DE Céladopole\nCHAMPIONNE: Erika », « MARCHE DES Dresseurs », « MANOIR Céladopole: SUITE DU GERANT » (CELADON MANSION est la Résidence Céladon), « 1ER / 2E… » pour les étages. À relire.
- `donnees.po` garde les noms du patch en capitales pour SCOPE SYLPHE, CLE ASCENSEUR, DENTIER EN OR, TRI-PASSE, THE : à passer en casse SS (Scope Sylphe, Clé Ascenseur, Dentier en Or, Tri-Passe, Thé).
