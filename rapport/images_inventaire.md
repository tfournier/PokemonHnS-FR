# Inventaire des images contenant du texte anglais

Source examinée : copie figée des originaux anglais `build/upstream_orig` (tag Release-v2.0.6).
`build/upstream` contient déjà les 132 fichiers FR copiés par la construction, il n'a donc pas servi de référence.
Détail ligne par ligne dans `rapport/images_inventaire.tsv` (241 lignes : 239 images + 2 tilemaps `.bin`).
Planches-contacts et rendus de travail : `/private/tmp/claude-501/-Users-tfournier-projets-gitlab-com-tfournier-PokemonHnS-FR/d65695bd-6542-4bbf-9aff-f39c55206823/scratchpad/images_inv/sheets/`.

## Chiffres clés

| | nombre |
|---|---|
| PNG de `graphics/` hors dossiers exclus, tous regardés en planche-contact | 1 049 |
| Échantillon des dossiers exclus regardé (tirage au hasard + `object_events/pics/misc` en entier + 28 icônes d'objets) | ~210 |
| `data/tilesets/**/tiles.png` regardés (planches x2, puis zoom x3 sur les panneaux) | 244 |
| Tilemaps rendues (planche + `.bin`, versions EN et FR côte à côte quand le FR existe) | ~70 |
| **Lignes avec du texte** | **241** |
| A_TRADUIRE | 43 |
| DEJA_TRADUIT | 110 (dont 25 icônes de type et 9 polices) |
| TRADUIT_PARTIELLEMENT | 5 |
| PAS_DE_TRADUCTION_NECESSAIRE | 83 (logos, mentions légales, noms de boutons, restes japonais, fichiers non compilés ou inutilisés) |

Les 115 PNG de `images/graphics` sont tous dans l'inventaire. Les 17 `.bin` FR apparaissent dans la colonne tilemap.

Règle appliquée pour le statut : **A_TRADUIRE** = image anglaise compilée dans la ROM HnS, même si l'écran est peut-être inaccessible (c'est alors dit dans la remarque).
**PAS_DE_TRADUCTION_NECESSAIRE** = pas de mot à traduire, ou fichier non compilé dans HnS.
La compilation a été déterminée en lisant les `INCBIN` et les `#if` qui les entourent :
IS_HNS=1, IS_FRLG=0, EXPANSION_INTRO=TRUE, POKEDEX_PLUS_HGSS=TRUE, HGSS_DECAPPED=FALSE, DEXNAV_ENABLED=FALSE, B_MOVE_DESCRIPTION_BUTTON=START.
La colonne remarque du TSV indique le fichier source qui référence l'image et la condition `#if` en vigueur.

## Résumé par dossier

Légende : `examiné` = toutes les images regardées ; `échantillon` = dossier exclu après vérification d'un échantillon.

| dossier | PNG | examen | avec texte | A_TRADUIRE | DÉJÀ | PARTIEL | PAS_NÉC. |
|---|---|---|---|---|---|---|---|
| bag | 12 | examiné | 5 | 1 | 1 | 0 | 3 |
| balls | 30 | échantillon | 0 | 0 | 0 | 0 | 0 |
| battle_anims | 476 | échantillon | 0 | 0 | 0 | 0 | 0 |
| battle_environment | 65 | examiné | 0 | 0 | 0 | 0 | 0 |
| battle_frontier | 17 | examiné | 2 | 0 | 1 | 0 | 1 |
| battle_interface | 119 | examiné | 32 | 6 | 7 | 0 | 19 |
| battle_transitions | 23 | examiné | 1 | 0 | 0 | 0 | 1 |
| berries | 67 | échantillon | 0 | 0 | 0 | 0 | 0 |
| berry_blender | 8 | examiné | 2 | 0 | 2 | 0 | 0 |
| berry_crush | 5 | examiné | 0 | 0 | 0 | 0 | 0 |
| berry_fix | 6 | examiné | 5 | 0 | 0 | 0 | 5 |
| birch_speech | 3 | examiné | 0 | 0 | 0 | 0 | 0 |
| cable_car | 4 | examiné | 0 | 0 | 0 | 0 | 0 |
| cave_transition | 1 | examiné | 0 | 0 | 0 | 0 | 0 |
| contest | 23 | examiné | 7 | 2 | 2 | 0 | 3 |
| crash_screen | 1 | examiné | 1 | 0 | 0 | 0 | 1 |
| credits | 1 | examiné | 1 | 0 | 0 | 0 | 1 |
| credits_frlg | 19 | examiné | 2 | 0 | 0 | 0 | 2 |
| decorations | 43 | échantillon | 0 | 0 | 0 | 0 | 0 |
| dexnav | 9 | examiné | 1 | 1 | 0 | 0 | 0 |
| diploma | 1 | examiné | 0 | 0 | 0 | 0 | 0 |
| dodrio_berry_picking | 6 | examiné | 0 | 0 | 0 | 0 | 0 |
| door_anims | 113 | échantillon | 0 | 0 | 0 | 0 | 0 |
| easy_chat | 9 | examiné | 3 | 0 | 2 | 0 | 1 |
| evolution_scene | 1 | examiné | 0 | 0 | 0 | 0 | 0 |
| expansion_intro | 4 | examiné | 2 | 0 | 0 | 0 | 2 |
| field_effects | 72 | échantillon | 0 | 0 | 0 | 0 | 0 |
| field_specials | 0 | examiné | 0 | 0 | 0 | 0 | 0 |
| fonts | 23 | examiné | 10 | 0 | 9 | 0 | 1 |
| frontier_pass | 8 | examiné | 3 | 1 | 2 | 0 | 0 |
| interface | 13 | examiné | 3 | 2 | 1 | 0 | 0 |
| intro | 36 | examiné | 2 | 0 | 0 | 0 | 2 |
| intro_frlg | 23 | examiné | 3 | 0 | 0 | 0 | 3 |
| items | 638 | échantillon | 0 | 0 | 0 | 0 | 0 |
| link | 8 | examiné | 2 | 2 | 0 | 0 | 0 |
| mail | 12 | examiné | 0 | 0 | 0 | 0 | 0 |
| map_popup | 38 | examiné | 0 | 0 | 0 | 0 | 0 |
| map_preview | 21 | examiné | 0 | 0 | 0 | 0 | 0 |
| misc | 10 | examiné | 3 | 0 | 0 | 0 | 3 |
| naming_screen | 17 | examiné | 6 | 0 | 4 | 0 | 2 |
| oak_speech | 10 | examiné | 1 | 0 | 0 | 0 | 1 |
| oak_speech_hns | 5 | examiné | 0 | 0 | 0 | 0 | 0 |
| object_events | 923 | échantillon | 3 | 2 | 0 | 0 | 1 |
| party_menu | 5 | examiné | 2 | 0 | 1 | 0 | 1 |
| picture_frame | 6 | examiné | 0 | 0 | 0 | 0 | 0 |
| pokeblock | 7 | examiné | 4 | 1 | 2 | 1 | 0 |
| pokedex | 32 | examiné | 19 | 2 | 9 | 1 | 7 |
| pokemon | 7997 | échantillon | 0 | 0 | 0 | 0 | 0 |
| pokemon_jump | 8 | examiné | 1 | 1 | 0 | 0 | 0 |
| pokemon_storage | 92 | examiné | 1 | 0 | 1 | 0 | 0 |
| pokenav | 83 | examiné | 38 | 2 | 34 | 0 | 2 |
| rayquaza_scene | 25 | examiné | 0 | 0 | 0 | 0 | 0 |
| reset_rtc_screen | 2 | examiné | 0 | 0 | 0 | 0 | 0 |
| rotating_gates | 8 | examiné | 0 | 0 | 0 | 0 | 0 |
| roulette | 18 | examiné | 2 | 1 | 0 | 0 | 1 |
| seagallop | 3 | examiné | 0 | 0 | 0 | 0 | 0 |
| shop | 3 | examiné | 2 | 2 | 0 | 0 | 0 |
| sliding_puzzle | 6 | examiné | 0 | 0 | 0 | 0 | 0 |
| slot_machine | 37 | examiné | 3 | 1 | 0 | 2 | 0 |
| ss_anne | 2 | examiné | 0 | 0 | 0 | 0 | 0 |
| starter_choose | 3 | examiné | 0 | 0 | 0 | 0 | 0 |
| summary_screen | 8 | examiné | 3 | 0 | 1 | 0 | 2 |
| text_window | 25 | examiné | 0 | 0 | 0 | 0 | 0 |
| title_screen | 12 | examiné | 6 | 0 | 2 | 0 | 4 |
| title_screen_frlg | 12 | examiné | 3 | 0 | 0 | 0 | 3 |
| trade | 11 | examiné | 3 | 0 | 1 | 0 | 2 |
| trainer_card | 6 | examiné | 2 | 0 | 2 | 0 | 0 |
| trainer_hill | 1 | examiné | 0 | 0 | 0 | 0 | 0 |
| trainers | 248 | échantillon | 0 | 0 | 0 | 0 | 0 |
| types | 28 | examiné | 26 | 0 | 25 | 0 | 1 |
| ui_screenshots | 4 | examiné | 0 | 0 | 0 | 0 | 0 |
| union_room_chat | 7 | examiné | 2 | 0 | 1 | 1 | 0 |
| unused | 11 | examiné | 4 | 0 | 0 | 0 | 4 |
| voltorb_flip | 6 | examiné | 3 | 2 | 0 | 0 | 1 |
| wallclock | 2 | examiné | 0 | 0 | 0 | 0 | 0 |
| weather | 10 | échantillon | 0 | 0 | 0 | 0 | 0 |
| wireless_status_screen | 1 | examiné | 0 | 0 | 0 | 0 | 0 |
| wonder_card | 9 | examiné | 0 | 0 | 0 | 0 | 0 |
| wonder_news | 5 | examiné | 0 | 0 | 0 | 0 | 0 |
| data/tilesets/primary | 15 | examiné | 10 | 10 | 0 | 0 | 0 |
| data/tilesets/secondary | 229 | examiné | 7 | 4 | 0 | 0 | 3 |
`field_specials` ne contient aucun PNG. Pour `pokedex`, deux lignes sont des tilemaps (`hgss/SelectBar.bin`, `hgss/SelectBar_clear.bin`). Pour `object_events`, les 81 images de `pics/misc` ont toutes été regardées.

## Dossiers exclus et raison

| dossier | raison (après échantillon) |
|---|---|
| pokemon (7 997) | sprites, icônes, empreintes des Pokémon : aucun texte |
| object_events (923) | sprites de personnages et d'objets. **Exception repérée** : `pics/misc/mart_light.png`, `mart_light_hns.png` (MART) et `gym_sign.png` (GYM, RFVF seulement) ont du texte, ils sont dans le TSV |
| battle_anims (476) | effets d'attaques, fonds d'animation : pas de texte (seuls « Z », « ? », « X » décoratifs) |
| trainers (248) | portraits de dresseurs |
| door_anims (113) | animations de portes |
| field_effects (72) | effets de terrain, bulles d'émotion « ! » « ? » |
| berries (67), balls (30), weather (10), decorations (43) | sprites sans texte |
| items (638) | icônes : échantillon de 28 (CT, CS, lettres, passes, tickets, cartes, boîtes). Aucune ne contient de texte (les CT/CS sont des disques sans lettres) |

Dossiers examinés **sans aucun texte** :
battle_environment, berry_crush, birch_speech, cable_car, cave_transition, diploma, dodrio_berry_picking, evolution_scene, mail, map_popup, map_preview, oak_speech_hns, picture_frame, rayquaza_scene, reset_rtc_screen, rotating_gates, seagallop, sliding_puzzle, ss_anne, starter_choose, text_window, trainer_hill, ui_screenshots, wallclock, wireless_status_screen, wonder_card, wonder_news, ainsi que 227 tilesets sur 244.
Dans ces écrans, le texte est dessiné par le code : noms de lieux des popups et des aperçus, courrier, Carte/Info mystère, bannière de montée de niveau, pop-up de talent.

## À traduire en priorité (écrans les plus vus)

1. `graphics/interface/status_icons.png` : PSN PAR SLP FRZ BRN PkRS FNT FRB, affichés dans le menu Équipe, le Résumé et le PC. La version combat (`battle_interface/hns/status*.png`) est traduite, celle-ci non.
2. `graphics/interface/menu_info.png` : TYPE / POWER / ACCURACY / PP et les 19 icônes de type, affichés dans la poche CT/CS du Sac (`item_menu.c`).
3. `graphics/shop/money.png` (MONEY, visible à chaque achat) et `graphics/shop/bp.png` (BP → PCo).
4. Panneaux des villes : MART / P.C / GYM dans les tilesets `johto_general_hns`, `kanto_general_hns`, `general_hns`, `johto_north_east/west/south_hns`, `mt_silver_exp_hns`, `bike_shop_hns`, `johto_bike_shop_hns`, `cianwood_city_hns`, plus l'objet animé `object_events/pics/misc/mart_light_hns.png`.
5. `graphics/battle_interface/move_info_window_start.png` (START MOVE INFO) : apparaît à chaque choix de capacité.
6. Pokédex HGSS, écran Zone : `hgss/SelectBar.bin` n'a pas été traduit. Il affiche encore INFO AREA STATS EVO CRY SIZE, et les tuiles « AREA » surlignées (0x71-0x78) de `tileset_menu1.png` sont restées en anglais.
7. Option « nouvelle interface » de combat (gen 4) : `battle_interface/gen4/hpbar.png` et `gen4/status{,2,3,4}.png`.
8. Voltorbataille : `voltorb_flip/gameboard.png` (NOTES) et `coins.png` (COINS:).
9. Casino, traduction incomplète : `slot_machine/menu.png` (BIG BONUS, REG BONUS, REPLAY, POWER), `digital_display.png` (seul REG a été effacé), `reel_symbols/7.png` (REPLAY).
10. `bag/check_berry.png` : fiche des baies (SPICY DRY SWEET BITTER SOUR).

Ensuite, défauts dans des images déjà traduites :
- `union_room_chat/background.png` : le bouton START apparaît coupé (« S » puis « TART »).
- `pokeblock/use_screen/updown.png` : DOWN est resté en anglais.

Puis les oublis isolés :
- `frontier_pass/map_and_card.png` : la carte dresseur en anglais pendant le zoom.
- `contest/applause.png` et `nextturn.png`.
- `pokenav/left_headers/condition.png` et `condition/cancel.png`.
- `roulette/credit.png`.
- `link/321start*.png` et `pokemon_jump/bonuses.png` (mini-jeux en lien).
- `dexnav/gui_tiles.png` (DexNav désactivé).
- `pokedex/interface.png` (Pokédex vanilla, non affiché).
- `battle_dome` (BATTLE FRONTIER).

## Pièges repérés

- **Copie de travail polluée** : `build/upstream` contient les images FR après construction. Il faut toujours comparer avec `build/upstream_orig`.
- **Tilemap qui partage des tuiles** : `pokedex/hgss/SelectBar.bin` (écran Zone) utilise les tuiles de `tileset_menu1.png`.
  Les autres écrans ont reçu des `.bin` FR pointant vers de nouvelles tuiles, mais pas celui-ci, ni `SelectBar_clear.bin`.
  Il faut le traiter comme `tilemap_info_screen.bin`.
- **Plusieurs variantes de la même image sont compilées**, et la variante affichée dépend d'une option ou d'une config :
  - interface de combat HnS ou gen 4 (`gSaveblock3.challengeSettings.newBattleUI`) : seule la variante HnS est traduite ;
  - vanilla ou HnS (`#if IS_HNS`) ;
  - variantes `_DECA` du Pokédex HGSS (compilées mais jamais chargées) ;
  - `move_info_window_{l,r,start}` selon `B_MOVE_DESCRIPTION_BUTTON` ;
  - Pokédex vanilla compilé mais remplacé par le HGSS.
- **Le même mot dans plusieurs images, traduit dans une seule** :
  - APPLAUSE : `contest/interface.png` traduit, `contest/applause.png` non ;
  - CONDITION : `pokenav/options` traduit, `left_headers` non ;
  - TRAINER CARD : `frontier_pass/bg.png` traduit, `map_and_card.png` non ;
  - icônes de statut : `battle_interface/hns` traduit, `gen4` et `interface/status_icons` non ;
  - noms de types : `types/*.png` traduit, `interface/menu_info.png` non.
- **Un même panneau dans le tileset et dans un objet animé** : l'enseigne MART existe en tuiles et en object event (`mart_light*.png`). Les deux doivent avoir la même graphie.
  Un même panneau se répète aussi dans plusieurs tilesets primaires (les variantes johto_* ont la même disposition).
- **Contraintes des tilesets** : certains ont un `-num_tiles` imposé dans `graphics_file_rules.mk` (`secondary/shop`, `pretty_petal_flower_shop`…), et les palettes réelles sont dans des `.pal` (beaucoup de PNG sont en niveaux de gris).
  La graphie officielle FR des panneaux (BOUTIQUE ? C.P ? ARÈNE ?) n'a pas été relevée : à vérifier dans `memoires/em_fr.gba`.
- **Formats particuliers** :
  - sprites stockés linéairement, 4 tuiles par ligne (`pokedex/hgss/tileset_interface*.png`) ;
  - image affine 8 bpp (`frontier_pass/map_and_card.png` avec `small_map_and_card_affine.bin`) ;
  - planche et tilemap compressées (`voltorb_flip/gameboard.4bpp.lz`, `.bin.lz`) ;
  - tilemaps 32x64 ou 64x32 (`diploma`, `tourney_info_card_tilemap.bin`).
- **Texte dessiné par le code, pas par l'image** : noms dans les popups et aperçus de lieu, courrier, Carte/Info mystère, montée de niveau, talents, noms sur la carte, textes des fenêtres. Pas d'image à traduire pour ces écrans.
- **Restes japonais présents dans des planches compilées mais non affichés** : `misc/japanese_hof.png`, `pokenav/region_map/zoom_tiles.png`, `contest/japanese/*`. Il ne faut pas les « traduire » sans avoir vérifié qu'ils s'affichent.
- **Retouches FR minimes** : `slot_machine/digital_display.png` (seul REG effacé), `pokenav/ribbons/list_bg.png` et `condition/search_results.png` (58 pixels).
  Dans `summary_screen/hns/tiles.png`, le rendu fait apparaître des pixels résiduels après EFFET et RUBAN et un « MÉMO DRESSEU(R) » qui semble tronqué. À confirmer en jeu, car mon rendu ignore les palettes par tuile.
- **En-tête de carte** : `pokenav/left_headers/hoenn_map.png` FR remplace « HOENN MAP » par « VUE ». Intentionnel ? À vérifier en jeu.

## Ce qui n'a pas pu être vérifié visuellement (honnêteté)

- **Rien n'a été vu en jeu** : tous les rendus utilisent la palette du PNG (pas les `.pal`/`.gbapal` ni les numéros de palette des tuiles).
  Les défauts de couleur ou les pixels résiduels sont donc incertains.
- **Planches-contacts non ouvertes** : `battle_environment` (45 images sur 65), `map_preview` (3 sur 21), `rayquaza_scene` (scènes 3 à 5), `intro` (scène 2 : sprites de personnages).
  Seuls les fonds, aperçus de terrain et sprites de ces dossiers n'ont pas été vus ; le risque de texte y est faible.
  Les polices (`fonts/*.png`) n'ont pas été relues glyphe par glyphe.
- **Tilesets regardés en x2 seulement**, avec zoom x3 sur les zones de panneaux.
  De petits textes illisibles restent possibles : plaques de `petalburg_gym`, tableau de `battle_frontier_ranking_hall`, lettre « F » des indicateurs d'étage des grands magasins.
- **Dossiers exclus vus seulement par échantillon** : ~100 images tirées au hasard, plus `object_events/pics/misc` en entier et 28 icônes d'objets.
- **Tilemaps non rendues ou mal rendues** :
  - trade, berry_crush, dodrio, wallclock, evolution_scene, starter_choose, cable_car, trainer_hill, wonder_card/news : seules les planches ont été vues ;
  - le titre « TRAINER CARD » de `trainer_card/*.bin` sort brouillé dans mon rendu (décalage d'index), en EN comme en FR ;
  - `oak_speech/controls_guide_page_*.bin` n'est rendu que partiellement ;
  - le `.bin` affine de `frontier_pass` n'est pas rendu.
- **Accessibilité des écrans** : je n'ai pas déterminé quelles cartes et quels tilesets sont réellement utilisés par HnS (les tilesets Hoenn sont peut-être inutilisés).
  Je ne sais pas non plus si Concours, Roulette, Pokéblocs, Zone de combat, Salle Union et mini-jeux en lien sont accessibles. Le TSV indique seulement s'ils sont compilés.
- **Graphies officielles** : la traduction attendue (graphies Émeraude FR / SoulSilver FR) n'a pas été comparée. Le statut dit seulement si l'image est encore en anglais.
