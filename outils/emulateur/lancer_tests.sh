#!/bin/bash
# Rejoue tous les scénarios de tests en émulateur sur une ROM.
# Usage : outils/emulateur/lancer_tests.sh <rom.gba> <dossier_sortie> [dossier_etats]
#   <dossier_sortie>/<scenario>/NN_nom.png : captures 240×160
#   [dossier_etats] (défaut : build/tests_emulateur/etats) : états de sauvegarde mGBA 0.10.5
#     (réouvrables dans mGBA : mGBA -t <etat.ss> <rom.gba>)
# Variables : SCENARIOS="01_titre_intro 02_debut_aventure" pour n'en jouer que certains
#             (chaque scénario part de l'état produit par le précédent, voir README.md).
set -uo pipefail
ICI="$(cd "$(dirname "$0")" && pwd)"
P="$(cd "$ICI/../.." && pwd)"
ROM="${1:?usage : lancer_tests.sh <rom.gba> <dossier_sortie> [dossier_etats]}"
SORTIE="${2:?usage : lancer_tests.sh <rom.gba> <dossier_sortie> [dossier_etats]}"
ETATS="${3:-$P/build/tests_emulateur/etats}"
BIN="$ICI/hns_run"

[ -x "$BIN" ] || "$ICI/build.sh"
JOURNAUX="$(dirname "$ETATS")/journaux"
mkdir -p "$SORTIE" "$ETATS" "$JOURNAUX"
# la sauvegarde de test ne vit jamais à côté des ROM
SAV="$ETATS/test.sav"

if [ -z "${SCENARIOS:-}" ]; then
  SCENARIOS="$(cd "$ICI/scenarios" && ls [0-9][0-9]_*.txt | sed 's/\.txt$//')"
fi

echoue=0
for s in $SCENARIOS; do
  out="$SORTIE/$s"
  rm -rf "$out"
  opts=()
  case "$s" in 01_*) opts+=(--fresh) ;; esac
  printf '== %s\n' "$s"
  if "$BIN" --rom "$ROM" --sav "$SAV" --out "$out" --states "$ETATS" ${opts[@]+"${opts[@]}"} \
       "$ICI/scenarios/$s.txt" > "$JOURNAUX/$s.log" 2>&1; then
    printf '   OK : %s captures  (%s)\n' "$(ls "$out" 2>/dev/null | wc -l | tr -d ' ')" "$(grep '\[hns_run\]' "$JOURNAUX/$s.log")"
  else
    echoue=$((echoue + 1))
    printf '   ÉCHEC (voir %s)\n' "$JOURNAUX/$s.log"
    grep -v '^#' "$JOURNAUX/$s.log" | tail -5 | sed 's/^/   | /'
  fi
done
exit $echoue
