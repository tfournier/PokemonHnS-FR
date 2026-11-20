#!/usr/bin/env bash
# Reconstruit memoires/hns_en.gba (ROM anglaise officielle de Heart & Soul) pour la CI :
#   1. déchiffre Émeraude US (fichier gpg du dépôt privé, phrase de passe dans $ROM_PASSPHRASE) ;
#   2. télécharge le patch officiel HnS depuis la release publique de pokehns-expansion ;
#   3. contrôle les empreintes (outils/ci/empreintes.txt) et applique le patch (CRC vérifiés).
#
#   ROM_PASSPHRASE=… outils/ci/preparer_rom.sh <emeraude_us.gba.gpg>
#
# Aucune ROM n'est écrite ailleurs que dans memoires/ (ignoré par git) ; rien n'est publié.
set -euo pipefail
gpgfile=${1:?usage: preparer_rom.sh <emeraude_us.gba.gpg>}
gpgfile=$(cd "$(dirname "$gpgfile")" && pwd)/$(basename "$gpgfile")
cd "$(dirname "$0")/../.."
: "${ROM_PASSPHRASE:?variable ROM_PASSPHRASE absente}"
PY=python3; [ -x .venv/bin/python ] && PY=.venv/bin/python

tag=$(tr -d '[:space:]' < upstream.txt)                 # ex. Release-v2.0.6
patch="pokemonHnS_${tag#Release-}.ups"                  # ex. pokemonHnS_v2.0.6.ups
empreinte() { awk -v k="$1" '$2 == k { print $1 }' outils/ci/empreintes.txt; }
verifier() {   # verifier <fichier> <clé dans empreintes.txt>
  attendu=$(empreinte "$2"); [ -n "$attendu" ] || { echo "empreinte de $2 absente de outils/ci/empreintes.txt" >&2; exit 1; }
  obtenu=$("$PY" -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$1")
  [ "$obtenu" = "$attendu" ] || { echo "$2 : empreinte inattendue ($obtenu)" >&2; exit 1; }
}

mkdir -p memoires
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT

# 1. Émeraude US
printf '%s' "$ROM_PASSPHRASE" | gpg --batch --quiet --pinentry-mode loopback --passphrase-fd 0 \
  --output memoires/emeraude_us.gba --decrypt "$gpgfile"
verifier memoires/emeraude_us.gba emeraude_us.gba

# 2. patch officiel HnS (public)
curl -fsSL -o "$tmp/$patch" \
  "https://github.com/PokemonHnS-Development/pokehns-expansion/releases/download/$tag/$patch"
verifier "$tmp/$patch" "$patch"

# 3. ROM anglaise de HnS
"$PY" -I outils/ups_appliquer.py memoires/emeraude_us.gba "$tmp/$patch" memoires/hns_en.gba
verifier memoires/hns_en.gba hns_en.gba
echo "memoires/hns_en.gba prête"
