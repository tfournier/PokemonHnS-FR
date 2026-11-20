# État des lieux — 20 novembre 2026 (reprise)

## Environnement
- ROM identifiées par contenu : Émeraude US (BPEE, CRC 0x1F1C08FB), Émeraude FR (BPEF, CRC 0xA3FDCCB1),
  SoulSilver FR (IPGF), patch officiel HnS v2.0.6 (UPS) → ROM anglaise **CRC 0x01713508** (conforme),
  patch HnS FR archive.org (BPS, source = ROM anglaise) → CRC 0x3C550CF8.
- `roms/Pokémon Heart And Soul FR.gba` n'est **pas** le patch archive.org : c'est une ancienne construction
  du projet pokehns-fr (textes style SoulSilver, « Prof. Orme », « Pokématos »).
- Le dépôt n'avait aucun commit : l'historique des décisions antérieures n'est connu que par le README,
  les commentaires des .po et les scripts.
- Compilation upstream (`make hns`) OK en 1 min 36 avec xPack GCC 14.2.1 ; ROM non identique octet à
  octet à l'officielle (compilateur différent), textes identiques.
- Construction FR actuelle OK : 30 109 textes appliqués, 7 068 occurrences non traduites, 2 textes trop
  longs remis en anglais (`Mortimer`, nom de Dresseur Frontier > 7 ; `COURROUSINGE`, surnom > 10).

## Textes (.po), après ajout des sources oubliées
| Fichier | Entrées | Émeraude FR | SoulSilver FR | Patch FR | Manuel / relu | Non traduit | dont compilé |
|---|---|---|---|---|---|---|---|
| dialogues.po | 14 854 | 2 837 | 1 374 | 6 760 | 479 | 3 401 | 25 |
| menus.po | 4 528 | 1 285 | 481 | 1 724 | 172 | 861 (+1 fuzzy) | 497 |
| donnees.po | 11 273 | 309 | 1 826 | 6 793 | 268 | 2 053 | 1 109 |
| contextes.po | 7 | — | — | — | 7 | 0 | — |
| **Total** | **30 662** | **4 431** | **3 681** | **15 277** | **926** | **6 315** | **1 631** |

- 838 textes n'étaient pas extraits du tout : debug (409), crédits (291), noms de Dresseurs `.party` (92
  nouveaux), noms de lieux JSON (46 nouveaux). Ils sont maintenant dans les .po (non traduits).
- La moitié des textes traduits (15 277) vient du patch FR existant : c'est le principal risque qualité.
- Non traduits sans texte officiel exact disponible : 3 369 dialogues (dont 2 833 dans les cartes FRLG non
  compilées, 445 data/text, 91 data/scripts) et 1 167 menus/données (debug, visualiseur de sprites,
  données de l'expansion…). Les autres (≈1 800, surtout noms de Dresseurs/Concours/Frontier) existent
  dans Émeraude US ou HGSS : lots A et B.

## Contrôles automatiques (outils/verifier.py) sur les 24 409 entrées traduites
| Contrôle | Alertes | Principale source |
|---|---|---|
| LARGEUR (> 198 px, officiels > 216 px) | 1 637 | patch FR (1 557) |
| FRAGMENT (patch FR : morceau d'une autre chaîne, ratio, casse) | 338 | patch FR |
| GLOSSAIRE | 101 | patch FR, officiels mal stylés (« PROF. SEKO ») |
| ESPACE (suffixe / fin de fragment perdus) | 60 | SoulSilver FR (36) |
| CODES | 48 | patch FR (42 avant affinage) |
| ANGLAIS (traduction = anglais) | 22 | manuel |
| LONGUEUR | 19 | patch FR |

## Anglais restant dans la ROM construite (outils/controle_anglais.py)
803 chaînes anglaises de la ROM de référence encore présentes, avant l'ajout des nouvelles sources :
noms de Dresseurs/Concours/Frontier (gros du « src/data »), debug (143), crédits (42), noms des
musiques/bruitages du test sonore (identifiants MUS-…/SE-…, issus de constantes : à traiter ou à
justifier), descriptions non traduites, quelques scripts.

## Images
Inventaire en cours (sous-agent) : `rapport/images_inventaire.tsv` et `.md`. 132 images déjà
traduites par le projet (`images/EMPREINTES_ORIGINAUX.txt`).

## Lots lancés
A (alignement Émeraude), B (alignement SoulSilver), D1 (dialogues data/text + data/scripts),
E (menus, données, debug), G (banc de test mGBA headless), inventaire des images (F, phase 1).
Prévus : C (audit des 15 277 textes du patch FR, après A et B pour ne pas auditer ce qui sera remplacé),
D2–D4 (cartes FRLG non compilées, 2 833 entrées), F phase 2 (traduction des images).
