"""Vignettes avant/après (×3) du 2e lot d'images (rapport/images/)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pnglike import *; from dexgfx import load_tiles, read_bin, compose
from spr1d import get
import numpy as np
U = 'build/upstream_orig/'; I = 'images/'; R = 'rapport/images/'
def name(p): return R + p.replace('/', '__') + ('' if p.endswith('.png') else '.png')
def jasc(p):
    L = open(p).read().split('\n')[3:]; return [tuple(int(v) for v in l.split()) for l in L if l.strip()]
def simple(p):
    vignette(load(U + p), load(I + p), palette(U + p), palette(I + p), name(p))
def screen(png_b, bin_b, png_a, bin_a, pal, cols=32, crop=None):
    _, tb = load_tiles(png_b); _, ta = load_tiles(png_a)
    B = compose(tb, read_bin(bin_b), cols); A = compose(ta, read_bin(bin_a), cols)
    if crop: y0, y1, x0, x1 = crop; B = B[y0:y1, x0:x1]; A = A[y0:y1, x0:x1]
    return B, A
for p in ['graphics/battle_interface/status.png', 'graphics/battle_interface/status2.png', 'graphics/battle_interface/status3.png',
          'graphics/battle_interface/status4.png', 'graphics/summary_screen/tiles.png', 'graphics/summary_screen/iv_ev_tiles.png',
          'graphics/battle_interface/move_info_window_l.png', 'graphics/battle_interface/move_info_window_r.png',
          'graphics/link/321start_static.png', 'graphics/roulette/credit.png', 'graphics/roulette/window.png',
          'graphics/voltorb_flip/Raw/gameboard.png', 'graphics/misc/japanese_hof.png', 'graphics/misc/japanese_hof_hns.png',
          'graphics/misc/hall_of_fame.png', 'graphics/pokenav/region_map/zoom_tiles.png', 'graphics/contest/japanese/letters.png',
          'graphics/contest/japanese/numbers.png', 'graphics/contest/japanese/interface.png', 'graphics/contest/japanese/voltage.png',
          'graphics/intro_frlg/game_freak/presents.png', 'graphics/pokedex/hgss/tileset_menu2.png',
          'graphics/pokedex/hgss/tileset_menu3.png']:
    simple(p)
# tileset_menu1 : la vignette existante (rendus d'écrans) est gardée ; planche avant/après dans un fichier à part
p = 'graphics/pokedex/hgss/tileset_menu1.png'
vignette(load(U + p), load(I + p), palette(U + p), palette(I + p), name(p).replace('.png', '.orphelines.png'))
# sprites de l'interface du Pokédex HGSS (feuille 1D de 4 tuiles de large) : RECH./MENU/VUS/PRIS/HOENN-JOHTO/NATIONAL
def sprites(a):
    parts = [get(a, 40, 4, 2), get(a, 56, 4, 2), get(a, 64, 8, 4), get(a, 96, 8, 4), get(a, 160, 4, 2), get(a, 168, 4, 2)]
    row = np.zeros((32, sum(p.shape[1] + 4 for p in parts)), np.uint8); x = 0
    for p in parts: row[:p.shape[0], x:x + p.shape[1]] = p; x += p.shape[1] + 4
    return row
for n in ['tileset_interface', 'tileset_interface_DECA', 'tileset_interface_DECA_hns']:
    p = 'graphics/pokedex/hgss/%s.png' % n; pal = palette(U + p); pal = [(96, 96, 96)] + pal[1:]
    vignette(sprites(load(U + p)), sprites(load(I + p)), pal, pal, name(p))
H = 'graphics/pokedex/hgss/'
pal = jasc(U + H + 'palette_default.pal')
Bs = []; As = []
for b in ['tilemap_start_menu_search_results', 'tilemap_list_screen']:
    B, A = screen(U + H + 'tileset_menu_list_DECA.png', U + H + b + '.bin', I + H + 'tileset_menu_list_DECA.png', I + H + b + '.bin', pal)
    Bs.append(B); As.append(A)
vignette(np.vstack(Bs), np.vstack(As), pal, pal, name(H + 'tileset_menu_list_DECA.png'))
pal = jasc(U + H + 'palette_search_menu.pal'); Bs = []; As = []
for b in ['tilemap_search_screen_national', 'tilemap_search_screen_hoenn']:
    B, A = screen(U + H + 'tileset_menu_search_DECA.png', U + H + b + '.bin', I + H + 'tileset_menu_search_DECA.png', I + H + b + '.bin', pal, crop=(0, 120, 0, 136))
    Bs.append(B); As.append(A)
vignette(np.vstack(Bs), np.vstack(As), pal, pal, name(H + 'tileset_menu_search_DECA.png'))
# écran Hoenn de la recherche (FR non-DECA) : avant = version FR précédente (git HEAD), après = corrigée
import subprocess, tempfile
TMP = tempfile.mkdtemp()
old = subprocess.run(['git', 'show', 'HEAD:images/' + H + 'tilemap_search_screen_hoenn.bin'], capture_output=True).stdout
oldts = subprocess.run(['git', 'show', 'HEAD:images/' + H + 'tileset_menu_search.png'], capture_output=True).stdout
open(TMP + '/old_hoenn.bin', 'wb').write(old); open(TMP + '/old_ts.png', 'wb').write(oldts)
B, A = screen(TMP + '/old_ts.png', TMP + '/old_hoenn.bin', I + H + 'tileset_menu_search.png', I + H + 'tilemap_search_screen_hoenn.bin', pal, crop=(0, 120, 0, 136))
vignette(B, A, pal, pal, name(H + 'tilemap_search_screen_hoenn.bin'))
# fin des crédits RFVF
p = 'graphics/credits_frlg/the_end'
pal = palette(U + p + '.png')
B, A = screen(U + p + '.png', U + p + '.bin', I + p + '.png', I + p + '.bin', pal, crop=(56, 96, 0, 240))
vignette(B, A, pal, pal, name(p + '.png'))
# DexNav
p = 'graphics/dexnav/gui_tiles'
pal = jasc(U + 'graphics/dexnav/gui.pal')
B, A = screen(U + p + '.png', U + 'graphics/dexnav/gui_tilemap.bin', I + p + '.png', I + 'graphics/dexnav/gui_tilemap.bin', pal, crop=(0, 160, 0, 240))
vignette(B, A, pal, pal, name(p + '.png'))
print('ok')
