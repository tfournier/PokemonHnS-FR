# Lot C2b — audit des menus et données hérités du patch FR

## Fichiers
- `C2b_corrections.json` : **1 429 entrées** à intégrer (format §6 ; `ancien` = texte des .po **après** l'intégration de C1 et C2a ; `note` commence par la liste des décisions entre crochets, ex. `[ChatGPT oubli : adaptée ; alerte LARGEUR : corrigée]`).
- `C2b_decisions.tsv` : une ligne par remarque ChatGPT (1 563), par alerte (715), par libellé mélangé (417) et par entrée ajoutée pour la cohérence (8). Cela fait 2 703 lignes. Colonnes : groupe, type, catégorie, décision, msgid, ancien, proposition ChatGPT ou détail, texte final, note, état final.
- `C2b_verifications.tsv` : sortie de `outils/verifier.py` sur les corrections. **Aucun problème bloquant.** Il reste 52 LARGEUR et 6 GLOSSAIRE, non bloquants :
  - LARGEUR, Pokédex : 50 descriptions dont toutes les lignes font au plus 236 px. Le texte est centré sur 240 px (`PrintInfoScreenText(…, GetStringCenterAlignXOffset(FONT_NORMAL, description, 0xF0))`).
  - LARGEUR, combat : 2 messages de combat. Ils sont coupés automatiquement à 208 px sur 2 lignes (`BreakStringAutomatic`, `BATTLE_MSG_MAX_WIDTH`).
  - GLOSSAIRE : 6 termes en capitales qui sont voulus (FUITE, NORMAL, ATTENTION, DJ LILY, AUCUN, ACIDE dans des libellés).
- Simulation d'`integrer_lot.py`, faite sans rien écrire, sur les .po du 20/11 à 18 h 21 :
  - 0 msgid inconnu, 0 rejet par contrôle, 0 officiel exact bloqué.
  - 26 entrées passent directement et 1 403 avec `--corriger`, toutes justifiées par leur `note`.

## Méthode
1. Les 2 375 msgid distincts touchés par les trois entrées ont été regroupés en fiches : texte anglais, texte français actuel, champ dans la source, limite en octets, largeur de chaque ligne, remarques, alertes et suggestion de casse.
2. Le travail a été réparti en 7 groupes : objets, capacités, talents/baies/types, Pokédex gen 1-4, Pokédex gen 5-9, combat/menus, divers. Les mêmes règles écrites et un contrôleur commun s'appliquaient à tous :
   - couverture et alignement des décisions ;
   - contrôles bloquants de `verifier.py` ;
   - largeur de fenêtre et nombre de lignes ;
   - majuscules accentuées et « Oeuf ».
3. Fenêtres mesurées dans `build/upstream_orig` :

   | Texte | Largeur | Source |
   |---|---|---|
   | Description d'objet | ≤ 109 px, 3 lignes | `WIN_DESCRIPTION`, 14 tuiles, x = 3 |
   | Description de capacité | ≤ 154 px, 2 lignes | résumé : 20 tuiles, x = 6 ; combat : `B_WIN_MOVE_DESCRIPTION`, police étroite, 144 px |
   | Description de talent | ≤ 144 px, 1 ligne | `PSS_DATA_WINDOW_INFO_ABILITY` |
   | Pokédex | ≤ 236 px | texte centré |
   | Baies | 200 px | |
   | Radio | 220 px, coupure automatique | |
   | Catalogue de Motisma | 96 px | |
   | Cube Zygarde | 88 px | |

4. Relecture du sens (§5) faite par l'agent principal du lot :
   - sur les descriptions du Pokédex que ChatGPT n'avait pas signalées ;
   - sur un échantillon de chaque groupe.
5. **Rebase** : C1 et C2a ont été intégrés pendant le travail (commits b19b6474 et a9e0a069). Sur les 1 580 corrections de départ, 162 portaient sur une entrée modifiée entre-temps :
   - **108** étaient déjà faites à l'identique : retirées.
   - **43** ont été abandonnées :
     - 12 sont devenues un texte officiel exact (Pension, Route 45/46, Easy Chat STOP/PSHT, WILLY…) ;
     - les autres sont un officiel adapté par C1 (panneaux d'Arène Rosalia/Acajou, Vent Arrière, Air Veinard…) ou des panneaux traités par C2a.
   - **3** sont maintenues contre C1 :
     - « ÇA » : la cédille est gardée (décision 14) ;
     - « ANDY » : colonne FR de `apprentice.h` ;
     - « Oh! {MON1} et {MON2} sauvages apparaissent! » : convention « sans article ».
   - **8** ont été réadaptées : les hôtes de hausse et de baisse des stats (voir plus bas).

## Chiffres
### Remarques ChatGPT (1 563)
| Catégorie | Total | Acceptées | Adaptées | Refusées |
|---|---|---|---|---|
| oubli | 407 | 100 | 194 | 113 |
| typographie | 372 | 178 | 111 | 83 |
| contresens | 278 | 94 | 128 | 56 |
| terminologie | 227 | 73 | 114 | 40 |
| orthographe | 104 | 39 | 49 | 16 |
| codes | 91 | 65 | 24 | 2 |
| autre_phrase | 78 | 60 | 18 | 0 |
| registre | 6 | 2 | 1 | 3 |
| **Total** | 1 563 | 611 | 639 | 313 |

Par groupe (acceptées / adaptées / refusées) :

| Groupe | Acceptées | Adaptées | Refusées |
|---|---|---|---|
| objets | 165 | 141 | 83 |
| capacités | 93 | 149 | 89 |
| talents/baies/types | 20 | 113 | 22 |
| Pokédex 1-4 | 58 | 129 | 31 |
| Pokédex 5-9 | 2 | 5 | 2 |
| combat/menus | 122 | 46 | 66 |
| divers | 151 | 56 | 20 |

**Motifs de refus ou d'adaptation**, par ordre de fréquence :
- **Débordement de fenêtre.** La correction ChatGPT dépasse 109, 154 ou 144 px, ou passe à 5 ou 6 lignes au Pokédex. Elle est alors reformulée plus court.
- **Noms en capitales.** ChatGPT écrit en capitales des noms d'objets, de capacités ou de talents (« AROMATE PRESSE », « DYNAMOPOING »). Ils sont remis en casse normale de style SoulSilver.
- **Abréviations.** AS/DS/AT ou ATT ont été refusés quand la place suffisait.
- **Graphies refusées.** « Oeuf » / « Voeu Soin » : le Œ est gardé. Les majuscules accentuées sont refusées aussi.
- **`\n` dans les messages de combat.** Ils ne servaient qu'à la mise en page, alors que la coupure est automatique.
- **Noms officiels faux** proposés par ChatGPT :
  - « ARCHE DUC », « SPECIAL + » ;
  - « Charge Foudre » comme catégorie : la bonne catégorie est « Foudroyeur », celle de FULGURIS ;
  - « Pattes Fortes » : la bonne forme est « Fort-Pied » ;
  - « capacité spéciale » au lieu de « talent ».
- **Réécritures de style** d'une description officielle correcte.

### Alertes automatiques (715)
| Contrôle | Total | Corrigées | Justifiées |
|---|---|---|---|
| LARGEUR | 461 | 94 | 367 (Pokédex ≤ 236 px, coupure auto en combat) |
| FRAGMENT | 115 | 36 | 79 |
| ANGLAIS | 85 | 8 | 77 |
| LONGUEUR | 20 | 16 | 4 |
| ESPACE | 15 | 14 | 1 |
| CODES | 15 | 12 | 3 |
| GLOSSAIRE | 4 | 2 | 2 |

Détail :
- **FRAGMENT justifiés (79).** Le texte est complet et fidèle à l'anglais, mais sa fin d'octets est partagée avec une autre chaîne de la ROM du patch : 40 descriptions de capacités, 24 en combat/menus, 15 autres. Ces entrées ne changent pas, donc `verifier.py` continuera de les signaler sur les .po. Pour les retrouver, filtrer `C2b_decisions.tsv` sur `alerte FRAGMENT justifie`.
- **Vrais fragments retraduits (36)**, par exemple :
  - ETONS → JETONS, « S » → WILLY/Billy, « E » → ED / GRACE, ICLIC → CLIC ;
  - CLYSMIQUE → Overdrive, CELL BATTERY → « Pile » ;
  - mots Easy Chat « 4 », « KET », « DINE »…
- **ANGLAIS justifiés** : crédits, noms propres officiels, catégories officielles identiques (Judo, Punk, Chinchilla, Viking…), colonnes étrangères de la table des apprentis.
- **LONGUEUR** : les capacités Z dépassant 16 octets sont abrégées. « Colère du Gardien » est laissé à 17 octets, comme l'anglais.

### Libellés en casse mélangée (417)
- **345 corrigés et 72 gardés.** Les 72 gardés sont des sigles ou des formes déjà justes : ROM ×17, CD, GB, VS, PCo…
- **Objets, capacités, talents, lieux** en casse normale avec les noms officiels : « Joyau Feu », « Pierre Foudre », « Maxi Pépite », 18 « Téra-Eclat … », « Poing-Eclair », « Grotte Tréfonds », « Tunnel Mérazon », « Tour Pokémon », « Mont Dresseurs », « Pyramide Niv.2 »…
- **Libellés de menus et d'interface** en capitales : PYRAMIDE DE COMBAT, BROYEUR DE BAIES, PTS COMBAT, menu Safari « FUITE »…
- **Panneaux** en casse de phrase SoulSilver.
- **Espèces** en capitales.
- La suggestion automatique a été rejetée à chaque erreur : « Coupé Globale », « Centre Pokémon Ny », « Rom Dragon », « 24PCO ».
- **116 textes officiels** ne changent que de casse (`retouche_officiel: true`, original dans `preuve`).
- **6 alignements officiels faux** ont été corrigés (`alignement_faux: true`) :
  - Pyramide Niv.2 à 5, décalés d'un étage ;
  - crédits Iwata et Tajiri ;
  - rubans CUTE et SMART CONTEST.

### Sources des 1 429 corrections
| Source | Nombre |
|---|---|
| traduction nouvelle | 795 |
| patch FR actuel (vérifié) | 486 |
| Émeraude FR officiel (adapté) | 128 |
| SoulSilver FR officiel (adapté) | 9 |
| SoulSilver FR officiel | 7 |
| Émeraude FR officiel | 4 |

« Patch FR actuel (vérifié) » ne couvre que les changements de forme : casse, typographie, codes, lignes.

## Hôtes des messages de hausse et de baisse des stats (à intégrer ensemble)
**Problème.** `{B_BUFF2}` vaut « sharply » / « harshly » / « drastically » / « severely » ou vide (`battle_script_commands.c` 7917-7957). Le patch donnait « très » / « énormément » placés devant le verbe : « ATTAQUE du PTITARD très augmente! ».

**Nouveau schéma** :
- Fragments :
  - sharply et harshly = « forte » ;
  - drastically et severely = « très forte ».
- Hôtes :
  - « {B_BUFF1} du {X} en {B_BUFF2}hausse/baisse! » (base SoulSilver 197:750/762 posée par C1) ;
  - « {TALENT} de {X}: {B_BUFF1} en {B_BUFF2}hausse/baisse! » ;
  - « Grâce à {B_LAST_ITEM}, {B_BUFF1} de {X} est en {B_BUFF2}hausse/baisse! ».

**Résultat.** « ATTAQUE du PTITARD ennemi en forte hausse! », et « … en hausse! » quand le fragment est vide.

**Entrées concernées.** 15 au total :
- 4 fragments ;
- 5 hôtes de base ;
- 2 hôtes d'objet ;
- 4 hôtes de talent.

Elles ne doivent pas être intégrées séparément.

**Défaut amont.** `pokemon.c` (BufferStatRoseMessage, objets X) ajoute déjà « rose! » au tampon et double le verbe, en anglais aussi.

## Termes officiels vérifiés
- **Poképédia** :
  - les 33 capacités G-Max (page Gigamax) : Fouet, Fournaise, Canonnade, Pestilence, Ondes, Récif, Téphra, Percée, Coup Final, Multicoup G-Max… ;
  - « Choc G-Max » (Salarsen Gigamax) est bien le nom officiel ;
  - objets : Boîte Pokémon, Armure de la Fortune, Rouleau des Ténèbres, Défense Extra, Bouchée Double ;
  - talents : Cœur Soin, Rage Poison, Force Sable, Epine de Fer, Griffe Dure, Repli Tactique, Expert Acier, Folle Furie, Surf Caudal, Boost Chimère, Système Alpha, Armure Miroir, Dent de Dragon, Blanche Ruade, Charge Quantique, Urne/Epée/Bois/Perles du Fléau, Armure Caudale, Force Fongique, Force Mémorielle ;
  - catégories : Monocorne, Ensorceleur, Fort-Pied, Echarpe, Foudroyeur ;
  - classes : Mécano, Rocker, Exorciste, Duo Baston, Fille Baston.
- **Liste française de PKHeX** (capacités récentes) : Vif Eclair, Pression Extrême, Téra Explosion, Piqué Supersonique, Trou Noir des Ombres, Incendie, Eau Revoir, Sprint Bouclier…
- **Glossaire / SoulSilver FR** : Glacéternel, ADN Berzerk, Poing-Eclair, Dynamopoing, Dracosouffle, Loubard, Croupier, Clément, Ian (banque 703), Loterie Pokémon, Antenne Pokémon, Chronique du Prof. Chen (banque 414), Rangma.
- **Émeraude FR** (`em_fr.gba`) :
  - noms de Dresseurs : MARIE, STANISLAS, VICENTE, ED, GRACE ;
  - adversaires de Concours : NIPIOT, OLGA ;
  - BUNNY HOPS ;
  - SALLE LINK DIRECT ;
  - format « 1000 JETONS ».

## À ajouter au glossaire (proposition)
- **Objets** : Glacéternel (remplace « Glace ETERNELLE » du patch), Joyau <type>, Téra-Eclat <type>, Aromate <nature>, Pomme Acidulée / Pomme Sucrée, Défense Extra / Offensive Extra / Esquive Extra / Double Extra, Armure de la Fortune / de la Rancune.
- **Lieux** : Grotte Tréfonds, Tunnel Mérazon, Grotte Granite, Grotte Origine, Mont Dresseurs, Tour Pokémon, Centre Météo, Grotte d'Akala, Grotte de Poni, Grotte d'Ula-Ula.
- **Capacités G-Max** : « <Nom> G-Max », en casse normale.

## Doutes et points laissés à l'agent principal
1. **Lieux de Hoenn.** Les lieux de Hoenn entièrement en capitales venus d'Émeraude FR (CLEMENTI-VILLE, CAVERNE FONDMER, PLANQUE MAGMA…) n'étaient pas dans mes entrées. Les entrées mélangées sont passées en casse normale, donc la carte mêle désormais les deux styles. Il faut une décision globale.
2. **Décorations.** Elles sont gardées en capitales Émeraude FR (COUSSIN PLANTE, POUP. METAMORPH), pour rester cohérentes avec les quelque 150 autres de la liste. C'est contraire à la règle « objets en casse normale » : à trancher globalement.
3. **Libellés restés en capitales hors lot.** 150 noms de talents, les autres aromates (AROMATE SOLO…), les bonbons de CREMY, le singulier « LETTRE RETRO » (dont le pluriel devient « Lettre Rétro ») et TERA-ECLAT STELL.
4. **Radio.** Le patch écrit MARIE et « BLABLA Pokémon » dans une quarantaine de lignes, là où SoulSilver dit Lula et « Chronique ». J'ai gardé la forme du patch dans mes lignes ; il faut un remplacement global.
5. **Abréviations forcées par les 16 octets** des capacités Z : « Turbo. Bulldozer », « Laser Cryogéniq. », « Imp. Choupinova », « Py. Cataclysmique »… Le visualiseur de sprites (debug) garde les noms complets.
6. **Largeur des noms de capacités.** En casse normale, ils sont jusqu'à 32 px plus larges que l'anglais en capitales. La largeur des cases de capacités en combat n'a pas été vérifiée en jeu, pas plus que celle des choix multiples de `script_menu.h` (« Carmin sur Mer »).
7. **Cube Zygarde.** Les libellés deviennent « FORME » / « TALENT » : « CHANGER DE … » dépasse la fenêtre de 88 px. Dans le Catalogue de Motisma, « FOUR MICRO-ONDES » devient « MICRO-ONDES ».
8. **Non vérifiés en ligne** : Mochi Force / Mochi Armure, « repaire » ou « antre » pour Pokémon Den, Osmose, « Mer Occident », Shehroz (Rose, Ethernatos), Island Cave (« Grotte Island », Émeraude FR).
9. **Mauvais alignements possibles hors lot.** D'autres entrées de `ribbon_descriptions.h` « Émeraude FR officiel » semblent mal alignées.
10. **Descriptions du Pokédex d'une autre forme.** Lors de la relecture du sens, j'ai corrigé 3 descriptions que ChatGPT n'avait pas signalées : RATTATAC d'Alola, OSSATUEUR d'Alola, la dernière phrase de Toxizap. Il peut en rester d'autres dans les descriptions hors de ce lot.
11. **Même anglais, sens différents.** Aucun nouveau msgctxt n'a été créé. « ANDY » et « Will » existent déjà avec plusieurs entrées, et les corrections gardent le msgctxt d'origine.
