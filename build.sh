#!/usr/bin/env bash
# Construit la traduction française de Pokémon Heart & Soul.
#   ./build.sh            -> ROM dans build/, patchs dans dist/, rapports dans rapport/
# Prérequis : git, make, gcc, g++, libpng, arm-none-eabi-gcc (avec newlib), python3 + polib
set -euo pipefail
cd "$(dirname "$0")"
# chaîne ARM : celle du PATH, sinon une chaîne xPack installée dans ~/.local
if ! command -v arm-none-eabi-gcc >/dev/null; then
  for d in "$HOME"/.local/xpack-arm-none-eabi-gcc-*/bin; do [ -x "$d/arm-none-eabi-gcc" ] && PATH="$d:$PATH"; done
fi
command -v arm-none-eabi-gcc >/dev/null || { echo "arm-none-eabi-gcc introuvable" >&2; exit 1; }
PY=python3; [ -x .venv/bin/python ] && PY=.venv/bin/python
"$PY" -I outils/construire.py . "$@"
