"""Images du 2e lot faites par copie ou collage simple (à lancer depuis la racine, argument : dossier de sortie)."""
import sys, struct; sys.path.insert(0, 'outils/graphismes')
from pnglike import *; from lz77 import lz77; from tiles4bpp import from4bpp; from dexgfx import load_tiles, read_bin, compose
import numpy as np, police3x5 as P
O = sys.argv[1]; U = 'build/upstream_orig/graphics/'; I = 'images/graphics/'
# summary_screen/iv_ev_tiles : tuiles modifiées de la version FR de hns/tiles.png (quartet bas), palette propre gardée
a = load(U + 'summary_screen/tiles.png'); v = load(U + 'summary_screen/iv_ev_tiles.png'); f = load(I + 'summary_screen/hns/tiles.png')
o = v.copy(); m = a != f; o[m] = (v[m] & 0xF0) | (f[m] & 15); save_like(U + 'summary_screen/iv_ev_tiles.png', o, O + '/iv_ev_tiles.png')
# move_info_window_l/r : zone texte de move_info_window_start FR (2 lignes plus haut)
s = load(I + 'battle_interface/move_info_window_start.png')
for n in 'lr':
    p = U + 'battle_interface/move_info_window_%s.png' % n; o = load(p).copy(); o[11:22, 2:30] = s[13:24, 2:30]; save_like(p, o, O + '/move_info_window_%s.png' % n)
# link/321start_static : GO! de 321start FR, même centrage que START
st = load(U + 'link/321start_static.png'); fr = load(I + 'link/321start.png')
Lf = np.hstack([fr[48:80], fr[80:112]]); L = np.zeros((32, 96), np.uint8); L[0:24, 23:74] = Lf[4:28, 39:90]
o = st.copy(); o[96:128] = L[:, :32]; o[128:160] = L[:, 32:64]; o[160:192] = L[:, 64:]; save_like(U + 'link/321start_static.png', o, O + '/321start_static.png')
# voltorb_flip/Raw/gameboard : MEMO de l'écran FR compilé, indices de couleur convertis vers la palette de Raw
e = read_bin(U + 'voltorb_flip/gameboard.bin'); _, to = load_tiles(U + 'voltorb_flip/gameboard.png'); _, tf = load_tiles(I + 'voltorb_flip/gameboard.png')
A = compose(to, e) & 15; B = compose(tf, e) & 15; R = load(U + 'voltorb_flip/Raw/gameboard.png')
mp = dict(zip(A[10:24, 176:216].flatten(), R[10:24, 176:216].flatten())); o = R.copy(); o[10:24, 176:216] = np.vectorize(mp.get)(B[10:24, 176:216])
save_like(U + 'voltorb_flip/Raw/gameboard.png', o, O + '/gameboard_raw.png')
# intro_frlg/game_freak/presents : PRESENTE officiel (Rouge Feu FR, LZ77 0xEAFCD0)
rf = open('roms/Pokemon - Version Rouge Feu (France).gba', 'rb').read()
save_like(U + 'intro_frlg/game_freak/presents.png', from4bpp(lz77(rf, 0xEAFCD0), 8), O + '/presents.png')
# pokenav/region_map/zoom_tiles : légende CENTRE POKéMON / BOUTIQUE
a = load(U + 'pokenav/region_map/zoom_tiles.png').copy(); a[48:56, 8:64] = 0; a[56:63, 8:64] = 0
P.draw(a, 8, 49, 'CENTRE POKéMON', 3); P.draw(a, 8, 57, 'BOUTIQUE', 5); save_like(U + 'pokenav/region_map/zoom_tiles.png', a, O + '/zoom_tiles.png')
# pokedex/hgss/tilemap_search_screen_hoenn.bin : lignes 10-13 remises comme l'original (bouton OK)
h = bytearray(open(I + 'pokedex/hgss/tilemap_search_screen_hoenn.bin', 'rb').read()); oh = open(U + 'pokedex/hgss/tilemap_search_screen_hoenn.bin', 'rb').read()
h[640:896] = oh[640:896]; open(O + '/tilemap_search_screen_hoenn.bin', 'wb').write(h)
# battle_interface/status*.png et summary_screen/tiles.png : identiques au pixel à hns/ -> copie des versions FR hns
