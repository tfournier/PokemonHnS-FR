# Noms à valider — vérification dans Rouge Feu FR (BPRF)

Adresses = décalages dans `roms/Pokemon - Version Rouge Feu (France).gba` ; texte brut tel qu'il est dans la
ROM (capitales sans accent). Trouvés par l'alignement BPRE↔BPRF (symbole pokefirered indiqué). Les ROM GB/GBC
n'ont pas été nécessaires : tous les points ci-dessous existent dans Rouge Feu FR.

| point | choix actuel | Rouge Feu FR officiel | adresse BPRF (symbole) |
|---|---|---|---|
| Rival GARY (nom par défaut) | REGIS | **YAN** — choix proposés au joueur : GREEN, YAN, MAEL, DAVY (EN : GREEN, GARY, KAZ, TORU). REGIS n'est pas un nom du rival : c'est le Marin DYLAN (TRAINER_SAILOR_DYLAN). Le nom fictif du rival dans la table des Dresseurs (TERRY) est NOAH | tableau sRivalNameChoices 0x45C728 ; GREEN 0x1C3EAE, YAN 0x1C3EC2 (gNameChoice_Gary), MAEL 0x1C3EC6, DAVY 0x1C3ECB ; NOAH 0x23C1C8 ; REGIS 0x23A490 |
| CRUSHER | COGNEUR | **BROYEUR** (origine d'un indice du Memorydex, Aldo/Agatha) | 0x1AFD03 (gFameCheckerFlavorTextOriginObjectName_Bruno3), aussi 0x1AFD11, 0x1AFD20, 0x1AFD28 |
| CHARINE (Janine, fille de Koga) | CHARINE | **JEANNINE** | 0x1AFC1D (…OriginObjectName_Koga3) |
| Devise Ile 1 | — | ILE 1 / Les amis se réunissent ici | 0x181769 (OneIsland_Text_IslandSign) |
| Devise Ile 2 | — | ILE 2 / Le bonheur à deux | 0x1817FC |
| Devise Ile 3 | — | ILE 3 / L’île où on se sent chez soi | 0x181DF1 |
| Devise Ile 4 | — | ILE 4 / La chaleureuse île glacée | 0x1827D9 |
| Devise Ile 5 | — | ILE 5 / L’île où le temps s’écoule comme une rivière | 0x182BCC |
| Devise Ile 6 | — | ILE 6 / Lîle de la sagesse (sic, apostrophe manquante dans la ROM) | 0x182F52 |
| Devise Ile 7 | — | ILE 7 / L’île de l’infinité | 0x182E22 |
| Panneau Centre Réseau (Ile 1) | — | Pour relier le monde entier / CENTRE RESEAU POKéMON | 0x18178A |
| Salle de jeu (Ile 2, « Joyful Game Corner ») | — | SALLE DE JEU / Affrontez vos adversaires | 0x181814 |
| « Kanto Angels » (KANTO RIDER FEDERATION) | Kanto Angels | **KANTO ANGELS** (confirmé) | 0x189C89 (ThreeIsland_Port_Text_WereKantoRiderFederation) |
| Machine Réseau (Network Machine) | Machine Réseau | **pas de nom propre** : « ma machine » dans les dialogues ; le panneau dit seulement « NIVEAU DE CONNEXION 0/1/2 » (le mot « Network Machine » est supprimé) | 0x1A028B, 0x1A0DE3, 0x1A0E28 |
| Maniaque des Capacités (MOVE MANIAC) | Maniaque des Capacités | **DINGUE DES CAPACITES** | 0x1A16D3 (TwoIsland_House_Text_TeachMonMoveForMushroom) |
| Maître Pêcheur (FISHING GURU) | Maître Pêcheur | **MAITRE PECHEUR** (confirmé) | 0x1934E5, 0x1742CD |
| Gardien (SAFARI WARDEN) | Gardien | **GARDIEN** (confirmé) | 0x177836, 0x198196 |
| Ticketaurore (AURORATICKET) | Ticketaurore | **TICKETAURORA** ; destination BIRTH ISLAND = ILE AURORE | 0x17F9EC (VermilionCity_Text_OhAuroraTicketTakeYouToBirthIsland) |
| Sac à Baies (BERRY POUCH) | Sac à Baies | **SAC A BAIES** dans le menu / l'objet, mais **POCHE A BAIES** dans deux dialogues | SAC A BAIES 0x40EEE2 (gText_BerryPouch), 0x40EEEE ; POCHE A BAIES 0x17ADAA, 0x192687 |
| Étages du Centre Commercial | 1F, 2F… | numérotation française : RDC / 1er / 2ème / 3ème / 4ème / TOIT (panneaux : « 1er: MARCHE DES DRESSEURS », « 3ème: CADEAUX », « TOIT: DISTRIBUTEURS », « Rdc: Renseignements ») | 0x194C67, 0x1950EE, 0x195540 |
| Étages de la Sylphe | 1F…11F | « SYLPHE SARL. / RDC. » … « 10ème étage. » (11F = 10ème) ; le Président est « au 10ème étage » | 0x1754A5 (1F) … 0x177257 (11F), 0x175440 |
| Ascenseur (gText_1F…) | — | RC, 1{SUPER_ER}, 2{SUPER_E} … 10{SUPER_E} ; sous-sols « 1 SS » … « 4 SS » ; TOIT | 0x4107FA … 0x410818 ; 0x41081C … 0x41082B ; 0x410830 |
| Cabane Secrète (SECRET HOUSE) | Cabane Secrète | **CABANE SECRETE** (confirmé) | 0x17776C, 0x1777FC, 0x177C14 |
| Dent d’Or (GOLD TEETH) | Dent d’Or | **DENT D’OR** (confirmé, singulier) | 0x177836, 0x198196 |
| Zone Centrale (Safari, CENTER AREA) | Zone Centrale | **PARC CENTRAL** ; AREA 1/2/3 = PARC 1/2/3 | 0x17770C, 0x17774C, 0x1778E2 |

## Autres termes Rouge Feu FR rencontrés (pour le glossaire)
| anglais | Rouge Feu FR | adresse BPRF |
|---|---|---|
| FAME CHECKER | MEMORYDEX | 0x410987, 0x1B3BDA |
| TEACHY TV | TV ABC | 0x414ECA |
| VS SEEKER | CHERCHE VS | 0x193923, 0x1BFE5B |
| TRI-PASS / RAINBOW PASS | TRI-PASSE / PASSE PRISME | 0x17F895, 0x17F92F, 0x1A06B6 |
| SEAGALLOP ferry / HI-SPEED 7 | FERRY FLECHE DES MERS / FLECHE DES MERS 7 | 0x17F895, 0x17F8E7 |
| ROCKET HIDEOUT | REPAIRE ROCKET | 0x1AFA5E |
| WATER PATH / RUIN VALLEY | AGUALCANAL / VALLEE RUINE | 0x18B824 |
| SEVAULT CANYON / TANOBY RUINS / TANOBY CHAMBERS | CANYON SESOR / RUINES TANOBY / CHAMBRES TANOBY | 0x18CAD7, 0x3E7686, 0x3E7738 |
| SEVII ISLANDS | ILES SEVII | 0x1828F8 |
| CELIO / LOSTELLE | CILEO / LOSTELLE | 0x180C44, 0x17ABEC |
| BIKERS | MOTARDS | 0x1860AE |
| THUNDERBADGE, CASCADEBADGE | BADGEFOUDRE, BADGECASCADE (proposés « Badge Foudre », « Badge Cascade ») | lot.json |
| MR. FUJI | MR FUJI / DR FUJI (proposé « M. Fuji » ; « Dr Fuji » laissé dans 2 textes) | lot.json |

## Noms des Dresseurs (trainers_frlg.party, trainer_tower_sets.c)
Nom = `gTrainers[i].trainerName` (BPRF 0x2347A8 + 40·i + 4) ou `sTrainerTowerFloor_X.trainers[k].name`.
Casse SoulSilver ; accents restitués sur les prénoms français (Frédéric, Hélène, Gérard…), à vérifier.
Les noms déjà « Émeraude FR officiel » / « SoulSilver FR officiel » (partagés avec Émeraude/HnS) ne sont pas
repris. Le Dresseur TRAINER_NONE (« PH ») est vide dans la ROM : non trouvé.

| anglais | actuel | proposé | ROM FR brut | adresse BPRF | fichier |
|---|---|---|---|---|---|
| AARON | Aaron | Igor | IGOR | 0x23C0D8 | party |
| ALAN | Alan | Al | AL | 0x23ABC0 | party |
| ALI | Ali | Meg | MEG | 0x23A210 | party |
| ALLEN | Allen | Alain | ALAIN | 0x23AC88 | party |
| ALLYSON | Allyson | Aline | ALINE | 0x476564 | tour |
| ALMA | Alma | Axelle | AXELLE | 0x23D7A8 | party |
| ANDREW | Andrew | Ali | ALI | 0x23B340 | party |
| ANGELICA | Angelica | Angélique | ANGELIQUE | 0x23D550 | party |
| ARIANA | Ariana | Kim | KIM | 0x23D910 | party |
| AVA & GEB | Ava & Geb | Ava & Ged | AVA & GED | 0x23E8D8 | party |
| AVERY | Avery | Evan | EVAN | 0x23AAA8 | party |
| AXE & REN | Axe & Ren | Léo & Léa | LEO & LEA | 0x479004, 0x47914C | tour |
| BARRY | Barry | Benoît | BENOIT | 0x23B4A8 | party |
| BEAU | Beau | Yanis | YANIS | 0x23C3F8 | party |
| BENNY | Benny | Frédo | FREDO | 0x23BE58, 0x23F648 | party |
| BERKE | Berke | Bertrand | BERTRAND | 0x23CD30 | party |
| BETH | Beth | Betty | BETTY | 0x23EC20 | party |
| BETHANY | Bethany | Marissa | MARISSA | 0x23EE00 | party |
| BILLY | Billy | Willy | WILLY | 0x23AE90 | party |
| BRANDON | Brandon | Florent | FLORENT | 0x23ECE8 | party |
| BRANDON | Brandon | Florent | FLORENT | 0x474A44 | tour |
| BRAYDON | Braydon | Rayan | RAYAN | 0x23C4E8 | party |
| BRENT | Brent | Brad | BRAD | 0x23A0A8 | party |
| BRIDGET | Bridget | Elodie | ELODIE | 0x23B840 | party |
| BROOKE | Brooke | Blanche | BLANCHE | 0x23CE70 | party |
| BRYCE | Bryce | Jean-Loïc | JEAN-LOIC | 0x23E590 | party |
| CAMERON | Cameron | Prosper | PROSPER | 0x23BAE8 | party |
| CAROL | Carol | Carole | CAROLE | 0x23A760 | party |
| CARTER | Carter | Francis | FRANCIS | 0x23BFC0 | party |
| CHAD | Chad | Cédric | CEDRIC | 0x239DB0, 0x23DCF8 | party |
| CHARLIE | Charlie | Charles | CHARLES | 0x23E1F8 | party |
| CLARK | Clark | Luigi | LUIGI | 0x23AC10 | party |
| CONNIE | Connie | Constance | CONSTANCE | 0x23BA48 | party |
| CONNOR | Connor | Joao | JOAO | 0x23C358 | party |
| COREY | Corey | Didier | DIDIER | 0x23B6D8, 0x23F8F0 | party |
| DALE | Dale | Fabio | FABIO | 0x23B1B0 | party |
| DANA | Dana | Christelle | CHRISTELLE | 0x23D8E8 | party |
| DAWN | Dawn | Maëlle | MAELLE | 0x23A2B0 | party |
| DEAN | Dean | Jean | JEAN | 0x23B4D0 | party |
| DEREK | Derek | Didier | DIDIER | 0x23AAD0 | party |
| DIANA | Diana | Diane | DIANE | 0x23A648 | party |
| DIRK | Dirk | Clément | CLEMENT | 0x23B778 | party |
| DOUGLAS | Douglas | Dominique | DOMINIQUE | 0x23B408 | party |
| DUDLEY | Dudley | Dorian | DORIAN | 0x23AC60 | party |
| DUNCAN | Duncan | Ludovic | LUDOVIC | 0x23A440 | party |
| DWAYNE | Dwayne | Harold | HAROLD | 0x23A4E0 | party |
| EDGAR | Edgar | Edgard | EDGARD | 0x23BCF0 | party |
| EDWARD | Edward | Edouard | EDOUARD | 0x23BC50 | party |
| EDWIN | Edwin | Martin | MARTIN | 0x23BE80 | party |
| ETHAN | Ethan | Diego | DIEGO | 0x23A558 | party |
| EVAN | Evan | Akim | AKIM | 0x23EB80, 0x23FFD0 | party |
| EVE & JON | Eve & Jon | Eve & Joe | EVE & JOE | 0x23EAE0 | party |
| FRANKLIN | Franklin | François | FRANÇOIS | 0x23AB48, 0x23DE88 | party |
| GARRETT | Garrett | Logan | LOGAN | 0x23E4C8 | party |
| GEB&MEGAN | Geb&Megan | Geb & Mel | GEB & MEL | 0x477104, 0x47724C | tour |
| GEORGE | George | Georges | GEORGES | 0x23CC40 | party |
| GIDEON | Gideon | Gedeon | GEDEON | 0x23E400 | party |
| GOON | Goon | Gabin | GABIN | 0x23E130, 0x23E158 | party |
| GREG | Greg | Gregory | GREGORY | 0x239F68 | party |
| GREGORY | Gregory | Jb | JB | 0x23BC28 | party |
| GWEN | Gwen | Gwenaëlle | GWENAELLE | 0x23D820 | party |
| HANK | Hank | Serge | SERGE | 0x23B250 | party |
| HERMAN | Herman | Hervé | HERVE | 0x23A850, 0x23F3A0 | party |
| HOPE | Hope | Hortense | HORTENSE | 0x23D410 | party |
| HUGH | Hugh | Hughes | HUGHES | 0x23E568, 0x23FBC0 | party |
| IRENE | Irene | Irène | IRENE | 0x23D8C0 | party |
| IVAN | Ivan | Yvan | YVAN | 0x23C510 | party |
| JAC | Jac | Ilan | ILAN | 0x472764 | tour |
| JACK | Jack | Jacques | JACQUES | 0x23B548, 0x23FA30 | party |
| JACLYN | Jaclyn | Jaqueline | JAQUELINE | 0x23DFA0, 0x23FE18 | party |
| JARED | Jared | Boris | BORIS | 0x23AD50 | party |
| JASON | Jason | Youri | YOURI | 0x23BD18 | party |
| JEFF | Jeff | Antonio | ANTONIO | 0x23A5A8, 0x23F0D0 | party |
| JEN & KIRA | Jen & Kira | Ery & Kira | ERY & KIRA | 0x475204, 0x47534C | tour |
| JEREMY | Jeremy | Maurice | MAURICE | 0x23D780, 0x23F350 | party |
| JERRY | Jerry | Julien | JULIEN | 0x23C380 | party |
| JODY | Jody | Joëlle | JOELLE | 0x23D488 | party |
| JONAH | Jonah | Jonas | JONAS | 0x23EE78 | party |
| JORDY | Jordy | Angelo | ANGELO | 0x473AC4 | tour |
| JOSE | Jose | José | JOSE | 0x23C3A8 | party |
| JOSH | Josh | Johnny | JOHNNY | 0x239D10 | party |
| JOSHUA | Joshua | Joseph | JOSEPH | 0x23C448 | party |
| JOY & MEG | Joy & Meg | Bea & Eva | BEA & EVA | 0x23E658, 0x23FC88 | party |
| KAT & KIPP | Kat & Kipp | Kat & Nino | KAT & NINO | 0x476D24, 0x476E6C | tour |
| KATI & GEB | Kati & Geb | Kati & Seb | KATI & SEB | 0x4793E4, 0x47952C | tour |
| KEITH | Keith | Mathieu | MATHIEU | 0x23BF98 | party |
| KELSEY | Kelsey | Zora | ZORA | 0x23A6C0, 0x23EFE0 | party |
| KENT | Kent | Ken | KEN | 0x239FB8 | party |
| KIRI & JAN | Kiri & Jan | Joy & Kate | JOY & KATE | 0x23DAF0 | party |
| KIRK | Kirk | Chris | CHRIS | 0x23BBD8 | party |
| LAO | Lao | Layo | LAYO | 0x23ADF0 | party |
| LARRY | Larry | Laurent | LAURENT | 0x23E9F0, 0x23FE90 | party |
| LEONARD | Leonard | Léonard | LEONARD | 0x23A418 | party |
| LEROY | Leroy | Léon | LEON | 0x23EC70, 0x240048 | party |
| LEWIS | Lewis | Samir | SAMIR | 0x23B110 | party |
| LEX & NYA | Lex & Nya | Paul & Nya | PAUL & NYA | 0x23ECC0, 0x240098 | party |
| LIA & LUC | Lia & Luc | Vivi & Sam | VIVI & SAM | 0x23DB68 | party |
| LIAM | Liam | Elvin | ELVIN | 0x23A508 | party |
| LIL & IAN | Lil & Ian | Ly & Ian | LY & IAN | 0x23DB90, 0x23FA58 | party |
| LILY | Lily | Flo | FLO | 0x474664 | tour |
| LISA | Lisa | Lisa | LISA | 0x23A3A0 | party (douteux) |
| LISA&LEAH | Lisa&Leah | Lisa&Erin | LISA&ERIN | 0x4774E4, 0x47762C | tour |
| LORI | Lori | Laurence | LAURENCE | 0x23B890 | party |
| MARK | Mark | Achille | ACHILLE | 0x23A828, 0x23EBA8 | party |
| MARTHA | Martha | Marthe | MARTHE | 0x23A7B0 | party |
| MARY | Mary | Marie | MARIE | 0x23CDA8 | party |
| MELISSA | Melissa | Mélissa | MELISSA | 0x23B958, 0x240188 | party |
| MIKAELA | Mikaela | Dorine | DORINE | 0x479CEC | tour |
| MIKE | Mike | Maxime | MAXIME | 0x23C088 | party |
| MIKE | Mike | Maxime | MAXIME | 0x473EA4 | tour |
| MILY | MILY | Lucille | LUCILLE | 0x472B44 | tour |
| MYMO | Mymo | Gavin | GAVIN | 0x23E888 | party |
| NATE | Nate | Vicente | VICENTE | 0x23BCA0 | party |
| NED | Ned | Erwan | ERWAN | 0x23B200 | party |
| NIKKI | Nikki | Mylène | MYLENE | 0x23E090 | party |
| NOB | Nob | Hiro | HIRO | 0x23AB70 | party |
| NORTON | Norton | Pacôme | PACOME | 0x23D118 | party |
| OLIVER | Oliver | Tanguy | TANGUY | 0x23AD00 | party |
| OWEN | Owen | Oliver | OLIVER | 0x23CD08 | party |
| OWEN | Owen | Oliver | OLIVER | 0x478464 | tour |
| PAIGE | Paige | Marine | MARINE | 0x23A2D8 | party |
| PARKER | Parker | Patrick | PATRICK | 0x23C470 | party |
| PHILLIP | Phillip | Philippe | PHILIPPE | 0x23A4B8 | party |
| PRESTON | Preston | Polo | POLO | 0x23BB10 | party |
| PRISCILLA | Priscilla | Ninon | NINON | 0x4778C4 | tour |
| QUINN | Quinn | Isidore | ISIDORE | 0x23B020 | party |
| RANDALL | Randall | Raphaël | RAPHAEL | 0x23BB38 | party |
| RAUL | Raul | Jason | JASON | 0x23B638 | party |
| RAY & TYRA | Ray & Tyra | Roméo&Tyra | ROMEO&TYRA | 0x23DAA0 | party |
| RELI | Reli | Lana | LANA | 0x23A1E8, 0x23DD20 | party |
| RIC & RENE | Ric & Rene | Ric & Lili | RIC & LILI | 0x474E24, 0x474F6C | tour |
| RICH | Rich | Blaise | BLAISE | 0x23B818, 0x23F490 | party |
| RICK | Rick | Omar | OMAR | 0x239EC8 | party |
| RICKY | Ricky | Rachid | RACHID | 0x23A580, 0x23F058 | party |
| RILEY | Riley | Marcel | MARCEL | 0x23EF68 | party |
| ROBERT | Robert | Bob | BOB | 0x23BE08, 0x23F558 | party |
| RODNEY | Rodney | Rodolphe | RODOLPHE | 0x23C3D0 | party |
| ROLAND | Roland | Pacôme | PACOME | 0x23B598 | party |
| RONALD | Ronald | Fabien | FABIEN | 0x23B2A0 | party |
| RUTH | Ruth | Aurore | AURORE | 0x23D4D8 | party |
| SHANE | Shane | Djamel | DJAMEL | 0x23A530 | party |
| SHANNON | Shannon | Samia | SAMIA | 0x23CE20 | party |
| SHARON | Sharon | Morgane | MORGANE | 0x23DFC8, 0x23FAD0 | party |
| SHAWN | Shawn | Robert | ROBERT | 0x23BC00 | party |
| SPENCER | Spencer | Sylvain | SYLVAIN | 0x23B520 | party |
| STAN | Stan | Stanislas | STANISLAS | 0x23B7C8 | party |
| STANLY | Stanly | Hugo | HUGO | 0x23E0B8 | party |
| STEVE | Steve | Stéphane | STEPHANE | 0x23A8A0 | party |
| SUSIE | Susie | Suzy | SUZY | 0x23D7D0, 0x23F5A8 | party |
| TED | Ted | Théo | THEO | 0x23C330 | party |
| THOMAS | Thomas | Tony | TONY | 0x23D0A0 | party |
| TIFFANY | Tiffany | Sabrina | SABRINA | 0x23B908 | party |
| TOBY | Toby | Manu | MANU | 0x23E748 | party |
| TOMMY | Tommy | Tom | TOM | 0x23E4F0 | party |
| TONY | Tony | Antoine | ANTOINE | 0x23B458, 0x240160 | party |
| TRAVIS | Travis | Thierry | THIERRY | 0x23C4C0 | party |
| TREVOR | Trevor | Trevor | TREVOR | 0x23A3F0 | party (douteux) |
| TUCKER | Tucker | Anatole | ANATOLE | 0x23D0F0 | party |
| TYLER | Tyler | Ethan | ETHAN | 0x239DD8 | party |
| TYLOR | Tylor | Titouan | TITOUAN | 0x23E860 | party |
| VALERIE | Valerie | Valeria | VALERIA | 0x23D7F8 | party |
| VANCE | Vance | Basil | BASIL | 0x23EEA0 | party |
| VIRGIL | Virgil | Virgile | VIRGILE | 0x23D848 | party |
| WADE | Wade | Aristide | ARISTIDE | 0x23B2F0, 0x23FA08 | party |
| WARREN | Warren | Wolfgang | WOLFGANG | 0x23CD80 | party |
| WAYNE | Wayne | Jérémy | JEREMY | 0x23AB98 | party |
| WILTON | Wilton | Wilfried | WILFRIED | 0x23BED0 | party |
| ZACKERY | Zackery | Mario | MARIO | 0x479A54 | tour |
