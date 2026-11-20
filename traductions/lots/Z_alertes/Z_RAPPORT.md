# Lot Z : dernières alertes des contrôles automatiques

Entrée : `rapport/verifications.tsv`, soit 131 alertes sur 31 209 entrées. Chaque alerte est soit **corrigée** (`Z_corrections.json`), soit **justifiée** (`Z_justifications.tsv`).

## Chiffres

| Contrôle | Alertes | Corrigées | Justifiées |
|---|---:|---:|---:|
| LARGEUR | 60 | 58 | 2 |
| GLOSSAIRE | 36 | 4 | 32 |
| ANGLAIS | 17 | 0 | 17 |
| FRAGMENT | 15 | 1 | 14 |
| CODES | 2 | 0 | 2 |
| ESPACE | 1 | 0 | 1 |
| **Total** | **131** | **63** | **68** |

`Z_corrections.json` contient 64 entrées :
- 62 entrées corrigent les 63 alertes du tableau (« STEVEN: This could only mean one thing. » portait 2 alertes, LARGEUR et GLOSSAIRE) ;
- 2 entrées viennent de vérifications liées aux alertes : le panneau « Dent d’Or » du Parc Safari, et la saveur SOUR.

Résultat de `verifier.py` sur le lot (`Z_verifications.tsv`) :
- **0 problème bloquant** ;
- 3 alertes GLOSSAIRE qui restent attendues : « PIERRE » pour Steven (décision 16). Le vérificateur ne retire les noms de personnages du glossaire que pour une source « Émeraude FR ».

À intégrer avec `integrer_lot.py Z_alertes … --corriger`. Toutes les entrées ont une `note`.

## Corrections

- **Descriptions de capacités (47, `moves_info.h`)** : limite de 152 px.
  - Chaque texte est raccourci avec le vocabulaire des descriptions officielles : lanceur, ennemi, « Peut apeurer », Atq. Spé., « Puissance variable ».
  - Les 2 lignes et le `\n` de l'anglais sont gardés. Neuf descriptions avaient leurs deux lignes trop larges ; les deux lignes ont été refaites.
  - Choix à relire :
    - « Puissance x2 si les stats du\nlanceur ont baissé ce tour. » : aucune coupe avec « doublée » ne tient ;
    - « Frappe d’une forte décharge.\nPuissance variable. » ;
    - « Monte fort Atq./Atq.Spé./\nVitesse. Baisse Déf./Déf.Spé. » : abréviations collées comme dans l'anglais (« Sp.Atk »).
- **Description de Concours (1, `contest_moves.h`)** : limite de 156 px. « Dépend du succès de l’action\ndu Pokémon précédent. »
- **Tutoriel de combat de Chen (3)**, limite de 190 px :
  - la 2ᵉ page devient « Une victoire te rapporte de l’argent\net fait progresser tes Pokémon! » ;
  - dans la règle du K.O., « leurs » passe à la ligne suivante.
- **Debug et visualiseur (6)** :
  - « images de réflexion » → « images d’IA » (fenêtre de 112 px, précédée d'un nombre) ;
  - « Le partenaire utilisera: » → « Partenaire: » ;
  - « ID musique: » → « Musique: » ;
  - visualiseur de sprites : la coupure de ligne de l'anglais est rétablie (elle avait été déplacée), « Fonds de cap. » → « Dépl. fonds » (Move BGs).
- **Steven (3)** : les répliques s'ouvrent par « PIERRE: » et non plus par « PIERRE ROCHARD: », et l'intro devient « Je m’appelle PIERRE, ». L'anglais ne donne que « Steven », et cela règle aussi le débordement à 205 px.
- **DJ LILY → DJ Lily** : graphie du glossaire, personnage.
- **« What do you want? »** : le patch donnait « Quoi? » (ratio 0,29). Corrigé en « Qu’est-ce que tu me veux? », réplique du Motard LAO.
- **Dentier en Or (Parmanie)** : seul l'avis de recherche du Parc Safari (`SafariZone_West_Frlg`) disait encore « la Dent d’Or perdue… Elle ». Il dit maintenant « le Dentier en Or perdu… Il », comme l'objet, sa description et la remise au Gardien. Aucun autre texte ne garde « Dent d’Or » pour GOLD TEETH.
- **SOUR → « ACIDE »** (`pokeblock.c`, `retouche_officiel`) :
  - Émeraude FR écrit EPICE / SEC / SUCRE / AMER / ACIDE en capitales (em_fr.gba, à partir de 0x5ED480) ;
  - le passage au style avait pris « ACIDE » pour la capacité Acide et l'avait changé en « Acide » ;
  - cette entrée rétablit l'officiel exact.

## Justifications (résumé)

- **GLOSSAIRE (32)** :
  - 23 cas : PIERRE = Steven (décision 16), dont « Multi PIERRE » dans le debug ;
  - 3 cas : crédits Émeraude FR officiels exacts (« POKéMON Designers »…) ;
  - capitales d'insistance : AUCUN, ATTENTION ;
  - FUITE et NORMAL : libellés de menu affichés en capitales ;
  - NOA = Nintendo of America ;
  - saveur ACIDE.
- **ANGLAIS (17)** :
  - noms propres : DEAN, Chad, noms proposés par défaut de FRLG ;
  - cris de Pokémon : Cha-Cha!, Shuck! ;
  - mots identiques en français officiel : catégories Chinchilla, Judo, Jujitsu, Punk, Viking ; Tri-Passes ; SEPIA et MINERAL en capitales sans accent.
- **FRAGMENT (14)** :
  - qualificatifs de combat placés après le nom (sauvage, ennemi, adverse, alliée) ;
  - noms courts officiels : IXON, Mue, Piles, DOJO ;
  - suites de phrases de la radio ;
  - « capacité CT » (mot en milieu de phrase) ;
  - temps de la Tour Dresseurs : vrai début de chaîne, précédé d'une table de pointeurs ;
  - suffixe « capacité » relu à la main.
- **CODES (2) et ESPACE (1)** : textes officiels exacts, vérifiés dans em_fr.gba :
  - {PLAYER} en plus dans le texte de PAPA (0x207C06) ;
  - {CLEAR_TO 80} au lieu de 0x53 (0x5F3A0F) ;
  - « / Onctuosité: » (0x3414B8).
- **LARGEUR (2)** : la limite estimée vient de la ligne anglaise, mais la fenêtre réelle est plus large :
  - Cadeau Mystère : WIN_MSG, 224 px ;
  - crédits FRLG : 240 px.

## Pour l'agent principal

- Le vérificateur pourrait appliquer `gl_em` (glossaire sans noms de personnages) aux répliques commençant par « STEVEN: ». Cela retirerait les 23 fausses alertes PIERRE.
- Le passage au style (`style.appliquer`) change des libellés en capitales qui sont aussi des noms de capacité ou de talent (ACIDE → Acide). D'autres libellés de menus officiels en capitales ont pu subir le même sort ; une recherche des entrées « Émeraude FR officiel » dont le texte n'est pas celui de la ROM le dirait.
