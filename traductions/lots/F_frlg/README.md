# Lot F — textes FRLG repris de Rouge Feu FR officiel

## Méthode
1. **ROM anglaise reconstruite** : `pret/pokefirered` et `pret/agbcc` clonés dans `build/` (ignoré par git),
   `agbcc/build.sh` + `install.sh ../pokefirered`, puis `make` et `make leafgreen` avec la chaîne xPack.
   Les deux ROM sont identiques à l'octet aux originales (SHA-1 `firered.sha1` / `leafgreen.sha1` du dépôt).
   Symboles : `arm-none-eabi-nm -n pokefirered.elf > build/pokefirered/syms.txt` (et `syms_lg.txt`).
2. **Pointeurs US → FR** (`outils/alignement/frlg_pointeurs.py`, repris de `em_pointeurs.py`) : marche parallèle
   BPRE↔BPRF (et BPGE↔BPGF avec `FRLG_VER=lg`), 43 000 cibles appariées, 95 % de la ROM couverte.
3. **Table des textes** (`frlg_table.py`) : chaque symbole pokefirered qui est un texte → adresse US → adresse FR
   (cible de pointeur la plus fréquente ; sinon texte contigu au précédent/suivant dans le même `text.inc`).
   16 776 textes (Rouge Feu), 16 902 (Vert Feuille).
4. **Appariement avec le hack** (`frlg_aligner.py`) : les étiquettes des `.inc`/`.c` FRLG du hack sont celles de
   pokefirered (`PalletTown_Text_OakDontGoOut`…) ; on compare le texte (sans les codes de police/couleur/musique,
   dont la graphie diffère entre pokefirered et pokeemerald-expansion). Repli par texte anglais identique si
   l'étiquette manque. Seules les entrées dont la source actuelle n'est **pas** « Émeraude FR officiel » ou
   « SoulSilver FR officiel » (exacts) sont examinées ; les « (adapté) » seulement si toutes leurs occurrences
   sont FRLG.
5. **Sortie** (`frlg_sortie.py`) : `em_commun.officiel` (glossaire, espèces en capitales) ; codes du hack remis
   à la place de ceux de Rouge Feu (`{PLAY_BGM 86 1}` → `{PLAY_BGM}{MUS_RG_…}`, `{FONT 4}` → `{FONT_MALE}`, dans
   l'ordre) ; capitales restantes (termes propres à Rouge Feu absents du glossaire : MOTARDS, CABANE SECRETE,
   noms de PNJ…) en casse normale avec accents restitués d'après SoulSilver FR et sans majuscule accentuée
   (détail dans `note`, « casse : X → Y ») ; cris en capitales gardés (NON, QUOI, BASTOONNN…) ; espace avant
   ! ? : ; retirée ; mise en page `em_commun.mise_en_page` (remise à 198 px seulement au-delà de 216 px).
6. **Noms de Dresseurs** (`frlg_noms.py`) : `trainers_frlg.party` → constante `TRAINER_X` → indice pokefirered →
   `gTrainers[i].trainerName` (BPRF 0x2347A8 + 40·i + 4) ; `trainer_tower_sets.c` → `sTrainerTowerFloor_X.trainers[k].name`
   (étages inutilisés : même décalage que les étages visés, vérifié constant sur les 28). Casse SoulSilver,
   accents restitués sur les prénoms français (Frédéric, Hélène…).

`ancien` est le msgstr actuel ; `preuve` = adresse BPRF (ou BPGF), symbole pokefirered, adresse BPRE, mode
(`ptr` = pointeur, `contigu` = texte voisin) et texte FR officiel brut.

## Chiffres
| | entrées |
|---|---|
| entrées FRLG examinées (dialogues, menus, données) | 3 411 |
| trouvées dans Rouge Feu / Vert Feuille | 3 411 (3 403 par étiquette, 4 par texte, 1 Vert Feuille) |
| déjà identiques au .po (rien proposé) | 135 |
| **lot.json : Rouge Feu FR officiel (exact, passage de style seul)** | **2 292** |
| **lot.json : Rouge Feu FR officiel (adapté)** (codes remis, casse, mise en page) | **945** |
| noms de Dresseurs (lot.json, tous « adapté » pour la casse) | 165 |
| douteux.json | 39 dialogues + 2 noms |
| non trouvés | 0 dialogue ; 1 nom (`PH`, TRAINER_NONE, vide dans la ROM) |

Total lot.json : **3 402** entrées (2 292 exactes, 1 110 adaptées). Sources remplacées : ≈ 3 280 « traduction
nouvelle », 58 SoulSilver adapté, 18 Émeraude adapté, 31 patch FR / relu à la main, 4 sans source.
`verifier.py` : 0 problème sur lot.json. Contrôles propres : codes {…} identiques au msgid (octets),
pas de `$`, pas de kana ni de caractère hors charmap, aucune ligne > 216 px, noms ≤ 10 caractères.

Écarts de longueur/nombres (`ratio`, `nombres` de `em_commun.controle`) : non bloquants quand l'alignement
est sûr (étiquette + pointeur) — Rouge Feu FR traduit librement (« 1F » → « Rdc », « fifty » → « 50 ») ; signalés
dans `note`.

## Douteux (douteux.json)
- 20 : codes différents du hack — Rouge Feu FR ajoute/retire un `{PLAYER}` ou n'a pas le code de couleur ; le
  texte proposé est l'officiel, à adapter à la main.
- 2 : crédits avec `{CLEAR_TO}` (« National Federation of the Blind »…), codes de colonne différents.
- 3 : texte coupé autrement par le hack (Nina qui toilette un Pokémon : 3 fragments pour 1 texte officiel) ;
  1 : phrase modifiée (« Your BAG is full of items. », Rouge Feu : « …of other items. »).
- 1 : fin en espace (CT26).
- 12 : répliques courtes partagées avec une carte HnS (« No! », « Help! », « Thank you! »…) : la traduction libre
  de Rouge Feu (« Waouargh! », « Glubb! J’me noie! ») ne convient pas forcément au PNJ HnS.
- 2 noms (LISA, TREVOR) : entrée partagée avec `trainers_hns.party` (il faudrait un msgctxt).

## Points d'attention pour l'intégration
- Termes Rouge Feu FR repris tels qu'officiels mais à arbitrer face au glossaire : voir `noms_a_valider.md`
  (Dingue des Capacités, Ticketaurora, Parc Central, Poche à Baies / Sac à Baies, Memorydex, TV ABC…).
- « Dr Fuji » (2 textes) laissé tel quel ; ailleurs « MR. FUJI » → « M. Fuji ».
- Locuteurs : « CHEN: » → « Chen: », comme les traductions actuelles du projet.
- Les textes de Rouge Feu FR sont souvent plus libres que l'anglais (sens parfois différent pour les répliques
  de Dresseurs : « You're mean! » → « Tiens, c’est ma photo! ») : c'est l'officiel, l'alignement par pointeur
  est sûr (vérifié à la main sur 60 entrées de Route 3, Bourg Palette, Jadielle, Ile 1, Sylphe…).

## 20 exemples contrôlés à la main (texte relu dans la ROM à l'adresse indiquée)
1. `Ready?\nBoing!\pWe're having a BODY SLAM match\nto see who wimps out f` (data/maps/FourIsland_PokemonCenter_1F_Frlg/scripts.inc:31) — Rouge Feu FR officiel  
   EN : Ready?\nBoing!\pWe're having a BODY SLAM match\nto see who wimps out first.\pIf you were to join us, you'd be\nsquashed like a bug, though…\pHow about  
   FR : Prêts?\nGo!\pOn fait un concours de Plaquage.\pSi tu veux essayer, tu vas te faire\nécraser comme un insecte!\pEt si j’apprenais plutôt cette\ncapacit  
   preuve : BPRF 0x1A20C4 (pokefirered Text_BodySlamTeach, BPRE 0x1A3505, ptr)

2. `Have you heard the legend of the\nwinged mirages?` (data/maps/Route14_Frlg/scripts.inc:59) — Rouge Feu FR officiel  
   EN : Have you heard the legend of the\nwinged mirages?  
   FR : Connais-tu la légende des\nmirages ailés?  
   preuve : BPRF 0x185BBB (pokefirered Route14_Text_DonaldIntro, BPRE 0x1860D9, ptr)

3. `Did you ride a SEAGALLOP ferry\nto get here?\pThere are at least ten o` (data/maps/SevenIsland_PokemonCenter_1F_Frlg/scripts.inc:37) — Rouge Feu FR officiel (adapté)  
   EN : Did you ride a SEAGALLOP ferry\nto get here?\pThere are at least ten of those\nhigh-speed ships.\pI don't know where they all go,\nthough.  
   FR : Tu as déjà embarqué sur un\nFerry Flèche des Mers?\pIl y en a au moins dix.\pMais je ne connais malheureusement\npas toutes leurs destinations.  
   preuve : BPRF 0x19F76C (pokefirered SevenIsland_PokemonCenter_1F_Text_DidYouRideSeagallopHere, BPRE 0x1A0C1F, ptr)

4. `I was given the best possible\neducation to become this strong.\pI don` (data/maps/SevenIsland_SevaultCanyon_Frlg/scripts.inc:76) — Rouge Feu FR officiel  
   EN : I was given the best possible\neducation to become this strong.\pI don't want to lose to anyone!  
   FR : J’ai reçu la meilleure éducation\npossible pour devenir aussi forte.\pJe ne peux perdre contre personne.  
   preuve : BPRF 0x18C7E8 (pokefirered SevenIsland_SevaultCanyon_Text_MichelleIntro, BPRE 0x18CC4F, ptr)

5. `Only the chosen can pass here!` (data/maps/VictoryRoad_3F_Frlg/scripts.inc:119) — Rouge Feu FR officiel  
   EN : Only the chosen can pass here!  
   FR : Seuls les élus peuvent passer!  
   preuve : BPRF 0x174BB0 (pokefirered VictoryRoad_3F_Text_ColbyIntro, BPRE 0x174C8A, ptr)

6. `I wish to see a POKéMON.\nA darling {STR_VAR_1}.\pI want to see one ri` (data/maps/FiveIsland_ResortGorgeous_House_Frlg/scripts.inc:151) — Rouge Feu FR officiel  
   EN : I wish to see a POKéMON.\nA darling {STR_VAR_1}.\pI want to see one right away.\nPlease, make my wish come true.  
   FR : Il y a un Pokémon que j’aimerais\nvoir. C’est {STR_VAR_1}.\pJe veux en voir un maintenant.\nExauce mon souhait!  
   preuve : BPRF 0x1A2E9B (pokefirered FiveIsland_ResortGorgeous_House_Text_WishToSeeMonPlease, BPRE 0x1A4315, ptr)

7. `That's right!\nIt's hard work!` (data/maps/PewterCity_Frlg/scripts.inc:902) — Rouge Feu FR officiel  
   EN : That's right!\nIt's hard work!  
   FR : Ah bon?\nOK.  
   preuve : BPRF 0x17E454 (pokefirered PewterCity_Text_ThatsRightItsHardWork, BPRE 0x17E626, ptr)

8. `Rare rocks and gems are displayed.` (data/maps/ThreeIsland_House1_Frlg/scripts.inc:23) — Rouge Feu FR officiel  
   EN : Rare rocks and gems are displayed.  
   FR : Des pierres rares sont mises\nen évidence.  
   preuve : BPRF 0x1A1B03 (pokefirered ThreeIsland_House1_Text_RareRocksGemsDisplayed, BPRE 0x1A2F92, ptr)

9. `We're careful about pollution here.\pWe've heard GRIMER multiplies in\` (data/maps/VermilionCity_Frlg/scripts.inc:267) — Rouge Feu FR officiel  
   EN : We're careful about pollution here.\pWe've heard GRIMER multiplies in\ntoxic sludge.  
   FR : On fait attention à l’environnement!\pOn dit que les TADMORV se\nmultiplient en zone toxique!  
   preuve : BPRF 0x17F4A8 (pokefirered VermilionCity_Text_GrimerMultipliesInSludge, BPRE 0x17F723, ptr)

10. `…Huh?\pI was envisioning my house, but\nthis is where I TELEPORT?` (data/maps/SixIsland_GreenPath_Frlg/scripts.inc:13) — Rouge Feu FR officiel  
   EN : …Huh?\pI was envisioning my house, but\nthis is where I TELEPORT?  
   FR : … Quoi?\pJe voulais arriver chez moi, mais\nle Téléport m’a amenée ici.  
   preuve : BPRF 0x18B244 (pokefirered SixIsland_GreenPath_Text_JaclynIntro, BPRE 0x18B7B0, ptr)

11. `POKéMON Designers\n\n\n\n\n\n` (src/credits_frlg.c:381) — Rouge Feu FR officiel  
   EN : POKéMON Designers\n\n\n\n\n\n  
   FR : Pokémon Designers\n\n\n\n\n\n  
   preuve : BPRF 0x415AF0 (pokefirered gCreditsString_POKeMON_Designers, BPRE 0x41D5E4, ptr)

12. `The door doesn't budge at all.\nCheck it more thoroughly?` (data/maps/SixIsland_RuinValley_Frlg/scripts.inc:54) — Rouge Feu FR officiel  
   EN : The door doesn't budge at all.\nCheck it more thoroughly?  
   FR : La porte ne bouge pas d’un pouce.\nL’examiner plus attentivement?  
   preuve : BPRF 0x18B8C1 (pokefirered SixIsland_RuinValley_Text_CheckDoorMoreThoroughly, BPRE 0x18BDC0, ptr)

13. `I'm done!` (data/maps/SilphCo_7F_Frlg/scripts.inc:304) — Rouge Feu FR officiel (adapté)  
   EN : I'm done!  
   FR : … Fichu!  
   preuve : BPRF 0x17653B (pokefirered SilphCo_7F_Text_JoshuaDefeat, BPRE 0x17660C, ptr)

14. `This island is too spread out…\nIt's not easy patrolling the place.` (data/maps/SevenIsland_SevaultCanyon_Entrance_Frlg/scripts.inc:36) — Rouge Feu FR officiel  
   EN : This island is too spread out…\nIt's not easy patrolling the place.  
   FR : Cette île est trop étendue…\nC’est difficile d’aller partout.  
   preuve : BPRF 0x18C04D (pokefirered SevenIsland_SevaultCanyon_Entrance_Text_NicolasIntro, BPRE 0x18C500, ptr)

15. `From where have you come, and\nwhere are you bound?` (data/text/trainers_frlg.inc:758) — Rouge Feu FR officiel  
   EN : From where have you come, and\nwhere are you bound?  
   FR : Mais dis-moi, tu vas où\ncomme ça?  
   preuve : BPRF 0x1C22F4 (pokefirered ThreeIsland_BondBridge_Text_VioletRematchIntro, BPRE 0x1C3ABF, ptr)

16. `…  …\p…  …\nI'm BROCK's fan!\pEven if I were his only fan,\nI swear it` (data/maps/SaffronCity_PokemonTrainerFanClub_Frlg/scripts.inc:468) — Rouge Feu FR officiel  
   EN : …  …\p…  …\nI'm BROCK's fan!\pEven if I were his only fan,\nI swear it on my rock-hard will,\land on my shorts!\pI'll be his fan to the bitter end!  
   FR : … …\pJe suis fan de Pierre!\pEt je le resterai quoi qu’il\narrive!\pJ’le jure sur mon short!  
   preuve : BPRF 0x19BA8E (pokefirered SaffronCity_PokemonTrainerFanClub_Text_BrocksFanToBitterEnd, BPRE 0x19C73A, ptr)

17. `GEB: My big sister and I are way\ntougher than before!` (data/text/trainers_frlg.inc:851) — Rouge Feu FR officiel (adapté)  
   EN : GEB: My big sister and I are way\ntougher than before!  
   FR : Ged: Avec ma sœur, on a\npeur de rien.  
   preuve : BPRF 0x1C277B (pokefirered SixIsland_OutcastIsland_Text_GebRematchIntro, BPRE 0x1C3FB3, ptr)

18. `{RIVAL}: I heard there was a CUT\nmaster on board.\pBut he was just a ` (data/maps/SSAnne_2F_Corridor_Frlg/scripts.inc:200) — Rouge Feu FR officiel  
   EN : {RIVAL}: I heard there was a CUT\nmaster on board.\pBut he was just a seasick old man!\pCUT itself is really useful.\nYup, it'll be handy.\pYou should  
   FR : {RIVAL}: Il y a le maître de la\ncapacité Coupe à bord.\pMais ce n’est qu’un vieil homme\nmalade et sénile!\pLa capacité Coupe est très\nutile!\pTu de  
   preuve : BPRF 0x1730FD (pokefirered SSAnne_2F_Corridor_Text_RivalPostBattle, BPRE 0x173164, ptr)

19. `OAK: Hey! Wait!\nDon't go out!` (data/maps/PalletTown_Frlg/scripts.inc:452) — Rouge Feu FR officiel (adapté)  
   EN : OAK: Hey! Wait!\nDon't go out!  
   FR : Chen: Hé, attends!\nNe pars pas!  
   preuve : BPRF 0x17D580 (pokefirered PalletTown_Text_OakDontGoOut, BPRE 0x17D72C, ptr)

20. `PALLET TOWN\nShades of your journey await!` (data/maps/PalletTown_Frlg/scripts.inc:483) — Rouge Feu FR officiel  
   EN : PALLET TOWN\nShades of your journey await!  
   FR : Bourg Palette\nUn monde de couleurs\ls’ouvre à vous!  
   preuve : BPRF 0x17D711 (pokefirered PalletTown_Text_TownSign, BPRE 0x17D895, ptr)

