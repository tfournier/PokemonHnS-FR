# Lot D2 : dialogues des cartes FRLG (première partie de Kanto)

## Résultat
- **850 / 850 entrées traduites** (toutes celles de `D2_a_traduire.json`, 94 cartes `*_Frlg`, aucune compilée dans HnS), réparties dans `D2_001.json` (141), `D2_002.json` (142), `D2_003.json` (142), `D2_004.json` (142), `D2_005.json` (143), `D2_006.json` (140), dans l’ordre des cartes puis des lignes.
- `D2_verifications.tsv` : **0 problème** (aucun CODES, KANA, CARACTERE, LONGUEUR, ESPACE, LARGEUR, GLOSSAIRE ni ANGLAIS).
- `D2_douteux.json` : 12 entrées à arbitrer (noms non vérifiés, choix de style). Elles sont **aussi** présentes, traduites, dans les `D2_00N.json` : le fichier douteux sert de liste de relecture, pas de complément.
- Chaque entrée a une `note` qui donne l’interlocuteur et le contexte, avec le script appelant (et la constante `TRAINER_…` pour les Dresseurs), puis « non compilé ».

### Par source
| Source | Entrées |
|---|---|
| traduction nouvelle | 831 |
| patch FR actuel (vérifié) | 10 (panneaux et répliques des cartes `*_hns` correspondantes : sens vérifié, casse corrigée, « de KANTO » retiré, etc. ; original dans `preuve`) |
| SoulSilver FR officiel (adapté) | 4 (Nina 449:1, panneau « Villa du Cap / Chez Léo » 363:15, Président du Fan Club ×2) |
| Émeraude FR officiel (adapté) | 3 (homme à la Poudre Baie de Poivressel ×2, Pension) |
| Émeraude FR officiel | 1 (« Contre quoi veux-tu l’échanger? ») |
| SoulSilver FR officiel | 1 (« Quel Pokémon veux-tu me confier? ») |

Peu d’officiels sont repris : les cartes HnS de Kanto (`*_hns`) suivent HGSS, pas FRLG, et les phrases proches (rapidfuzz ≥ 72) sont rares. Les répliques déjà traduites dans le lot D1 (revanches de `trainers_frlg.inc`, citations du Mémorydex de `fame_checker_frlg.inc`, échanges de `ingame_trade_frlg.inc`) ont servi de référence : les premières répliques des Dresseurs et les phrases citées par le Mémorydex (Pierre, Ondine au cap) sont alignées sur elles.

### Par carte
| Zone | Cartes | Entrées | Détail |
|---|---|---|---|
| Bourg Palette (PalletTown_*) | 5 | 105 | PalletTown 18, PlayersHouse_1F 7, PlayersHouse_2F 1, ProfessorOaksLab 56, RivalsHouse 23 |
| Route 1 | 1 | 5 | |
| Jadielle (ViridianCity_*) | 6 | 80 | ViridianCity 20, Gym 33, House 4, Mart 6, PokemonCenter_1F 3, School 14 |
| Routes 22 / 23 | 2 | 8 | Route22 7, Route23 1 |
| Route 2 et Forêt de Jade | 6 | 33 | Route2_EastBuilding 4, Route2 1, Route2_House 1, entrées nord 3 / sud 2, ViridianForest 22 |
| Argenta (PewterCity_*) | 8 | 69 | PewterCity 21, Gym 16, House1 3, House2 2, Mart 2, Museum_1F 13, Museum_2F 7, PokemonCenter_1F 5 |
| Route 3, Route 4, Mont Sélénite | 5 | 91 | MtMoon_1F 20, MtMoon_B2F 20, Route3 26, Route4 15, Route4_PokemonCenter_1F 10 |
| Azuria et Caverne Azurée | 11 | 99 | CeruleanCave_B1F 1, BikeShop 11, CeruleanCity 30, Gym 15, House1 11, House2 4, House3 1, House4 8, House5 12, Mart 2, PokemonCenter_1F 4 |
| Routes 24 / 25 et Villa du Cap | 3 | 56 | Route24 11, Route25 30, Route25_SeaCottage 15 |
| Routes 5 / 6 et Souterrain | 7 | 36 | Route5 1, Route5_PokemonDayCare 12, Route5_SouthEntrance 3, Route6 17, UndergroundPath (3 entrées) 3 |
| Carmin sur Mer (VermilionCity_*) | 8 | 74 | VermilionCity 22, Gym 20, House1 4, House2 3, House3 3, Mart 2, PokemonCenter_1F 6, PokemonFanClub 14 |
| Océane (SSAnne_*) | 24 | 95 | Kitchen 10, Deck 9, CaptainsOffice 8, cabines et couloirs 68 |
| Route 11 et Cave TAUPIQUEUR | 5 | 39 | Route11 29, Route11_EastEntrance 1F 2 / 2F 6, DiglettsCave entrées nord 1 / sud 1 |
| Routes 20 / 21 | 3 | 60 | Route20 30, Route21_North 7, Route21_South 23 |
| **Total** | **94** | **850** | |

## Méthode
- Contexte extrait de `build/upstream_orig/data/maps/<carte>/scripts.inc` pour chaque texte : label, script appelant, constante de Dresseur, ordre des répliques (intro / défaite / après-combat), variantes garçon/fille (`…Male` / `…Female`, « pal » / « lady »), fragments.
- Recherche rapidfuzz (seuil 72) sur les msgid déjà traduits des quatre .po, puis reprise adaptée des officiels quand le sens correspondait.
- Mise en page : `Gen3.reformater(…, 198)` page par page. Les pages que j’avais coupées à la main sont gardées telles quelles. Une page de trois lignes est découpée automatiquement à une fin de phrase quand les deux moitiés tiennent en deux lignes ; sinon, j’ai raccourci le texte. Il reste 15 lignes `\l`, toutes là où l’anglais défile aussi (Léo, Président du Fan Club, garde au Thé, Giovanni…). « Prof. Chen », « M. … » et « Major Bob » ne sont jamais coupés en fin de ligne. Les fragments (#236, #237, fin en `\n`) et les fins en espace (#765, #774) sont conservés.
- Les textes anglais d’une ligne restent sur une ligne (raccourcis si besoin).
- **Décision 14 appliquée à tout le lot** (message de l’agent principal) : aucune majuscule accentuée, même en casse normale. Exemples : Cramois’Ile, Iles Ecume, Ile 1, Eclate-Roc, type Electrik, « A plus », « Eclair Américain », « Economisons ». Le Ç est gardé (« Ça », comme SoulSilver FR). Les citations officielles dans `preuve` ne sont pas modifiées.

## Noms officiels relevés (FRLG / SoulSilver FR)
| Anglais | Français retenu | Source |
|---|---|---|
| S.S. ANNE | l’Océane (« le bateau de croisière Océane ») | Poképédia, page « Océane » |
| NUGGET BRIDGE | Pont Pépite | Poképédia, page « Pont Pépite » |
| BIKE SHOP (Azuria) | Cycles à Gogo | Poképédia, page « Cycles à Gogo » (FRLG et HGSS). Le glossaire a « Boutique de Vélo » (Doublonville HGSS) : **à distinguer** |
| BIKE VOUCHER | Bon Commande | Poképédia, page « Bon Commande » |
| OAK’S PARCEL | Colis de Chen (dialogues ; « Colis Chen » dans le Sac) | Poképédia, page « Colis de Chen » |
| SEA COTTAGE | Villa du Cap (« Villa du Cap\nChez Léo! ») | SoulSilver FR 363:15 ; Pokébip (Route 25 FRLG) |
| UNDERGROUND PATH | Souterrain | Poképédia, page « Souterrain (Azuria ⇄ Carmin sur Mer) » |
| ONE ISLAND | Ile 1 | Poképédia « Île 1 » ; .po « ILE 1 » ; décision 14 |
| TRI-PASS / RAINBOW PASS | Tri-Passe / Passe Prisme | Poképédia, page « Tri-Passe » ; .po (patch) |
| SEAGALLOP HI-SPEED n | Ferry Flèche des Mers n | CONSIGNES_FRLG |
| MYSTICTICKET / NAVEL ROCK | Ticketmystik / Roc Nombri | Poképédia, pages « Ticketmystik » et « Roc Nombri » |
| AURORATICKET / BIRTH ISLAND | Ticketaurore (non vérifié) / Ile Aurore | par analogie ; Émeraude FR « ILE AURORE » |
| TEA | Thé | CONSIGNES_FRLG |
| TEACHY TV / VS SEEKER / ITEMFINDER | TV ABC / Cherche VS / Cherch’Objet | .po, glossaire |
| RUNNING SHOES | Chaussures de Sport | SoulSilver FR (banques 221, 375) |
| BOULDER- / CASCADE- / THUNDER- / EARTHBADGE | Badge Roche / Cascade / Foudre / Terre | SoulSilver FR 462, 469, 485, 454 |
| POKéMON FAN CLUB, CHAIRMAN | Fan Club Pokémon, Président | SoulSilver FR 280:74 ; VermilionCity_FanClub_hns |
| DAISY | Nina | SoulSilver FR 449 (comme le lot D1) |
| OLD ROD | Canne | SoulSilver FR |
| BERRY POWDER | Poudre Baie | Émeraude FR « POUDRE BAIE » + casse SS |
| HELIX FOSSIL / DOME FOSSIL / OLD AMBER | Nautile / Fossile Dôme / Vieil Ambre | glossaire |

Autres formes de traduction nouvelle : GLOBAL POLICE = Police Internationale ; HIDDEN MACHINE = Capsule Secrète ; TELEPORTER = Téléporteur, Cell Separation System = Système de Séparation Cellulaire ; DEPARTMENT STORE = Centre Commercial de Céladopole ; GRUNT (locuteur) = « Sbire: » ; OAK (locuteur) = « Chen: » ; MOM = « Maman: » ; Gramps = Papy ; AIDE = assistant ; TRAINER TIPS = « Conseils aux Dresseurs! » (SoulSilver FR).

## Décisions de style et de registre
- **Tutoiement** : rival, Prof. Chen, Nina, Champions (Pierre, Ondine, Major Bob, Giovanni, avec un ton hautain pour ce dernier), guides d’Arène, Dresseurs, enfants, gardes, Léo, assistants, vendeur de MAGICARPE, Hôte de la Pension (comme SoulSilver FR), PNJ des maisons. **Vouvoiement** : personnel des Boutiques, de Cycles à Gogo, du Musée et de l’Océane, passagers distingués qui s’adressent à l’enfant (Room6), panneaux et affiches (« Appuyez sur START… »), e-mail de la Ligue.
- Les accords sont au masculin par défaut quand le texte ne dépend pas du sexe du joueur, comme dans les officiels Gen 3. Les variantes garçon/fille suivent l’anglais : « mon vieux » / « ma belle » (Léo), « mon garçon » / « ma jolie » (vendeur de MAGICARPE), « Serveur » / « Serveuse », « petit frère » / « petite sœur ».
- **Statues d’Arène** en casse SoulSilver : « Arène Pokémon d’Azuria\nChampionne: Ondine\pVainqueurs:\n{RIVAL} ». Les entrées `_hns` du .po ont « CHAMPIONNE: » et « VAINQUEURS: » en capitales (patch) : **à harmoniser**. Pour Jadielle, « Champion: ? » garde une espace avant « ? » : le « ? » remplace le nom.
- **Panneaux** : « Route 1\nBourg Palette - Jadielle » (les caractères « — » et « ↔ » des consignes ne sont pas dans la charmap, d’où « - »). Slogans traduits librement : « Ton voyage haut en couleur t’attend! », « Une mystérieuse aura bleue l’entoure » (patch), « Le paradis éternellement vert » (patch).
- Types dans les dialogues en casse SoulSilver (« de type Eau », « Pokémon Electrik ») : le vérificateur GLOSSAIRE refuse « EAU » en capitales dans une phrase. Espèces en capitales sans accent (banque 237 : MELOFEE, SALAMECHE…).
- « Lv. 30 » devient « niveau 30 » dans les phrases. « second floor » des Centres devient « premier étage ».
- **Jeux de langue** : le serveur et le chef de l’Océane parlent en anglais francisé (« le waiter », « Salmon du Salad ») : je l’ai inversé en français anglicisé (« Je suis the serveur », « Salade of saumon! »). Le Major Bob a un franglais léger (« kid », « Hey ») comme dans SoulSilver FR. Le rival dit « Hello! » sur l’Océane.
- « Smell ya later! » = « A plus, minable! » (et « A plus, minables! » quand il parle au joueur et à Papy, #177).
- Le surnom SPEARY devient « PIAFI » (PIAFABEC).
- Duo Lil & Ian : noms gardés comme dans le lot D1.

## Doutes (voir `D2_douteux.json`)
1. DIRECT CORNER = « Coin Direct » (forme du patch FR, non trouvée dans Rouge Feu / Vert Feuille FR) : #84.
2. FISHING GURU = « Maître Pêcheur » : aucun nom FRLG FR trouvé sur Poképédia ni chez Pokébip (#642, #717, #718).
3. AURORATICKET = « Ticketaurore » par analogie avec Ticketmystik (#692).
4. BERRY POUCH = « Sac à Baies » : le .po a « Sac A Baies » ; à fixer au glossaire (#81).
5. « A plus, minable! » pour « Smell ya » : réplique officielle FRLG FR non vérifiée.
6. Choix de style à valider : franglais (serveur, chef, Major Bob), surnom PIAFI, « Le Séminaire Pokémon du Prof. Chen ».

## Termes proposés pour le glossaire
| Anglais | Proposition | Origine |
|---|---|---|
| BIKE SHOP (Azuria) | Cycles à Gogo | Poképédia (FRLG, HGSS) |
| NUGGET BRIDGE | Pont Pépite | Poképédia |
| S.S. ANNE | Océane | Poképédia |
| SEA COTTAGE | Villa du Cap | SoulSilver FR 363:15 |
| UNDERGROUND PATH | Souterrain | Poképédia |
| BIKE VOUCHER | Bon Commande | Poképédia (le .po a « BON COMMANDE ») |
| OAK’S PARCEL | Colis de Chen (dialogues) | Poképédia |
| TRI-PASS / RAINBOW PASS | Tri-Passe / Passe Prisme | Poképédia |
| MYSTICTICKET / NAVEL ROCK | Ticketmystik / Roc Nombri | Poképédia (le .po a « ROC NOMBRI ») |
| RUNNING SHOES | Chaussures de Sport | SoulSilver FR |
| THUNDERBADGE | Badge Foudre | SoulSilver FR 485 (le .po a « BADGEFOUDRE », patch) |
| EARTHBADGE | Badge Terre | SoulSilver FR 454 (le .po a « Badge TERRE ») |
| GRUNT (locuteur) | Sbire | consignes FRLG |

## Signalements pour l’agent principal
- Décision 14 contre glossaire : le glossaire a encore `ELECTRIK → Électrik`. J’ai écrit « Electrik », et le vérificateur ne le signale pas.
- Le dictionnaire de noms tiré des .po contient des formes fausses ou incohérentes, venant du patch : `NIDORAN♂ → NIDORAN♀`, `OAK → CHEN`, `THUNDERBADGE → BADGEFOUDRE`, `EARTHBADGE → Badge TERRE`, `TEAM ROCKET → Rocket`. À corriger.
- Les statues d’Arène `*_hns` (patch) mélangent les casses (« Arène Pokémon DE Safrania », « CHAMPIONNE: Morgane ») : à aligner sur le format ci-dessus.
