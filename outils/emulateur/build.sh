#!/bin/bash
# Construit libmgba (statique, sans interface) puis le lanceur hns_run.
# Usage : outils/emulateur/build.sh [--propre]
#   --propre : supprime les objets intermédiaires de mGBA après la construction
#              (garde libmgba.a et les en-têtes générés).
set -euo pipefail
ICI="$(cd "$(dirname "$0")" && pwd)"
P="$(cd "$ICI/../.." && pwd)"
SRC="$P/build/mgba-src"
BLD="$P/build/mgba-build"
TAG=0.10.5

if [ ! -d "$SRC" ]; then
  git clone --depth 1 --branch "$TAG" https://github.com/mgba-emu/mgba.git "$SRC"
fi

if [ ! -f "$BLD/libmgba.a" ]; then
  mkdir -p "$BLD"
  cmake -S "$SRC" -B "$BLD" -DCMAKE_BUILD_TYPE=Release \
    -DUSE_FFMPEG=OFF -DBUILD_QT=OFF -DBUILD_SDL=OFF -DUSE_LUA=OFF -DENABLE_SCRIPTING=OFF \
    -DUSE_EDITLINE=OFF -DUSE_SQLITE3=OFF -DUSE_LIBZIP=OFF -DUSE_MINIZIP=OFF -DUSE_ELF=OFF \
    -DUSE_DISCORD_RPC=OFF -DUSE_EPOXY=OFF -DBUILD_GL=OFF -DBUILD_GLES2=OFF -DBUILD_GLES3=OFF \
    -DUSE_DEBUGGERS=OFF -DUSE_GDB_STUB=OFF -DM_CORE_GB=OFF -DUSE_PNG=ON -DUSE_ZLIB=ON \
    -DUSE_LZMA=OFF -DBUILD_PERF=OFF -DBUILD_TEST=OFF -DBUILD_SUITE=OFF -DBUILD_CINEMA=OFF \
    -DBUILD_EXAMPLE=OFF -DBUILD_UPDATER=OFF -DBUILD_SHARED=OFF -DBUILD_STATIC=ON
  make -C "$BLD" -j"$(sysctl -n hw.ncpu 2>/dev/null || nproc)" mgba
fi

DEFS="-DBUILD_STATIC -DM_CORE_GBA -DUSE_PNG -DUSE_ZLIB -DUSE_PTHREADS -DHAVE_CRC32 -DHAVE_LOCALTIME_R -DHAVE_STRDUP -DHAVE_STRLCPY -DHAVE_STRNDUP -DHAVE_XLOCALE"
PNG_CFLAGS="$(pkg-config --cflags libpng)"
PNG_LIBS="$(pkg-config --libs libpng)"

cc -O2 -flto -std=c11 -Wall $DEFS -I"$SRC/include" -I"$BLD/include" $PNG_CFLAGS \
  "$ICI/hns_run.c" "$BLD/libmgba.a" $PNG_LIBS -lz -lpthread -framework CoreFoundation -o "$ICI/hns_run"
echo "OK : $ICI/hns_run"

if [ "${1:-}" = "--propre" ]; then
  rm -rf "$BLD/CMakeFiles" "$BLD"/src "$BLD"/version.c
  echo "Objets intermédiaires supprimés ($(du -sh "$BLD" | cut -f1) restants dans $BLD)."
fi
