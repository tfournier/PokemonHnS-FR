# Lot EC : répliques « Easy Chat » (tableaux d'identifiants de mots)

Correctif produit : `code/easy-chat-fr.patch` (appliqué par `outils/construire.py` comme les autres
patchs de `code/`, avant les textes). Il remplace uniquement des identifiants `EC_WORD_*`,
`EC_MOVE(…)`, `EC_MOVE2(…)`, `EC_POKEMON(…)`, `EC_POKEMON_NATIONAL(…)` et `EC_EMPTY_WORD`/`-1`/`0xFFFF` ;
aucune chaîne de caractères n'est touchée, aucun fichier ne change de nombre de lignes
(12 fichiers, 1 922 lignes modifiées). Vérifié : `git apply --check` sur une copie propre de
`build/upstream_orig`, puis compilation (`cpp | preproc | cc1 -Werror`) des 12 unités de traduction
concernées sans erreur nouvelle.

## Méthode

1. **Recensement** : toutes les accolades `{…}` du code dont tous les éléments sont des identifiants
   Easy Chat (hors `src/data/easy_chat/` et `src/data/bard_music/`), plus les 16 champs
   `.answer = EC_WORD_…` de la Dame Quiz (`src/data/lilycove_lady.h`). 1 861 répliques au total.
2. **Repérage dans Émeraude US** : `build/pokeemerald` a été cloné et compilé (ROM identique octet
   pour octet à `memoires/emeraude_us.gba`, symboles par `nm`). Chaque réplique anglaise de HnS est
   convertie en octets avec les constantes de pokeemerald (espèces en numérotation interne Émeraude,
   capacités Gen 3) et cherchée dans la ROM US ; le symbole qui la contient donne la table et l'offset.
   Les doublons (même phrase anglaise à plusieurs endroits) sont départagés par l'ordre du fichier.
3. **Passage à Émeraude FR** : la même table dans `memoires/em_fr.gba` est trouvée par décalage
   d'ancrage (symboles voisins de contenu identique dans les deux ROM, même décalage avant et après
   la table). Contrôles : tous les mots FR lus sont des mots valides du vocabulaire Émeraude FR ;
   pour la Zone de combat et les Tentes, le nom anglais du Dresseur dans la ROM US au même index est
   celui du source HnS (1 171 répliques vérifiées, 0 décalage) ; pour le Trainer Hill, le nom à
   l'offset −16 de chaque réplique est vérifié de la même façon.
4. **Trainer Tower (Rouge Feu)** : même méthode avec `build/pokefirered` (ROM US + symboles via
   `nm pokefirered.elf`) et `roms/Pokemon - Version Rouge Feu (France).gba` ; les 32 étages sont au
   même décalage (−34 860 octets) et, comparés octet par octet, ne diffèrent que dans les noms, les
   répliques et les surnoms (classes, équipes, objets identiques).
5. **Conversion** vers les constantes d'expansion : mots par groupe/index (les 1 009 `EC_WORD_*` sont
   identiques entre pokeemerald et expansion), capacités par numéro (≤ 354, même numérotation),
   espèces **par nom** (numéro interne Émeraude → `SPECIES_*` d'expansion). Chaque identifiant
   obtenu existe dans les en-têtes d'expansion (vérifié par assertion puis par compilation).
6. **Relecture** : chaque phrase est décodée avec le vocabulaire officiel (table des mots de la ROM)
   et avec les msgstr actuels des `.po` ; tout est dans `tables_easychat.tsv`.

## Tables traitées

| Source HnS | Table (Émeraude US → FR) | Répliques |
|---|---|---|
| `battle_frontier_trainers.h` | `gBattleFrontierTrainers` 0x5D5ACC → 0x5D9FC8 | 900 officielles + 1 (Tente) + 59 composées |
| `battle_tent.h` | `gSlateport/Verdanturf/FallarborBattleTentTrainers` → 0x5E1F10 / 0x5E2B0C / 0x5E3580 | 270 |
| `trainer_hill.h` | `sFloors_JPDefault/Normal/Variety/Unique/Expert` → 0x629FB8… | 272 (dont 16 JP inchangées) |
| `apprentice.h` | `gApprentices` → 0x614CF8 | 16 |
| `trade.h` | `sIngameTradeMail` → 0x340B44 | 3 officielles + 1 composée |
| `lilycove_lady.h` | `sQuizLadyQuestion1..16` → 0x60F40C, `sQuizLadyQuizAnswers` → 0x60F56C | 16 questions + 16 réponses |
| `mauville_old_man.c` | `sDefaultBardSongLyrics` → 0x5A36DC | 1 |
| `battle_tower.c` | `sRecordTrainerSpeechWon/Lost` → 0x5E3F46 / 0x5E3F52 | 2 |
| `battle_pike.c` | `sNPCSpeeches` → 0x61676C | 42 |
| `easy_chat.c` | `sMysteryGiftPhrase`, `sBerryMasterWifePhrases`, `sDefaultProfile/BattleStart/Won/LostWords` | 10 |
| `ereader_helpers.c` | `sTrainerHillTrainerTemplates_JP` → 0x629A80 | 16 (identiques dans la ROM FR : rien à changer) |
| `trainer_tower_sets.c` | Rouge Feu `sTrainerTowerFloor_*` (US 0x47ABAC → FR 0x472380…) | 219 + 21 non traitées |
| `scrcmd.c` | courrier de KENYA (propre à HnS) | 1 composée |
| `easy_chat.c` | `sInterviewPasswords` (propre à HnS) | 11 non traitées (voir plus bas) |

## Chiffres

- Reprises de l'officiel : **1 768** répliques (1 549 Émeraude FR, dont 1 505 modifiées et 44 déjà
  identiques — 32 de ces 44 sont les données japonaises inutilisées ; 219 Rouge Feu FR, dont 216
  modifiées) + **16** réponses de la Dame Quiz (6 modifiées).
- Composées à la main : **61** (51 modifiées, 10 où l'identifiant anglais donne déjà le bon français) :
  les 20 Champions/Dresseurs ajoutés par HnS à la Zone de combat (59 répliques), le courrier de
  l'échange de LIPPOUTOU, le courrier de KENYA.
- Non traitées : **32** — 11 mots de passe de l'Œuf Étrange, 21 répliques des 3 étages inutilisés de la
  Trainer Tower (`Double_Unused1/2/3`, jamais référencés) que Rouge Feu FR a vidés.

## Répliques composées (propres à HnS, vocabulaire officiel Émeraude FR)

| Dresseur | Avant | Victoire | Défaite |
|---|---|---|---|
| BROCK | MA ROCHE EST SOLIDE ! | C’EST LA VIE | C’EST LA VIE ……… |
| CHUCK | HE TOI! ALLEZ !! | QUEL MATCH FACILE ! | QUEL MATCH ATROCE ……… |
| LT SURGE | AUJOURD’HUI LA METEO EST ELECTRIK ! | AUJOURD’HUI JE GAGNE … | FIN DE LA METEO … |
| BLAINE | MON AVANTAGE C’EST SECHERESSE … | MON FEU EST TROP FORT ! | MON FEU EST TROP FAIBLE … |
| WHITNEY | COUCOU … C’EST PARTI ! | HA! HA! HA! C’EST OK … | QUELLE JOIE POUR TA MERE ! |
| FALKNER | ALLEZ MES AMIS VOL ! | MON TALENT VOL EST INVINCIBLE ! | JE SUIS DETRUIT ……… |
| SABRINA | SOIS PRET POUR MOI | C’EST TRES FACILE | WAOUH ! J’AI PERDU ! |
| JANINE | JE SUIS INVINCIBLE | C’ETAIT DIFFICILE ! | SNIFF |
| MISTY | LE TYPE EAU EST MEILLEUR … | HO LA LA ……… | HA! HA! HA! ……… QUOI? !! |
| BUGSY | LE TYPE INSECTE EST MERVEILLEUX ! | PAS MAUVAIS POUR MOI ! | QUOI? ……… TU ES TROP FORT … |
| JASMINE | LE TYPE ACIER EST MERVEILLEUX ! | C’EST CA ! | EXCUSE-MOI ……… JE SUIS TROP FAIBLE … |
| RED | … | … | … |
| LEAF | C’EST PARTI ! | J’AI GAGNE ! | BON MATCH ! |
| BLUE | SALUT ! | OH QUOI? | UN JOUR JE VAIS GAGNER ! |
| ERIKA | J’AIME LE JARDINAGE ! | TES POKéMON SONT TROP FAIBLE ! | TES POKéMON SONT TROP FORT ! |
| PRYCE | GLACE EST CHAUD OU FROID ? | TU AS PERDU DANS LE FROID | GLACE EST FROID ET TOI AUSSI |
| MORTY | PAS PARLER JUSTE COMBATTRE | CIAO! | CHENAPAN ! (officiel, voir cas douteux) |
| CLAIR | MON HOBBY C’EST POKéMON DRAGON ! | DRAGON PUISSANT ! | DRAGON DETRUIT DRAGON DETRUIT !! |
| LANCE | JE DOIS GAGNER ! | J’AI GAGNE … | J’AI PERDU … |
| STEVEN | LE TYPE ROCHE EST GENIAL … | LE TYPE ACIER EST MIEUX … | TERRIBLE … |

Courriers : LIPPOUTOU EST EN FORME ! SOIS SYMPA AVEC LIPPOUTOU ! (`trade.h`) ;
COURRIER ! PRENDS CE POKéMON ! PAS PERDRE ! (KENYA, `scrcmd.c`).
Le détail (constantes) est dans `scripts/manuel.py`.

## 20 exemples (anglais → FR officiel décodé)

| Source | Anglais (identifiants d'origine) | FR officiel repris |
|---|---|---|
| Zone de combat, PEGGY | GET READY TO BE DESTROYED ! | TU VAS ETRE EN LAMBEAUX !! |
| Zone de combat, MANUEL | ME LOSE ? THAT’S PREPOSTEROUS ! | MOI … PERDRE ? RIDICULE … |
| Zone de combat, TINA | HERE IT IS YOUR SWEET KISS FROM MY JYNX | UN DOUX BAISER DE LIPPOUTOU ! |
| Zone de combat, QUINN | THIS IS A BEAUTIFUL DREAM ! | C’EST UN MERVEILLEUX REVE ! |
| Zone de combat, QUINN | THIS IS AN AWFUL NIGHTMARE ! | C’EST UN TERRIBLE CAUCHEMAR ! |
| Tente de Poivressel | I AM FEELING LIKE IT’S FRIDAY ! | C’EST COMME SI ON ETAIT VENDREDI ! |
| Tente de Vergazon | IT’S A NON-STOP EXPLOSION OF JOY | C’EST UNE EXPLOSION DE JOIE ! |
| Tente de Lavandia | A NIGHTMARE OF SWEETS SHOCKED ME | UN CAUCHEMAR PLEIN DE BONBONS … |
| Trainer Hill | I WILL DISAPPEAR IN THE DARK | ARRRG ! DISPARAITRE DANS LES TENEBRES |
| Trainer Hill | NO NO … THAT WON’T DO | NON … CA NE MARCHE PAS |
| Battle Pike | I AM LOST I NEED A HELPING HAND | JE SUIS PERDU DONNE-MOI UN COUP D’MAIN ! |
| Battle Pike | TOXIC IS A TERRIBLE THING ISN’T IT? | TOXIK C’EST VRAIMENT TERRIBLE ! |
| Apprenti | YOUR WIN ANGERS ME ! | TA VICTOIRE ME DEMORALISE ! |
| Trainer Tower | EEK !! I AM SORRY I SURRENDER | OUILLE !! PARDON JE DOIS ABANDONNER |
| Trainer Tower | WE HAVE TO WORK BETTER | IL FAUT TRAVAILLER MIEUX !! |
| Trainer Tower | ELECTRIC ! IT’S ABOUT WIRELESS LINK | ELECTRIK ! C’EST UNE CONNEXION SANS FIL |
| Courrier d'échange | I WILL MAKE BAGON TOUGH PLEASE TRAIN HORSEA WELL | DRABY EST CORIACE ! ENTRAINE HYPOTREMPE S’TE PLAIT ! |
| Dame Quiz | A POKéMON WAS ONCE THIS ? PHONE PLUSH DOLL LETTER (réponse PLUSH DOLL) | VIBRAQUA C’EST UNE ? CAPACITE COULEUR OU UNE ODEUR (réponse CAPACITE) |
| Barde (chanson par défaut) | SHAKE IT DO THE DIET DANCE | LA DIETETIQUE C’EST COOL |
| Phrase de combat par défaut | ARE YOU READY ? HERE I COME ! | ATTENTION ! ME VOILA ! |

## Cas douteux / points à suivre

1. **Le vocabulaire des `.po` ne correspond pas encore à l'officiel** (bloquant pour le rendu) : les
   phrases officielles supposent le mot d'Émeraude FR à chaque index. Or 227 mots Easy Chat ont un
   msgstr différent (101 en casse seulement, p. ex. « C’est », « Mon », « Je Suis », « Allez »,
   « Quoi? » ; 112 de sens ou d'accent ; 14 vides), sans doute parce que le msgid est fusionné avec
   d'autres chaînes. 155 d'entre eux sont utilisés par ce patch, p. ex. LET_S « ÇA VA? » au lieu de
   « SOIS », HER « ELLE » au lieu de « TA », IT « ÇA » au lieu de « TU VEUX », ON « OUI » au lieu de
   « VEUX », COOL « SG-FD » au lieu de « COOL », RECOMMEND « RECOMMANDE » au lieu de « TROP »,
   MISS « MISS » au lieu de « L’ », TIME « DUREE JEU » au lieu de « TEMPS », OFF (vide) au lieu de
   « VONT ». Liste complète avec l'adresse du mot dans `em_fr.gba` : `vocabulaire_po_vs_officiel.tsv`
   (colonne « emplois_dans_le_patch »). Les mots A et I (non extraits) sont, dans Émeraude FR :
   ENDINGS 32 = « UN » (entrée 0x59E930, texte 0x59E6D1) et PEOPLE 1 = « JE » (entrée 0x59D958,
   texte 0x59D78B).
2. **Trainer Tower, `trainer_tower_sets.c:2685`** : Rouge Feu FR et Émeraude FR n'ont pas le même mot
   à STATUS 0 / STATUS 14 (Rouge Feu FR : « PSY » / « HORRIBLE » ; Émeraude FR : « TENEBRES » / « PSY »).
   La réplique officielle « LE POISON C’EST HORRIBLE HEIN? » aurait donné « … C’EST PSY HEIN? » : le mot
   a été remplacé par EC_WORD_AWFUL (« TERRIBLE »). Aucune autre réplique de la Trainer Tower n'emploie ces index.
3. **MORTY, défaite (`battle_frontier_trainers.h:2539`, KTHX, BYE.)** : phrase identique à celle d'une
   Dresseuse de la Tente de Poivressel ; la version officielle « CHENAPAN ! » a été reprise telle quelle
   (fidèle à la méthode, mais peu naturelle pour un Champion).
4. **Mots de passe de l'Œuf Étrange (`easy_chat.c:1416-1426`)** non modifiés : ils sont comparés par
   identifiant à la saisie du joueur, il ne faut pas les changer. En jeu, le joueur devra saisir les
   mots FR officiels des mêmes index (p. ex. STATIK / ELECTRIK / OUAH / SATISFAIT pour la 1ʳᵉ ligne :
   les talents et types gardent leur sens, mais les cris/actions FR n'ont plus le même sens que
   l'anglais). Aucune réplique du jeu ne donne ces mots ; si une aide externe est traduite, elle devra
   citer les mots FR des mêmes identifiants.
5. **Phrases secrètes** (cadeau mystère « CONNEXION AVEC LES DRESSEUR », phrases de la femme du Maître
   des Baies « SPLENDIDE COMBAT », « CONCOURS DEFI », « IRRESISTIBLE LATIAS », « COOL LATIOS »,
   « SUPER AGITATION ») : ce sont maintenant celles d'Émeraude FR ; aucun texte de HnS ne les cite.
6. **Trainer Hill** : HnS a renommé 38 des 68 Dresseurs mais garde les répliques d'Émeraude ; les
   répliques sont reprises par contenu (exact), sans lien avec les noms.
7. **Noms officiels qui diffèrent des `.po`** (relevés en passant, non modifiés) : Zone de combat
   MARCO = TARIK (po : Marcus), TRISTAN = GILDAS (po : FRANCK), LAMAR = LAMAR (po : NACER),
   REGINA = REGINA (po : Régina) ; Tente de Vergazon DENNIS = DENNIS (po : Gilles).
8. Les traductions officielles sont des adaptations libres (p. ex. « IT’S SAD TO SEE YOU STRUGGLE » →
   « J’ADORE LES MAGAZINES DE MODE ! ») : reprises telles quelles.

## Fichiers

- `tables_easychat.tsv` : une ligne par réplique — fichier, ligne, source (adresse dans la ROM FR),
  anglais décodé, FR officiel décodé, FR tel qu'affiché avec les `.po` actuels, ancien affichage
  (identifiants anglais + `.po`), constantes écrites.
- `vocabulaire_po_vs_officiel.tsv` : mots Easy Chat dont le msgstr diffère du mot officiel.
- `scripts/` : chaîne qui a produit le patch (`build.py` en dernier ; nécessite `build/pokeemerald`
  compilé et les tables de symboles `nm` de pokeemerald et pokefirered).
