# Lot A : ré-alignement Émeraude US ↔ Émeraude FR

## 1. Résumé

| Fichier | Entrées | Contenu |
|---|---:|---|
| `exact.json` | 1 917 | octets anglais retrouvés dans Émeraude US, FR par pointeur (1 392) ou par « zone parallèle » (525, structures de longueur fixe) |
| `tables.json` | 334 | tables par index : Dresseurs Frontier/Tentes/Concours/échanges/apprentis (329), tables de noms à pas fixe (5) |
| `contexte.json` | 16 | séquences de chaînes voisines vérifiées des deux côtés |
| `adapte.json` | 467 | approché : 427 textes identiques à Émeraude à la casse/ponctuation/mise en page près (source « Émeraude FR officiel »), 36 adaptés (codes, nombres, noms) ; plus 4 textes exacts dont les codes `CLEAR_TO` ont été remis à l’anglais |
| `douteux.json` | 877 | dont 197 propositions avec `msgctxt` (même anglais, sens différents) |
| `confirmes.json` (en plus) | 6 321 | msgstr actuel **identique** au texte Émeraude FR officiel (6 205) ou même terme à la casse/aux accents près ou abrégé (116, l’actuel est gardé) : seule la source du .po change (patch FR 5 045, SoulSilver 1 220…) |
| `verifications.tsv` | 181 lignes | 0 problème bloquant hors `douteux.json` (voir §6) |

Entrées examinées : 26 402 entrées des .po sans « source : Émeraude FR officiel » (dont 4 524 vides). Textes anglais présents
octet pour octet dans Émeraude US : 9 509 msgid ; avec au moins un candidat FR : 9 202.

**Changements proposés hors douteux : 2 734** (exact + tables + contexte + adapte), qui remplacent :
1 262 entrées non traduites, 1 125 « patch FR actuel », 220 « SoulSilver FR officiel », 79 « traduction manuelle »,
38 « relu et corrigé à la main », 10 sans source.

## 2. Méthode (scripts dans `outils/alignement/`, relançables)

```
LOTA_TMP=<dossier temporaire> .venv/bin/python outils/alignement/em_lot_a.py
```
(`LOTA_TMP` par défaut : `memoires/lotA`, ~25 Mo de pickles ; toutes les sorties finales vont dans `traductions/lots/A_emeraude/`.)

1. **`em_pointeurs.py` — marche parallèle.** Ancres = fenêtres de 16 octets uniques (pointeurs masqués **à tout décalage**,
   donc aussi les pointeurs non alignés des scripts : `msgbox`/`loadword`…). Depuis chaque ancre et chaque paire de cibles
   découverte, on avance dans les deux ROM tant que les octets sont égaux ; une différence expliquée par un pointeur
   (08/09 au même endroit dans les deux ROM) donne une paire *cible US → cible FR* et une nouvelle graine. Règles de
   reprise au même décalage : champ texte complété par des 00 (tables de noms), resynchronisation après un champ court,
   tables `{pointeur, entiers}` à pas de 12 (mots Easy Chat). 65 196 cibles, 87,9 % de la ROM US parcourue, 5 s.
   Le tableau des décalages est gardé (`em_delta.npz`).
2. **`em_candidats.py`** : chaque msgid encodé (`Gen3(build/upstream_orig)`) est cherché (+FF) dans Émeraude US ;
   candidats `ptr` (cible du même pointeur), `delta` (zone parcourue en parallèle, avec début de champ identique et
   reprise de la marche après les deux textes), `table` (base = cible FR du pointeur de code précédent, contrôle que
   tous les débuts de texte voisins à ±96 octets sont aussi des débuts de texte en FR au même écart), `seq`/`seq1`
   (k-ième chaîne après/avant une chaîne connue du même bloc, deux côtés concordants / un seul), `tm` (table octets).
   **`tm_em_bytes.pkl` étendue** : 4 842 → 23 221 paires (copie : `memoires/tm_em_bytes_v2.pkl`).
3. **`em_tables.py` — tables par index** (ordre du fichier upstream = index ; table US retrouvée par les noms à pas
   constant, table FR par le pointeur de code + contrôle de structure entrée par entrée) :
   gTrainers (US 310034 / FR 317B64, pas 40, 854/855 noms identiques, octets hors nom identiques 90 %),
   gBattleFrontierTrainers (300/300, classe identique pour 300/300), 3 Tentes (3×30), gContestOpponents nom et surnom
   (96+96), gDefaultContestWinners (8+8), sIngameTrades surnom/dresseur (4+4), 18 groupes Easy Chat (EC_WORD, structure
   {texte, ordre, activé} vérifiée), apprentis (16 : le nom FR est dans la même structure upstream, présent dans les deux ROM).
   Les catégories du Pokédex d’Émeraude (US 56B5B0) sont repérées pour écarter les faux amis (IRON BALL, DISCHARGE…).
4. **`em_approche.py`** : rapidfuzz (≥ 85) sur les 14 550 textes Émeraude US à FR connu ; reprise telle quelle si seules
   casse/ponctuation/coupures diffèrent ; sinon adaptation limitée à des nombres, des codes (correspondance 1:1) et des noms
   propres dont le FR est connu des deux côtés ; tout le reste → douteux (≥ 88) ou ignoré.
5. **`em_sortie.py`** : décision, contrôles, style, écriture. Contrôles automatiques sur 100 % : mêmes codes en octets,
   nombres (avec équivalence un/one/1…), ratio 0,5–2,2 (phrases), fins `\n \p \l` et espaces, kana, longueur des champs
   (`verifier.Verif.champ`), anglais resté tel quel dans la ROM FR (318 candidats rejetés : la ROM FR contient des textes
   anglais non traduits/inutilisés), nom court hors contexte (fichiers HnS des textes voisins dans Émeraude US).
   Passage au style : `style.appliquer(…, glossaire, especes)` puis `gen3.nettoyer_kana`, graphie anglaise des codes
   remise quand les octets sont identiques (`{CLEAR_TO 78}` → `{CLEAR_TO 0x4E}`), retours à la ligne d’Émeraude FR gardés
   sauf ligne > max(216 px, ligne anglaise la plus large) ou texte anglais sur une ligne (lignes jointes, césures
   « inten-\nsifie » recollées d’après le vocabulaire FR) ; si le FR joint ne tient pas sur une ligne, coupures gardées (note).

## 3. Chiffres par domaine et par zone (hors douteux)

| Zone | dialogues | menus | données | total |
|---|---:|---:|---:|---:|
| données (`src/data`, .party) | – | 14 | 898 | 912 |
| Battle Frontier / Tentes / Mont Dresseurs / apprentis | 125 | 10 | 384 | 519 |
| Match Call / PokéNav | 61 | 1 | 292 | 354 |
| cartes Hoenn | 302 | – | – | 302 |
| scripts / textes communs (`data/scripts`, `data/text`) | 201 | – | 14 | 215 |
| Concours | 7 | 5 | 191 | 203 |
| moteur (`src/*.c`) | – | 151 | – | 151 |
| TV | 47 | – | – | 47 |
| cartes HnS (Johto/Kanto) | 21 | – | – | 21 |
| cartes FRLG | 10 | – | – | 10 |

Les cartes FRLG non compilées et la plupart des textes `data/text` restés vides ne sont pas dans Émeraude (FRLG FR n’est pas
une source disponible) : peu de gain possible au-delà de ce qui est listé.

Douteux par zone : données 412, moteur 145, Frontier 131, cartes Hoenn 38, scripts communs 34, Concours 25, Match Call 25,
cartes HnS 19, FRLG 14, TV 4.

## 4. Taux d’erreur par méthode (relecture manuelle d’échantillons aléatoires)

| Méthode | Échantillon relu | Erreurs à la 1ʳᵉ relecture | Corrections | Taux final observé |
|---|---|---|---|---|
| `ptr` (pointeurs) | 3 × 100 | 4/100 : mots Easy Chat (mot FR du même index, pas une traduction) | Easy Chat → douteux | **0/100** |
| `delta` (zone parallèle) | 4 × 100 | 6/100 : faux sens (catégorie Pokédex « MEDITATION » pour la capacité, « LUNE », « SOUHAIT »), copies anglaises (« B Button », « …RANK STAGE! »), 1 décalage dû à une espace (« LILY » → « D’Eau ») | plage Pokédex exclue, ambiguïtés → msgctxt, règle « espace ≠ début de chaîne », rejet des copies anglaises | **0/100** |
| `tidx` (tables par index) | 2 × 100 | Easy Chat : ~25 % de mots non équivalents (« PLACE » → « IL A ») ; noms : 0 | Easy Chat → douteux (> 2 %) | **0/100** (noms) |
| `table` (pas fixe) | 7/7 puis 5/5 | 1 (« ADMIN » → « MAGMA », 2ᵉ mot de « ADMIN MAGMA ») | même règle d’espace | **0/5** |
| `seq` (séquence) | 25/25 puis 16/16 | 7/25 : copies anglaises de la ROM FR | rejet des copies | **0/16** |
| `approche` | 100 | 2/100 : césures mal recollées (« s’inten- sifie ») | recollage d’après le vocabulaire | 0 (après correction) |
| Easy Chat (toutes méthodes) | 100 | ~25 % | **rangés dans douteux** (règle > 2 %) | – |

Les morceaux de phrases composées (TV, Match Call, présentations : « but different desserts. » → « mais pas les mêmes glaces. »,
~8 % des `ptr`) ont été comptés justes : c’est le texte FR officiel du même emplacement (la phrase française est découpée
autrement) ; isolés, ils ne se traduisent pas mot à mot.

## 5. Entrées remplaçant une source de rang inférieur : 20 différences notables

Plusieurs textes du **patch FR** étaient associés à la mauvaise phrase (répliques permutées) :

| anglais | actuel | Émeraude FR officiel |
|---|---|---|
| Something unseeable is in the way.\pWant to use the DEVON SCOPE? | (patch) Certains Pokémon évoluent quand ils sont échangés!… | Quelque chose d’invisible bloque la\nvoie.\pVoulez-vous utiliser le DEVON SCOPE? |
| There are POKéMON that evolve when\nyou trade them!… | (patch) Quelque chose d’invisible bloque la voie… | Certains Pokémon évoluent quand ils\nsont échangés! C’est ce qu’on raconte! |
| Falling… Losing…\nThis is so humiliating for me! | (patch) Je veux aller à Poivressel et provoquer une bagarre! | Tomber… Perdre…\nTout ça est si humiliant pour moi! |
| TEAM AQUA's actions should bring\nsmiles to people's faces! | (patch) C’est un sol meuble et fertile. Voulez-vous planter une Baie? | Les actions de la TEAM AQUA rendront\nle sourire à tout le monde! |
| This is my first job after joining\nTEAM AQUA. It's a little scary. | (patch) La pêche repose sur la concentration… | C’est ma première mission en tant que\nmembre de la TEAM AQUA. J’ai les j’tons! |
| MOVE TUTOR'S HOUSE\n“New moves taught to POKéMON.” | (patch) “Rajeunissez vos partenaires fatigués!” CENTRE Pokémon | MAISON DU Maître DES CAPACITES\n“Venez apprendre de nouvelles\lcapacités à vos Pokémon!” |
| Wow…\nHow could you be so strong? | (patch) Waouh…\nQuelle puissance! | Waouh… Comment peut-on avoir autant\nde talent? |
| If seawater gets up your nose,… | (patch) L’eau de mer dans le nez, c’est horrible, non? | Tu ne trouves pas ça affreux d’avaler\nde l’eau salée par le nez? |
| Inflicts a burn on\nthe foe with\nintense fire. | (patch) Brûle l’ennemi avec un feu intense. | Inflige une douloureuse \nbrûlure à l’ennemi. |

Données venant de **SoulSilver** (banques mal alignées) ou non traduites :

| anglais | actuel | Émeraude FR officiel |
|---|---|---|
| DOUBLE TEAM (capacité) | (SS) Duo | Reflet |
| NIDORAN♂ | (SS) NIDORAN♀ | NIDORAN♂ |
| HELD ITEM | (SS) Held item | OBJET TENU |
| LINK CONTEST | (SS) Link Contest | CONCOURS EN LINK |
| KEATON (adversaire de Concours) | (SS) Aleks | KARIM |
| MACY (apprentie) | (SS) Magali | AMELIE |
| MASTER (Mixeur) | (SS) Master | Maître |
| The door is locked. | (SS) C’est fermé… | La porte est fermée. |
| No?\nThat's too bad. | (SS) OK…\nA bientôt j’espère. | Non?\nTant pis. |
| I lost! | (SS) Perdu... | Défaite |
| Communication error. | (SS) Erreur de communication... | Erreur de transmission… |

Les 1 220 entrées SoulSilver de `confirmes.json` (noms d’espèces, objets, capacités…) sont identiques au texte Émeraude
après passage au style : aucune contradiction pour elles.

## 6. Vérifications (`verifications.tsv`, 181 lignes)

- **Hors douteux : 74 lignes, toutes justifiées.**
  - `GLOSSAIRE` (45) : noms de personnages Hoenn gardés en capitales d’Émeraude FR alors que le glossaire SoulSilver les
    écrit en casse normale (ARTHUR/Arthur, PIERRE/Pierre = Steven, KIM, LANA, IAN, LEO…). Décision du §3 des consignes ;
    chaque entrée concernée porte une note.
  - `ANGLAIS` (29) : noms propres identiques en français (VICTOR, JENNA, Satoshi Tajiri, AGATHA, PLUS…) et quelques
    intitulés du générique laissés en anglais dans Émeraude FR (« Music Composition », « Coordinators », « Artwork »).
- Douteux : 107 lignes (`CODES` 73, `ESPACE` 20, `ANGLAIS` 10, `KANA` 3, `GLOSSAIRE` 1), raisons données dans `note`.
- Pas de ligne > 216 px hors douteux ; aucune `LONGUEUR` hors douteux (15 noms du Mont Dresseurs > 7 octets → douteux).

## 7. Contenu de `douteux.json` (877)

| Raison | Nombre |
|---|---:|
| nom de table Émeraude aussi porté par un Dresseur HnS (trainers_hns.party) : nom SoulSilver prioritaire | 263 |
| même anglais, sens différents : propositions avec `msgctxt` = chemin du fichier | 197 entrées (110 msgid) |
| approché sans adaptation automatique possible (FR officiel fourni, à adapter) | 157 (+13 contrôle) |
| mot Easy Chat (mot FR officiel du même EC_WORD, pas une traduction) | 148 |
| glyphe 0x64 d’Émeraude FR (abréviation des Points de Combat) remplacé par « PCo » (graphie du patch) | 50 |
| plusieurs textes Émeraude FR pour le même anglais, contexte non décidable | 40 |
| codes de contrôle différents (FR sans `{PLAYER}`, `{CLEAR_TO}` en plus…) | 25 |
| nombres différents (contenu localisé : Pokédex, 2 à 6 tours…) | 17 |
| fragments / ratio de longueur / séquence d’un seul côté / trop long pour le champ | ~40 |

## 8. Termes officiels Émeraude FR qui contredisent ou manquent au glossaire (propositions)

- **Noms Hoenn changés par le glossaire** (115 noms protégés automatiquement : noms FR des tables de Dresseurs et locuteurs
  « NOM: » d’Émeraude FR dont le glossaire a une entrée `personnage`) : ARTHUR (Arthur), PIERRE (Pierre = Pierre Rochard,
  homonyme du Pierre de Kanto), KIM, LANA, IAN, LEO, ALAIN, ARMAND, AUDE… Proposition : marquer ces entrées du glossaire
  comme « Johto/Kanto seulement » ou ajouter une liste d’exceptions Hoenn.
- **Absents du glossaire, restés en capitales** (les plus fréquents) : TEAM MAGMA, TEAM AQUA, CHENAL (routes marines),
  HOENN, LAVANDIA, POIVRESSEL, MEROUVILLE, PACIFIVILLE, ATALANOPOLIS, VILLAGE MYOKARA, CIMETRONELLE, MONT CHIMNEE,
  MONT MEMORIA, PISTE CYCLABLE, BASE SECRETE, PASSE ZONE, ZONE/TOUR/DOME/SALLE/PALACE/DOJO DE COMBAT, TOURNOI,
  CONCOURS, ARBITRE, ANIMATRICE, PRESIDENT, BILLET DE LOTERIE, VELO, BOITE, ATTAQUE / DEFENSE / VITESSE / ATQ. SPE. /
  DEF. SPE., PKMN (abréviation d’Émeraude FR dans les libellés courts).
- **Suites mixtes produites par `style.appliquer`** (le glossaire ne convertit qu’une partie d’une suite en capitales) :
  « CONSEILS AUX Dresseurs », « SALLE DE Combat SOLO », « Carte DE Dresseur », « MAISON DU Maître DES CAPACITES »,
  « BROYEUR DE Baies », « POINTS DE Combat » (des centaines d’occurrences, aussi dans les .po actuels). `style.homogeneiser`
  ou des entrées glossaire multi-mots (« CONSEILS AUX DRESSEURS », « POINTS DE COMBAT »…) régleraient cela ; je ne l’ai
  pas appliqué (consigne : `style.appliquer` seulement).
- **Termes où l’officiel Émeraude contredit la source actuelle** : DOUBLE TEAM = Reflet (actuel SS « Duo »), HELD ITEM = OBJET
  TENU, LINK CONTEST = CONCOURS EN LINK, Battle Points = POINTS DE COMBAT (abrégé glyphe 0x64, le patch écrit « PCo »).
- `OEUF` figure dans la liste `especes` (banque 237 « Œuf ») et n’était donc jamais passé au glossaire : je l’ai retiré de la
  liste dans mes scripts (« Œuf »). À corriger dans `amorcer.py`/le passage de style global.

## 9. Même anglais, sens différents

- 110 msgid ont des propositions avec `msgctxt` dans `douteux.json`. Exemples :
  MEDITATE (capacité YOGA / catégorie Pokédex MEDITATION), MOONLIGHT (Rayon Lune / LUNE), WISH (Voeu / SOUHAIT),
  MAGNET (Aimant / catégorie MAGNETIQUE), THUNDER, SCREECH, BARRIER, SLUDGE, SPIKES, SWALLOW, SUPERPOWER, POISON GAS ;
  ONE…SEVEN ISLAND (ILE 1… pour la carte et le Fame Checker) ; répliques de cartes différentes (« Here you go! » Voici!/Voilà!,
  « Which would you like to learn about? » Sur quel bâtiment…/Sur quel sujet…, répliques de FLORA/BRICE selon la route).
- Noms d’Émeraude portés par plusieurs Dresseurs différents (AVERY → EVAN/GREG, BEAU → YANIS/JANIE, KELSEY, PAIGE…) : douteux.
- Noms partagés avec des Dresseurs HnS (trainers_hns.party, 263) : le nom Émeraude n’est pas proposé (personnages
  Johto/Kanto → SoulSilver, lot B).
- Noms partagés seulement avec des données FRLG (trainers_frlg.party, Fame Checker) : nom Émeraude proposé faute de FRLG FR,
  avec note.
- `contextes.po` (7 entrées avec msgctxt) n’a pas été traité.

## 10. Problèmes rencontrés et contournements (fichiers partagés non modifiés)

- **`style.appliquer` ne voit pas un mot en capitales collé à `\n`, `\l` ou `\p`** (la lettre n/l/p précède : lookbehind) :
  ~360 entrées des .po actuels gardent des « POKéMON » ou « COUPE » en début de ligne. Contournement : application ligne par
  ligne dans `em_commun.officiel`. Même cause pour les élisions (« D’ARENE » converti seulement s’il suit une lettre).
- La ROM Émeraude FR contient de l’anglais non traduit (textes inutilisés) : rejeté automatiquement.
- `verifier.py` : le contrôle `ANGLAIS` signale les noms propres identiques (normal) ; la prise en compte de la source
  « officiel » pour les lots JSON a été corrigée pendant mon travail (préfixe « source : »).
- Pour relancer depuis zéro : `em_lot_a.py` (≈ 1 min). Les fichiers temporaires du scratchpad peuvent être supprimés.
