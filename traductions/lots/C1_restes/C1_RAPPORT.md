# Lot C1 : derniers textes non traduits et arbitrage des douteux des lots A et B

## 1. Résultat

| Fichier | Entrées | Contenu |
|---|---:|---|
| `C1_001.json` | 605 | noms de Dresseurs et de personnages, une valeur par fichier (301 entrées générales, 304 `msgctxt`) |
| `C1_002.json` | 116 | autres textes non traduits (dialogues, debug, Club Union, crédits FRLG, Match Call…) et 4 corrections du générique FRLG |
| `C1_003.json` | 348 | douteux du lot A (retenus ou adaptés) et traductions qui remplacent un douteux rejeté |
| `C1_004.json` | 262 | douteux du lot B, même principe |
| `C1_exceptions.json` | 58 | textes gardés tels quels, avec leur justification (anglais identique dans Émeraude FR, noms propres, japonais inutilisé) |
| `C1_rejets.json` | 715 | douteux rejetés : proposition d'origine, raison, remplacement éventuel |
| `C1_verifications.tsv` | 14 lignes | 0 problème bloquant (détail au §6) |

Par source, sur les 1 331 entrées des quatre `C1_00x.json` :
- Émeraude FR officiel : 406 ;
- Émeraude FR officiel (adapté) : 205 ;
- SoulSilver FR officiel : 167 ;
- SoulSilver FR officiel (adapté) : 145 ;
- traduction nouvelle : 408 (dont 269 noms de Dresseurs Johto/Kanto/FRLG sans nom officiel).

**Non traduits.** Les 439 entrées à `msgstr` vide sont toutes traitées : 381 reçoivent une traduction, 58 sont gardées à l'identique et justifiées dans `C1_exceptions.json`. Il n'en reste aucune.

**Douteux.**

| Lot | Retenus | Adaptés | Rejetés | Total |
|---|---:|---:|---:|---:|
| A | 456 | 149 | 272 | 877 |
| B | 105 | 226 | 439 | 770 |

Un douteux rejeté dont l'entrée du .po était vide ou fausse reçoit une traduction, indiquée dans `remplacement`. Les autres gardent le .po actuel.

## 2. Noms de Dresseurs (`C1_001.json`, scripts `noms1.py` et `noms2.py`)

**Périmètre.** Il comprend 317 prénoms anglais. Ce sont les noms encore vides et ceux des douteux A/B, hors noms d'espèces, qui sont traités avec les autres douteux. Pour chacun, j'ai fixé une valeur fichier par fichier.

**Valeurs par fichier.**
- **Fichiers Hoenn** (`trainers.party`, `battle_frontier_trainers.h`, `battle_tent.h`, `contest_opponents.h`, `trainer_hill.h`) : nom Émeraude FR **du même index**, lu dans les deux ROM. J'ai rechargé les tables et vérifié que l'anglais des deux côtés est identique pour 100 % des entrées :
  - gTrainers : 855 entrées, pas de 40 ;
  - gBattleFrontierTrainers : 300 entrées, pas de 52 ;
  - trois Tentes de Combat : 3 × 30 ;
  - gDefaultContestWinners (8) et gContestOpponents (96). HnS ajoute 8 entrées en tête de `contest_opponents.h` : le décalage est pris en compte ;
  - noms du Mont Dresseurs, retrouvés par adresse.

  `trainers.party` n'est **pas compilé** dans HnS (`IS_HNS` n'inclut que `trainers_hns.h`), mais je l'ai traduit quand même. Les 20 Dresseurs de la Zone de Combat ajoutés par HnS (index 300 et suivants : Sandra, Jasmine, Peter…) reçoivent leur nom SoulSilver.
- **`trainers_hns.party`** :
  - l'entrée à contexte existante est gardée ;
  - sinon, je prends le nom SoulSilver FR (banque 729, décodée depuis la ROM et rapprochée de `trainers.json` de pret) quand c'est **le même Dresseur** : même nom anglais et au moins une espèce en commun. J'ai relu chaque cas à la main ; HnS change souvent la classe (« Collector Hns » = Scientifique de la planque Rocket, « Hex Maniac » = Mystimaniac…) ;
  - sinon, prénom anglais en casse normale (« Jed », « Allan »).
  - Exceptions : les Meneurs de la Zone de Combat (ANABEL, SPENSER, GRETA) gardent leur nom Émeraude FR (CATHY, ESTEBAN, CAROLE).
- **`trainers_frlg.party`, `trainer_tower_sets.c`, Pokédex des célébrités FRLG** : nom SoulSilver seulement pour le même personnage (Farouk, Giovanni, Koga, Peter et les entrées à contexte existantes). Sinon, prénom anglais en casse normale. J'ai rejeté 11 homonymes SoulSilver de classe différente (BENJAMIN, HANK, HUGH, JARED…).
- **`trade.h`** :
  - les 4 échanges d'Émeraude gardent le nom Émeraude FR (LUDOVIC, PIPIO…) ;
  - les échanges HnS prennent le nom et le surnom SoulSilver FR de la **banque 200** (noms et surnoms des échanges HGSS) : JOSE → Devon, BILLY → Voltounet, MAGGIE → Ovni, PAUL → Quetzal. KENYA (`scrcmd.c`) → Piou Piou ;
  - les autres gardent le prénom anglais en casse normale.
- **`apprentice.h`** : les noms des autres langues (colonnes DE/ES… de gApprentices : DAVID, BRIAN, BRUNO…) sont gardés par `msgctxt`, pour qu'une entrée générale traduite ne les modifie pas.
- **`new_game_intro_frlg.inc`** : les noms proposés restent en capitales, comme les autres noms de ce fichier.

**Entrée générale.** Elle reçoit le nom du fichier Hoenn principal. Chaque fichier dont la valeur diffère a une entrée `msgctxt`. Le texte reste dans l'entrée générale quand il sert aussi ailleurs avec un autre sens (MARK = MARQUER, SUMMER = ETE, ROY = SAM du Match Call). Trois entrées générales sont imposées :
- LANCE → Peter ;
- KOGA → Koga ;
- BRUNO → Aldo.

**Entrées `msgctxt` créées : 337.**
- Par fichier :
  - noms : `trainers_frlg.party` 179, `trainers_hns.party` 81, `contest_opponents.h` 12, `trade.h` 12, `fame_checker_frlg.inc` 6, `trainer_tower_sets.c` 5, `apprentice.h` 5, `trainer_hill.h` 3, `new_game_intro_frlg.inc` 2 ;
  - autres : Easy Chat 11, cartes Hoenn 9, `landmark.c` 2, `abilities.h` 2, divers 9.
- Chaque `msgctxt` a été vérifié : c'est un chemin où `hnsfr.scan(build/upstream_orig)` trouve exactement ce texte.

## 3. Autres non traduits (`C1_002.json`, exceptions)

- **Crédits `credits.h`** (50) : Émeraude FR garde ces lignes **en anglais**. Elles sont présentes octet pour octet dans la ROM FR, comme « French Version Coordinators » : je les garde telles quelles (exceptions, adresse FR en preuve). Deux lignes absentes de la ROM FR (« Royal New Zealand Federation for the Blind », « Nicola Pratt-Barlow ») sont des noms propres.
- **Crédits `credits_frlg.c`** : les rubriques sont traduites comme les rubriques sœurs déjà traduites (Direction, Composition musicale, Remerciements…), avec les `\n` de l'anglais. Les noms de personnes restent tels quels. J'ai corrigé au passage 4 entrées « SoulSilver FR officiel » fausses, avec `alignement_faux` : banque 440 mal alignée, Satoshi Tajiri → « Shusaku Egami », Satoru Iwata → « Hiroaki Tsuru », mise en page perdue pour Go Ichinose et Kenji Matsushima.
- **Debug** (`battle_debug.c`, `debug.c`), traité comme le lot E :
  - noms officiels des capacités et objets du .po (Vampigraine, Piège de Roc, Accro Griffe…) ;
  - colonnes `{CLEAR_TO 90}` de l'anglais ;
  - PNJ suiveurs : FLORA, PIERRE, Red.
- **Match Call** (10 demi-phrases de profils) : texte Émeraude FR **exact**. Lot A ne l'avait pas trouvé parce que l'anglais de HnS écrit « we've » avec une apostrophe droite, et Émeraude US « we’ve ». J'ai relu les adresses dans la table de profils (FR = US + 17 348, contrôlé par les lignes voisines déjà officielles). Au passage, « every day. » valait « tous les jours. » : ce texte n'apparaît que dans ce fichier, et il donnait « Tous les jours, je nage au / tous les jours. ». Il devient « moins 10 km. », la suite officielle.
- **Club Union / panneau d'échange** (12) : traduction nouvelle, avec le vouvoiement et le vocabulaire des textes Émeraude FR voisins. J'écris « PANNEAU D'ECHANGE » en capitales sans accent ; le .po contient par endroits la forme mixte « PANNEAU D'Echange ».
- **`berry_blender.c`** (いいTVができました / ダメTVができました) : **jamais affichés** (`sJPText_GoodTvReady` et `sJPText_BadTvReady`, marqués `// Unused`, sans aucune référence). Je les garde (exceptions). Les traductions proposées par les sous-agents pour les douteux A et B correspondants sont rejetées.
- **Divers** :
  - Pokédex des célébrités FRLG (Prof. Chen, Pierre, Ondine, Major Bob, Erika, Morgane, Auguste, Léo) ;
  - météo de debug en capitales (SOLEIL, PLUIE à la place de « Rain », BROUILLARD, OMBRE) ;
  - environnements de combat (Glace, Montagne, Zone de Combat, Arène, Flaque) ;
  - BOURG-EN-VOL, ZONE SPECIALE ;
  - « LR » (mode des boutons, identique dans Émeraude FR) ;
  - « Chad » et « Joey » (pseudonymes).
- **Trouvé au passage** (échanges `trade.h`, banque 200) :
  - MUSCLE → Gonflor (l'entrée générale valait « LE MUSCLE », texte de `lilycove_lady.h`) ;
  - IRON → Pôlo (valait « Fer », le nom de l'objet) ;
  - LORENZO → Quantin ;
  - STEVEN → Rochard.

## 4. Douteux

**Méthode.** J'ai arbitré moi-même les noms, les entrées à contexte du lot A (162), les mots Easy Chat (106) et les « PCo » (50). Les entrées approchées et les cas particuliers ont été répartis entre quatre sous-agents, qui avaient tous la même consigne (`scripts/BRIEF_sous_agents.md`) :
- B approchés : 2 × 172 ;
- A approchés et autres : 254 ;
- B autres : 246.

J'ai relu un échantillon de leurs sorties et tranché les doublons entre lots (13 conflits ; la version retenue est la plus fidèle à l'anglais).

**Règles appliquées.**
- **Contextes du lot A** :
  - je retiens le texte Émeraude FR propre au fichier quand il diffère de l'entrée générale : répliques de FLORA/BRICE sur Route104, panneaux du tunnel MERAZON, « Hmm… You're pretty good. » sur 3 cartes, Karatéka, LETTRES PORT… ;
  - les 93 propositions identiques à l'entrée générale sont rejetées comme inutiles ;
  - les types restent écrits pareil partout (décision 3).
- **Easy Chat** : le mot Émeraude FR est gardé quand il veut dire la même chose (ENSEIGNER, MAGAZINES, COUCOU…). Sinon, le mot anglais est traduit (BALLON, COEUR, D'ACCORD…).
  - Plusieurs entrées actuelles étaient cassées (« N », « SSE », « KET », « LL », « ISME ») ou en anglais (« Morning », « Look », « Heart ») ; elles sont remplacées.
  - Quand le mot est partagé avec un menu, l'entrée porte un `msgctxt` vers le fichier Easy Chat (NEXT, ALL, ON…).
  - OFF n'apparaît que dans `challenge_menu.c` : la proposition est rejetée.
- **PCo** : les 50 sont retenus, dont 10 adaptés (nom complet Émeraude FR à la place de l'abréviation du patch ; largeur contrôlée sous la colonne `{CLEAR_TO}`).
- **Lot B approché** : texte SoulSilver adapté quand HnS ne diffère de HGSS que par un détail.
  - Rejet si HnS ajoute une phrase, si l'accord féminin de SS vise le joueur, ou si le .po est déjà Émeraude FR officiel.
  - Les accords masculins visant le joueur sont neutralisés quand c'est possible.

## 5. Doutes et points à arbitrer (agent principal)

1. **Noms FRLG** : 93 noms déjà intégrés (`trainers.party` + `trainers_frlg.party`) donnent aux Dresseurs FRLG le nom Émeraude de l'entrée générale (ERIN, NINA…). Mes entrées suivent la consigne : nom SoulSilver, sinon prénom anglais en casse normale. Pour harmoniser, il faudrait ajouter des `msgctxt = src/data/trainers_frlg.party` à ces 93 noms.
2. **Intégration** : 4 entrées de `C1_001` et 15 de `C1_003` remplacent un « officiel exact » faux, et portent `alignement_faux: true` avec la raison :
   - JOE pour DAN, Mikail pour FRANK, Nathan pour NATHAN (= Jason dans SS), Omar pour OMAR ;
   - mots du Livret alignés sur une banque SS d'un autre contexte ;
   - deux mises en page SS rétablies.

   Environ 18 entrées « traduction nouvelle » remplacent un texte du patch (IEN → Ian…) : elles demandent `--corriger`.
3. **PSYCHIC (classe)** : « KINESISTE » en capitales jure avec Montagnard ou Scout, mais c'est un Émeraude FR exact, que je n'ai pas remplacé (rejet A:163/164).
4. **RIBBON awarded for** (A:581/597) : Émeraude FR dit « RUBAN pour récompenser » dans les deux fichiers, le .po « RUBAN pour le triomphe ». Les 2es lignes des rubans cadeaux ont été traduites pour « le triomphe ». C'est à décider d'un bloc.
5. **Remontés par les sous-agents** :
   - **Voix et cohérence**
     - Bob (Arène de Carmin) : SS lui donne un franglais. 3 répliques sur 6 sont rejetées pour garder une voix uniforme.
     - Appels Pokématos `match_call_hns` : la salutation du .po (« Hé, {PLAYER}! C'est BRENT! ») est gardée devant le texte SS (~20 entrées).
     - Une entrée `msgctxt` Mahoganytown_hns (« Tu n'as pas assez d'argent. ») : le marchand d'Acajou tutoie, alors que le texte général vouvoie.
   - **Noms et lieux SoulSilver à harmoniser**
     - SOUL HOUSE = « Maison des Souvenirs » (le .po dit MAISON DES AMES).
     - AMY = Lia, TUSCANY = Marie, WESLEY = Homer, MONICA = Lucie.
     - Salle de Danse (le .po dit THEATRE DE DANSE), Ranch Meumeu, « l'Ancien » pour Elder.
     - MARY = Lula dans SS, mais la radio dit MARIE partout : B:221 est rejeté.
   - **Défauts relevés dans le .po**
     - « {B_BUFF2}augmente » donne « très augmente ».
     - Restes de casse mixte : « SALLE DE Combat », « TENTE DE Combat », « l'Hôte DE LA Pension », « D'ARENE », « Œuf ETRANGE ».
   - **Messages de combat** : quelques messages SS plus larges que 198 px ont été acceptés, parce que le moteur les coupe lui-même (`BreakStringAutomatic`). C'est justifié dans chaque `note`.
6. **Dresseurs HnS qui reprennent un Meneur de la Zone de Combat** (TUCKER, NOLAND, BRANDON) : leurs entrées BF_BRAIN ont la même équipe qu'un Dresseur ordinaire du même nom. Un seul `msgctxt` est possible par fichier, et c'est le nom SoulSilver du Dresseur ordinaire qui est retenu (Sergei, Evrard, Brandon).

## 6. Vérifications (`C1_verifications.tsv`, 14 lignes, aucune bloquante)

- `ANGLAIS` (11) : noms identiques en Émeraude FR (DEAN, BENJAMIN, GILBERT, IRENE, KELLY, LAURA, TARA, WALTER, HENRY ; FRANK dans `apprentice.h`), plus le pseudonyme « Chad ».
- `LARGEUR` (2) : messages de combat sur une ligne, coupés automatiquement par le moteur (cf. §5).
- `GLOSSAIRE` (1) : « NOA » = Nintendo of America, et non le personnage du glossaire.
- `C1_exceptions.json` n'est pas passé au vérificateur : il contient les deux textes japonais gardés exprès (KANA). Ces exceptions sont des `msgstr` identiques au `msgid`, à intégrer seulement pour marquer l'entrée comme traitée.

Scripts (relançables, dans l'ordre) : `scripts/tables_em.py`, `noms1.py`, `noms2.py`, `mes_decisions.py`, `mes_decisions2.py`, `fusion.py`, `stats.py`. Ils lisent leurs fichiers de travail dans le scratchpad de la session, chemin écrit dans `commun.py`.
