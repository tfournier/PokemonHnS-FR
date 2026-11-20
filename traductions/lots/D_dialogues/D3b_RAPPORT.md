# Lot D3b : dialogues des cartes FRLG non compilées (Kanto, 3e partie)

## Résultat
- **629 / 629 entrées traduites** (toutes celles de `D3b_a_traduire.json`, 629 msgid distincts), réparties dans `D3b_001.json` à `D3b_004.json` (126 chacun) et `D3b_005.json` (125). Ordre : celui de `D3b_a_traduire.json`.
- `D3b_verifications.tsv` : **0 problème bloquant** (CODES, KANA, CARACTERE, LONGUEUR, ESPACE, LARGEUR = 0). Il reste 1 signalement GLOSSAIRE, voulu : « VIVE LA TEAM ROCKET! » est en capitales comme le cri de l’anglais (« TEAM ROCKET RULES! », Route 15, Motard Ernest).
- `D3b_douteux.json` : 13 entrées à confirmer. Elles figurent **aussi** dans les fichiers principaux, avec la traduction proposée. Le fichier sert seulement de liste de relecture : ne pas l’intégrer.
- Toutes les entrées sont du code FRLG mort (cartes `*_Frlg`). Chaque note porte la mention `[non compilé]`.

### Par source
| Source | Entrées |
|---|---|
| traduction nouvelle | 608 |
| SoulSilver FR officiel (adapté) | 19 |
| SoulSilver FR officiel | 1 (panneau de la Route 9, SS 340:0) |
| Émeraude FR officiel (adapté) | 1 (« Hein?\nJ’ai perdu? ») |

Les textes SS repris :
- panneaux de route au format SS (« Route 18\nEst: Parmanie », « Route 9\nAzuria - Grotte ») ;
- Piste Cyclable (354:0) ;
- panneau de Safrania (529:10) et Maison de M. Psy (529:14) ;
- produit Sylphe (537:2) et accueil Sylphe (537:0) ;
- Copieuse et son père (540:0, 541:0/2/9) ;
- M. Psy (534:0, 534:1) ;
- Kinésiste de l’Arène (728:371) ;
- « Tu n’as plus de place » (550:22, 627:3).

Le texte d’origine est cité dans `preuve`. Rien ne vient du patch FR.

### Par carte
| Carte | Entrées | Sources |
|---|---|---|
| Route7 | 1 | SS adapté 1 (panneau du Souterrain) |
| Route8 | 41 | nouv. 41 |
| Route9 | 27 | nouv. 26, SS 1 |
| Route14 | 37 | nouv. 36, SS adapté 1 |
| Route15 (+ WestEntrance 1F/2F) | 37 + 1 + 3 | nouv. 40, SS adapté 1 |
| Route16 (+ House, NorthEntrance 1F/2F) | 26 + 5 + 4 + 7 | nouv. 39, SS adapté 3 |
| Route17 | 34 | nouv. 33, SS adapté 1 |
| Route18 (+ EastEntrance 1F/2F) | 10 + 2 + 2 | nouv. 13, SS adapté 1 |
| Route19 | 37 | nouv. 37 |
| SafariZone (Center, East, North, West, maisons de repos, SecretHouse) | 26 | nouv. 26 |
| SaffronCity | 22 | nouv. 19, SS adapté 3 |
| SaffronCity_Gym | 28 | nouv. 27, SS adapté 1 |
| SaffronCity_Dojo | 21 | nouv. 21 |
| SaffronCity_PokemonTrainerFanClub | 38 | nouv. 38 |
| SaffronCity_CopycatsHouse 1F/2F | 2 + 11 | nouv. 10, SS adapté 3 |
| SaffronCity_MrPsychicsHouse | 4 | nouv. 2, SS adapté 2 |
| SaffronCity House / Mart / PokemonCenter_1F | 4 + 2 + 4 | nouv. 10 |
| SilphCo 1F → 11F | 2, 17, 8, 10, 18, 18, 24, 12, 11, 9, 17 | nouv. 144, SS adapté 2, Ém. adapté 1 |
| SeafoamIslands_B4F | 6 | nouv. 6 (tuteur Eboulement, panneaux) |
| VictoryRoad 1F/2F/3F | 6 + 12 + 23 | nouv. 41 (dont le tuteur Damoclès) |

## Méthode
- Pour chaque entrée, j’ai lu le contexte dans `build/upstream_orig` : le label, le script appelant dans la carte ou dans `data/scripts/trainers_frlg.inc`, le Dresseur (nom et classe tirés de `src/data/trainers_frlg.party`), les répliques voisines et leur traduction quand elle existe déjà. La note de chaque entrée est générée à partir de ce contexte (carte, interlocuteur, moment du combat, registre) et complétée à la main quand il le fallait.
- J’ai cherché des phrases proches (rapidfuzz, ratio ≥ 72) dans les quatre .po et dans `tm_ss_pairs.pkl` (sans la banque 802). Les revanches du lot D1 (`trainers_frlg.inc`) ont donné le ton et le vocabulaire des Dresseurs. La citation du Mémorydex sur Koga (D1) est reprise mot pour mot pour le PNJ du Parc Safari.
- Mise en page :
  - j’ai écrit les sauts de ligne à la main ;
  - je n’ai reformaté à 198 px (`Gen3.reformater`) que les pages qui dépassaient ;
  - les 14 textes d’une seule ligne en anglais restent sur une ligne et font 198 px au plus ;
  - la réplique de la Copieuse (version joueuse), qui utilise `\l \l`, garde sa mise en page manuelle.
- J’ai lancé le vérificateur sur les 5 fichiers après chaque correction.

## Noms officiels et formes relevés
| Anglais | Français retenu | Source |
|---|---|---|
| CYCLING ROAD | Piste Cyclable | SS 354:0, 356:1 |
| SEA ROUTE 19 | Chenal 19 | glossaire (SS) |
| SEAFOAM ISLANDS | Iles Ecume | glossaire, décision 14 |
| ROCK TUNNEL | Grotte | SS 340:0 |
| UNDERGROUND PATH | Souterrain | .po (SOUTERRAIN) |
| SAFFRON CITY sign | Safrania / Le berceau doré du commerce | SS 529:10 |
| MR. PSYCHIC | M. Psy | SS 529:14, 662:20 |
| COPYCAT | Copieuse | SS 529:3, 540:0, 541 |
| FIGHTING DOJO / MASTER | Dojo / Maître | SS 529:11, 533:0 |
| MARSHBADGE | Badge Marais | SS 531:1-2 |
| POKé DOLL | Poképoupée | glossaire, SS 529:3 |
| CARD KEY | Carte Magnétique (en toutes lettres dans les dialogues) | comme les entrées déjà au .po ; objet = Carte Magn. |
| SECRET HOUSE | Cabane Secrète | Poképédia « Parc Safari (Kanto) », Pokébip (liste CT/CS RFVF : CS03 « dans la Cabane Secrète ») |
| GOLD TEETH | Dent d’Or | Poképédia (objet RFVF) |
| CENTER AREA / AREA 1-3 | Zone Centrale / Zone 1-3 | Pokébip, guide du Parc Safari RFVF |
| REST HOUSE | Maison de repos (MAISON DE REPOS déjà au .po) | .po, Pokébip |
| ROCK / BAIT (Safari) | Caillou / Appât | menus.po (combat Safari) |
| TRAINER TIPS | Conseils aux Dresseurs (panneaux au vouvoiement) | SS 115:27, 390:11 |
| POKéMON TRAINER FAN CLUB | Fan Club des Dresseurs Pokémon | traduction nouvelle, d’après le patch (Lilycove) |
| ELITE FOUR / POKéMON LEAGUE | Conseil 4 / Ligue Pokémon | glossaire |
| BROCK / LANCE / SABRINA / KOGA | Pierre / Peter / Morgane / Koga | consignes, SS |
| Espèces | RAPASDEPIC, ARTIKODIN, ELECTHOR, SULFURA, VOLTORBE, LOKHLASS, MIAOUSS, ROUCOOL, MELOFEE, TADMORV, LEVEINARD, EVOLI, PYROLI, AQUALI, KICKLEE, TYGNON, ROUCARNAGE, SMOGO, SMOGOGO… | banque SS 237 |
| Objets et capacités | Multi Exp, Pièce Rune, Master Ball, Total Soin, Super Ball, PP Plus, Max Repousse, Superepousse, Rappel, Pierre Lune ; Vol, Surf, Flash, Plénitude, Psyko, Copie, Eboulement, Cage-Eclair, Damoclès, Séisme, Abîme | banques SS 222 / 750, glossaire |

## Décisions de style et de registre
- **Tutoiement** : Dresseurs, PNJ, enfants, Morgane, Giovanni, le rival, le Président et la secrétaire de la Sylphe (adultes face à un enfant, comme SS), le conseiller de l’Arène, M. Psy, le Maître Karaté, les gardes des portes de la Piste Cyclable (comme SS 356:1).
- **Vouvoiement** : les panneaux « Conseils aux Dresseurs » (comme SS), l’employé de la Cabane Secrète (CS03), l’accueil de la Sylphe.
- Accords au masculin par défaut quand l’anglais ne varie pas selon le joueur (comme D1). Les deux versions du Président (« dear boy / dear girl ») donnent « mon cher petit / ma chère petite ».
- Noms des duos de Dresseurs en casse SS, prénoms anglais gardés comme dans D1 : Kiri/Jan, Mya/Ron, Jed/Lea, Lia/Luc, Eli/Anne, Ray/Tyra, ainsi que Sara/Erik.
- BIKE = Vélo (comme D1), BICYCLE = Bicyclette (objet SS), BIKER = Motard (classe du glossaire).
- **Étages de la Sylphe** : j’ai suivi la numérotation française, 1F = rez-de-chaussée, 2F = 1er étage… 11F = 10e étage. Le .po fait déjà ainsi (« 4E: PHARMACIE » pour 5F). Les panneaux s’écrivent « Sylphe SARL - Siège social\nNe étage » et les répliques suivent la même règle (« Bienvenue au 9e étage! » pour 10F, « Tu n’es qu’au 4e étage » pour 5F). **À harmoniser** avec le menu d’ascenseur (`gText_1F`…`gText_11F`, absents des .po).
- **Majuscules sans accent** (décision 14 de l’agent principal, appliquée à tous les paquets après coup) : Iles Ecume, « A quel Pokémon… », « Elever », « Ecoute », Electrik, Eboulement, Cage-Eclair. Le Ç est gardé, comme dans SoulSilver FR (« Ça »).
- Types dans les dialogues : « Pokémon Combat », « type Psy », « type Electrik », comme dans les dialogues SS (le glossaire signale les capitales).
- Jeux de mots anglais adaptés : « Ne jetez pas l’éponge, jetez plutôt des Poké Balls! », « MIROIR, MON BEAU MIROIR, SUIS-JE LA PLUS BELLE? » (DODUO). « Smell ya! » = « À plus! ».
- Onomatopées japonaises gardées : « Kurukkoo! » (ROUCOOL), « Fwaaa! », « Hiyah! ».

## Termes proposés pour le glossaire
| Anglais | Proposition | Origine |
|---|---|---|
| CYCLING ROAD | Piste Cyclable | SS |
| SECRET HOUSE | Cabane Secrète | Poképédia, Pokébip (RFVF) |
| GOLD TEETH | Dent d’Or | Poképédia (RFVF) |
| CENTER AREA | Zone Centrale | Pokébip (RFVF) |
| COPYCAT | Copieuse | SS 540:0 |
| MR. PSYCHIC | M. Psy | SS |
| POKéMON TRAINER FAN CLUB | Fan Club des Dresseurs Pokémon | traduction nouvelle |
| ROCKET BROTHERS | Frères Rocket | traduction nouvelle |
| TIKSI BRANCH | filiale de Tiksi | traduction nouvelle |
| TRAINER TIPS | Conseils aux Dresseurs | SS |
| WARDEN (Parc Safari) | Gardien | .po / SS (Gardien du Parc Naturel) |

## Doutes (voir `D3b_douteux.json`)
- **Maître Karaté** (KARATE MASTER) : forme reprise du lot D1, non vérifiée dans RFVF FR.
- **Frères Rocket**, **filiale de Tiksi** : pas de forme RFVF FR trouvée.
- **Gardien** : Poképédia dit « l’intendant » pour RFVF ; j’ai gardé « Gardien », cohérent avec les entrées déjà au .po.
- **Numérotation des étages** de la Sylphe (voir plus haut).
- **Zone Centrale / Cabane Secrète** : formes tirées de guides de fans (Poképédia, Pokébip), sans capture du jeu.
