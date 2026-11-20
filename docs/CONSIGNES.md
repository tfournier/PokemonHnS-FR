# Consignes communes aux lots de traduction (pokehns-fr)

Ce document est la référence pour **tout** travail sur un lot. Lis-le en entier avant de commencer.

## 1. Le projet
- Traduction française complète de Pokémon Heart & Soul v2.0.6 (hack d'Émeraude sur pokeemerald-expansion), posée en couche sur le dépôt upstream `PokemonHnS-Development/pokehns-expansion`, tag `Release-v2.0.6`.
- Racine : `/Users/tfournier/projets/gitlab.com/tfournier/PokemonHnS-FR` (appelée `$P` ci-dessous).
- Python : `$P/.venv/bin/python` (polib, pyahocorasick, rapidfuzz, ndspy, pillow, numpy). Lance tes scripts avec `-I` seulement s'ils n'importent pas `outils/` ; sinon ajoute `sys.path.insert(0, '$P/outils')`.
- Code upstream **vierge, en lecture seule** : `$P/build/upstream_orig` (ce n'est pas un dépôt git ; `hnsfr.scan()` y fonctionne). **Ne touche jamais** à `$P/build/upstream` (arbre de compilation partagé) et ne lance jamais `build.sh` / `construire.py` : c'est l'agent principal qui compile.
- Textes : `$P/traductions/{dialogues,menus,donnees,contextes}.po`. La clé (`msgid`) est la phrase anglaise telle qu'écrite dans le code source (`\n`, `\l`, `\p`, `{PLAYER}`…). Le commentaire de chaque entrée commence par `source : …`. `contextes.po` utilise `msgctxt` = chemin du fichier quand un même anglais a deux sens.
- **Tu n'écris jamais dans les .po principaux** ni dans `glossaire.tsv`. Tu écris uniquement dans ton dossier de lot `$P/traductions/lots/<ton lot>/` et, si on te le dit, dans tes scripts.
- ROM (jamais distribuées, jamais copiées ailleurs que dans `$P/memoires` ou ton scratchpad) :
  - `memoires/emeraude_us.gba` (BPEE), `memoires/em_fr.gba` (BPEF),
  - `memoires/hns_en.gba` (HnS anglais officiel, CRC 0x01713508), `memoires/hns_fr_patch.gba` (HnS + patch FR archive.org),
  - `build/pokehns_en_local.gba` (HnS anglais compilé localement : même texte, adresses différentes),
  - `roms/Pokemon Argent SoulSilver FR.nds`.
- Mémoires dérivées : `memoires/tm_em_bytes.pkl` (octets EN → octets FR, Émeraude), `em_ctx_ok.pkl`, `em_ctx_pairs.pkl`, `em_seq_pairs.pkl`, `tm_ss_pairs.pkl` (liste (banque, index, anglais HGSS, français SS)), `ss_fr_msg.json` (banques de messages SS FR déchiffrées, {banque: [lignes]}).
- Outils : `outils/gen3.py` (Gen3 : encode/decode/largeur/reformater, à instancier avec `build/upstream_orig`), `outils/hnsfr.py` (scan des textes), `outils/style.py` (passage au style SoulSilver via le glossaire), `outils/verifier.py` (contrôles automatiques : à lancer sur ton lot avant de rendre), `outils/alignement/*` (scripts d'alignement : ils contiennent encore des chemins `/home/claude/...` à adapter).

## 2. Ordre de priorité des sources (strict)
1. **Émeraude FR officiel** : alignement Émeraude US ↔ FR par octets, par pointeurs (y compris non alignés dans les scripts de carte), par contexte de script, et par index dans les tables (Dresseurs, adversaires de Concours, Dresseurs Frontier, noms d'échange…).
2. **SoulSilver FR officiel** : banques du NARC `a/0/2/7` alignées sur l'anglais de pret/pokeheartgold. Exact d'abord, puis approché avec adaptation (noms, nombres, codes). Banques prioritaires : 222 (objets), 237 (espèces), 750 (capacités), 720 (talents), 279 (lieux), 730 (classes), 735. **Banque 802 exclue** de l'alignement automatique (mal alignée).
3. **Patch Heart & Soul FR existant** (`hns_fr_patch.gba`) : récupération par pointeur, avec les contrôles du §5.
4. **Traduction nouvelle**, au plus près du style et du vocabulaire officiels Émeraude FR et SoulSilver FR.

Quand une source de rang inférieur contredit une source officielle sur un terme (lieu, objet, capacité, personnage), l'officiel gagne. Signale-le dans ton rapport (l'agent principal met à jour le glossaire).

## 3. Style et décisions déjà prises
- Style **SoulSilver FR** : « Pokémon », « Dresseur », « Pokématos », « Prof. Orme », « Prof. Chen » ; lieux, objets, capacités en minuscules avec majuscule initiale (« Bourg Geon », « Potion », « Super Ball ») ; **noms d'espèces en capitales** (banque 237 : BULBIZARRE, PTITARD).
- Lieux et personnages de **Johto/Kanto** selon SoulSilver FR (Bourg Geon, Ville Griotte, Rosalia, Fargas, Léo…) ; noms **Hoenn** selon Émeraude FR (FLORA, BRICE, TIMMY, Prof. SEKO…) — les noms de personnages Hoenn gardent leurs capitales d'Émeraude FR, mais « Prof. » s'écrit ainsi.
- Les textes Émeraude FR officiels sont passés au style SoulSilver par `style.appliquer(texte, glossaire, especes)` (POKéMON → Pokémon, etc.). Ne réécris pas un texte officiel au-delà de ce passage de style.
- Menu START en capitales comme Émeraude FR : POKéDEX, POKéMON, SAC, {POKE}MATOS, SAUVER, OPTIONS, RETOUR.
- Combat : « PTITARD sauvage », « … ennemi » : le qualificatif suit le nom, **sans article**. Glyphe « Lv » remplacé par « N. ».
- Statuts : PSN, PAR, SOM, GEL, BRU, GLR. Stats : PV, AT, DF, AS, DS, VI. Types : Émeraude FR officiel (en capitales : NORMAL, FEU, EAU, PLANTE, ÉLECTRIK, GLACE, COMBAT, POISON, SOL, VOL, PSY, INSECTE, ROCHE, SPECTRE, DRAGON, TÉNÈBRES, ACIER) + FÉE et STELL.
- Pokédex : onglets INFO, ZONE, STATS, EVO, CRI, TAIL. ; VUS / PRIS ; RECH. ; RETOUR LISTE / HAUT DE LISTE / BAS DE LISTE / FERMER POKéDEX.
- Registre : tutoiement/vouvoiement comme dans les officiels (le personnel des Centres, Boutiques, Frontier, accueil… vouvoie ; enfants, rivaux, Dresseurs, amis tutoient en général). Garde la cohérence d'un même personnage.
- Typographie des officiels Gen 3/4 : pas d'espace avant « ! ? : ; » (contrainte de largeur, comme Émeraude FR), apostrophe typographique ’, points de suspension « … » (un seul caractère), guillemets “ ” comme Émeraude FR. Majuscules accentuées (É, À…) autorisées.
- Toute nouvelle décision de terminologie est **proposée** dans ton rapport ; c'est l'agent principal qui l'inscrit dans `traductions/glossaire.tsv` et `DECISIONS.md`.

## 4. Contraintes techniques (à vérifier sur 100 % de tes entrées)
- **Codes de contrôle identiques à l'anglais**, en nombre, type et arguments : `{BACKGROUND …}`, `{TEXT_COLORS …}`, `{COLOR …}`, `{STR_VAR_n}`, `{B_…}`, `{PLAYER}`, `{RIVAL}`, `{PAUSE …}`, `{FONT_…}`, `{CLEAR_TO …}`, `{PLAY_SE …}`, boutons `{A_BUTTON}`… Écris-les exactement comme dans l'anglais (pas `{FONT 0}` pour `{FONT_SMALL}`). Les glyphes `{PKMN}`, `{POKE}`, `{POKEBLOCK}`, `{SUPER_E}`, `{SUPER_ER}`, flèches, ne sont pas des codes : ils peuvent apparaître en français (ex. « 1{SUPER_ER} »).
- Une chaîne anglaise qui commence par une espace, ou qui est un suffixe (« 's BASE », « BERRY »), doit rester un suffixe ; une chaîne qui finit par `\n`, `\p`, `\l` ou une espace doit finir pareil.
- **Aucun kana** ni caractère hors charmap (`hnsfr.Charmap(root).invalid(s)` doit être vide). Pour les octets à double nom, utilise `{PKMN}`, `{POKE}`, `{POKEBLOCK}`, `{SUPER_E}`, `{SUPER_ER}`, `{UP_ARROW}`… (`gen3.nettoyer_kana`).
- **Mise en page des dialogues** : largeur max **198 px** par ligne (`Gen3.largeur`), `\n` pour la 2ᵉ ligne, `\l` pour les suivantes, `\p` pour une nouvelle page (`Gen3.reformater(texte, 198)`). Ne reformate pas les fragments qui se terminent par `\n` ou `\p` (concaténés à l'exécution), ni les chaînes contenant `{DYNAMIC n}` ou `{CLEAR_TO}`. Les textes officiels sont tolérés jusqu'à 216 px (largeur réelle de la fenêtre) mais pas au-delà.
- Une chaîne d'une seule ligne en anglais (libellé, menu) reste sur une ligne.
- **Longueurs maximales** (en octets encodés, codes compris) : classe de Dresseur 12, catégorie Pokédex 12, nom de type 8, `generic` 16, objet 19 (pluriel 21) — la fin de chaîne compte, capacité 16, talent 16, espèce 12, nom de Dresseur 10, nom de Dresseur Frontier 7, surnom Mont Dresseurs 10. Si la forme française dépasse, propose une abréviation lisible et signale-la.
- Ne traduis **jamais** `src/text_input_strings.c` (claviers).
- Même texte anglais, sens différents (ex. PSYCHIC : type Psy / classe Kinésiste ; entrées du menu START) : propose une entrée avec `msgctxt` = chemin du fichier et signale-la.

## 5. Pièges du patch FR existant (rang 3)
Le patch partage des fins de chaînes : un pointeur peut tomber au milieu d'un autre texte (« LLON » pour OUI, « UEURS » pour MODE, « ortue » pour Tortue, « TO » pour JOHTO, répliques associées à la mauvaise phrase). Pour **chaque** texte venant de ce patch :
1. début de chaîne réel dans la ROM FR (octet précédent = 0xFF, ou 0x00 de remplissage) ;
2. ratio de longueur plausible avec l'anglais ;
3. majuscule initiale cohérente avec l'anglais ;
4. mêmes codes de contrôle (le patch a produit des `{BACKGROUND}Ó{TEXT_COLORS}ÒÔÓ` cassés) ;
5. **sens vérifié** : la phrase française dit bien la même chose que l'anglais.

## 6. Format de sortie d'un lot
Fichiers JSON (UTF-8, `ensure_ascii=False`, indentés) dans `$P/traductions/lots/<lot>/`, chacun une **liste** d'objets :

```json
{
  "msgid": "texte anglais exact (clé du .po)",
  "msgctxt": "",                       // seulement si contexte nécessaire
  "msgstr": "traduction proposée",
  "source": "Émeraude FR officiel" | "Émeraude FR officiel (adapté)" | "SoulSilver FR officiel" | "SoulSilver FR officiel (adapté)" | "patch FR actuel (vérifié)" | "traduction nouvelle",
  "fichier": "data/maps/…/scripts.inc", "ligne": 123,   // première occurrence (référence du .po)
  "ancien": "msgstr actuel du .po, s'il y en a un",
  "preuve": "adresse/pointeur/banque:index ou texte officiel d'origine avant adaptation",
  "note": "doute, contexte, interlocuteur, choix de registre…"
}
```
- Une entrée par `msgid` (+ `msgctxt`). N'inclus pas les entrées que tu ne changes pas.
- « (adapté) » = texte officiel retouché (nom, nombre, code, passage de style au-delà de `style.appliquer`) : indique l'original dans `preuve`.
- Lance `$P/.venv/bin/python $P/outils/verifier.py $P/build/upstream_orig <tes .json> --sortie $P/traductions/lots/<lot>/verifications.tsv` et corrige tout ce qui est signalé (ou justifie-le dans `note`).
- Écris aussi `$P/traductions/lots/<lot>/RAPPORT.md` : méthode, chiffres (entrées examinées, trouvées, par source, rejetées et pourquoi), doutes, termes à ajouter au glossaire, cas de même anglais / sens différents.

## 7. Façon de travailler
- Teste toute règle automatique sur un échantillon et regarde le résultat avant de l'appliquer en masse (une règle trop large a déjà abîmé des noms propres : « le mont memoria »).
- Ne devine pas : si une correspondance est douteuse, mets-la dans un fichier séparé `douteux.json` avec la raison.
- Reste dans ton périmètre : deux lots ne travaillent jamais sur les mêmes fichiers.
