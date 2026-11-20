# Anomalies repérées, à traiter (audit C ou agent principal)

| Origine | Entrée / fichier | Problème |
|---|---|---|
| lot D1 | data/text/battle_tent.inc, entrée PALACE | à l'écran « le défi de la défi de la… » : fragments concaténés incohérents |
| lot D1 | data/text/pc_transfer.inc « BILL'S PC.\p » | le \p final a été perdu ; « was full » ne s'enchaîne plus avec son préfixe |
| lot D1 | fame_checker (FRLG) | libellés KOGA et PETER en capitales, AGATHA et LORELEI vides |
| lot B | Kinésiste NATHAN (trainers_hns.party) | le .po donne « Nathan », SoulSilver FR l'appelle « Jason » |
| lot B | glossaire | SS écrit « Oeuf », capitales sans accent (Electrik, Iles Ecume), « Champion d’Arène » : le glossaire garde Œuf, accents, à harmoniser |
| lot B | 15 Dresseurs de trainers_hns.party | absents des références du .po (références tronquées à 6 occurrences) |
| inventaire images | union_room_chat/background.png | bouton START coupé (« S…TART ») — confié au lot F |
| inventaire images | pokeblock/use_screen/updown.png | DOWN resté en anglais — confié au lot F |
| lot D1 | noms FRLG introuvables | « Ile 4 », « Grotte de Glace », « Seagallop {n} », CELIO, CHARINE gardés ; CRUSHER → COGNEUR ; GARY → REGIS : à valider |
