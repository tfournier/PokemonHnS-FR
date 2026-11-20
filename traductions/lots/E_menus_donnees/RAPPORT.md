# Lot E : menus, données et textes de développement

## Méthode
- Entrée : `a_traduire.json`, soit 1 167 msgid. Pour chacun, j'ai lu le code dans `build/upstream_orig` : structure, taille des tableaux `char[]`, largeur des fenêtres, `{CLEAR_TO}`, police, concaténation.
- Terminologie : pour Gen 1-4, graphie du .po (sources SoulSilver FR et Émeraude FR officiel). Au-delà de la Gen 4, noms officiels FR : patch FR (dont les noms d'objets correspondent à Poképédia), vérifiés sur Poképédia quand j'avais un doute. Espèces en capitales sans accent, comme la banque 237 (EVOLI, DEMOLOSSE…).
- Contrôles automatiques sur 100 % des entrées, faits par mon script puis par `outils/verifier.py` :
  - mêmes codes que l'anglais, charmap, débuts et fins de chaîne ;
  - nombre de lignes ;
  - tableaux `char[]` : animations du visualiseur ≤ 23 caractères, fonds ≤ 27, météo ≤ 23 ;
  - champs à longueur fixe : catégorie 12, lieu 16, Dresseur 10, Frontier 7, Mont Dresseurs 7 (seuil du contrôle), surnom 10, DO 7 ;
  - largeurs en pixels :
    - menu debug : ≤ 110 px pour les entrées de sous-menu, ≤ 128 px pour les autres ;
    - liste principale du debug de combat : 64 px ; liste secondaire : 19 caractères ;
    - descriptions d'objet : 112 px ;
    - Pokédex : 4 lignes au plus, largeur ≤ max(198 px, largeur maxi de l'anglais), coupure automatique sans séparer un nombre de son unité.
- Recoupement avec les autres lots : 51 msgid de ma liste avaient déjà une traduction de rang supérieur. Je ne les ai **pas** repris (voir plus bas).

## Chiffres
- 907 entrées traduites dans `E_001.json` à `E_007.json` (906 msgid, plus 1 entrée `msgctxt`).
  - 904 en « traduction nouvelle ».
  - 3 en SoulSilver FR officiel : Giovanni, et Major Bob / Maj.Bob (adapté).
- 210 exceptions (`exceptions.json`).
- 51 entrées couvertes ailleurs : 46 par le lot B, 5 par le lot A.
- 8 entrées dans `douteux.json`.
- `verifications.tsv` : 1 125 entrées vérifiées, 37 signalements, dont aucun bloquant réel.
  - 36 ANGLAIS : ce sont des exceptions voulues (noms propres des crédits, pseudos, « Omniscient », « H PIVOT »…).
  - 1 CARACTERE, faux positif : `CATCH{0x5B}: ` → `CAPT.{0x5B}: `.
    - `{0x5B}` est l'octet brut du « % », écrit ainsi dans l'anglais et accepté par preproc.
    - Les outils du projet ne savent pas lire ce jeton : avec « % », le contrôle CODES le signalerait à son tour. J'ai donc gardé le jeton identique à l'anglais.

| Fichier source | À traduire | Traduites (E_*.json) | Exceptions | Couvertes par A/B |
|---|---:|---:|---:|---:|
| src/pokemon_sprite_visualizer.c | 230 | 228 | 2 | 0 |
| src/debug.c | 161 | 150 | 11 | 0 |
| src/battle_debug.c | 142 | 139 | 3 | 0 |
| src/data/credits_hns.h | 136 | 10 | 126 | 0 |
| src/data/trainers_hns.party | 82 | 40 | 0 | 42 |
| src/credits_frlg.c | 59 | 23 | 36 | 0 |
| src/data/pokemon/species_info/gen_1_families.h | 35 | 35 | 0 | 0 |
| src/data/battle_environment.h | 27 | 24 | 3 | 0 |
| src/data/pokemon/species_info/gen_3_families.h | 26 | 26 | 0 | 0 |
| src/scrcmd.c | 25 | 0 | 25 | 0 |
| src/data/trainers_frlg.party | 24 | 21 | 0 | 3 |
| src/data/pokemon/species_info/gen_8_families.h | 22 | 22 | 0 | 0 |
| src/pokedex_plus_hgss.c | 21 | 21 | 0 | 0 |
| src/trainer_tower_sets.c | 18 | 18 | 0 | 0 |
| src/data/trade.h | 18 | 18 | 0 | 0 |
| src/data/battle_frontier/trainer_hill.h | 18 | 18 | 0 | 0 |
| src/data/items.h | 15 | 10 | 0 | 5 |
| src/data/pokemon/species_info/gen_6_families.h | 12 | 12 | 0 | 0 |
| src/data/pokemon/species_info/gen_5_families.h | 11 | 11 | 0 | 0 |
| src/data/pokemon/species_info/gen_7_families.h | 10 | 10 | 0 | 0 |
| src/field_weather.c | 9 | 9 | 0 | 0 |
| src/data/pokemon/species_info/gen_4_families.h | 9 | 9 | 0 | 0 |
| src/data/moves_info.h | 8 | 8 | 0 | 0 |
| src/data/pokemon/species_info/gen_2_families.h | 8 | 8 | 0 | 0 |
| src/data/pokemon/species_info/gen_9_families.h | 7 | 6 | 1 | 0 |
| src/pokemon_summary_screen.c | 5 | 5 | 0 | 0 |
| src/data/region_map/region_map_sections.json | 5 | 4 | 1 | 0 |
| src/data/script_menu.h | 4 | 4 | 0 | 0 |
| src/battle_controller_player.c | 3 | 2 | 1 | 0 |
| src/dexnav.c | 3 | 3 | 0 | 0 |
| src/battle_controller_oak_old_man.c | 2 | 2 | 0 | 0 |
| src/pokenav_main_menu.c | 2 | 2 | 0 | 0 |
| data/text/fame_checker_frlg.inc | 2 | 2 | 0 | 0 |
| src/battle_message.c | 1 | 1 | 0 | 0 |
| src/battle_z_move.c | 1 | 1 | 0 | 0 |
| src/field_specials.c | 1 | 0 | 1 | 0 |
| src/start_menu.c | 1 | 1 | 0 | 0 |
| src/data/abilities.h | 1 | 1 | 0 | 0 |
| src/data/debug_trainers.party | 1 | 1 | 0 | 0 |
| data/text/new_game_intro_frlg.inc | 1 | 0 | 0 | 1 |
| src/data/battle_frontier/battle_frontier_trainers.h | 1 | 1 | 0 | 0 |
| **Total** | 1167 | 906 | 210 | 51 |

## Entrées couvertes par d'autres lots (non reprises ici)
- **Lot B, `noms.json`** : 46 noms de Dresseurs de `trainers_hns.party` présents dans la banque 729 de SoulSilver FR.
  - Exemples : MIKEY → Mandé, PROTON → Lance, ARCHER → Amos, PETREL → Lambda, EUSINE → Eusine, CASSIE → Claudia, LORI → Sonja, EDNA → Edna, NICOLE → Stéfie…
  - Ma liste initiale les classait « absents d'HGSS » parce que la banque 729 était compressée. Je ne les ai pas dupliqués.
- **Lot A, `adapte.json`** : 5 descriptions d'objets officielles d'Émeraude FR (Multi Exp, CT Flash, Clé Sous-Sol, Météorite, Carte Magn.).
- **Lot B, `douteux.json`** : homonymes d'une autre classe dans SoulSilver (CODY, GREGG, ETHEL, TREVOR, THOM & KAE, CONNOR).
  - Dans `E_*.json`, je garde le nom (casse SoulSilver).
  - L'homonyme SoulSilver est proposé dans `douteux.json`.
  - GIOVANNI → Giovanni est sûr : c'est le même personnage. Je l'ai pris.

## Choix principaux
- **Noms de Dresseurs absents de SoulSilver** (party, Frontier, Mont et Tour Dresseurs, échanges) : nom conservé, avec la casse SoulSilver (« Mikaela », « Jos & Anne »), comme les noms déjà traduits du .po.
  - Adaptations :
    - LORELEI → Olga ;
    - SAMSON OAK → Samson (Samson Chen fait 11 caractères, plus que les 10 permis) ;
    - MILKMAN → Laitier ;
    - JOHN DOE → Dupont ;
    - MS. NIDO → Mlle Nido ;
    - DUDUNSPARC → Deusolourd (nom FR tronqué à 10 lettres, comme l'anglais) ;
    - REGINALD → Renaud et CORNELIA → Coralie : seuil de 7 du contrôle Mont Dresseurs. Le tableau du code en permet 10 : à rétablir si le contrôle est corrigé ;
    - Debugger → Débogueur.
  - **LTSURGE** : même anglais, deux longueurs :
    - sans contexte : « Major Bob » (trainers_hns.party, 10 max) ;
    - `msgctxt` = `src/data/battle_frontier/battle_frontier_trainers.h` : « Maj.Bob » (7 max).
- **Shiny = Brillant** : terme d'Émeraude FR dans le visualiseur et le debug. **Frontier Pass = Passe Zone** et **Battle Points = Points de combat** (Émeraude FR). **VS Seeker = Cherche VS**.
- **Visualiseur de sprites** : lexique compact et constant, pour tenir dans le tableau de 23 caractères :
  - VIBRE, GLISSE, RESSORT, TREMBLE, ÉTIRE, HALO (pour glow), x2 (pour twice), RAP./RAPIDE, LENT ;
  - H/V gardés (horizontal/vertical).
- **Debug** : « Bascule {STR_VAR_1}… » pour Toggle. `{STR_VAR_1}` est un code couleur qui colore le libellé.
  - Libellés positifs (« Sans collision », « Dress. aveugles »), car la couleur montre l'état.
  - Sigles techniques gardés : IV, EV, ROM, EWRAM, GBS, flag/var.
- **Pokédex** (135 descriptions Méga/Gigamax/formes) : traduction nouvelle dans le style des descriptions officielles, unités converties.
  - 3 600 °F → 2 000 degrés, 32 ft → 10 mètres, 880 lbs → 400 kg, 30 miles → 50 km.
  - Le « ° » n'est pas dans la charmap.
  - Deux textes anglais portent un reste parasite « crescent. » (Méga-Drattak, Méga-Lockpin). Je ne l'ai pas traduit, et c'est signalé dans la note.
- **Crédits Rouge Feu/Vert Feuille et Heart & Soul** : rubriques traduites, structure des `\n` conservée ligne pour ligne. Noms de personnes, pseudos, organismes et projets gardés tels quels.
  - Remarque : Émeraude FR officiel laissait ses crédits en anglais (cf. lot A, `douteux.json`). Le brief demandant de tout traduire, j'ai traduit les rubriques.

## Exceptions (`exceptions.json`, 210)
- 162 noms de personnes, pseudos, organismes et projets des crédits : 126 dans credits_hns.h, 36 dans credits_frlg.c. On y trouve aussi le titre « POKéMON HEART & SOUL » et les rubriques « Sprites » et « Gameplay », anglicismes d’usage en français.
- 25 noms de `scrcmd.c` (`sOddEggShinyNameList`) : comparés **à l'octet près** au nom saisi par le joueur pour rendre l'Œuf Mystère chromatique. Les traduire casse l'easter egg.
- `SampleCode` : code comparé à une saisie du joueur (`GetCodeFeedback`).
- Mots identiques en français : Types, Stats, Omniscient, Script 1-8, Scripts…, « cycles », lignes IV/EV du debug.
- Sigle « XL » (taille d'ombre, tableau de 4), « H PIVOT ».
- Magma, Aqua (noms d'équipes), Koga, SINJOH (nom officiel SoulSilver FR).
- Catégorie « Olive » (officielle FR : « Pokémon Olive »).

## Termes nouveaux proposés pour le glossaire (anglais → français officiel, source)
| Anglais | Français | Type | Vérification |
|---|---|---|---|
| Terrain Extender | Champ’Duit | objet | Poképédia |
| Clear Amulet | Talisman Sain | objet | Poképédia |
| Mirror Herb | Feuille Copieuse | objet | Poképédia |
| Covert Cloak | Cape Obscure | objet | Poképédia |
| Adrenaline Orb | Orbe Frousse | objet | Poképédia |
| Berserk Gene | ADN Berzerk | objet | Poképédia (OAC FR) ; **le patch FR donne « GENE BERSERK »** |
| Room Service | Chariot Distordu | objet | patch FR = Poképédia |
| Kee / Maranga Berry | Baie Éka / Baie Rangma | objet | patch FR |
| G-Max Steelsurge | Percée G-Max | capacité | Poképédia (Gigamax) ; **le patch FR donne « G-MAX PICS Fer »** |
| Bloom Doom | Pétalexplosion Éblouissante | capacité Z | Poképédia |
| Twinkle Tackle | Impact Choupinova | capacité Z | Poképédia |
| Shattered Psyche | Psycho-Pulvérisation EX | capacité Z | Poképédia |
| Inferno Overdrive | Pyro-Explosion Cataclysmique | capacité Z | Poképédia (patch : « PY. CATACLYSMIQUE ») |
| Never-Ending Nightmare | Appel des Ombres Éternelles | capacité Z | Poképédia |
| Black Hole Eclipse | Trou Noir des Ombres | capacité Z | Poképédia |
| Tectonic Rage | Éruption Géo-Sismique | capacité Z | Poképédia |
| Soul-Stealing 7-Star Strike | Fauche-Âme des Sept Étoiles | capacité Z | Poképédia |
| Malicious Moonsault | Dark Body Press | capacité Z | Poképédia |
| Clangorous Soulblaze | Dracacophonie Flamboyante | capacité Z | Poképédia |
| Snuggle Forever | Patati-Patattrape | capacité Z | Poképédia |
| High King (catégorie) | Empereur | catégorie | Poképédia (Sylveroy Cavalier du Froid) |
| Double Jaw (Méga-Aligatueur) | Mâchoire | catégorie | Dexerto/Pokébip (Légendes Z-A) |
| Olive (catégorie) | Olive | catégorie | Pokébip, Pokemondb |
| Melemele | Mele-Mele | lieu | officiel Soleil/Lune, cf. « ILE DE MELE-MELE » déjà au .po |
| Mt. Lanakila | Mont Lanakila | lieu | officiel Soleil/Lune (l'anglais du jeu a une coquille : LANIKALA) |
| Olivine Lighthouse | Phare d’Oliville | lieu | SoulSilver FR |
| Ultra Space | Ultra-Dimension | terme | Soleil/Lune FR |
| Lorelei | Olga | personnage | Rouge Feu/Vert Feuille FR |
| Sidney / Phoebe / Glacia | DAMIEN / SPECTRA / GLACIA | personnage | Émeraude FR |
| Bruno / Karen | Aldo / Marion | personnage | SoulSilver FR |
| Frontier Pass | Passe Zone | objet | Émeraude FR (dialogues officiels) |
| VS Seeker | Cherche VS | objet | patch FR / Rouge Feu FR |
| Tera Type | Téra-type | terme | Écarlate/Violet FR |
| Move Tutor (résumé) | Moniteur (« RAPPEL MONIT. ») | terme | usage officiel FR |

## Doutes (`douteux.json`)
- Six homonymes SoulSilver FR d'une autre classe (voir plus haut), à choisir entre le nom conservé et le nom SoulSilver.
- « Imposing » (catégorie de Méga-Draïeul, Légendes Z-A Méga-Dimension) → « Imposant » : catégorie officielle FR non trouvée.
- Non mis dans `douteux.json` mais à relire :
  - « Drill » → « Perceur » (fond du visualiseur, déjà au .po), que j'ai suivi : « Perceur - Concours » ;
  - les intitulés des crédits Rouge Feu/Vert Feuille (pas de source officielle FR accessible) ;
  - « MER DE MELE-MELE » (16 caractères, la limite).

## Même anglais, sens différents
- **LTSURGE** : nom de Dresseur (10) et nom de Dresseur Frontier (7). Une entrée `msgctxt`, déjà décrite plus haut.
- **CHOW** → « Quentin » (SoulSilver, lot B) et **QUENTIN** → « Quentin » : deux Dresseurs différents porteront le même prénom FR. Acceptable, mais à savoir.
- **TIM** : DO d'un échange (7 max) et nom de Dresseur → « Tim » convient aux deux.
- **CASSIE**, **GIOVANNI**, **LORELEI** servent aussi dans le Fame Checker et l'intro de Rouge Feu (non compilés) : même traduction partout.
- **Sayu** et **Brick** : à la fois crédits et liste de l'Œuf Mystère, donc exceptions (inchangés).

## Problèmes repérés dans les .po existants (à corriger par l'agent principal)
1. **Œuf Mystère chromatique** (`src/scrcmd.c`, `sOddEggShinyNameList`) : plusieurs pseudos ont été « traduits ». L'easter egg est alors cassé : le joueur devrait saisir « Olwen » au lieu de « Anthony ». Il faut garder l'anglais.
   - « Anthony » → Olwen, « RAINBOW » → Rainbow, « Cameron » → Gwen ;
   - « Casper » → Casey : c'est aussi un pseudo des crédits HnS ;
   - « DYLAN » → REGIS : msgid partagé avec trainers.party, il faudrait un `msgctxt` pour scrcmd.c.
2. **Crédits Rouge Feu/Vert Feuille** : noms décalés.
   - « Satoshi Tajiri » → Shusaku Egami, « Satoru Iwata » → Hiroaki Tsuru, « Tsunekaz Ishihara » → Satoshi Tajiri.
   - De plus, les `\n` de structure ont été supprimés.
3. `Psychic` → « Kinésiste » (menus.po, visualiseur) : c'est le fond Psy. contextes.po corrige déjà en « Psy ».
4. `Grass` → « PLANTE » (battle_environment, environnement « herbe » traduit comme le type). `Drake` → « Drake » alors que le nom Hoenn d'Émeraude FR est en capitales (DRAKE).
5. Les noms du patch FR « GENE BERSERK » et « G-MAX PICS Fer » contredisent les noms officiels : ADN Berzerk, Percée G-Max.
6. Lot A, `douteux.json` : « Summons hail in battle. » → « Invoque la pluie en combat. » est faux. Ma version : « Invoque la grêle en combat. ».
7. `Morning` / `Evening` / `Night` (debug.c, pokedex_plus_hgss.c) sont restés en anglais dans menus.po.
