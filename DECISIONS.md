# Décisions de traduction et d'outillage

Chaque décision : date, décision, raison, conséquences. Les décisions de terminologie sont aussi
reportées dans `traductions/glossaire.tsv`.

## Décisions héritées du projet (avant reprise)

| Sujet | Décision |
|---|---|
| Style | SoulSilver FR : « Pokémon », « Dresseur », « Pokématos », « Prof. Orme », « Prof. Chen » ; lieux/objets/capacités en minuscules avec majuscule initiale ; espèces en capitales (banque 237). |
| Noms | Johto/Kanto selon SoulSilver FR (Bourg Geon, Ville Griotte, Rosalia, Fargas, Léo…) ; Hoenn selon Émeraude FR (FLORA, BRICE, TIMMY, Prof. SEKO…). |
| Menu START | En capitales comme Émeraude FR : POKéDEX, POKéMON, SAC, {POKE}MATOS, SAUVER, OPTIONS, RETOUR (ligature {POKE} car « Pokématos » entier est tronqué). |
| Horloge | 24 h (`code/horloge-24h.patch`). |
| Combat | « PTITARD sauvage », « … ennemi » : qualificatif après le nom, sans article (`code/nom-sauvage-ennemi.patch`). Glyphe 0x105 « Lv » → « N. » dans toutes les polices latines. |
| Abréviations | Statuts PSN, PAR, SOM, GEL, BRU, GLR ; stats PV, AT, DF, AS, DS, VI. |
| Pokédex | INFO, ZONE, STATS, EVO, CRI, TAIL. ; VUS / PRIS ; RECH. ; RETOUR LISTE / HAUT DE LISTE / BAS DE LISTE / FERMER POKéDEX. |
| Claviers | `src/text_input_strings.c` jamais traduit : la disposition affichée doit suivre celle du code. |
| Même anglais, sens différents | `traductions/contextes.po` (msgctxt = fichier) : PSYCHIC (type Psy / classe Kinésiste), entrées du menu START. |

## 2026-11-20 — reprise du projet

1. **Sources de texte supplémentaires.** Les noms de Dresseurs (`src/data/*.party`) et de lieux
   (`src/data/region_map/region_map_sections.json`) sont traduits dans ces fichiers sources : les `.h`
   correspondants sont générés à la compilation et ne doivent plus être lus (`hnsfr.py` ne lit plus que
   les fichiers suivis par git). Les textes de debug (`debug.c`, `battle_debug.c`) et les crédits ne
   sont plus exclus : le brief demande de tout traduire, y compris les textes de développement.
2. **Entrées purgées.** 351 entrées dont la clé était déjà du français (amorçage précédent fait sur
   un arbre déjà traduit : « Steevy », « EPAVE »…) ou des claviers exclus ont été retirées des .po.
3. **Noms de types.** Émeraude FR tronquait à 6 lettres (ELECTR, TENEBR) ; HnS autorise 8 caractères.
   Noms complets en capitales, sans accent (voir décision 14) : NORMAL, COMBAT, VOL, POISON, SOL, ROCHE,
   INSECTE, SPECTRE, ACIER, FEU, EAU, PLANTE, ELECTRIK, PSY, GLACE, DRAGON, TENEBRES, FEE, STELL. (« Stellaire », 9 lettres, dépasse la limite de 8). Les mêmes clés servent aux
   mots Easy Chat et à la radio : même graphie partout (ce sont des libellés).
4. **Largeur des textes officiels.** La règle des 198 px s'applique aux traductions nouvelles et au
   patch FR. Un texte officiel (Émeraude FR / SoulSilver FR) est toléré jusqu'à 216 px, largeur
   réelle de la fenêtre de dialogue (27 tuiles), pour ne pas réécrire un texte officiel qui s'affiche
   correctement dans le moteur d'Émeraude.
5. **Codes équivalents.** Un code écrit autrement mais de mêmes octets (`{FONT 0}` / `{FONT_SMALL}`,
   `{CLEAR_TO 87}` / `{CLEAR_TO 0x57}`) n'est pas une erreur pour le contrôle, mais on réécrit la
   graphie anglaise lors de l'intégration.
6. **Ponctuation.** Pas d'espace avant ! ? : ; dans tout le projet (mesuré : c'est déjà le cas de
   toutes les sources, y compris les textes SoulSilver convertis).
7. **Relecteur indépendant.** ChatGPT est appelé via la CLI Codex (`codex exec`, compte ChatGPT de
   l'utilisateur) par `outils/relecture_chatgpt.py`. Les textes officiels exacts ne lui sont soumis
   qu'en mode « alignement » (est-ce la bonne phrase ?).
8. **Arbitrage automatique** (`outils/arbitrer_relecture.py`) : refus des remarques qui ne changent que
   la mise en page, qui touchent un texte officiel, qui cassent un contrôle bloquant ou qui ajoutent
   une espace avant la ponctuation ; termes hors glossaire laissés à l'arbitrage de l'agent principal.
9. **Priorité à l'intégration** (`outils/integrer_lot.py`) : Émeraude FR exact (1) < Émeraude FR adapté
   (1,5) < SoulSilver FR exact (2) < SoulSilver FR adapté (2,5) < patch FR (3) < traduction nouvelle (4).
   Une source moins bonne ne remplace jamais une meilleure, sauf correction justifiée (`--corriger`),
   et jamais un officiel exact sauf alignement faux démontré.
10. **Commits non signés** dans ce dépôt (clé GPG sur YubiKey, bloquante pour un agent).
11. **Sauts de ligne SoulSilver.** `\f` (Gen 4 : défilement d'une ligne dans la même boîte) devient `\l`
    et non `\p` : `\p` coupait les phrases en deux pages. `\r` (nouvelle boîte) devient `\p`. (Lot B.)
12. **Symbole monétaire.** Le « $ » des textes SoulSilver (Pokédollar) vaut 0xFF en Gen 3, c'est-à-dire la
    fin de chaîne : il est converti en « ¥ » après le nombre (« 500¥ »), comme Émeraude FR. Le
    vérificateur rejette désormais tout « $ » absent de l'anglais.
13. **Noms de Dresseurs homonymes.** Un même prénom anglais peut désigner des personnes différentes selon
    la région (BILL Cracheur de feu → Andréa ; BILL le personnage → Léo). Les noms de Dresseurs
    SoulSilver sont donc posés avec `msgctxt` = fichier `.party` (contextes.po).
14. **Capitales sans accent dans les libellés en capitales** (corrige la première version de la décision 3).
    Mesuré dans Émeraude FR : RESUME, DEPLACER, BOITE, ETEINDRE, DEFENSE, CAPACITE, DUREE, ATQ. SPE
    apparaissent sans accent, et aucune forme accentuée n'existe ; SoulSilver FR fait de même (HERICENDRE,
    ELECTRIK). Les libellés entièrement en capitales (menus, onglets, types, espèces) ne portent donc
    jamais d'accent, sauf le « é » minuscule de POKéMON / POKéDEX. Dans le texte courant (casse normale),
    les majuscules gardent leurs accents comme le glossaire du projet (« À la prochaine », « Cramois’Île »,
    « Îles Écume »).
