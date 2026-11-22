# Décisions de traduction et d'outillage

Chaque décision : date, décision, raison, conséquences. Les décisions de terminologie sont aussi
reportées dans `traductions/glossaire.tsv`.

## Décisions héritées du projet (avant reprise)

| Sujet | Décision |
|---|---|
| Style | SoulSilver FR : « Pokémon », « Dresseur », « Pokématos », « Prof. Orme », « Prof. Chen » ; lieux/objets/capacités en minuscules avec majuscule initiale ; espèces en capitales (banque 237). |
| Noms | Johto/Kanto selon SoulSilver FR (Bourg Geon, Ville Griotte, Rosalia, Fargas, Léo…) ; Hoenn selon Émeraude FR (FLORA, BRICE, TIMMY, Prof. SEKO…). |
| Menu START | En capitales comme Émeraude FR : POKéDEX, POKéMON, SAC, {POKE}MATOS, SAUVER, OPTIONS, RETOUR (ligature {POKE} car « Pokématos » entier est tronqué). |
| Horloge | 24 h (`code/horloge-24h.patch`). |
| Combat | « PTITARD sauvage », « … ennemi » : qualificatif après le nom, sans article (`code/nom-sauvage-ennemi.patch`). Glyphe 0x105 « Lv » → « N. » dans toutes les polices latines. |
| Abréviations | Statuts PSN, PAR, SOM, GEL, BRU, GLR ; stats PV, AT, DF, AS, DS, VI. |
| Pokédex | INFO, ZONE, STATS, EVO, CRI, TAIL. ; VUS / PRIS ; RECH. ; RETOUR LISTE / HAUT DE LISTE / BAS DE LISTE / FERMER POKéDEX. |
| Claviers | `src/text_input_strings.c` jamais traduit : la disposition affichée doit suivre celle du code. |
| Même anglais, sens différents | `traductions/contextes.po` (msgctxt = fichier) : PSYCHIC (type Psy / classe Kinésiste), entrées du menu START. |

## 2026-11-20 — reprise du projet

1. **Sources de texte supplémentaires.** Les noms de Dresseurs (`src/data/*.party`) et de lieux
   (`src/data/region_map/region_map_sections.json`) sont traduits dans ces fichiers sources : les `.h`
   correspondants sont générés à la compilation et ne doivent plus être lus (`hnsfr.py` ne lit plus que
   les fichiers suivis par git). Les textes de debug (`debug.c`, `battle_debug.c`) et les crédits ne
   sont plus exclus : le brief demande de tout traduire, y compris les textes de développement.
2. **Entrées purgées.** 351 entrées dont la clé était déjà du français (amorçage précédent fait sur
   un arbre déjà traduit : « Steevy », « EPAVE »…) ou des claviers exclus ont été retirées des .po.
3. **Noms de types.** Émeraude FR tronquait à 6 lettres (ELECTR, TENEBR) ; HnS autorise 8 caractères.
   Noms complets en capitales, sans accent (voir décision 14) : NORMAL, COMBAT, VOL, POISON, SOL, ROCHE,
   INSECTE, SPECTRE, ACIER, FEU, EAU, PLANTE, ELECTRIK, PSY, GLACE, DRAGON, TENEBRES, FEE, STELL. (« Stellaire », 9 lettres, dépasse la limite de 8). Les mêmes clés servent aux
   mots Easy Chat et à la radio : même graphie partout (ce sont des libellés).
4. **Largeur des textes officiels.** La règle des 198 px s'applique aux traductions nouvelles et au
   patch FR. Un texte officiel (Émeraude FR / SoulSilver FR) est toléré jusqu'à 216 px, largeur
   réelle de la fenêtre de dialogue (27 tuiles), pour ne pas réécrire un texte officiel qui s'affiche
   correctement dans le moteur d'Émeraude.
5. **Codes équivalents.** Un code écrit autrement mais de mêmes octets (`{FONT 0}` / `{FONT_SMALL}`,
   `{CLEAR_TO 87}` / `{CLEAR_TO 0x57}`) n'est pas une erreur pour le contrôle, mais on réécrit la
   graphie anglaise lors de l'intégration.
6. **Ponctuation.** Pas d'espace avant ! ? : ; dans tout le projet (mesuré : c'est déjà le cas de
   toutes les sources, y compris les textes SoulSilver convertis).
7. **Relecteur indépendant.** ChatGPT est appelé via la CLI Codex (`codex exec`, compte ChatGPT de
   l'utilisateur) par `outils/relecture_chatgpt.py`. Les textes officiels exacts ne lui sont soumis
   qu'en mode « alignement » (est-ce la bonne phrase ?).
8. **Arbitrage automatique** (`outils/arbitrer_relecture.py`) : refus des remarques qui ne changent que
   la mise en page, qui touchent un texte officiel, qui cassent un contrôle bloquant ou qui ajoutent
   une espace avant la ponctuation ; termes hors glossaire laissés à l'arbitrage de l'agent principal.
9. **Priorité à l'intégration** (`outils/integrer_lot.py`) : Émeraude FR exact (1) < Émeraude FR adapté
   (1,5) < SoulSilver FR exact (2) < SoulSilver FR adapté (2,5) < patch FR (3) < traduction nouvelle (4).
   Une source moins bonne ne remplace jamais une meilleure, sauf correction justifiée (`--corriger`),
   et jamais un officiel exact sauf alignement faux démontré.
10. **Commits non signés** dans ce dépôt (clé GPG sur YubiKey, bloquante pour un agent).
11. **Sauts de ligne SoulSilver.** `\f` (Gen 4 : défilement d'une ligne dans la même boîte) devient `\l`
    et non `\p` : `\p` coupait les phrases en deux pages. `\r` (nouvelle boîte) devient `\p`. (Lot B.)
12. **Symbole monétaire.** Le « $ » des textes SoulSilver (Pokédollar) vaut 0xFF en Gen 3, c'est-à-dire la
    fin de chaîne : il est converti en « ¥ » après le nombre (« 500¥ »), comme Émeraude FR. Le
    vérificateur rejette désormais tout « $ » absent de l'anglais.
13. **Noms de Dresseurs homonymes.** Un même prénom anglais peut désigner des personnes différentes selon
    la région (BILL Cracheur de feu → Andréa ; BILL le personnage → Léo). Les noms de Dresseurs
    SoulSilver sont donc posés avec `msgctxt` = fichier `.party` (contextes.po).
14. **Pas d'accent sur les majuscules** (corrige la première version de la décision 3). Mesuré dans les deux
    officiels : Émeraude FR écrit RESUME, DEPLACER, BOITE, DEFENSE, ATQ. SPE, « A bientôt » (44 fois, 0 « À
    bientôt »), « Echange » ; SoulSilver FR écrit Iles Ecume, Ile de Fer, Cramois’Ile, Electrik, Echange,
    « Etes », HERICENDRE, et aucun É, À ou Î. Mais tous deux gardent la **cédille** (« Ça » 314 fois dans
    Émeraude FR, 327 dans SoulSilver FR ; GARÇON) et la ligature Œ. Règle : À Â É È Ê Ë Î Ï Ô Ù Û Ü → A A E
    E E E I I O U U U, partout (libellés et texte courant) ; Ç et Œ restent ; le « é » minuscule de POKéMON
    reste. Appliquée aux .po et au glossaire, et automatiquement par integrer_lot.py.
15. **Relecture ChatGPT différée (lots C1, C2a, C2b).** La limite d'usage du compte ChatGPT a été atteinte
    pendant l'audit des textes hérités (13 paquets sur 77 non relus). Les lots C1 et C2 sont intégrés après
    vérification automatique et validation ligne à ligne par sous-agent ; leur relecture ChatGPT sera faite
    dès la levée de la limite (`relecture_chatgpt.py` reprend les paquets manquants), puis arbitrée.
16. **Noms de personnages homonymes.** Steven = PIERRE (Émeraude FR, capitales) ; Brock = Pierre (SoulSilver
    FR). Le glossaire garde PIERRE → Pierre (personnage de Kanto) ; pour les textes Hoenn le glossaire est
    appliqué sans les noms de personnages, et les répliques de Steven écrivent « PIERRE: ».
17. **Termes communs d'Émeraude en casse SoulSilver.** Émeraude FR écrit en capitales des termes communs
    (CONCOURS, BASE SECRETE, VELO, TENTE DE COMBAT, ZONE DE COMBAT, RUBAN, MUSEE, MIXEUR, CENTRE POKéMON…) ;
    le style SoulSilver du projet les écrit en casse normale (Concours, Base Secrète, Vélo, Tente de Combat…).
    Ajoutés au glossaire et appliqués, y compris quand un saut de ligne coupe le terme (« CENTRE\nPokémon »
    était resté à moitié converti). Les noms propres de Hoenn (villes, personnages, TEAM AQUA/MAGMA) gardent
    les capitales d'Émeraude FR, conformément au brief.
18. **Autres textes officiels français, entre SoulSilver et le patch FR.** Les textes officiels de Rouge Feu /
    Vert Feuille FR (cartes et données FRLG du code, alignés par pointeurs sur une ROM US reconstruite depuis
    pret/pokefirered, lot F) et les descriptions / catégories du Pokédex des jeux récents (X/Y, ROSA, Soleil/Lune,
    Épée/Bouclier…, d'après PokeAPI et Poképédia, lots K et P) passent avant le patch FR et les traductions
    nouvelles (rang 2.8, adaptés 2.9 dans integrer_lot.py), après Émeraude FR et SoulSilver FR.
19. **Relecture ChatGPT différée faite (lot R).** 926 remarques sur 4 437 entrées ; arbitrage automatique, puis
    contre-relecture indépendante des corrections acceptées (sous-agent) : 244 retenues sur 926, les autres
    refusées (pinaillage, allongement sans gain, conventions du projet : {PKMN} écrit « Pokémon », {SUPER_E},
    capitales de Hoenn, « N. » réservé au niveau). Corrections des descriptions de capacités remises en page à
    152 px. Détail : rapport/relectures/R_relecture_differee/ et traductions/lots/R_relecture_differee/.
20. **Cas douteux de Rouge Feu FR (lot F) et termes propres à Rouge Feu.** Texte officiel retenu quand seul un
    {PLAYER} répété est omis (verifier.py traite désormais Rouge Feu / Vert Feuille FR comme Émeraude et
    SoulSilver : un officiel peut omettre un code, jamais en ajouter) ; refusé quand il en ajoute un, quand le hack
    a modifié la phrase (Nina qui bichonne), quand l'alignement est faux (« x un aussi! ») et pour les crédits
    (autres personnes). Les répliques courtes partagées avec HnS (« No! », « Kaboom! »…) reçoivent le texte de
    Rouge Feu FR par une entrée propre au fichier FRLG dont le pointeur est confirmé ; les cartes HnS gardent la
    traduction générale. Les termes de Rouge Feu FR (Dingue des Capacités, Ticketaurora, Parc Central,
    Memorydex, Cherche VS…) valent pour les textes FRLG ; les textes Johto/HnS gardent ceux de SoulSilver FR.
21. **Un seul patch distribué : sur Heart & Soul anglais.** Le patch de traduction s'applique à la ROM HnS
    anglaise officielle ; le patch sur Émeraude US n'est plus produit par défaut (option `--patch-emeraude`
    de build.sh / construire.py, gardée au cas où). Chaque patch produit est vérifié automatiquement :
    appliqué à sa ROM source (outils/ups_appliquer.py, contrôle des trois CRC), il doit redonner la ROM construite.
22. **Style SoulSilver FR confirmé par l'utilisateur (2026-11-20).** Le texte anglais de HnS suit la convention
    des jeux anglais de 3e génération (POKéMON, TRAINER, GYM, lieux et personnages en capitales : 1 388
    « POKéMON » pour 0 « Pokémon » dans les cartes HnS), alors que HeartGold anglais écrit « Pokémon »,
    « Pokémon Center ». L'équivalent fidèle serait le style d'Émeraude FR ; le style SoulSilver FR est gardé :
    c'est celui du jeu que HnS refait, il est plus lisible, et il est déjà appliqué et vérifié partout.
23. **Publication automatique du patch (GitHub Actions).** À chaque push sur main, la CI construit la ROM et
    publie une release v<version HnS>-fr.<n> (n = numéro de publication, la dernière marquée Latest) avec le
    seul fichier UPS ; un tag mobile « derniere-version » a été essayé puis abandonné. Pour calculer le patch, elle reconstruit
    la ROM anglaise de HnS à partir d'Émeraude US (chiffrée avec gpg, dans le dépôt privé tfournier/hns-roms,
    récupérée avec une deploy key en lecture seule) et du patch officiel HnS (release publique). Une ROM
    téléchargée sur un site tiers (archive.org) a été écartée : copie non autorisée, lien fragile. Les secrets
    GitHub Actions (48 Ko) ne peuvent pas contenir une ROM.
24. **Textes que l'extracteur ne voyait pas (signalés en jeu par l'utilisateur).** (a) 49 descriptions
    d'objets et de capacités coupées par `#if` au milieu de la chaîne : chaque variante est désormais un texte
    complet (début commun + branche + fin commune), réécrit branche par branche sans changer le nombre de lignes
    (hnsfr.py, type « cif ») ; (b) 9 descriptions avec une macro au milieu (`"for "BINDING_TURNS" turns."`) : la
    macro devient le code `{C:BINDING_TURNS}`, la valeur du `#define` est traduite à part ; (c) les textes
    d'une lettre ou sans deux lettres consécutives (« A », « I », « 1F », « 's ») et les restes japonais du code
    étaient ignorés : tout texte contenant une lettre est désormais extrait (157 traduits, les symboles et notes
    A–S gardés). Le contrôle de l'anglais restant ne range plus les chaînes sans source parmi le « bruit » :
    seules celles situées dans des données binaires (tuiles, sprites, d'après le .map) sont écartées, le reste
    est à vérifier. Consigne de l'utilisateur : on traduit aussi les textes qui ne s'affichent jamais.
25. **Phrases Easy Chat officielles.** Les répliques des Dresseurs de la Zone de combat, des Tentes, du
    Trainer Hill, de l'apprenti, de la Trainer Tower, etc. sont des suites de mots : les suites anglaises
    donnaient des phrases absurdes avec le vocabulaire français (« CE EST A CAUCHEMAR POUR TU »). Les suites
    officielles d'Émeraude FR et de Rouge Feu FR sont reprises (1 768 répliques, code/easy-chat-fr.patch,
    lot EC_easychat) ; 61 répliques propres à HnS sont composées avec le vocabulaire officiel ; les mots de passe
    de l'Œuf Étrange (comparés par identifiant) ne changent pas. Le vocabulaire Easy Chat suit exactement les
    mots officiels d'Émeraude FR au même index (capitales comprises) : 227 mots partageaient leur texte anglais
    avec d'autres chaînes et recevaient une autre traduction ; ils ont une entrée propre à leur fichier de groupe.
26. **Possessif anglais construit par le code.** La bulle de talent affichait « PIKACHU's » : le code ajoutait
    « ' » et « s » ; correctif code/bulle-talent-sans-possessif.patch (nom seul, talent en dessous). Écran
    d'assertion (débogage) traduit (code/ecran-assertion.patch). Restent en anglais, volontairement : marqueurs
    du protocole de connexion (« PokemonSioInfo », « GameFreak inc. »), journaux de débogage de la console de
    l'émulateur, rangées du clavier de saisie (décision initiale), identifiants du test sonore (noms de constantes
    du code, à trancher avec l'utilisateur), octets de tuiles qui ressemblent à du texte.
27. **Inscriptions en braille.** Les 61 inscriptions (`.braille` de data/text/braille.inc, ignorées jusqu'ici par
    l'extracteur) reprennent les inscriptions officielles d'Émeraude FR (22, Chambre Scellée…) et de Rouge Feu FR
    (39, Chemin Rubis, Trou Pointillé…), lues dans les ROM ; les octets codent les points, recopiés tels quels
    (l'apostrophe de la table anglaise de preproc donne le point final du braille français). Les cases d'alphabet
    d'Émeraude (ABCD, IJKL…) diffèrent de celles de Rouge Feu (ABC, GHI…) pour un même anglais :
    code/braille-alphabet-emeraude.patch.
28. **Descriptions du Pokédex HGSS.** Le texte est centré sur 240 px d'après sa ligne la plus longue : au-delà de
    224 px (largeur maximale de l'anglais) il touche le bord gauche ; `\l` provoque une pause « ▼ ». Toutes les
    descriptions sont limitées à 4 lignes de 224 px, sans `\l` ni `\p` (495 remises en page, mots inchangés ;
    3 raccourcies) ; verifier.py applique cette règle à toutes les sources, officielles comprises.
29. **Images, second passage (lot F2) et fin des crédits.** 30 images de plus (états, résumé, Pokédex DECA,
    roulette, restes japonais, DexNav, « PRESENTE »/« FIN » de Rouge Feu FR…). Les tuiles anglaises restées aux
    anciens indices des onglets du Pokédex (AREA, CRY, SIZE) apparaissaient un instant au changement de page
    (tuiles chargées avant la tilemap) : remplacées par leur équivalent français. Les crédits HnS dessinent
    « THE END » tuile par tuile : code/credits-fin.patch affiche « FIN ». Unité impériale « lbs. » → « lb »
    (code/unite-livre.patch). Étiquettes de type de 6 lettres (TENEBR, ELECTR…) : celles d'Émeraude FR.
30. **Elixir Max et Repousse Max (demande de l'utilisateur).** SoulSilver FR écrit « Max Elixir » et
    « Max Repousse » (ordre de la 4e génération), alors que le jeu affiche « Potion Max », « Rappel Max »,
    « Huile Max » : on prend l'ordre des jeux suivants, « Elixir Max » et « Repousse Max », partout (noms,
    dialogues, glossaire). Exception assumée à la priorité des textes officiels.
