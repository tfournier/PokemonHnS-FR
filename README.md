# pokehns-fr — traduction française de Pokémon Heart & Soul

Projet **posé par-dessus** [pokehns-expansion](https://github.com/PokemonHnS-Development/pokehns-expansion) :
il ne contient aucun fichier du projet d'origine, seulement nos textes, nos images et nos
petits correctifs. À chaque nouvelle version upstream, on change `upstream.txt` et on relance.

## Contenu

| Dossier / fichier | Rôle |
|---|---|
| `upstream.txt` | Version upstream traduite (tag Git, ex. `Release-v2.0.6`) |
| `traductions` | Textes : **la clé est la phrase anglaise elle-même** (`msgid`), traduction dans `msgstr` |
| `traductions/glossaire.tsv` | Graphie officielle SoulSilver des noms (lieux, objets, capacités, personnages…) |
| `images` | Images françaises + `EMPREINTES_ORIGINAUX.txt` (empreinte de l'original anglais) |
| `code` | Correctifs de code (ex. horloge 24 h) |
| `outils` | Scripts (extraction, application, construction, amorçage) |
| `memoires` | Mémoires de traduction et **vos** ROM de base (jamais distribuées) |
| `rapport/` | Rapports de la dernière construction |
| `dist/` | Patchs produits |

## Construire

```
./build.sh
```

1. télécharge le code upstream à la version de `upstream.txt` (dans `build/upstream`) ;
2. copie les images — si upstream a modifié une image depuis notre traduction, elle n'est **pas**
   écrasée et apparaît dans `rapport/images_a_revoir.txt` ;
3. applique `code` (signale ceux qui ne s'appliquent plus) ;
4. remplace chaque texte anglais par sa traduction (`rapport/textes.txt`) ;
5. compile (`make hns`) ; un texte trop long pour un champ fixe est remis en anglais et listé
   dans `rapport/trop_longs.txt` ;
6. produit les patchs UPS dans `dist/` à partir des ROM présentes dans `memoires` :
   - `emeraude_us.gba` → patch à appliquer sur **Pokémon Émeraude US** ;
   - `hns_en.gba` → patch à appliquer sur **Heart & Soul anglais officiel**.

Prérequis : `git make gcc g++ libpng-dev gcc-arm-none-eabi python3`, et `pip install polib`.

## Traduire

Ouvrir les `.po` avec Poedit (ou un éditeur de texte). Syntaxe du jeu à respecter :
`\n` 2ᵉ ligne, `\l` ligne suivante (défilement), `\p` nouvelle page, `{PLAYER}`, `{STR_VAR_1}`…
Les entrées marquées *à revoir* (`#, fuzzy`) ne sont **pas** utilisées tant qu'elles n'ont pas été
validées. Le commentaire de chaque entrée indique sa source (Émeraude FR / SoulSilver FR
officiels, patch FR actuel, traduction nouvelle).

## Nouvelle version upstream

1. modifier `upstream.txt` ;
2. `python3 outils/hnsfr.py extraire build/upstream nouveaux.pot` puis
   `msgmerge --update traductions/dialogues.po nouveaux.pot` (idem menus/donnees) : les phrases
   inchangées gardent leur traduction, les phrases modifiées passent *à revoir*, les nouvelles
   apparaissent non traduites ;
3. `build.sh` et lire `rapport/`.

## Choix de traduction

- Style d'écriture : **SoulSilver FR** (« Pokémon », « Dresseur », « Pokématos », lieux et objets
  en minuscules ; noms d'espèces en capitales).
- Priorité des sources : Émeraude FR officiel (moteur) > SoulSilver FR officiel (dialogues
  Johto/Kanto) > patch FR actuel > traductions nouvelles.
- Horloge du menu Start en 24 h.

## Contenu complet des sources

- `traductions` : les textes (`dialogues.po`, `menus.po`, `donnees.po`, `contextes.po` pour les cas où un même mot anglais a deux sens), le glossaire SoulSilver et `lots_manuels/` (les traductions écrites à la main, par lots).
- `images` : toutes les images modifiées, rangées comme dans le dépôt upstream, avec `EMPREINTES_ORIGINAUX.txt` (empreinte de l'original upstream de chaque fichier, pour détecter un changement dans une future version).
- `code` : correctifs de code (`horloge-24h.patch`, `nom-sauvage-ennemi.patch`).
- `outils` : `construire.py` (construction complète), `hnsfr.py` (extraction/application des textes), `gen3.py`, `style.py`, `amorcer.py`, `appliquer_traductions.py`, `ups.py`.
  - `outils/graphismes` : scripts utilisés pour retoucher les images (tuiles, tilemaps, polices).
  - `outils/alignement` : scripts de récupération des textes officiels (Émeraude FR, SoulSilver FR) et du patch FR existant.
    Ces scripts d'appoint contiennent encore des chemins absolus de la machine de travail (`/home/claude/...`) : à adapter avant de les relancer.
- `memoires` : données dérivées (correspondances de textes). Les ROM ne sont pas incluses.

Les ROM ne sont jamais distribuées : il faut fournir soi-même Émeraude US, la ROM anglaise de Heart & Soul v2.0.6 (ou son patch officiel) pour construire.
