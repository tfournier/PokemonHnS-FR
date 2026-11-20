# Lot D4 : dialogues des cartes FRLG des îles Sevii

## Résultat
- Décision 14 appliquée : aucune majuscule accentuée (Ile, Iles Sevii, Entree, Vallee, Etage…) dans les 669 msgstr ; les noms Poképédia (Île, Îles, Écume…) sont écrits sans accent sur la majuscule.
- **669 / 669 entrées traduites** (toutes celles de `D4_a_traduire.json`, 68 cartes `*_Frlg`, aucune compilée dans HnS), réparties dans `D4_001.json` (134), `D4_002.json` (134), `D4_003.json` (133), `D4_004.json` (134), `D4_005.json` (134), par ordre fichier/ligne.
- `D4_verifications.tsv` : **0 problème** (aucun bloquant : CODES, KANA, CARACTERE, LONGUEUR, ESPACE, LARGEUR = 0 ; GLOSSAIRE = 0 après passage à « Œuf », « Pokémon Insecte/Glace », « type Psy » et panneaux en casse SS).
- `D4_douteux.json` : 21 entrées **déjà traduites dans les paquets** mais à relire (noms ou devises dont la forme exacte du jeu FR n’a pas pu être vérifiée). Ce fichier n’est pas un lot à intégrer : il liste msgid, msgstr proposé et raison.
- Source : **traduction nouvelle** pour les 669 entrées. Aucune réplique Emeraude FR / SoulSilver FR proche (rapidfuzz ≥ 82 sur `tm_em_bytes.pkl`, ≥ 85 sur `tm_ss_pairs.pkl` hors banque 802 : aucune correspondance de sens). 146 entrées ont un champ `preuve` qui cite la source Poképédia des noms officiels qu’elles contiennent.

## Méthode
- Contexte lu pour chaque entrée dans `build/upstream_orig/data/maps/<carte>/scripts.inc` (label = interlocuteur et situation : intro/défaite/après-combat, panneau, PNJ). La note de chaque entrée donne la carte, le label, la situation et le registre.
- Recherche de phrases proches (rapidfuzz ≥ 78) dans les quatre .po : reprise et harmonisation avec les **revanches** de `trainers_frlg.inc` (lot D1 : Miu/Mia, Eve/Jon, Lex/Nya, Ava, Kia, Daryl…) et avec les **fiches du Mémorydex** (lot D1) qui citent mot pour mot des répliques de ces cartes (Giovanni roux, Aldo, Olga, Léo/ABRA, Doublonville, Agatha, Nina…).
- Deux entrées du Maniaque des Capacités calquées sur les entrées voisines du .po (patch FR, sens vérifié ; « attaque » → « capacité »).
- Mise en page : `Gen3.reformater(…, 198)` page par page ; les pages à sauts manuels (« … …  … … » , panneaux, Machine Réseau) gardent leurs sauts si elles tiennent en 198 px ; les textes d’une ligne en anglais restent d’une ligne (raccourcis si besoin) ; aucun fragment `\n`/`\p` dans ce lot.

## Chiffres par carte
| Carte | Entrées | Paquet |
|---|---|---|
| FiveIsland_Frlg | 3 | D4_001 |
| FiveIsland_House1_Frlg | 1 | D4_001 |
| FiveIsland_House2_Frlg | 1 | D4_001 |
| FiveIsland_LostCave_Room10_Frlg | 3 | D4_001 |
| FiveIsland_LostCave_Room1_Frlg | 3 | D4_001 |
| FiveIsland_LostCave_Room4_Frlg | 3 | D4_001 |
| FiveIsland_Meadow_Frlg | 12 | D4_001 |
| FiveIsland_MemorialPillar_Frlg | 20 | D4_001 |
| FiveIsland_PokemonCenter_1F_Frlg | 2 | D4_001 |
| FiveIsland_ResortGorgeous_Frlg | 23 | D4_001 |
| FiveIsland_ResortGorgeous_House_Frlg | 11 | D4_001 |
| FiveIsland_RocketWarehouse_Frlg | 23 | D4_001 |
| FiveIsland_WaterLabyrinth_Frlg | 10 | D4_001 |
| FourIsland_Frlg | 7 | D4_001 |
| FourIsland_House1_Frlg | 1 | D4_001 |
| FourIsland_IcefallCave_Back_Frlg | 10 | D4_001 |
| FourIsland_LoreleisHouse_Frlg | 4 | D4_001, D4_002 |
| FourIsland_Mart_Frlg | 2 | D4_002 |
| FourIsland_PokemonCenter_1F_Frlg | 7 | D4_002 |
| MtEmber_Exterior_Frlg | 26 | D4_002 |
| MtEmber_RubyPath_B3F_Frlg | 1 | D4_002 |
| OneIsland_Frlg | 8 | D4_002 |
| OneIsland_House1_Frlg | 2 | D4_002 |
| OneIsland_House2_Frlg | 1 | D4_002 |
| OneIsland_KindleRoad_EmberSpa_Frlg | 8 | D4_002 |
| OneIsland_KindleRoad_Frlg | 41 | D4_002 |
| OneIsland_PokemonCenter_1F_Frlg | 59 | D4_002, D4_003 |
| OneIsland_TreasureBeach_Frlg | 4 | D4_003 |
| SevenIsland_Frlg | 7 | D4_003 |
| SevenIsland_House_Room1_Frlg | 10 | D4_003 |
| SevenIsland_Mart_Frlg | 3 | D4_003 |
| SevenIsland_PokemonCenter_1F_Frlg | 3 | D4_003 |
| SevenIsland_SevaultCanyon_Entrance_Frlg | 21 | D4_003 |
| SevenIsland_SevaultCanyon_Frlg | 28 | D4_003 |
| SevenIsland_SevaultCanyon_House_Frlg | 6 | D4_003 |
| SevenIsland_SevaultCanyon_TanobyKey_Frlg | 1 | D4_003 |
| SevenIsland_TanobyRuins_Frlg | 12 | D4_003 |
| SevenIsland_TrainerTower_Frlg | 8 | D4_003 |
| SixIsland_DottedHole_SapphireRoom_Frlg | 3 | D4_003 |
| SixIsland_Frlg | 3 | D4_003 |
| SixIsland_GreenPath_Frlg | 5 | D4_004 |
| SixIsland_House_Frlg | 1 | D4_004 |
| SixIsland_Mart_Frlg | 2 | D4_004 |
| SixIsland_OutcastIsland_Frlg | 19 | D4_004 |
| SixIsland_PatternBush_Frlg | 35 | D4_004 |
| SixIsland_PokemonCenter_1F_Frlg | 3 | D4_004 |
| SixIsland_RuinValley_Frlg | 19 | D4_004 |
| SixIsland_WaterPath_Frlg | 24 | D4_004 |
| SixIsland_WaterPath_House1_Frlg | 9 | D4_004 |
| SixIsland_WaterPath_House2_Frlg | 1 | D4_004 |
| ThreeIsland_BerryForest_Frlg | 7 | D4_004 |
| ThreeIsland_BondBridge_Frlg | 25 | D4_004, D4_005 |
| ThreeIsland_DunsparceTunnel_Frlg | 3 | D4_005 |
| ThreeIsland_Frlg | 31 | D4_005 |
| ThreeIsland_House1_Frlg | 2 | D4_005 |
| ThreeIsland_House2_Frlg | 2 | D4_005 |
| ThreeIsland_House3_Frlg | 1 | D4_005 |
| ThreeIsland_House4_Frlg | 2 | D4_005 |
| ThreeIsland_House5_Frlg | 2 | D4_005 |
| ThreeIsland_Mart_Frlg | 3 | D4_005 |
| ThreeIsland_PokemonCenter_1F_Frlg | 3 | D4_005 |
| ThreeIsland_Port_Frlg | 5 | D4_005 |
| TrainerTower_Lobby_Frlg | 14 | D4_005 |
| TwoIsland_CapeBrink_House_Frlg | 9 | D4_005 |
| TwoIsland_Frlg | 13 | D4_005 |
| TwoIsland_House_Frlg | 8 | D4_005 |
| TwoIsland_JoyfulGameCorner_Frlg | 18 | D4_005 |
| TwoIsland_PokemonCenter_1F_Frlg | 2 | D4_005 |
## Noms officiels FRLG relevés (anglais → français, à ajouter au glossaire)
| Anglais | Français | Type | Source |
|---|---|---|---|
| SEVII ISLANDS | Iles Sevii (Poképédia : Îles Sevii ; majuscule sans accent, décision 14) | lieu | pokepedia.fr/Îles_Sevii |
| ONE … SEVEN ISLAND | Ile 1 … Ile 7 | lieu | pokepedia.fr/Îles_Sevii (le .po a « ILE 1 »… venant du patch : à corriger en « Ile 1 »…) |
| KINDLE ROAD | Route Tison | lieu | pokepedia.fr/Île_1 |
| MT. EMBER | Mont Braise | lieu | pokepedia.fr/Île_1 |
| EMBER SPA | Source Braise | lieu | pokepedia.fr/Route_Tison |
| TREASURE BEACH | Plage Trésor | lieu | pokepedia.fr/Île_1 |
| CAPE BRINK | Cap Falaise | lieu | pokepedia.fr/Îles_Sevii |
| JOYFUL GAME CORNER | Salle de Jeu | lieu | pokepedia.fr/Île_2 |
| THREE ISLE PORT / PATH | Port Ile 3 / Chemin Ile 3 | lieu | pokepedia.fr/Île_3 |
| BOND BRIDGE | Pont du Lien | lieu | pokepedia.fr/Île_3 |
| BERRY FOREST | Bois Baies | lieu | pokepedia.fr/Île_3 |
| ICEFALL CAVE | Grotte de Glace | lieu | pokepedia.fr/Île_4 (**confirme** la forme provisoire du lot D1) |
| LORELEI'S HOUSE | Maison d’Olga | lieu | (Olga = LORELEI, SS FR) |
| FIVE ISLE MEADOW | Pré (Pré Ile 5) | lieu | pokepedia.fr/Île_5, Mémorial |
| ROCKET WAREHOUSE | Entrepôt Rocket | lieu | pokepedia.fr/Entrepôt_Rocket |
| MEMORIAL PILLAR | Mémorial | lieu | pokepedia.fr/Mémorial |
| WATER LABYRINTH | Labyrinthe d’O | lieu | pokepedia.fr/Île_5 |
| RESORT GORGEOUS | Camp de Vacances | lieu | pokepedia.fr/Camp_de_Vacances |
| LOST CAVE | Grotte Perdue | lieu | pokepedia.fr/Grotte_Perdue |
| WATER PATH | Agualcanal | lieu | pokepedia.fr/Agualcanal |
| GREEN PATH | Chemin Vert | lieu | pokepedia.fr/Île_6 |
| PATTERN BUSH | Forbuissons | lieu | pokepedia.fr/Île_6 |
| OUTCAST ISLAND | Ile du Lointain | lieu | pokepedia.fr/Île_6 |
| RUIN VALLEY | Vallée Ruine | lieu | pokepedia.fr/Île_6 |
| DOTTED HOLE | Trou Percé | lieu | pokepedia.fr/Île_6 |
| ALTERING CAVE | Grotte Métamo | lieu | pokepedia.fr/Île_6 (le .po a « Grotte METAMO », Emeraude FR) |
| SEVAULT CANYON / CANYON ENTRANCE | Canyon Sesor / Entrée Canyon | lieu | pokepedia.fr/Île_7 |
| TANOBY RUINS / CHAMBERS / KEY | Ruines Tanoby / Chambres Tanoby / Clé Tanoby | lieu | pokepedia.fr/Île_7, Ruines_Tanoby |
| TRAINER TOWER | Tour Dresseurs | lieu | pokepedia.fr/Île_7 |
| POKéMON NET CENTER | Centre Réseau Pokémon | lieu | pokepedia.fr/Ciléo |
| CELIO | **Ciléo** | personnage | pokepedia.fr/Ciléo (« Nom anglais : Celio ») — **corrige** « Celio » du lot D1 |
| LOSTELLE | Lostelle | personnage | pokepedia.fr/Bois_Baies, Météorite_(Hoenn) |
| SELPHY | **Themis** | personnage | pokepedia.fr/Camp_de_Vacances (« Mademoiselle Themis ») |
| SEBASTIAN | Sebastian | personnage | pokepedia.fr/Camp_de_Vacances |
| TECTONIX | Tectonix | surnom (ONIX) | pokepedia.fr/Mémorial |
| GIDEON | Gédéon (Poképédia écrit « Gedeon ») | personnage | pokepedia.fr/Entrepôt_Rocket (nom absent des textes D4) |
| CLIFFORD (Gentleman, Tanoby) | Xavier | Dresseur | pokepedia.fr/Ruines_Tanoby |
| GILLIAN (Mademoiselle, Camp) | Reine | Dresseuse | pokepedia.fr/Camp_de_Vacances (Wattouat/Lainergie) |
| KANTO RIDER FEDERATION (motards de l’Ile 3) | Kanto Angels | groupe | pokepedia.fr/Île_3_(ville) (réplique exacte non vérifiée) |
| RUBY / SAPPHIRE | Rubis / Saphir | objet | pokepedia.fr/Rubis_(objet) |
| TRI-PASS | Tri-Passe | objet | pokepedia.fr/Tri-Passe (le .po a « TRI-PASSE », patch : casse à revoir) |
| RAINBOW PASS | Passe Prisme | objet | pokepedia.fr/Passe_Prisme |
| BERRY POUCH | Sac à Baies | objet | pokepedia.fr/Sac_à_Baies (le .po a « Sac A Baies », patch) |
| METEORITE | Météorite | objet | pokepedia.fr/Météorite_(Hoenn) (le .po a « METEORITE ») |
| LEMONADE | Limonade | objet | .po (SS) et pokepedia.fr/Mémorial |
| Mots de passe de l’Entrepôt (GOLDEEN need log / Yes, nah, CHANSEY) | “Ici GIRAFARIG ici.” / “TARSAL la star.” | texte | pokepedia.fr/Entrepôt_Rocket, Mont_Braise (palindromes FR ; ponctuation exacte non vérifiée) |
| Devises des îles (panneaux) | Ile 1 « Les amis se réunissent ici », Ile 2 « Le bonheur à deux », Ile 3 « L’île où on se sent chez soi », Ile 4 « La chaleureuse île glacée », Ile 5 « L’île où le temps s’écoule comme une rivière », Ile 6 « L’île de la sagesse », Ile 7 « L’île de l’infinité » | panneau | sous-titres des pages Poképédia de chaque île (texte exact des panneaux non vérifié) |

### Traductions nouvelles (aucun nom officiel trouvé)
| Anglais | Proposition |
|---|---|
| Network Machine | Machine Réseau |
| SIX ISLE PORT | port de l’Ile 6 (déjà au .po pour la revanche de Mymo) |
| POKéMON MOVE MANIAC | Maniaque des Capacités |
| TIME ATTACK / Time Board / OWNER (Tour Dresseurs) | Contre-la-Montre / Tableau des Temps / Propriétaire |
| BIRD BROTHERS | Frères Oiseaux (comme D1) |
| Skip & Chomp! (enseigne) | Sautez et croquez! |
| Butler / Lady SELPHY | Majordome / Mademoiselle Themis |

## Corrections à reporter (formes provisoires du lot D1 et du .po)
- **« Ile 4 »** du lot D1 est la bonne graphie (décision 14 : aucune majuscule accentuée ; nom officiel « Île 4 » sur Poképédia). Seule la casse de « ILE 1 »… « ILE 7 », « ILES SEVII » de `donnees.po` (patch) est à ramener à « Ile 1 »… « Iles Sevii » en dialogue.
- **ICEFALL CAVE = « Grotte de Glace »** : forme officielle, confirmée.
- **CELIO = « Ciléo »** (et non « Celio ») : à corriger dans `dialogues.po` (entrée « CELIO » du Mémorydex, lot D1) et dans les fiches qui le citent.
- **CHARINE** : hors de mon périmètre (source du Mémorydex pour Koga) ; aucune forme officielle trouvée, « Charine » reste provisoire.
- Fiche du Mémorydex « BRUNO… visits the SPA » : D1 a « aux thermes » ; la carte D4 dit « à la Source Braise » (nom officiel). A aligner.
- GILLIAN → Reine et CLIFFORD → Xavier : à reporter dans les noms de `trainers_frlg.party` quand ils seront traduits.

## Décisions de registre
- **Vouvoiement** : Themis et son majordome (« Mademoiselle »), les Mademoiselles et le Gentleman du Camp de Vacances (Jacki, Toby), l’accueil et le Propriétaire de la Tour Dresseurs, le commerçant de l’Ile 2 (avec {PLAYER}), le marin de la Flèche des Mers, les panneaux, les textes système (« Vous obtenez le Tri-Passe! »). Le chef des motards vouvoie les habitants (« Retournez à Kanto ») et inversement.
- **Tutoiement** : Dresseurs, enfants, Sbires Rocket (familiers : « T’es venu ici… »), Olga (avec {PLAYER}), Ciléo et Léo, le rival, les PNJ des îles, le vieil homme de la pièce cachée, la vieille dame du Cap Falaise (accords au féminin : « je me suis trompée »).
- Duos : noms gardés en casse SS (Kia, Mik, Eve, Jon, Lex, Nya, Ava, Geb, Miu, Mia, Joy, Meg), comme au lot D1 ; Poképédia donne « Miu & Mia » à l’identique.
- Kanto / Hoenn en casse SS (« Kanto », comme les entrées SoulSilver FR du .po) ; ANNETTE et BASTIEN en capitales Emeraude FR ; espèces en capitales (LOKHLASS, LEVEINARD, SCARHINO, ONIX, DODUO, GIRAFARIG, TARSAL) ; « Pokédex NATIONAL » comme la majorité du .po.
- « Rage Candybars » = Bonbons Rage ; FULL RESTORE = Guérison ; TOWN MAP = Carte ; RUNNING SHOES = Chaussures de Sport ; MAIL = LETTRE ; BODY SLAM = Plaquage ; SWORDS DANCE = Danse-Lames ; ICE BEAM = Laser Glace ; HASTY = Pressé ; TINYMUSHROOM / BIG MUSHROOM = Petit Champi / Gros Champi (formes du .po).
- Mesures : les tailles de SCARHINO restent en pouces ({STR_VAR_2}/{STR_VAR_3} calculés en pouces par le code) ; la taille écrite en clair (67.0 inches) est convertie (1,70 m).
- Jeux de mots recréés : « appeal / peel / bell » → « charme / chaume / carme » ; comptine du fan de SCARHINO ; mots de passe palindromes officiels FR.

## Doutes (voir `D4_douteux.json`, 21 entrées)
- Devises des sept îles : reprises des sous-titres Poképédia, texte exact des panneaux non vérifié.
- Mots de passe (« Ici GIRAFARIG ici. » / « TARSAL la star. ») : formes officielles d’après Poképédia, ponctuation et attribution à vérifier.
- « Kanto Angels » pour KANTO RIDER FEDERATION.
- Machine Réseau, port de l’Ile 6, Maniaque des Capacités, termes de la Tour Dresseurs, enseigne de la Salle de Jeu, slogan de la Source Braise : traductions nouvelles.
- Reine (GILLIAN) et Xavier (CLIFFORD) : noms officiels, mais à aligner avec la table des Dresseurs.
