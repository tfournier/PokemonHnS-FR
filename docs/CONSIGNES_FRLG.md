# Consignes complémentaires : cartes FRLG (lots D2, D3a, D3b, D4)

Les cartes `data/maps/*_Frlg` viennent de la branche Rouge Feu / Vert Feuille de pokeemerald-expansion.
Elles ne sont pas compilées dans HnS mais doivent être traduites (règle « rien en anglais »).

## Noms et termes déjà fixés (à respecter dans toutes les tranches)
- Kanto selon SoulSilver FR : Bourg Palette, Jadielle, Argenta, Azuria, Carmin sur Mer, Lavanville, Céladopole,
  Safrania, Parmanie, Cramois’Ile, Plateau Indigo, Mont Sélénite, Grotte (Rock Tunnel = « Grotte », pas
  « Grotte Sombre » qui est la Dark Cave de Johto), Route Victoire, Tour Pokémon, Sylphe SARL, Centre Commercial
  de Céladopole, Iles Ecume, Parc Safari… — vérifie toujours dans `traductions/glossaire.tsv` et dans les entrées
  officielles des .po.
- Personnages (SoulSilver FR) : Prof. Chen, Pierre, Ondine, Major Bob, Erika, Koga, Morgane, Auguste, Giovanni,
  Olga, Aldo, Agatha, Peter, Léo (BILL), M. Fuji, Nina (DAISY, sœur du rival). Le rival du joueur est `{RIVAL}`.
- Rouge Feu / Vert Feuille FR (vérifiés sur Poképédia) : SEAGALLOP → « Flèche des Mers » (« Ferry Flèche des
  Mers {STR_VAR_1} »), TEA → « Thé ». Pour les **îles Sevii, leurs lieux, leurs personnages et les objets propres
  à Rouge Feu / Vert Feuille**, emploie les noms officiels français de Rouge Feu / Vert Feuille : vérifie-les sur
  Poképédia (pokepedia.fr ; WebSearch / WebFetch chargeables avec ToolSearch) et note la source dans `preuve`.
  Si tu ne trouves pas de nom officiel, garde une forme neutre et mets l'entrée dans `douteux.json`.
- Team Rocket (jamais « les Rocket » seul pour l'organisation), Sbire Rocket, Dresseur, Pokémon, Pokédex, Badge,
  Arène, Champion d’Arène / Championne, Conseil 4, Maître, Centre Pokémon, Boutique, PC de Léo, Sac, CT/CS.
- Typographie : pas d'espace avant ! ? : ; — apostrophe ’ — points de suspension … — guillemets “ ”.

## Méthode
- Ouvre `build/upstream_orig/data/maps/<carte>/scripts.inc` pour chaque texte : qui parle (label, script,
  objet/PNJ), registre tu/vous, texte précédent/suivant, fragments (fin en `\n`/`\p`).
- Les cartes HnS de Kanto (`*_hns`, compilées, déjà traduites dans les .po) reprennent souvent les mêmes
  répliques : cherche-les (rapidfuzz ≥ 80 sur les msgid traduits) et reprends la traduction **officielle**
  correspondante (adaptée) ; si la référence vient du patch FR, vérifie le sens.
- Les répliques des Dresseurs (intro / défaite / après-combat) sont courtes et vivantes, comme dans les
  officiels ; les panneaux suivent le style des panneaux officiels (« Route 1 — Bourg Palette ↔ Jadielle »).
- Mise en page : `Gen3(build/upstream_orig).reformater(texte, 198)` (corrigé : les codes à espace ne bouclent
  plus), sauf fragments en `\n`/`\p`, `{DYNAMIC}`, `{CLEAR_TO}`. Un texte d'une ligne reste d'une ligne.

## Précisions (mises à jour)
- Aucune majuscule accentuée, même en casse normale (décision 14) : Cramois’Ile, Iles Ecume, Ile 1, Badge Ame, A la…
- CELIO → Ciléo (Rouge Feu / Vert Feuille FR, Poképédia).
