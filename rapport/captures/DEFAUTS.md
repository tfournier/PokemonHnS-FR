# Défauts visibles relevés en émulateur (lot G)

ROM testée : `build/pokehns_fr.gba` du 20/11 à 16:23, copiée avant les tests. Captures produites
par `outils/emulateur/lancer_tests.sh` (9 scénarios, 471 captures, environ 23 s).
Les chemins de la colonne Capture sont relatifs à `rapport/captures/`.

Gravité : **haute** (anglais visible, texte faux, coupé ou illisible), **moyenne** (terminologie
ou style contraires aux consignes §3, registre), **basse** (accent manquant sur une capitale,
typographie).

## Tableau des défauts

| # | Capture | Écran | Texte vu | Problème | Gravité |
|---|---|---|---|---|---|
| 1 | 08_menu_start/20_pokedex_zone.png | Pokédex, onglet ZONE | `INFO AREA STATS EVO CRY SIZE` | Bandeau d'onglets en anglais (image) sur la page ZONE ; les autres pages affichent bien INFO ZONE STATS EVO CRI TAIL. | haute |
| 2 | 03_combat_sauvage/05_capacites.png, 09_combat_dresseur/22_capacites.png | Combat, liste des capacités | `START MOVE INFO` | Bouton en anglais (image) | haute |
| 3 | 02_debut_aventure/60_surnom_clavier.png | Clavier du surnom | `HERICENDRESurnom de ?` | Chaîne suffixe traduite comme une phrase : nom collé devant « Surnom de ? ». Il faut un texte qui suive le nom (ex. « : surnom ? ») ou revoir le code | haute |
| 4 | 03_combat_sauvage/06_capacites_infos.png, 09_combat_dresseur/23_capacites_infos.png | Combat, infos de capacité (START) | `CAT: … PUIS: 40 PREC: 10` | Précision 100 affichée « 10 » : le 3ᵉ chiffre est coupé par le bord de la fenêtre (libellés trop larges). PRÉC sans accent | haute |
| 5 | 08_menu_start/29_equipe.png, 33_resume_infos.png, 03_combat_sauvage/13_equipe_combat.png | Équipe, résumé | `Lv6` | Glyphe « Lv » non remplacé par « N. » (il l'est en combat : « N.5 ») | haute |
| 6 | 08_menu_start/24_pokedex_evo.png | Pokédex EVO | `FEURISSON: Lv↑14.`, `TYPHLOSION: Lv↑36, sur Sinjoh.` / `TYPHLOSION-H: … en Sinjoh.` | « Lv » au lieu de « N. » ; « sur Sinjoh » / « en Sinjoh » incohérents | haute |
| 7 | 08_menu_start/34_resume_aptitudes.png, 35, 36 | Résumé, page APTITU. | `ATQ. SP`, `DEF. SP`, `VITESS` | Libellés tronqués et chevauchés par les valeurs ; DEFENSE sans accent | haute |
| 8 | 01_titre_intro/53_modes_difficulte_fin.png | Réglages de partie, DIFFICULTÉ | `EV DRESSEURS  NÉCHELLDIFFICILE` | Les trois valeurs NON / ÉCHELLE / DIFFICILE se superposent, illisible | haute |
| 9 | 01_titre_intro/49_modes_nuzlocke.png | Réglages, NUZLOCKE | `NONFACILE NORMAL` | Valeurs collées (pas d'espace) | haute |
| 10 | 01_titre_intro/09_options_soin_rapide.png, 10_options_fenetre.png | Options | `METRIQUEIMPÉRIAL` | Valeurs collées ; MÉTRIQUE sans accent | haute |
| 11 | 06_boutique/06_liste_achat.png (et 09 à 19) | Boutique, liste d'achat | `MONEY ₽3000` | Étiquette « MONEY » en anglais (image), Émeraude FR : ARGENT | haute |
| 12 | 08_menu_start/55_pokematos_condition_equipe.png | Pokématos, CONDITION | `CANCEL` | Bouton en anglais (image) ; BEAUTE, GRACE sans accent | haute |
| 13 | 08_menu_start/22_pokedex_stats_a.png | Pokédex STATS (A) | `Field` | Groupe d'œufs en anglais ; AMITIE, PAS ECLOS. sans accent | haute |
| 14 | 08_menu_start/21_pokedex_stats.png | Pokédex STATS | `CATCH%: TRES DIFF.`, `ATT DEF A.SP D.SP VIT`, `POUVOI✱ 18 PRECIS. 80` | « CATCH% » en anglais ; abréviations des stats différentes des consignes (PV AT DF AS DS VI, utilisées sur la liste du Pokédex) ; « POUVOIR » tronqué par l'icône ; TRES, PRECIS. sans accent | haute |
| 15 | 08_menu_start/19_pokedex_info.png | Pokédex INFO | `Souris Feu Pokémon` | Ordre anglais, il faut « Pokémon Souris Feu » (Orme le dit bien en 02/56) | haute |
| 16 | 01_titre_intro/12_options_combat_bas.png | Options de combat, BALL RAPIDE | `changer de ᴾᴷᴹᴺBALL.` | Glyphe {PKMN} au lieu de {POKE} (« Poké Ball »), collé à BALL ; « lancer une BALL » | moyenne |
| 17 | 08_menu_start/01_menu_start.png | Menu START | `Pokédex`, `Pokémon` | Consignes : POKéDEX, POKéMON en capitales comme les autres entrées (SAC, SAUVER…) | moyenne |
| 18 | 03_combat_sauvage/04_menu_combat.png, 09_combat_dresseur/21 | Menu de combat | `ATTAQUE Sac / POKéMON Fuite` | Casse incohérente (Émeraude FR : ATTAQUE SAC POKéMON FUITE) | moyenne |
| 19 | 02_debut_aventure/52_labo_orme.png, 04_ville_griotte/16_guide.png | Dialogues Orme, guide | `POKéMON contenus dans ces BALLS`, `On y vend des BALLS` | Ancien style POKéMON ; « BALLS » au lieu de « Poké Balls » | moyenne |
| 20 | 07_pokedex/26_dialogue.png, 30, 35 | Dialogue Prof. Chen | `tes POKéMON avec amour`, `les POKéMON vus ou capturés`, `tous les POKéMON` | Ancien style POKéMON (consignes : Pokémon) | moyenne |
| 21 | 05_centre_pokemon/02_infirmiere_bienvenue.png | Centre Pokémon | `Bienvenue au CENTRE POKéMON.` | Ancien style ; « Centre Pokémon » | moyenne |
| 22 | 01_titre_intro/16_intro.png, 07_pokedex/15 à 18 | Introduction, M. Pokémon | `Je m'appelle CHEN.`, `le Prof. CHEN ici présent`, `CHEN: Ah!`, `Je suis CHEN!` | Consignes : « Prof. Chen » (style SoulSilver), pas de capitales | moyenne |
| 23 | 07_pokedex/24_dialogue.png | Dialogue Prof. Chen | `le Prof. ORME t'a confié` | « Prof. Orme » ailleurs | moyenne |
| 24 | 02_debut_aventure/62_orme_m_pokemon.png, 63 | Dialogue Orme | `VILLE GRIOTTE` | Lieux en minuscules avec majuscule initiale : « Ville Griotte » | moyenne |
| 25 | 02_debut_aventure/18_maman.png, 19 | Dialogue Maman | `CHAUSSURES DE SPORT` | Objet en capitales (style Émeraude) | moyenne |
| 26 | 02_debut_aventure/05_horloge_info_options.png ; 01_titre_intro/54_modes_defis.png | Info horloge ; DÉFIS | `CENTRE Pokémon`, `OBJETS RARES du Sac`, `CENTRES ᴾᴷᴹᴺ` | Casse mixte, style incohérent | moyenne |
| 27 | 01_titre_intro/35_reglages_info.png | Introduction (Orme) | `Quel défi vous tente?` | Le professeur tutoie juste avant (« Tu t'appelles Max? ») : registre incohérent | moyenne |
| 28 | 01_titre_intro/04 à 13 | Options | `ANIMAT. Combat`, `STYLE Combat`, `Combat RAPIDE`, `DECORS DE Combat`, `Surf AUTO`, `Soin RAPIDE`, `MUSIQUE Surf`, `Turbo` | Casse mixte dans des libellés en capitales (remplacement automatique « Combat », « Surf », « Soin » ?) | moyenne |
| 29 | 08_menu_start/57_pokematos_appels_liste.png | Pokématos, APPELS | `Prof.ᴾᴷᴹᴺ   Orme`, `Nb dresseurs:` | Classe « Prof. Pokémon » rendue par le glyphe PKMN collé ; « Dresseurs » sans majuscule | moyenne |
| 30 | 08_menu_start/25_pokedex_cri.png | Pokédex CRI | `CRI DE HERICENDRE` | Élision : « CRI D'HÉRICENDRE » | moyenne |
| 31 | 08_menu_start/42 à 49 | Sac | `OBJETS`, `OBJ. RARES` / `Soins`, `Poké Balls`, `Baies`, `CT & CS` | Casse des noms de poches incohérente ; 02/74 à 80 « POCHE Soins », 07/10 « POCHE OBJ. RARES. » | moyenne |
| 32 | 01_titre_intro/50_modes_nuzlocke_fin.png | Réglages, NUZLOCKE | `K.O.  TOMBE  RELÂCHER` | « TOMBE » obscur (sans doute « mort »/« K.O. » du Pokémon) | moyenne |
| 33 | 01_titre_intro/54 à 56 | Réglages, DÉFIS | `R SAUVE`, `Sauver` | Abréviation tronquée, casse mixte | basse |
| 34 | 07_pokedex/08_dialogue.png à 12 | M. Pokémon | `Oeuf Mystère`, `cet OEUF` | « Œuf » (si le jeu de caractères le permet) ; casse incohérente | basse |
| 35 | 08_menu_start/19_pokedex_info.png | Pokédex INFO | `HAUT. 0.5 m`, `POIDS 7.9 kg.` | Point décimal (FR : virgule) ; point après « kg » | basse |
| 36 | 08_menu_start/61_carte_dresseur_recto.png | Carte Dresseur | `ARGENT ₽3000/0`, `N°ID /28947` | « /0 » et « / » parasites ; DUREE JEU sans accent | basse |
| 37 | 05_centre_pokemon/16 à 32 | PC | `DEPLACER Pokémon`, `DEPOSER Pokémon`, `BOITES`, `BOITE 1`, `DONNEES`, `EQUIPE ᴾᴷᴹᴺ`, `FERMER BOITE`, `DECONNEXION`, `BOITE LETTRE`, `ETEINDRE` | Accents manquants (É, Î) ; casse mixte « DEPLACER Pokémon » | basse |
| 38 | 01_titre_intro/04 à 13 | Options | `DEFINI`, `PECHE FACILE`, `UNITES`, `FENETRE`, `MUSIQUE VELO`, `DECORS`, `L'INFIRMIERE` | Accents manquants sur capitales (alors que STÉRÉO, IMPÉRIAL, GÉN. en ont) | basse |
| 39 | 08_menu_start/30_equipe_sousmenu.png, 33 à 38 | Équipe, résumé | `RESUME`, `CAPACITE SPE.`, `MEMO DRESSEUR`, `CAPACITES COMB.`, `CAPACITES CONC.` | Accents manquants | basse |
| 40 | 08_menu_start/15_pokedex_recherche.png, 27_pokedex_taille.png | Pokédex | `INDIFFERENT`, `MODE NUMERIQUE`, `TAILLE COMPAREE A Max` | Accents manquants | basse |
| 41 | 08_menu_start/51_pokematos.png, 63 à 65 | Pokématos, Sauver | `ETEINDRE`, `DUREE JEU`, `NE PAS ETEINDRE` | Accents manquants | basse |
| 42 | 09_combat_dresseur/61_combat.png | Montée de niveau | `DEFENSE`, `ATQ. SPE.`, `DEF. SPE.` | Accents manquants | basse |
| 43 | 05_centre_pokemon/38_pc_defis4.png | PC, DÉFIS | `PHYSIQUE ou SPECIALE dépend de la CAPACITE.` | Accents manquants | basse |
| 44 | 06_boutique/22_au_revoir.png | Boutique | `A la prochaine!` | « À » | basse |
| 45 | 01_titre_intro/30_clavier_majuscules.png | Clavier | `DEPL.` ; pas de lettres accentuées | DÉPL. ; le clavier (non traduit, consigne §4) ne permet pas de saisir de nom accentué | basse |
| 46 | 02_debut_aventure/56_starter_choix.png et partout | Espèces | `HERICENDRE`, `FEURISSON` | Sans accent (SoulSilver : HÉRICENDRE) : à confirmer selon le choix du glossaire | basse |
| 47 | 04_ville_griotte/12_guide.png à 16 | Ville Griotte (décor) | toits `MART`, `P.C` | Enseignes en anglais dans les tuiles : à vérifier par rapport à Émeraude FR | basse |

Aucun caractère carré, aucune lettre cyrillique ni tuile cassée n'a été vu sur ces écrans.
Le message « HERICENDRE: D » (09/36, 09/42) est une capture prise pendant l'affichage
progressif, pas un défaut.

## Écrans de la définition de « terminé » non atteints ou incomplets

| Écran | Raison |
|---|---|
| Saisie d'un nom avec accents | Le clavier n'a pas de lettres accentuées (trois pages : majuscules, minuscules, chiffres et symboles). Nom saisi : « Max » |
| Pokématos : application Radio | Cette version n'a que CARTE, CONDITION et APPELS (capturés). Un appel sortant n'affiche que « …… » à cet endroit |
| Carte Dresseur, verso | Atteint mais vide à ce stade du jeu (aucune donnée à afficher) |
| Pokédex : résultats d'une recherche | Écran de recherche, tri et choix du nom capturés ; la recherche n'a pas été lancée (seulement 4 espèces vues) |
| PC : écrans de stockage d'objets et de la boîte aux lettres | Menus capturés, sous-écrans non ouverts (aucun objet ni lettre) |
| Combat : changement de Pokémon, capture, messages de statut (PSN, PAR…) | Une seule créature dans l'équipe, aucune Poké Ball, aucun statut infligé dans ces combats |
| Écran titre : « Appuyez sur START » | Aucun texte visible sur l'écran titre capturé (02_ecran_titre.png) : à vérifier s'il clignote ou n'existe pas |
