# Lot C2a : audit des dialogues hérités (patch FR, traductions manuelles anciennes)

## Ce qui a été examiné
- **934 remarques ChatGPT** (`C_audit/remarques_dialogues.json`) et **234 alertes automatiques** (`C_audit/alertes_dialogues.json`) : 1 095 msgid différents, tous dans `dialogues.po`.
- 1 035 msgid viennent du patch FR ou de traductions manuelles. Les 60 autres sont des textes officiels ou presque officiels : 47 Émeraude FR / SoulSilver FR, avec des alertes seulement, et 13 « SoulSilver FR, correspondance approchée », avec remarques.
- **Base de travail : le msgstr actuel du .po**, et non le texte que ChatGPT a relu. Pour 234 remarques, le .po a changé depuis la relecture (passage de style POKéMON → Pokémon, Œuf…). Chaque correction a donc été reportée sur le texte actuel. Une centaine de remarques déjà réglées par ce passage sont refusées pour cette raison (« déjà corrigé »).

## Méthode
- Chaque élément a été examiné à la main, avec :
  - le contexte upstream (interlocuteur, fragments voisins) ;
  - les répliques voisines des .po ;
  - les textes SoulSilver FR (`memoires/ss_fr_msg.json`) pour les noms et la terminologie ;
  - le texte du patch FR, retrouvé par pointeur : adresse anglaise dans `hns_en.gba`, pointeurs (alignés ou non), puis cible dans `hns_fr_patch.gba`.
- Remises en page avec `Gen3.reformater(…, 198)`. Une chaîne qui continue une chaîne terminée par `\n` garde `\l` comme premier saut. Les fragments `\n` / `\p` et les chaînes avec `{DYNAMIC}` / `{CLEAR_TO}` n'ont pas été reformatés.
- Contrôle : `outils/verifier.py` sur `C2a_corrections.json`. Résultat dans `C2a_verifications.tsv` : **0 problème bloquant** (CODES, ESPACE, FRAGMENT, TYPO, LONGUEUR, CARACTERE, KANA). Restent 22 signalements non bloquants, détaillés plus bas.
- Contrôles ajoutés au-delà du vérificateur :
  - pas de majuscule accentuée ;
  - pas de « Oeuf » ni de « les Rocket » ;
  - pas d'apostrophe droite, de « ... » ni de guillemets droits ;
  - une chaîne anglaise sur une ligne reste sur une ligne ;
  - une décision pour chaque remarque et chaque alerte.

## Sorties
| Fichier | Contenu |
|---|---|
| `C2a_corrections.json` | **785 entrées** au format §6, avec `ancien` = msgstr actuel et `note` = la décision et sa raison |
| `C2a_decisions.tsv` | 1 168 lignes : 934 remarques + 234 alertes (type, réf. R/A, msgid tronqué, catégorie, décision, raison) |
| `C2a_verifications.tsv` | verifier.py sur le JSON : 0 bloquant |
| `C2a_annexe_noms_dresseurs.tsv` | correspondance anglais → français des noms de Dresseurs HnS (donnees.po / contextes.po), utilisée pour les appels Pokématos |

Sources des 785 corrections :

| Source | Entrées |
|---|---|
| traduction nouvelle | 415 |
| patch FR actuel (vérifié) | 355 (seule la forme change : mise en page, codes, casse et graphie du glossaire, typographie) |
| SoulSilver FR, correspondance approchée (adapté) | 10 |
| Émeraude FR officiel / officiel (adapté) | 4, avec `retouche_officiel` |
| SoulSilver FR officiel (adapté) | 1, avec `retouche_officiel` |

Une entrée porte `alignement_faux: true` : « BILL'S PC.\p » (voir plus bas).

## Chiffres par catégorie et par décision

### Remarques ChatGPT (934)
| Catégorie | Accepté | Adapté | Refusé | Total |
|---|---|---|---|---|
| typographie | 148 | 55 | 92 | 295 |
| terminologie | 89 | 79 | 46 | 214 |
| contresens | 92 | 49 | 41 | 182 |
| oubli | 71 | 39 | 27 | 137 |
| orthographe | 23 | 13 | 14 | 50 |
| registre | 16 | 6 | 5 | 27 |
| codes | 12 | 4 | 10 | 26 |
| autre_phrase | 1 | 1 | 1 | 3 |
| **Total** | **452** | **246** | **236** | 934 |

Motifs de refus les plus fréquents :
- remarque déjà réglée dans le .po actuel, ou correction identique au texte actuel (~100) ;
- mise en page seule sans dépassement (~30), puisque le vérificateur compte déjà `{PLAYER}` = 42 px et `{STR_VAR}` = 60 px ;
- calque de l'anglais ou préférence de style sans faute (~25) ;
- graphie ou tournure déjà officielle SoulSilver FR ou Émeraude FR (~20) ;
- vouvoiement proposé à tort : les sages de Rosalia, le vendeur de vélos et les tuteurs tutoient dans les officiels ;
- « Oeuf » ;
- `{FONT 11}` / `{PAUSE 0x0F}` : mêmes octets, graphie réécrite à l'intégration (décision 5).

Motifs d'adaptation les plus fréquents : majuscules accentuées, casse des noms Hoenn (à garder en capitales), noms de Dresseurs Johto inventés par ChatGPT (voir plus bas), ligne trop longue, correction qui retirait autre chose.

### Alertes automatiques (234)
| Contrôle | Accepté | Adapté | Refusé | Total |
|---|---|---|---|---|
| LARGEUR | 50 | 28 | 26 | 104 |
| FRAGMENT | 3 | 0 | 73 | 76 |
| CODES | 9 | 0 | 16 | 25 |
| ESPACE | 13 | 0 | 0 | 13 |
| ANGLAIS | 1 | 0 | 7 | 8 |
| GLOSSAIRE | 2 | 6 | 0 | 8 |
| **Total** | **78** | **34** | **122** | 234 |

- **FRAGMENT : 73 faux positifs sur 76.** Le patch FR a souvent inséré ses textes juste après le code de script qui les appelle (`0F 00 <ptr> 09 02`). L'octet précédent vaut alors 0x02 (fin de commande), que `verifier.py` prend pour une lettre accentuée. Pour ces 73 textes, un pointeur du patch vise exactement l'adresse : le début est réel. Le sens a été vérifié pour chacun.
  - Proposition pour `verifier.py` : accepter un début de chaîne quand un pointeur `0x08xxxxxx` vers cette adresse existe dans la ROM du patch.
  - Les 3 vrais fragments ont été retraduits :
    - « défi de la TENTE DE Combat? » devient « Tente de Combat Palace? », pour se raccorder au fragment précédent qui finit par « défi de la\n » ;
    - « \nTant pis. » (fin de « Non?\nTant pis. ») devient « C’est dommage. » ;
    - « zzz… » devient « …Zzzz… », la vraie cible du pointeur du patch.
- **CODES : 16 refus**, tous sur des textes **Émeraude FR officiels** : variable omise ou ajoutée par l'officiel lui-même, qui s'affiche correctement. Les 9 autres codes ont été rétablis (`{PLAYER}` manquant chez BRICE, `{PLAYER}{KUN}` en trop chez FLORA…).
- **LARGEUR : 26 refus**, dont 24 sur des officiels Émeraude FR. Ils sont tolérés, et la largeur calculée compte `{STR_VAR}` à 60 px alors que ce sont des nombres ou des noms courts. Les 78 autres ont été remis en page ou raccourcis.
- **ANGLAIS : 7 refus.**
  - Cinq noms par défaut proposés au joueur (JUNE, MOMO, NORIE, SAI, TOSH), gardés comme leurs voisins.
  - Deux onomatopées de cri non dérivées du nom anglais (Cha-Cha!, Shuck!).
  - Le cri dérivé du nom anglais a été adapté.

## Exemples
- **Débuts tronqués du patch** : « rganisons le Tournoi K.O. », « ègle\nessentielle… », « ons des tournois Echange » deviennent « nous organisons… », « une règle essentielle… », « on tient des tournois Echange… ». Le raccord avec le fragment précédent a été vérifié.
- **autre_phrase** : « ?\nTu veux retourner à Oliville? » devient « Tu veux retourner à Oliville? ». Le « ?\n » venait de la chaîne précédente du patch.
- **Alignement faux** (officiel SoulSilver) : le fragment de dialogue « BILL'S PC.\p » portait le libellé de menu « PC DE LEO », sans `\p`. Il devient « le PC de Léo.\p », dans la suite de « {STR_VAR_2} a été transféré dans\n ».
- **Contresens accepté** : « AMY & MAY: Oh, double malheur! » devient « … double surprise! » (anglais : *double goodness*).
- **Oubli adapté** : « Un OBJET RARE peut être assigné à SELECT pour s’en servir vite. » devient « Maintenir SELECT permet d’utiliser\nvite un Objet Rare enregistré. ». ChatGPT vouvoyait, alors que les répliques voisines sont impersonnelles.
- **Terminologie refusée** : PROTON = « Lance » dans SoulSilver FR. L'étiquette est gardée, ADMIN devient « Commandant » (SoulSilver FR, banque 68), et la reformulation de ChatGPT n'est pas reprise.
- **Artefacts du passage de style corrigés** dans les entrées touchées : « TENTE DE Combat », « CENTRE\lPokémon », « Championne D’ARENE », « POLICE DE Céladopole », « LAC Colère », « SBIRE de la TEAM\nRocket », « Prof. CHEN », « ZONE DE Combat ».
- **Officiels retouchés** (`retouche_officiel`) :
  - deux répliques de Dresseur Émeraude FR sur une seule ligne de 260 et 238 px, qui sortaient de la fenêtre : saut de ligne ajouté, texte inchangé ;
  - « POINT(S) DE Combat » devient « Point(s) de Combat » (artefact de style) ;
  - « POKéMON 1, 2, et 3 » devient « Pokémon… » (passage de style) ;
  - réplique SoulSilver de Bourg Geon : fin `$\p` rétablie et `\p` en milieu de phrase remplacé par `\l` (décision 11).

## Harmonisations faites à la fusion (28 entrées)
- **Steven** : écrit « PIERRE » (étiquette « PIERRE: ») et « PIERRE ROCHARD » pour le nom complet, selon la règle des noms Hoenn en capitales d'Émeraude FR. Les relecteurs avaient produit au choix « Pierre: » ou « Pierre Rochard: ».
- **Étiquettes Johto/Kanto** en casse SoulSilver, comme la majorité du .po : « Peter: » (et non PETER:), « Chen: » (et non CHEN:).

## Doutes et points à arbitrer par l'agent principal
1. **Collision PIERRE.** Le glossaire a `PIERRE → Pierre` (Brock). Le passage de style a donc écrit « Pierre: » pour Steven dans 23 textes Émeraude FR officiels du .po, contre 10 « PIERRE: » restés en capitales.
   - J'ai appliqué la règle : Steven = PIERRE, d'où 21 signalements GLOSSAIRE non bloquants dans `C2a_verifications.tsv`.
   - À trancher : passer `PIERRE` en `msgctxt`, ou ajouter une exception de style pour les étiquettes Hoenn.
2. **Noms de Dresseurs Johto dans les appels Pokématos.** ChatGPT inventait des prénoms (Zeppo, Samson, Armelle…). Ils ont été remplacés par les noms SoulSilver FR déjà posés dans `contextes.po` / `donnees.po` : CHAD = Mathys, IRWIN = Anthony, REENA = Audrey, BEVERLY = Jade, ALAN = Aimé, DANA = Rekka, BRENT = Wilfrid…
   - Correspondance complète : `C2a_annexe_noms_dresseurs.tsv`.
   - Des répliques hors liste gardent encore l'ancien nom anglais.
3. **Noms SoulSilver posés dans les dialogues**, à reporter au glossaire et dans les répliques hors liste :
   - fratrie des jours : FRIEDA = Vanessa, WESLEY = Homer, SANTOS = Samuel, MONICA = Lucie, TUSCANY = Marie, SUNNY = Dimitri ;
   - Kimonos : ZUKI = Tamao, NAOKO = Umeko, MIKI = Satsuki, SAYO = Sakura, KUNI = Komomo ;
   - DJ MARY = Lula, BONNIE = Buena, SAMSON OAK = Raphaël Chen, LANCE = Peter.
   - Restent à harmoniser hors liste : RadioTower_2F l. 231/237/243 (BONNIE) et les « ZUKI/NAOKO…: Go, face HO-OH. » de TinTower_RoofDay.
4. **Artefacts du passage de style dans des textes officiels non audités** : « TENTE DE Combat » (une douzaine d'officiels Émeraude FR), « MONT Dresseurs », « CONSEILS AUX Dresseurs ». Il faut corriger `style.py` ou le glossaire (entrées TENTE DE COMBAT, MONT DRESSEURS).
5. **Tentes de Combat** : j'ai écrit « Tente de Combat » partout, sur le modèle de Tour de Combat et Usine de Combat. Les fragments voisins hors liste écrivent encore « TENTE DE COMBAT ARENE/PALACE/USINE ». Une entrée propose « Tente de Combat Dojo » pour ARENE.
6. **Points Combat / Points de Combat** : les deux graphies existent dans SoulSilver FR (banque 748 contre banques 10, 26, 96). Les deux restent dans le lot, selon le contexte d'origine. À unifier, de préférence sur « Points de Combat ».
7. **EON MAIL = « Lettre Evoli »** : nom d'Or/Argent FR écrit de mémoire, absent du glossaire et des textes SoulSilver FR. À vérifier.
8. **Libellés du dojo de Safrania** (lot C2b) : les dialogues utilisent maintenant AS, DS, VI. Les libellés ATK / DEF de `menus.po` sont à aligner.
9. Doutes isolés :
   - « Pokémon postier » choisi pour tenir sur une ligne ;
   - panneau abrégé en « BUREAU DE DEV. HEART & SOUL » ;
   - « Attaque Spéciale » / « Défense Spéciale » écrits en toutes lettres dans deux dialogues ;
   - BETH et RILEY laissés en anglais, car le .po ne les traduit pas encore.

## Termes proposés pour le glossaire
- **Graphie à corriger** : TENTE DE COMBAT → Tente de Combat ; MONT DRESSEURS → Mont Dresseurs ; KANTO → Kanto ; JOHTO → Johto ; SINJOH → Sinjoh (Nouveau Sinjoh) ; POKEDEX NATIONAL → Pokédex National ; POINTS DE COMBAT → Points de Combat ; COMBAT HASARD → Combat Hasard ; POKé FLUTE → Poké Flûte.
- **Lieux et bâtiments** : FAST SHIP / S.S. AQUA → Bateau Express (Aquaria) ; GOLDENROD TUNNEL → Doublon-Tunnel ; SOUL HOUSE → Maison des Souvenirs ; Centre Commercial ; Cycles à Gogo ; Salon Pokémon ; Ranch Meumeu ; Académie Pokémon ; Marché du Dresseur ; Salle de Danse ; Train Magnétique.
- **Divers** : Badges Foudre, Terre, Minéral, Plaine ; Chronique Pokémon (du Prof. Chen) ; Commandant (Rocket Executive) ; Glas Transparent.
- **Personnages** : voir le point 3 ci-dessus, plus Major Bob et Red.
