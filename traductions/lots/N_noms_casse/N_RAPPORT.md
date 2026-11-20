# Lot N : graphie officielle des noms de capacités, talents et objets

## Méthode
- Point de départ : `N_proposition.json` (829 noms hérités du patch FR, encore en capitales).
- Noms officiels FR récupérés pour **toutes** les entrées dans les données de PokeAPI (`item_names.csv`,
  `move_names.csv`, `ability_names.csv`, langue 5 = français, jusqu'aux Méga-Gemmes de Légendes Z-A et de son DLC),
  avec rapprochement par le nom anglais (822 trouvés sur 829 ; les 7 autres sont saisis à la main).
- Vérification complémentaire sur Poképédia (API MediaWiki) des noms douteux ou surprenants : Amphinolite,
  Kravarekite, Sepiatrocite, Floréclatite, Éokite, Golemastokite, Darkraïte, Scovilainite, Zeraorite, Magearnite,
  Neigeux de Mots, Tisse Ombre, Pika-Piqué, Neuf pour Un, TrouDimensionnel, Peau Féérique, Libéro, Œil Révélateur,
  Frotte-Frimousse, Nappage, Nuée de Poudre, Remède / Super Remède / Hyper Remède, Poupée Pokéshi, GS Ball,
  Téra-Éclat Stellaire, Lettre Rétro, Lettre Méca : toutes ces pages existent sous ce nom.
- Croisement avec les noms officiels déjà fixés : glossaire, banques SoulSilver FR 222/720/750
  (`tm_ss_pairs.pkl`, rapprochées par l'anglais HGSS) et entrées « Émeraude FR officiel » des .po.
- Décision 14 appliquée : pas d'accent sur les majuscules (Etrange Ball, Egide Inflexible, Ere Glaciaire,
  Er. Géo-Sismique), accents des minuscules rétablis, Œ/œ et ç gardés, sigles en capitales (CT, ADN, GS, EX, XS, XL, TV ABC).
- `N_verifications.tsv` : **0 problème** sur 827 entrées.

## Chiffres
| | |
|---|---|
| Entrées examinées | 829 (155 talents, 327 capacités, 347 objets) |
| Entrées rendues (`N_corrections.json`) | 827 |
| Laissées telles quelles | 2 : SQUIRTBOTTLE « CARAPUCE à O » (SoulSilver FR officiel exact, espèce en capitales, glossaire) ; TEACHY TV « TV ABC » (sigle Émeraude FR) |
| Différentes de la proposition automatique | 199 (surtout des accents de minuscules oubliés) |
| Source « patch FR actuel (vérifié) » (seuls la casse et les accents changent) | 747 |
| « Émeraude FR officiel (adapté) » + `retouche_officiel` (casse seule) | 34 |
| « SoulSilver FR officiel » (forme officielle SS reprise) | 18 |
| « traduction nouvelle » | 28 |

Les traductions du patch FR sont justes dans l'immense majorité des cas : seuls 5 noms étaient faux (ci-dessous).
La proposition automatique ajoutait aussi des erreurs qui ne venaient pas du patch : « Récolté » (Récolte),
« Fraise en Sucré » et les autres friandises (en Sucre), « Vieil Eçu » (Vieil Ecu), « Ravagé Rampant » (Ravage Rampant),
« Tissé Ombre » (Tisse Ombre), « Heavy Métal » (Heavy Metal), « Boîte {pokeblock}s » (code de contrôle cassé),
« Carapuce A O », « Bonbon Exp. l », « Pointeau Adn », « Gs Ball », « Tout Ou Rien », « Psycho-Pulve. Ex ».

## Traductions fausses corrigées
| Anglais | Ancien | Nouveau | Remarque |
|---|---|---|---|
| NUZZLE (capacité) | NUZZLE | Frotte-Frimousse | anglais laissé tel quel, faussement étiqueté « SoulSilver FR officiel » : `alignement_faux` |
| WITHDRAW (capacité) | RETIRER | Repli | même clé que la commande « RETIRER » du PC : entrée à `msgctxt` = `src/data/moves_info.h` |
| SIMPLE (talent) | UNI | Simple | même clé que le fond d'écran « UNI » et le mot Easy Chat : `msgctxt` = `src/data/abilities.h` |
| DECORATE (capacité) | DECORER | Nappage | même clé que le menu « DECORER » : `msgctxt` = `src/data/moves_info.h` |
| POWDER (capacité) | POUDRE | Nuée de Poudre | même clé qu'un texte de strings.c : `msgctxt` = `src/data/moves_info.h` |

Les quatre entrées à contexte sont nouvelles (elles iront dans `contextes.po`) ; l'entrée générale garde le mot de menu.

## Choix à valider (doutes)
1. **Noms Gen 2-4 : forme officielle SoulSilver plutôt que nom récent.** Le glossaire et les autres lots gardent les
   formes officielles SS/Émeraude, abréviations comprises (Mouch. Soie, Lunet. Choix, Ecailledraco). J'ai donc écrit :
   Vit.Extrême (récent : Vitesse Extrême), Pouv.Antique (Pouvoir Antique), Danse-Plume (Danse Plumes),
   Oeil Composé, Repli, Simple, Bâton pour LEEK (récent : Poireau), Ecailleocéan (Écaille Océan),
   Cuillertordu (Cuillère Tordue), Poudre Arg. (Poudre Argentée), Lunet.Noires (Lunettes Noires),
   Poudreclaire (Poudre Claire), Noigrume Blu/Jne/Ver/Ros/Blc/Noi (Noigrume Bleu/Jaune/Vert/Rose/Blanc/Noir ;
   RED APRICORN est déjà « Noigrume Rge »). Ces noms sont aussi ceux des dialogues (« lancé à Vit.Extrême »,
   « des Lunet.Noires », « mon Ecailleocéan »). Le brief citait « Vitesse Extrême » : si vous préférez les noms récents,
   il faut changer ces 16 entrées (Oeil Composé, Repli et Simple sont aussi les noms récents) **et** les clés du glossaire. Chaque note donne le nom récent.
2. **Œil Révélateur** (MIND'S EYE) garde la ligature (décision 14), alors que SoulSilver FR écrit « Oeil Composé » et
   « Oeil Miracle ». À harmoniser si l'on veut « Oeil Révélateur ».
3. **Objets clés d'Émeraude gardés sous leur forme Émeraude FR** (rang 1) même quand le nom récent diffère :
   Vélo Course (récent : Vélo de Course), Seau Wailmer (Wailmerrosoir), Boîte {POKEBLOCK}S (Boîte Pokéblocs ;
   glyphe en capitales comme dans les dialogues), Lunet. Sable (Lunettes Sable ; le pluriel du .po dit déjà « Lunettes Sable »).
4. **Glossaire préféré à Émeraude FR** pour GOLD TEETH → Dentier en Or (Émeraude : DENT D’OR) et LIFT KEY →
   Clé Ascenseur (Émeraude : CLE ASC.) : noms officiels Rouge Feu/Vert Feuille déjà dans le glossaire et dans les
   dialogues. Ces deux entrées portent `retouche_officiel` ; l'AVIS DE RECHERCHE de Parmanie dit encore « la Dent d’Or perdue »
   (dialogues.po, ~l. 91134) : à aligner sur « Dentier en Or ».
5. **Abréviations gardées** (nom officiel trop long) : capacités Z Déluge Causti-T., Er. Géo-Sismique, Super Tourbillon,
   Pé. Eblouissante, Fulgur. Gigavolt, Psycho-Pulvé. EX, Pik. Foudroyante, Sym. des Ondines ; objet Téra-Eclat Stell.
   (« Téra-Éclat Stellaire » fait 20 caractères, la limite réelle est 19 + fin de chaîne).
6. **Sans nom officiel** : RARECANDY BOX (objet propre à Heart & Soul) → « Boîte Bonbon », traduction du patch gardée.
7. POUNCE (Bond), POWER OF ALCHEMY (Osmose), SCHOOLING (Banc) : le contrôle FRAGMENT signalait le pointeur du patch ;
   les noms sont officiels (PokeAPI) et passent donc en « traduction nouvelle ».
8. HARBOR MAIL « Lettre Port » sert aussi au choix du quiz Mechadoll (script_menu.h) : même graphie.

## Intégration
- Les 747 entrées « patch FR actuel (vérifié) » et les « traduction nouvelle » qui remplacent une entrée du même rang
  demandent `integrer_lot.py --corriger` (toutes ont une `note`).
- Les 34 « Émeraude FR officiel (adapté) » et les deux entrées du point 4 portent `"retouche_officiel": true` ; NUZZLE
  porte `"alignement_faux": true`.

## Termes à ajouter au glossaire (proposition)
Graphie des objets clés d'Émeraude encore en capitales dans les dialogues : VELO COURSE → Vélo Course, VELO CROSS → Vélo Cross,
DEVON SCOPE → Devon Scope, PACK DEVON → Pack Devon, SCANNER → Scanner, SCEAU MAGMA → Sceau Magma,
BON COMMANDE → Bon Commande, BOITE CT → Boîte CT, POT POUDRE → Pot Poudre, SEAU WAILMER → Seau Wailmer,
MEMORYDEX → Memorydex, TICKETMYSTIK → Ticketmystik, TICKETAURORA → Ticketaurora, VIEILLECARTE → Vieillecarte,
PASSE EON → Passe Eon, LUNET. SABLE → Lunet. Sable, CLE SALLE → Clé Salle. Plus largement, les 827 noms de ce lot peuvent servir
de clés au glossaire (types capacité/talent/objet).
