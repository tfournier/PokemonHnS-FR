# Rapport — traduction française de Pokémon Heart & Soul (Release-v2.0.6)

Rapport généré par `outils/rapport.py`. Détails : `DECISIONS.md`, `rapport/ETAT_DES_LIEUX.md`, `rapport/relectures/`, `rapport/integrations/`, `rapport/images/RAPPORT.md`, `rapport/captures/`.

## Textes par source

| Source | dialogues | menus | donnees | contextes | Total |
|---|---|---|---|---|---|
| Émeraude FR officiel | 7022 | 1918 | 4685 | 36 | **13661** |
| Émeraude FR officiel (adapté) | 86 | 200 | 134 | 9 | **429** |
| SoulSilver FR officiel | 1494 | 457 | 897 | 233 | **3081** |
| SoulSilver FR officiel (adapté) | 441 | 27 | 26 | 2 | **496** |
| patch FR existant (vérifié) | 381 | 39 | 1200 | 0 | **1620** |
| patch FR existant | 1503 | 727 | 2916 | 0 | **5146** |
| traduction nouvelle ou manuelle | 3844 | 1040 | 1154 | 259 | **6297** |
| gardé tel quel (exception) | 80 | 119 | 260 | 8 | **467** |
| sans source | 3 | 1 | 1 | 7 | **12** |
| **Total** | 14854 | 4528 | 11273 | 554 | **31209** |

## Construction et contrôles

- Construction : `./build.sh` (make hns) — traduit: 38071 ; non traduit: 2.
- `rapport/trop_longs.txt` : 0 texte(s) remis en anglais faute de place.
- `rapport/images_a_revoir.txt` : 0 image(s) modifiée(s) par HnS depuis notre traduction.
- Contrôles automatiques (`outils/verifier.py`, 100 % des entrées) : aucune alerte.
- Chaînes anglaises de la ROM de référence encore présentes (`outils/controle_anglais.py`) : 454, dont 192 identifiants du test sonore (exception) ; le détail est dans `rapport/anglais_restant.tsv`.
- Test aller-retour (`outils/test_aller_retour.py`, msgstr = msgid) : ROM identique à la référence (dernier passage consigné dans l’historique git).

## Relectures ChatGPT

| Lot | Remarques | Acceptées | Refusées | À arbitrer / vérifier |
|---|---|---|---|---|
| A_emeraude | 17 | 2 | 15 | 0 |
| A_emeraude_alignement | 10 | 0 | 0 | 0 |
| B_soulsilver | 179 | 9 | 170 | 0 |
| B_soulsilver_alignement | 15 | 0 | 0 | 0 |
| C_audit | 2497 | 2275 | 40 | 182 |
| D1_dialogues | 81 | 73 | 8 | 0 |
| D2_dialogues | 134 | 123 | 11 | 0 |
| D3a_dialogues | 90 | 81 | 9 | 0 |
| D3b_dialogues | 117 | 85 | 32 | 0 |
| D4_dialogues | 118 | 113 | 5 | 0 |
| E_menus_donnees | 171 | 166 | 5 | 0 |

## Images traduites

170 fichiers (images et tilemaps) dans `images/`, par dossier : data/tilesets (11), graphics/bag (3), graphics/battle_frontier (1), graphics/battle_interface (13), graphics/berry_blender (2), graphics/contest (4), graphics/easy_chat (2), graphics/fonts (9), graphics/frontier_pass (3), graphics/interface (3), graphics/link (1), graphics/naming_screen (4), graphics/object_events (2), graphics/party_menu (1), graphics/pokeblock (3), graphics/pokedex (25), graphics/pokemon_jump (2), graphics/pokemon_storage (1), graphics/pokenav (37), graphics/shop (2), graphics/slot_machine (3), graphics/summary_screen (1), graphics/title_screen (2), graphics/trade (1), graphics/trainer_card (4), graphics/types (25), graphics/union_room_chat (3), graphics/voltorb_flip (2).

Détail image par image, méthode et vérification : `rapport/images/RAPPORT.md`.

## Exceptions (textes gardés tels quels)

- credits_hns.h (124) : générique : nom de personne, pseudo, organisme ou projet (nom propre conservé)
- credits.h (48) : générique d’Émeraude : Émeraude FR garde cette ligne en anglais (rubriques et noms) ; gardé tel quel, comme « 
- credits_frlg.c (36) : générique : nom de personne, pseudo, organisme ou projet (nom propre conservé)
- scrcmd.c (25) : liste des noms de joueur qui rendent chromatique l’Œuf Mystère (comparaison exacte avec le nom saisi, scrcmd.c
- debug.c (7) : menu debug (fenêtre de 17 tuiles ; les sous-menus ajoutent {CLEAR_TO 110}{RIGHT_ARROW} : libellé ≤ 110 px)
- new_game_intro_frlg.inc (3) : nom proposé à l’introduction FRLG : gardé tel quel en capitales, comme les autres noms de ce fichier (KAZ, TOR
- berry_blender.c (2) : texte japonais jamais affiché (tableau marqué Unused, aucune référence) : gardé tel quel ; il contient des kan
- credits_frlg.c (2) : générique FRLG : nom de personne gardé tel quel (mise en page de l’anglais)
- credits.h (2) : générique d’Émeraude : nom propre (personne ou organisme anglophone, propre à la version anglaise) gardé tel q
- credits_hns.h (2) : liste des noms de joueur qui rendent chromatique l’Œuf Mystère (comparaison exacte avec le nom saisi, scrcmd.c
- credits_hns.h (1) : générique HnS : pseudonyme d’une personne, gardé tel quel
- battle_controller_player.c (1) : debug IA : « cycles » (processeur) est identique en français ; suffixe après un nombre
- field_specials.c (1) : code d’exemple comparé au texte saisi par le joueur (GetCodeFeedback) : identifiant fonctionnel, à garder tel 
- pokemon_sprite_visualizer.c (1) : visualiseur de sprites (debug), nom d’animation de dos, tableau gBackAnimNames[24] : 23 caractères max ; H/V =
- pokemon_sprite_visualizer.c (1) : visualiseur de sprites, taille d’ombre (tableau [4]) : sigle de taille identique en français
- battle_debug.c (1) : menu debug de combat, liste principale (fenêtre de 9 tuiles, ~64 px utiles) : mot identique en français
- battle_debug.c (1) : menu debug de combat, liste principale (fenêtre de 9 tuiles, ~64 px utiles) : abréviation identique en françai
- battle_debug.c (1) : menu debug de combat, liste secondaire (tampon de 19 caractères, PadString) : drapeau de l’IA : mot identique 
- debug.c (1) : menu debug, fenêtre de saisie numérique : texte avant {CLEAR_TO 90} ≤ 90 px, colonnes conservées ; IV = sigle 
- debug.c (1) : menu debug, fenêtre de saisie numérique : texte avant {CLEAR_TO 90} ≤ 90 px, colonnes conservées ; EV = sigle 
- debug.c (1) : menu debug (fenêtre de 17 tuiles ; les sous-menus ajoutent {CLEAR_TO 110}{RIGHT_ARROW} : libellé ≤ 110 px) : «
- debug.c (1) : menu debug (fenêtre de 17 tuiles ; les sous-menus ajoutent {CLEAR_TO 110}{RIGHT_ARROW} : libellé ≤ 110 px) : m
- battle_environment.h (1) : nom d’environnement de combat (champ .name, affiché en debug) ; nom d’équipe (Team Magma) identique en françai
- battle_environment.h (1) : nom d’environnement de combat (champ .name, affiché en debug) ; nom d’équipe (Team Aqua) identique en français
- battle_environment.h (1) : nom d’environnement de combat (champ .name, affiché en debug) ; Koga (SoulSilver FR)
- gen_9_families.h (1) : catégorie Pokédex (Olivini) : catégorie officielle FR « Pokémon Olive » (EV), identique à l’anglais
- region_map_sections.json (1) : nom de lieu (carte) : Ruines Sinjoh, « Sinjoh » est le nom officiel SoulSilver FR
- Identifiants du test sonore (MUS-…, SE-…, 192 chaînes) : générés à partir des noms de constantes du code, non traduisibles sans modifier le code ; écran de débogage.
- Code `{KUN}` (suffixe japonais) omis par les textes officiels français ; claviers (`src/text_input_strings.c`) non traduits volontairement.

## Points à valider par un humain

Ces points ont été tranchés provisoirement ; un œil humain (idéalement avec les jeux officiels) est utile.

**Noms sans source officielle vérifiée**
- Rouge Feu / Vert Feuille (cartes FRLG non compilées) : GARY → REGIS (nom du dessin animé), CRUSHER → COGNEUR,
  CHARINE gardé, devises des îles Sevii (sous-titres Poképédia, texte exact des panneaux non vérifié),
  « Kanto Angels » (KANTO RIDER FEDERATION), Machine Réseau, Maniaque des Capacités, Maître Pêcheur, Gardien,
  « Ticketaurore », « Sac à Baies », étages du Centre Commercial et de la Sylphe (RDC, 1{SUPER_ER}…),
  Cabane Secrète, Dent d’Or, Zone Centrale (Poképédia/Pokébip, sans capture du jeu) — listes dans
  `traductions/lots/D_dialogues/D*_douteux.json`.
- Catégorie Pokédex « Imposant » (Méga-Draïeul), « Tomberoche » (TOMBSTONY), « Lettre Evoli ».

**Choix de projet à confirmer**
- Décision 14 : pas d'accent sur les majuscules (comme les jeux officiels), cédille gardée.
- Noms des types en capitales (ELECTRIK, TENEBRES, FEE, STELL.).
- Rubriques des crédits HnS traduites alors qu'Émeraude FR laissait les siennes en anglais.
- Noms de Dresseurs homonymes : un nom par fichier (Hoenn = Émeraude FR, Johto/Kanto = SoulSilver FR si c'est le
  même Dresseur, sinon prénom anglais).
- « Points Combat » / « Points de Combat » ; abréviation « PCo » (glyphe BP).

**Écrans non vérifiés en jeu**
- Saisie d'un nom accentué : impossible, le clavier (non traduit par principe) n'a pas de lettres accentuées.
- Pokématos Radio (absente de cette version), verso de la carte Dresseur (vide en début de jeu), capture, changement de
  Pokémon et messages de statut en combat, recherche du Pokédex, sous-écrans du PC (objets, boîte aux lettres).
- Concours, Roulette, Pokéblocs, Zone de combat, machine à sous, Voltorbataille : images traduites mais non vues en jeu.
- Enseignes de toit SHOP / POKé / ARN (3×3 px) : lisibilité à vérifier.
- « N. » dans les polices étroites (ressemble à « n »).
- Bouton « EQUIPE {PKMN} » du stockage PC : origine non identifiée ; « ₽3000/0 » sur la carte Dresseur (argent puis
  épargne de Maman, affichage du code upstream).

**Relecture**
- Relecture ChatGPT des lots C1, C2a, C2b et de 13 paquets de l'audit : différée (limite d'usage du compte), voir
  DECISIONS.md n° 15.

