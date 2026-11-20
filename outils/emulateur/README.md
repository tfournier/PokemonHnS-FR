# Tests en émulateur (lot G)

Lanceur mGBA sans interface, piloté par script, pour rejouer des parcours dans la ROM
française et produire des captures d'écran (`rapport/captures/`).

## Construire

```sh
outils/emulateur/build.sh            # clone mGBA 0.10.5 dans build/mgba-src, compile libmgba
                                     # (statique, sans Qt/SDL/ffmpeg/Lua) dans build/mgba-build,
                                     # puis lie outils/emulateur/hns_run
outils/emulateur/build.sh --propre   # idem, puis supprime les objets intermédiaires de mGBA
```

Dépendances : cmake, un compilateur C, libpng (Homebrew) et zlib (système). Rien d'autre.
`hns_run` tourne à environ 3 700 images/s sur un Mac arm64 (environ 60 fois le temps réel),
et à environ 2 500 images/s quand le scénario calcule des trajets (`goto`).

## Lancer tous les tests

```sh
outils/emulateur/lancer_tests.sh build/pokehns_fr.gba rapport/captures
# options : 3e argument = dossier des états (défaut build/tests_emulateur/etats)
#           SCENARIOS="08_menu_start" pour ne rejouer qu'un scénario
```

Copiez de préférence la ROM dans un dossier de test : elle peut être reconstruite pendant
les tests. Les journaux sont dans `build/tests_emulateur/journaux/`, la sauvegarde de test
(`test.sav`, repartie de zéro au scénario 01) dans le dossier des états, jamais à côté des ROM.

Les scénarios s'enchaînent par états de sauvegarde :

| Scénario | Part de | Produit | Contenu |
|---|---|---|---|
| 01_titre_intro | sauvegarde vide | chambre.ss | écran titre, options (3 pages), discours du professeur, clavier (3 pages + saisie), réglages de partie (6 pages) |
| 02_debut_aventure | chambre.ss | route29.ss | horloge, Maman, laboratoire, starter, surnom, Potion |
| 03_combat_sauvage | route29.ss | avant_combat.ss, apres_combat.ss | premier combat : menu, capacités, infos capacité, Sac, équipe, victoire ; second combat : fuite |
| 04_ville_griotte | apres_combat.ss | griotte.ss | Route 29, visite guidée de Ville Griotte |
| 05_centre_pokemon | griotte.ss | centre.ss | soins, PC (stockage, boîtes, PC du joueur, défis) |
| 06_boutique | griotte.ss | boutique.ss | Acheter/Vendre, prix, quantité, confirmation, vente |
| 07_pokedex | griotte.ss | pokedex.ss | Route 30, M. Pokémon, Prof. Chen, Pokédex |
| 08_menu_start | pokedex.ss | menu_start.ss | menu START et toutes ses entrées |
| 09_combat_dresseur | pokedex.ss | avant_rival.ss | appel du Prof. Orme, combat contre le rival |

États utiles dans `build/tests_emulateur/etats/` : `avant_combat.ss` (dans les herbes de la
Route 29), `menu_start.ss` (menu START ouvert), `centre.ss` (devant l'infirmière),
`boutique.ss` (devant le vendeur), `avant_rival.ss`, etc.

### Rouvrir un état à la main

Les états sont au format de mGBA 0.10.5 (PNG avec l'état intégré) : l'application officielle
les ouvre directement.

```sh
/Applications/mGBA.app/Contents/MacOS/mGBA -t build/tests_emulateur/etats/menu_start.ss build/pokehns_fr.gba
```

La ROM doit être celle qui a servi à produire l'état (ou une ROM dont la RAM est organisée de la
même façon). mGBA charge alors la sauvegarde `.sav` placée à côté de la ROM, sans incidence
sur l'écran affiché.

## Écrire un scénario

Un scénario est un fichier texte `scenarios/NN_nom.txt` (une commande par ligne, `#` pour les
commentaires). Il est joué par `hns_run --rom R --sav S --out DOSSIER --states ETATS fichier.txt`.

| Commande | Effet |
|---|---|
| `wait N` | avance N images |
| `press KEY [H] [W]` | appuie KEY pendant H images (4 par défaut) puis relâche W images (16). KEY : A B SELECT START RIGHT LEFT UP DOWN R L, combinables (`A+B`) |
| `hold KEY N` | maintient KEY N images |
| `repeat N CMD ; CMD2` | répète N fois une ou plusieurs commandes |
| `shot NOM` | capture `<out>/NN_NOM.png` (NN : compteur automatique ; `--x2` ajoute une version agrandie dans `<out>/x2/`) |
| `save F` / `load F` | état de sauvegarde (relatif à `--states`), données de cartouche et horloge comprises |
| `rtc 2026-11-20T10:00` | fixe l'horloge de la cartouche (heure locale), qui avance ensuite avec l'émulation |
| `include F` | joue un autre script (relatif au script courant), ex. `include commun.txt` |
| `posaddr PTR DEC` / `pos` | où lire la position du joueur / l'afficher (HnS : `posaddr 030041d8 4`, dans `commun.txt`) |
| `walk DIR N [W]` | avance de N cases, contrôlé par la position ; signale un blocage |
| `goto CARTE X Y` | marche jusqu'à (X,Y) sur la carte `data/maps/CARTE` ; trajet calculé par `chemin.py` à partir de `build/upstream_orig` (collisions, eau, rebords, PNJ) ; recalcule si un PNJ bloque |
| `mark ADR` | mémorise le mot de 32 bits à ADR (ex. `mark 03005bdc`, gMain.callback2, sur la carte) |
| `ifmark CMD` / `ifnotmark CMD` | exécute CMD si la valeur mémorisée est inchangée / a changé (combat, menu plein écran) |
| `untilmark MAX [KEY]` | avance (en tapotant KEY) jusqu'au retour de la valeur mémorisée |
| `guard ADR FICHIER` | pendant `walk`/`goto`, si ADR change (début de combat), joue FICHIER puis reprend ; `guard` seul désactive. `fuite.txt` fuit un combat sauvage, `combat_auto.txt` combat |
| `ifeq ADR VAL CMD` / `ifne` | exécute CMD selon la valeur d'un mot mémoire |
| `peek ADR [N]` / `peekp PTR DEC [N]` | affiche des octets de la mémoire (directement / via un pointeur) |
| `echo TEXTE`, `counter N`, `reset` | divers |

Conseils :
- partez d'un état existant (`load griotte.ss`) plutôt que de rejouer l'introduction ;
- pour un dialogue, `repeat N press A 4 90 ; shot nom` donne une capture par page ; pour
  avancer jusqu'à la fin d'une scène plein écran, `mark 03005bdc` puis
  `repeat 30 ifmark press A 4 100 ; ifmark shot nom` ;
- en combat, `B` fait défiler les messages d'ouverture sans effet dans le menu ; le menu se
  souvient de la position du curseur ;
- pour sortir d'un bâtiment, `goto` jusqu'au tapis puis `hold DOWN 30` (les tapis de sortie
  demandent d'appuyer encore dans la direction) ; pour un escalier, idem avec la direction
  de l'escalier ;
- l'émulation est déterministe : un scénario rejoué sur la même ROM donne les mêmes captures.
  Après un changement de textes, vérifiez les captures : une page de dialogue en plus ou en
  moins décale la suite ;
- `.venv/bin/python outils/emulateur/chemin.py CARTE X0 Y0 X1 Y1` affiche le trajet calculé.

Les adresses RAM utilisées (`030041d8` gSaveBlock1Ptr, `03005bdc` gMain.callback2) viennent
de `build/upstream/pokehns.map` ; elles ne bougent pas quand seuls les textes changent.
