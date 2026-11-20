# Arbitrage d'entrées douteuses — traduction FR de Pokémon Heart & Soul

Tu aides le lot C1 de la traduction française du hack GBA « Pokémon Heart & Soul » (moteur Émeraude,
régions Johto/Kanto). Racine du projet : P=/Users/tfournier/projets/gitlab.com/tfournier/PokemonHnS-FR

## À lire d'abord (en entier)
- `$P/docs/CONSIGNES.md` (règles communes, format §6, contraintes techniques §4)
- `$P/DECISIONS.md` (surtout 4 : tolérance 216 px des textes officiels ; 6 : pas d'espace avant ! ? : ; ;
  11 : `\f` SoulSilver → `\l`, `\r` → `\p` ; 12 : jamais de « $ », le Pokédollar s'écrit « 500¥ » ;
  14 : **aucune majuscule accentuée** (É→E, À→A, Î→I…), la cédille Ç et Œ restent ; « é » de POKéMON reste)
- Glossaire des graphies officielles : `$P/traductions/glossaire.tsv`

## Interdits
- N'écris RIEN dans `$P` (ni .po, ni glossaire, ni lots). Écris seulement dans le dossier de sortie indiqué
  dans ta mission (scratchpad). Ne lance ni build.sh ni construire.py.

## Ce qu'on te donne
Un fichier JSON d'entrées « douteuses » mises de côté par deux lots d'alignement :
- lot A (`_id` « A:n ») : alignement Émeraude US ↔ Émeraude FR. `msgstr` = proposition (texte FR officiel
  d'Émeraude, déjà passé au style SoulSilver), `preuve` = adresse ou texte officiel d'origine, `note` = raison
  du doute (approché, codes différents, nombres différents, plusieurs textes possibles…).
- lot B (`_id` « B:n ») : alignement SoulSilver FR. `msgstr` souvent vide ; `preuve` = « banque:index — texte
  SoulSilver FR » (codes Gen 4 : `{STRVAR_1 3, 0, 0}` = une variable, `\r` = nouvelle boîte, `\f` = défilement
  d'une ligne, `\n` = 2e ligne) ; `note` = raison + anglais HGSS d'origine.
- Pour chaque entrée : `msgid` (anglais de HnS, clé exacte : ne jamais le modifier), `msgctxt` éventuel,
  `fichier`/`ligne`, `po_base` = [msgstr actuel de l'entrée générale du .po, source actuelle],
  `po_ctx` = idem pour l'entrée à contexte si elle existe, `po_fichiers` = fichiers où le texte apparaît.
  Pour voir le contexte d'une réplique, lis le fichier source dans `$P/build/upstream_orig/<fichier>`.

## Ce que tu décides, pour CHAQUE entrée
- **retenu** : la proposition `msgstr` est juste telle quelle (même sens, contrôles OK).
- **adapté** : tu pars du texte officiel (Émeraude FR ou SoulSilver FR) et tu le retouches au minimum pour
  qu'il dise exactement ce que dit l'anglais de HnS (nom, nombre, variable, objet, petite phrase ajoutée ou
  retirée, mise en page). Source « Émeraude FR officiel (adapté) » ou « SoulSilver FR officiel (adapté) »,
  `preuve` = texte officiel d'origine. N'adapte que si le texte officiel reste majoritaire et le sens identique.
- **rejeté** : le texte officiel ne correspond pas (sens différent, réplique d'un autre personnage, accord
  féminin/masculin figé qu'on ne peut pas neutraliser simplement, trop long, contexte différent…) OU le
  .po actuel est déjà aussi bon ou meilleur (par ex. déjà « Émeraude FR officiel » exact pour un douteux B).
  Dans ce cas : si le .po actuel est juste, `msgstr` = "" ; s'il est vide ou faux (contresens, morceau d'une
  autre phrase, anglais), propose une traduction (`source` « traduction nouvelle ») dans `msgstr`.

Priorité des sources : Émeraude FR exact > Émeraude FR adapté > SoulSilver FR exact > SoulSilver FR adapté >
patch FR > traduction nouvelle. Un officiel adapté remplace volontiers un « patch FR actuel » ou une
« traduction nouvelle/manuelle » ; il ne remplace jamais un « Émeraude FR officiel » exact.
Sois honnête : en cas de doute réel, rejette et explique.

## Règles de forme (à vérifier sur 100 % de tes msgstr non vides)
- Codes de contrôle `{…}` identiques à l'anglais (nombre, type, arguments, graphie exacte de l'anglais).
  Conversion SoulSilver : chaque `{STRVAR_…}` devient la variable HnS de même rôle (`{PLAYER}`, `{STR_VAR_1}`,
  `{B_ATK_NAME_WITH_PREFIX}`…). Supprime les codes Gen 4 sans équivalent (`{COLOR…}` de SS, `{YESNO}`…).
- Même début/fin que l'anglais : espace initiale, fin `\n`, `\p`, `\l` ou espace conservées.
- Typographie : pas d'espace avant ! ? : ; ; apostrophe ’ ; points de suspension « … » (un caractère) ;
  guillemets “ ” ; pas de majuscule accentuée (Etes, A bientôt, Ecorcia) ; « Pokémon », « Dresseur »,
  lieux/objets/capacités en casse normale avec majuscule initiale (style SoulSilver), espèces en CAPITALES.
  Noms : Johto/Kanto selon SoulSilver FR (glossaire), Hoenn selon Émeraude FR (capitales).
- Le joueur peut être une fille ou un garçon : évite les accords genrés qui le visent (SoulSilver a des
  variantes « menée/mené » : reformule de façon neutre, sinon rejette).
- Mise en page des dialogues : lignes ≤ 198 px (`Gen3.largeur`), `\n` pour la 2e ligne d'une boîte, `\l` pour
  les suivantes, `\p` nouvelle boîte ; tu peux utiliser `Gen3.reformater(texte, 198)` (mais pas sur un
  fragment qui finit par `\n`/`\p`, ni sur un texte avec `{DYNAMIC}`/`{CLEAR_TO}`). Un libellé d'une ligne
  en anglais reste sur une ligne. Garde le découpage en boîtes (`\p`) de l'anglais de HnS quand c'est possible.
- Pas de kana ni de caractère hors charmap.

Outils Python (`$P/.venv/bin/python`) :
```python
import sys; sys.path.insert(0, '/Users/tfournier/projets/gitlab.com/tfournier/PokemonHnS-FR/outils')
from gen3 import Gen3; g = Gen3('/Users/tfournier/projets/gitlab.com/tfournier/PokemonHnS-FR/build/upstream_orig')
g.largeur('Une ligne'); g.reformater('texte long…', 198)
```
Dans les JSON, les `\n` des textes sont écrits `\\n` (deux caractères : antislash + n), exactement comme dans
les msgid fournis.

## Sortie
Un fichier JSON (UTF-8, ensure_ascii=False, indenté), liste avec **une entrée par entrée reçue** (même `_id`) :
```json
{"_id": "B:12", "decision": "retenu|adapté|rejeté", "msgid": "...", "msgctxt": "(seulement si l'entrée
 en avait un)", "msgstr": "proposition finale ou \"\"", "source": "Émeraude FR officiel | Émeraude FR officiel
 (adapté) | SoulSilver FR officiel | SoulSilver FR officiel (adapté) | traduction nouvelle",
 "fichier": "...", "ligne": 0, "ancien": "msgstr actuel du .po (po_ctx sinon po_base)",
 "preuve": "texte officiel d'origine / adresse / banque:index", "note": "décision et raison, en français, courte"}
```
Puis contrôle : écris dans ton dossier un fichier `controle.json` = la liste de tes entrées dont `msgstr` est non
vide, et lance
`$P/.venv/bin/python $P/outils/verifier.py $P/build/upstream_orig <dossier>/controle.json --sortie <dossier>/verif.tsv`.
Corrige tout ce qui est bloquant (CODES, KANA, CARACTERE, LONGUEUR, ESPACE, TYPO) ; LARGEUR doit être nulle
pour tes adaptations (≤ 198 px) ; GLOSSAIRE/ANGLAIS : corrige ou justifie dans `note`.

Termine par un compte rendu de 10 lignes au plus : nombres retenus / adaptés / rejetés (dont avec nouvelle
traduction), problèmes rencontrés, cas que tu n'as pas su trancher.
