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
| `memoires` | **Vos** ROM de base et les extraits tirés des ROM officielles — local, jamais versionné ni distribué |
| `rapport/` | Rapports de la dernière construction |
| `dist/` | Patchs produits |

## Construire

```
.venv/bin/python outils/preparer_roms.py roms memoires   # une fois : identifie vos ROM et patchs par leur contenu
./build.sh
```

1. télécharge le code upstream à la version de `upstream.txt` (dans `build/upstream`) ;
2. copie les images — si upstream a modifié une image depuis notre traduction, elle n'est **pas**
   écrasée et apparaît dans `rapport/images_a_revoir.txt` ;
3. applique `code` (signale ceux qui ne s'appliquent plus) ;
4. remplace chaque texte anglais par sa traduction (`rapport/textes.txt`) ;
5. compile (`make hns`) ; un texte trop long pour un champ fixe est remis en anglais et listé
   dans `rapport/trop_longs.txt` ;
6. produit le patch UPS distribué dans `dist/`, à appliquer sur **Heart & Soul anglais officiel**
   (`memoires/hns_en.gba`), et le vérifie : appliqué à cette ROM, il doit redonner exactement la ROM
   construite (CRC compris). L'option `--patch-emeraude` (`./build.sh --patch-emeraude`)
   produit en plus un patch sur **Pokémon Émeraude US** (`memoires/emeraude_us.gba`), gardé au cas où
   mais non distribué. Vérification à la main : `outils/ups_appliquer.py <rom_source> <patch.ups> <sortie.gba>`.

Prérequis : `git make gcc g++ libpng`, une chaîne `arm-none-eabi-gcc` **avec newlib** (sous macOS : la
chaîne xPack, décompressée dans `~/.local/xpack-arm-none-eabi-gcc-*`, est trouvée automatiquement), `python3`
et un environnement `.venv` : `python3 -m venv .venv && .venv/bin/pip install polib pyahocorasick rapidfuzz ndspy pillow numpy`.

## Traduire

Ouvrir les `.po` avec Poedit (ou un éditeur de texte). Syntaxe du jeu à respecter :
`\n` 2ᵉ ligne, `\l` ligne suivante (défilement), `\p` nouvelle page, `{PLAYER}`, `{STR_VAR_1}`…
Les entrées marquées *à revoir* (`#, fuzzy`) ne sont **pas** utilisées tant qu'elles n'ont pas été
validées. Le commentaire de chaque entrée indique sa source (Émeraude FR / SoulSilver FR
officiels, patch FR actuel, traduction nouvelle).

## Nouvelle version upstream

1. Modifier `upstream.txt` (nouveau tag, ex. `Release-v2.0.7`).
2. Préparer une copie vierge du nouveau code (lecture seule, sert à l'extraction et aux contrôles) :
   ```
   rm -rf build/upstream_orig && mkdir -p build/upstream_orig
   git -C build/upstream fetch --depth 1 origin tag <tag> && git -C build/upstream archive <tag> | tar -x -C build/upstream_orig
   ```
3. Mettre les .po à jour : `.venv/bin/python outils/actualiser_po.py build/upstream_orig traductions`
   (bilan sans rien écrire), puis avec `--appliquer` ; `--purger` retire les entrées dont l'anglais a
   disparu du code (à faire après avoir regardé la liste). Les phrases inchangées gardent leur
   traduction (la clé est la phrase anglaise), les phrases nouvelles ou modifiées apparaissent non
   traduites.
4. `./build.sh` puis lire `rapport/` :
   - `images_a_revoir.txt` : images modifiées par l'équipe HnS depuis notre traduction (l'empreinte de
     l'original ne correspond plus) — on garde la leur, à retraduire en fusionnant au pixel près ;
   - correctifs de code qui « ne s'appliquent plus » : les refaire sur le nouveau code (`git apply`) ;
   - `trop_longs.txt` : textes remis en anglais car trop longs pour leur champ.
5. Contrôles : `.venv/bin/python outils/verifier.py build/upstream_orig traductions/*.po` et
   `.venv/bin/python outils/controle_anglais.py build/upstream_orig memoires/hns_en.gba build/pokehns_fr.gba rapport/anglais_restant.tsv`
   (la ROM anglaise de la nouvelle version doit être reconstruite à partir de son patch officiel).
6. Traduire les nouveautés par lots (`docs/CONSIGNES.md`, `outils/integrer_lot.py`), faire relire
   (`outils/relecture_chatgpt.py`, `outils/arbitrer_relecture.py`), reconstruire, tester en émulateur.
7. CI : mettre à jour `outils/ci/empreintes.txt` (SHA-256 du nouveau patch officiel `pokemonHnS_<version>.ups`
   et de la nouvelle ROM anglaise `memoires/hns_en.gba`).

## Publication automatique (GitHub Actions)

À chaque push sur `main`, `.github/workflows/publier.yml` construit la traduction et crée une release
**v\<version HnS\>-fr.\<n\>** (ex. `v2.0.6-fr.3`, n = numéro de publication de la CI), marquée *Latest*, avec le
seul fichier UPS (sur Heart & Soul anglais) en pièce jointe. La dernière est toujours à
<https://github.com/tfournier/PokemonHnS-FR/releases/latest>. Aucune ROM n'est publiée.

- La CI reconstruit la ROM anglaise de HnS : Émeraude US, chiffrée avec gpg (AES-256), est dans le dépôt
  **privé** `tfournier/hns-roms` ; le patch officiel HnS vient de la release publique de pokehns-expansion.
  Les empreintes de ces fichiers sont contrôlées (`outils/ci/preparer_rom.sh`, `outils/ci/empreintes.txt`).
- Secrets du dépôt (Settings → Secrets and variables → Actions) : `HNS_ROMS_DEPLOY_KEY` (clé SSH en lecture
  seule, déclarée comme deploy key de `tfournier/hns-roms`) et `ROM_PASSPHRASE` (phrase de passe du fichier gpg).
- Même chaîne ARM qu'en local (xPack 14.2.1, empreinte vérifiée) : la ROM publiée est identique à celle
  construite par `./build.sh` ; son CRC32 figure dans les notes de la release.
- La construction échoue si un texte est remis en anglais faute de place, si une image a été modifiée
  par upstream, ou si le patch ne redonne pas exactement la ROM construite.
- Changer de ROM ou de phrase de passe : rechiffrer (`gpg --symmetric --cipher-algo AES256`), remplacer
  `emeraude_us.gba.gpg` dans `tfournier/hns-roms` et mettre à jour le secret `ROM_PASSPHRASE`.

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
- `memoires` : local, ignoré par git. Il contient vos ROM de base (`preparer_roms.py`) et des extraits tirés des ROM
  officielles, jamais distribués : `ss_fr_msg.json` (textes de SoulSilver FR, `outils/alignement/gen4msg.py`),
  `tm_*.pkl` et `em_*.pkl` (mémoires de traduction Émeraude et SoulSilver, `outils/alignement/em_*.py`, `amorcer.py`).
  Ils servent au contrôle de l'anglais restant, au lexique de la relecture et au réalignement ; la construction
  (`build.sh`) n'en a pas besoin.

Les ROM ne sont jamais distribuées : il faut fournir soi-même Émeraude US, la ROM anglaise de Heart & Soul v2.0.6 (ou son patch officiel) pour construire.
