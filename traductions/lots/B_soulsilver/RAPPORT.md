# Lot B — ré-alignement SoulSilver FR : rapport

## 1. Résultat

| Fichier | Entrées | Contenu |
|---|---:|---|
| `exact.json` | 424 | anglais HnS normalisé = message HGSS entier → texte SS FR converti |
| `adapte.json` | 325 | même texte SS à une retouche près (détail ci-dessous) |
| `noms.json` | 264 | Dresseurs Johto/Kanto (257 : 246 `trainers_hns.party`, 11 `trainers_frlg.party`), classes (4), lieux (3) |
| `douteux.json` | 770 | correspondances trouvées mais non sûres, chacune avec sa raison dans `note` |
| `confirmations.json` | 95 | proposition SS **identique** au msgstr actuel : seule la source changerait (« patch FR » → « SoulSilver FR officiel ») |
| `verifications.tsv` | 6 lignes | toutes dans `douteux.json`, déjà expliquées dans leur `note` (voir §6) |

Sur `exact` + `adapte` + `noms` : **0 problème** pour `verifier.py`.

Ce que remplaceraient ces 1 013 entrées (exact + adapté + noms) :

| Source actuelle dans le .po | exact | adapté | noms |
|---|---:|---:|---:|
| patch FR actuel (toutes variantes) | 347 | 285 | 7 |
| non traduit | 60 | 14 | 228 |
| traduction manuelle | 12 | 12 | 5 |
| relu et corrigé à la main | 5 | 9 | 1 |
| Émeraude / SoulSilver officiel (seulement des entrées `msgctxt` par fichier, cf. §4) | – | – | 23 |

Par domaine : exact = menus 228 / dialogues 109 / données 87 ; adapté = dialogues 295 / menus 14 / données 11 ; noms = données 249 / menus 15 (domaine du .po où se trouve le msgid).
Par type de texte : exact = messages de combat 153, réactions du Pokémon qui suit 106, cartes Johto/Kanto `_hns` 89, menu de debug (noms d'objets) 45, divers 31 ; adapté = cartes Johto/Kanto `_hns` 256, cartes Kanto `_Frlg` 24, divers 45.

Entrées examinées : 19 304 entrées texte hors officiel (non traduites, patch FR, traductions manuelles, relues), après exclusion des noms (traités à part) et des mots du Livret (`easy_chat`, vocabulaire Émeraude). Pour les noms : les 1 275 Dresseurs de `trainers_hns.party` et `trainers_frlg.party`, et les noms d'objets, capacités, talents, espèces, classes et lieux hors officiel.

Peu de résultats au total, et c'est attendu : la plupart des textes encore hors officiel viennent de Hoenn (lot A), de FRLG (textes Rouge Feu, pas HGSS), de l'expansion (Gen 5 à 9) ou ont été réécrits par le hack. Par exemple, 474 noms d'objets, 483 capacités, 184 talents et 587 espèces encore hors officiel n'existent pas dans SoulSilver.

## 2. Méthode (scripts relançables dans `outils/alignement/`)

```
# clone partiel de pret/pokeheartgold (≈ 10 Mo)
git clone --depth 1 --filter=blob:none --sparse https://github.com/pret/pokeheartgold.git phg
cd phg && git sparse-checkout set --no-cone '/files/msgdata/msg/*' '/tools/msgenc/charmap.txt' \
    '/files/msgdata/NARC_msg.txt' '/files/poketool/trainer/*'
# puis, depuis $P :
.venv/bin/python outils/alignement/ss_paires.py  --phg <phg> --travail <dossier>
.venv/bin/python outils/alignement/ss_aligner.py --travail <dossier>
.venv/bin/python outils/alignement/ss_noms.py    --travail <dossier> --phg <phg>
.venv/bin/python outils/alignement/ss_sorties.py --travail <dossier>      # écrit dans traductions/lots/B_soulsilver
```

- `gen4msg.py` (repris) : charmap en argument (`--charmap`), option `--format pret`, et **décodage des chaînes compressées** (0xF100, caractères de 9 bits). Sans ça, la banque 729 (noms de Dresseurs) et une partie de la 246 ne donnaient que `{TRNAME}` dans `memoires/ss_fr_msg.json`. Je n'ai pas écrasé ce fichier, qui est partagé.
- `ss_paires.py` : anglais HGSS lu dans les JSON de pret (`files/msgdata/msg/msg_XXXX.json`), plus la banque 729 générée à partir de `trainers.json`. Le français est relu dans la ROM, au même format que l'anglais. Les fichiers pret sont numérotés comme le NARC `a/0/2/7` (828 fichiers + la 729 générée = 829 banques, comme dans la ROM).
- `ss_commun.py` : normalisation (sans codes, casse, accents, ponctuation, `\n \l \p \r \f`) et conversion du français :
  - variables `{STRVAR_x t, i, …}` → variable HnS de même rang dans l'anglais. On vérifie que le nombre est le même et que la correspondance est cohérente : une même case HGSS va toujours vers le même code HnS. Le français peut réordonner les variables ;
  - codes HGSS sans équivalent (COLOR, YESNO, PAUSE, ALN…) supprimés ; codes de forme HnS en tête ou en queue (`{COLOR}`, `{PLAY_SE}`, `{PAUSE}`…) remis à leur place ; si un code est au milieu → douteux ;
  - « » → “ ” ; espaces fines supprimées ; `...` → `…` ; `₧₦` → `{PKMN}` ; `¹`/`⁴` (étages 1ᵉʳ, 2ᵉ) → `{SUPER_ER}`/`{SUPER_E}` ; **`$` (Pokédollar SS) → `¥` collé au nombre**, comme Émeraude FR (« 500¥ »). En Gen 3, `$` vaut 0xFF, la fin de chaîne (cf. §6).
  - `\r` → `\p`. **Écart volontaire par rapport à la consigne** : `\f` devient `\l` et non `\p`. En Gen 4, `\f` attend puis fait défiler une seule ligne : dans pret, il vient après la 2ᵉ ligne d'une boîte dans 2 928 cas sur 3 754, et `\r` après la 1ʳᵉ ligne dans 3 205 cas. Le mettre en `\p` coupe les phrases en deux boîtes. C'est déjà arrivé à 134 entrées « SoulSilver FR officiel » existantes (« tu ne peux pas\ntransporter\pplus de Pokémon… »).
- Mise en page : la coupure officielle SS est gardée si chaque ligne tient en 198 px. Sinon, on remet en page à 198 px sans fusionner une ligne SS qui finit une phrase ou un titre (« Puits RAMOLOSS »). Les fragments (`\n`/`\p` final, `{DYNAMIC}`, `{CLEAR_TO}`) ne sont pas remis en page. Un libellé anglais d'une ligne reste sur une ligne ; s'il devient nettement plus large que l'anglais → douteux. Les descriptions à lignes fixes (données) suivent la largeur de l'anglais, sans ajouter de ligne.
- Contrôle final de chaque proposition : mêmes codes que l'anglais, nombres identiques, fins (`\n \p \l`, espace) et espace initiale conservées, aucun caractère hors charmap.

### Exact (424)
Clé = anglais normalisé du **message HGSS entier**. L'interlocuteur HnS peut différer d'écriture (« LANCE: » / « Lance: ») ; il est rendu par le préfixe SS (« Peter: »). Les entrées anglaises courtes (≤ 2 mots) ne sont gardées que si le contexte HnS correspond à la banque SS : `items.h`/`battle_debug.c` ↔ 222, `moves_info.h` ↔ 750, `abilities.h` ↔ 720, `battle_message.c` ↔ 197, carte ↔ 279, suiveur ↔ 265. Les 173 autres ont été rejetées sans être recopiées.
Quand le même anglais a plusieurs français SS :
- même texte à la casse près → graphie en casse normale ;
- variantes masculin/féminin ou tu/vous → douteux ;
- banques différentes et textes éloignés → douteux ;
- sinon, la première variante, avec les autres dans `note`.

### Adapté (325)
- 73 : anglais identique aux espaces et abréviations près (`PROF.`/Professor, `DEPT.STORE`, `S.S.TICKET`), ou à une contraction / un article près (’s/is, the/a, « -type », « CITY »…) ;
- 27 : extrait de pages d'un message SS (même nombre de boîtes `\r` en anglais et en français, au moins 5 mots), ou deux messages SS consécutifs fusionnés par le hack ;
- 26 : interlocuteur ajouté ou retiré (« KIMONO GIRL: » → « Kimono: », « PROF.ELM: » → « Orme: », préfixe SS « Jasmine: » retiré quand le hack ne l'a pas) ;
- 16 : substitution d'**espèce, objet, CT/CS, nombre** (« Mon PHANPY » → « Mon GRANBULL », « CT85 » → « CT42 ») ou variable SS → valeur en dur du hack (« {STRVAR_1 50…} » → « 6 »). Garde-fous : le terme SS doit apparaître une seule fois, l'élision doit rester correcte (de/d’, le/l’, ce/cet), et on ne substitue jamais une personne (cf. §5) ;
- 178 : **relus à la main** (`outils/alignement/ss_valides.json`). Ce sont les correspondances approchées à 94 % et plus dont l'anglais HnS ne diffère de HGSS que par un détail sans effet sur le français SS : orthographe (« BLACKGLASSES »), interjection (« Gah »/« Gaah »), mot retiré, synonyme (« TIN TOWER »/« Bell Tower » = Tour Carillon, comme dans le .po), « tamer »/« trainer »… J'ai examiné 240 candidats : 187 acceptés, 53 refusés (numéro différent, objet différent, phrase ajoutée par le hack, variable en plus, nom de personne différent…). Le texte SS est repris tel quel. 1 entrée a été écartée à la relecture (§5).
- 5 : autres (préfixe identique, casse).

### Noms (264)
- **Dresseurs** (257) : chaque Dresseur HnS est rapproché des Dresseurs HGSS de même nom anglais (`trainers.json`, index = ligne de la banque 729). On départage par la classe (« Hiker Hns » ↔ `TRAINERCLASS_HIKER`, Cooltrainer ↔ Ace Trainer, Officer ↔ Policeman, Rocket Admin ↔ Executive…) et par l'équipe (indice de Jaccard sur les espèces). Statut :
  - sûr : un seul nom FR possible et même classe ;
  - départagé : plusieurs noms FR possibles, une seule correspondance par la classe et l'équipe ;
  - ambigu ou simple homonyme (classe différente) → douteux.

  Longueur ≤ 10 vérifiée. Quand le msgid est partagé avec un autre fichier (Dresseur de Hoenn, Frontier, échange, Pokédex des célébrités FRLG…), l'entrée porte `msgctxt` = chemin du fichier Johto/Kanto (190 entrées). Exemple : BILL (Cracheur de feu de `trainers_hns.party`) → « Andréa », alors que le msgid BILL vaut « Léo » pour le personnage.
- **Classes** (4) : OFFICER → Agent, ROCKET → Rocket, ROCKET ADMIN → Commandant (HGSS « Executive »), BOSS → Boss Rocket. COOLTRAINER et POKéMANIAC sont confirmés tels quels (`confirmations.json`).
- **Lieux** (3) : ROUTE 23, POKéMON MANSION → Manoir Pokémon, MT. MORTAR → Mont Creuset. Seuls ces trois-là étaient encore hors officiel.
- Objets, capacités, talents, espèces : 6 trouvés seulement (FLY → Vol, DIG → Tunnel, MEW, MUK…), tous déjà identiques au .po (`confirmations.json`). Les autres étaient déjà officiels ou n'existent pas en Gen 4.

### Douteux (770)
| Raison | Nb |
|---|---:|
| approché (88 à 97 %), non adaptable automatiquement ; anglais HGSS et texte SS dans `note`/`preuve`, `msgstr` vide | 344 |
| Dresseur : homonyme HGSS de classe différente (souvent un Dresseur FRLG portant le nom d'un Dresseur Johto) | 173 |
| même anglais, plusieurs français SS (genre, tu/vous, contextes différents) | 99 |
| libellé d'une ligne trop large une fois traduit (surtout `battle_message.c`) | 38 |
| variables HnS / SS différentes (messages de combat Gen 3, `{DYNAMIC}`, `{PLAYER}` absent du SS…) | 47 |
| codes de mise en forme au milieu (`{CLEAR_TO}` / `{CURSOR_X}` dans les menus de prix) | 13 |
| nombres différents (« Je suis le quatrième » / « No. 5 »…) | 20 |
| autres : description trop longue, interlocuteur sans équivalent, glyphe ♡ ☆ ♌, écarté à la relecture… | 36 |

## 3. Qualité des paires HGSS EN ↔ SS FR
- Les 44 267 paires de `memoires/tm_ss_pairs.pkl` ont l'anglais **identique** à pret (0 différence). Il leur manque la banque 729 (noms compressés). Mes paires (`ss_paires.py`, 45 000 non vides) ont, pour **les 829 banques**, le même nombre de lignes en anglais et en français.
- **Banque 802** (Pokédex) : en fait alignée ligne à ligne. Seuls défauts : lignes 13/16 (même français pour deux anglais) et 23/24 (une phrase coupée en deux lignes FR). Elle reste exclue, comme demandé ; de toute façon HnS utilise le Pokédex de l'expansion.
- Autres banques à exclure ou à manier avec soin, repérées par le ratio de longueur et la cohérence des codes et nombres :
  - **440** (crédits : les noms du personnel de localisation diffèrent d'une langue à l'autre) ;
  - **812 à 815** (tailles et poids : pieds/livres ↔ m/kg, 0,2 % de nombres cohérents) ;
  - **27, 310** (listes de prénoms sans lien d'identité) ;
  - **246** (noms compressés).

  Toutes sont exclues de l'alignement de textes.
- Lignes SS « Non utilisé » (ex. 582:1) et paires au ratio de longueur aberrant (< 0,4 ou > 2,6 dès 15 caractères) : filtrées. Sans ce filtre, « Waaaaaah! You're mean! » recevait « Non utilisé ».
- Banques à codes peu cohérents (664, 548, 557, 379…) : alignement correct, mais la traduction SS omet ou ajoute des variables (« Mon poussin » au lieu de `{PLAYER}`). Ces cas tombent en douteux (variables différentes).

## 4. Taux d'erreur observés (relecture manuelle)
| Méthode | Échantillon | Erreurs | Taux |
|---|---|---|---|
| exact | 100 tirées au hasard (graine 101) | 0 (+1 problème de registre sur un msgid partagé, « You don't have enough money. » : tu chez le marchand d'Acajou, vous au Musée d'Argenta et à la Pension) | 0 % → la règle tu/vous a envoyé ce type de cas en douteux |
| adapté (automatique) | 100 (graine 202), puis relecture des 142 restants après correctifs | 1ʳᵉ passe : 2 (« de la part de Auguste », élision ; « Champion: Koga / Miss je-sais-tout-sur-les-poisons », épithète de Jeannine) ; 2ᵉ passe : 0 | 2 % → 0 % après correctifs (garde d'élision, plus de substitution de personnes) |
| adapté (relu à la main) | 178/178 relus un par un | 0 retenue fautive connue ; 1 écartée (§5) | – |
| noms | 100 (graine 303) | 0 (classe et équipe concordantes dans les 100 cas) | 0 % |

Aucune méthode ne dépasse 2 % ; rien n'a été rangé en douteux pour ce motif.

## 5. Points à arbitrer

**Même anglais, sens différents.** Proposés avec `msgctxt` par fichier, ou laissés en douteux :
- prénoms de Dresseurs partagés avec Hoenn/Frontier/FRLG (190 entrées `msgctxt`). Exemples : WILL (Conseil 4 → Clément ; mot du Livret « JE VAIS »), BILL (Cracheur de feu → Andréa ; personnage Léo), BLUE (Blue / « BLEU »), RED (Red / « ROUGE »), LANCE (Peter), JOHNNY (aussi un nom par défaut de `main_menu.c`) ;
- textes génériques à registre variable (« You don't have enough money. ») ;
- variantes genrées SS (« Mon petit / Ma petite », « Merci de t'être occupée d'elle ») → douteux, à traiter avec les codes de genre si le hack en a.

**Textes officiels SS discordants avec le hack.**
- « PROF.ELM: … My assistant is at the POKéMON CENTER in VIOLET CITY » : le texte SS dit « Boutique Pokémon de Mauville », alors que l'assistant est au Centre Pokémon dans HnS → écarté (douteux).
- « Merci de t'être occupée d'elle » : forme féminine figée → refusée.

**Existant suspect.** NATHAN vaut « Nathan » (SoulSilver officiel) dans le .po, mais le Kinésiste Nathan de HGSS s'appelle « Jason » en FR → douteux. 15 Dresseurs de `trainers_hns.party` (RICKY, VALERIE, CALVIN, LAO…) **n'ont pas leur occurrence** `trainers_hns.party:<ligne>` dans les références du .po ; leurs entrées pointent quand même sur la bonne ligne.

**FRLG.** Les Dresseurs de `trainers_frlg.party` ne sont rapprochés que par le nom et la classe (11 retenus). Leur source officielle naturelle serait Rouge Feu FR, absente des sources.

## 6. Signalements pour l'agent principal (fichiers partagés, non modifiés)
1. **`$` = 0xFF en Gen 3** (fin de chaîne) et `verifier.py` ne le signale pas, puisqu'il est dans la charmap. Tout texte SS recopié avec « 500 $ » tronquerait la chaîne. Aucun msgstr actuel n'en contient (vérifié).
2. `verifier.py` en mode JSON : `com` reçoit le champ `source` (« SoulSilver FR officiel »), mais le code cherche « source : … ». La tolérance de 216 px des officiels et les contrôles FRAGMENT ne s'appliquent donc jamais aux lots JSON. Pour les classes de Dresseurs (`battle_main.c`, syntaxe `{ _("HIKER"), 10 }`), la longueur 12 n'est pas contrôlée : je l'ai vérifiée moi-même.
3. `memoires/ss_fr_msg.json` : banques 729 et 246 non décodées. Il suffit de relancer `gen4msg.py` (sans `--format pret`) pour régénérer le fichier.
4. 3 681 entrées « SoulSilver FR officiel » existantes : 346 gardent « ... » (3 points) et 134 ont un `\p` en milieu de phrase (ancien `\f`). Elles pourraient repasser par `ss_commun.convertir_fr` et la mise en page de `ss_aligner.py`.
5. 6 lignes de `verifications.tsv`, toutes dans `douteux.json`. Elles sont attendues : glyphes SS ♡ ☆ ♌ absents de la charmap (4) et `{PLAYER}` absent du texte SS (2). La raison figure dans la `note` de chaque entrée.

## 7. Termes SS qui contredisent le glossaire actuel
- « Oeuf » (SS, partout) / glossaire « Œuf » ;
- « Electrik », « Etincelle », « Ecorcia », « Iles Ecume », « Ebènelle », « Elève » : SS ne met pas d'accent sur les capitales, le glossaire et les consignes en mettent (« Électrik »). Les textes SS repris gardent leur graphie ;
- « Champion d’Arène » (apostrophe ’) / glossaire « Champion d'Arène » (apostrophe droite, contraire à la typographie retenue) ;
- classes : ROCKET ADMIN = « Commandant » (patch : « ADMIN ROCKET »), OFFICER = « Agent », BOSS = « Boss Rocket », Cooltrainer = « Topdresseur » ;
- TIN TOWER = « Tour Carillon » (cohérent avec le .po ; GSC FR disait « Tour Ferraille ») ;
- Dresseuse « Leia » (Topdresseuse HGSS, 729:115) / glossaire « Léïa » (personnage). Il s'agit probablement de deux personnes : vérifier avant d'unifier.

## 8. Vingt exemples notables (remplacement du patch FR ou d'une traduction manuelle)
| msgid | actuel | proposé (SS) |
|---|---|---|
| WILL (Conseil 4) | JE VAIS | Clément |
| BILLY (Écolier) | S | Bilhal |
| ED | E | Odilon |
| AL (Scout) | ME | Jean-Loïc |
| KENNY (`trainers_hns.party`) | GWENN | Gilles |
| BLUE | BLEU | Blue |
| RED | ROUGE | Red |
| LANCE (Champion) | PETER | Peter |
| ROCKET ADMIN | ADMIN ROCKET | Commandant |
| « Sorry, I'll be out for a while.\nMISTY, GYM LEADER… » | « …ONDINE, Championne D’ARENE… » | « Je suis absente pour l’instant.\nOndine, Champion de l’Arène… » |
| « It's the CARD KEY slot. » | « C’est la fente pour Carte MAGN. » | « Un lecteur de Carte Magnétique. » |
| « Where did I meet this SCIZOR? » | « …ce CISAYOX? » (faute) | « Où et quand ai-je rencontré\nce CIZAYOX? » |
| « Accessed BILL's PC. » | (patch) | « Accès au PC de Léo. » |
| « That will be ¥500, please. » | (patch) | « Ce sera 500¥! » |
| « EUSINE: Yo, {PLAYER}.\pWasn't that SUICUNE… » | « EUSINE: Salut… » | « Eusine: Salut, {PLAYER}.\pC’était…\nC’était SUICUNE, hein?… » |
| « What?! You made it past our men in\nthe UNDERGROUND? » | « …nos gars du\nSOUTERRAIN? » | « Quoi?! Tu as réchappé à nos hommes du\nSouterrain? Comment t’as fait? » |
| « That's WHIRLPOOL. Teach it to a\nPOKéMON… » | « …Apprends-la à un\nPOKéMON… » | « C’est Siphon.\pApprends-le à un Pokémon pour\ntraverser les tourbillons!… » |
| « Monday, MONICA\nROUTE 40\p… » | (patch) | « Lundi, Lucie\nChenal 40\pMardi, Marie\nRoute 29… » |
| « So, want to know how to raise\nPOKéMON well? » | trad. manuelle | « Alors! Tu veux savoir\ncomment élever des\lPokémon! qui sont forts? » (ponctuation SS d'origine) |
| « I'm training to\nbecome the CHAMP! » | « Je m’entraîne pour\ndevenir Maître! » | « Je brigue moi aussi la position de\nMaître! » |

## 9. Propositions pour le glossaire / DECISIONS
- Noms SS des Dresseurs Johto (banque 729) par fichier : retenir `msgctxt = src/data/trainers_hns.party` quand un prénom anglais est partagé avec Hoenn.
- Décider Oeuf/Œuf et l'accentuation des capitales (Electrik/Électrik…), qui touchent tous les textes SS repris.
- Pokédollar : « 500¥ » (Émeraude FR) partout, jamais « $ ».
