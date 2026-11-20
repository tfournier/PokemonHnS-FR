"""Outils communs du lot F (alignement Rouge Feu US <-> Rouge Feu FR).

La ROM US (BPRE 1.0) est reconstruite depuis pret/pokefirered dans build/pokefirered (jamais committé) :
  git clone pret/agbcc + pret/pokefirered ; agbcc/build.sh ; install.sh ../pokefirered ; make
La ROM FR est roms/Pokemon - Version Rouge Feu (France).gba (BPRF).
"""
import os, sys, re, glob

P = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(P, 'outils'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen3 import Gen3  # noqa: E402

ROOT = os.path.join(P, 'build', 'upstream_orig')
PFR = os.path.join(P, 'build', 'pokefirered')
LOT = os.path.join(P, 'traductions', 'lots', 'F_frlg')
TMP = os.path.join(P, 'build', 'lotF')   # dérivés des ROM (37 Mo) : dans build/, ignoré par git
ROM_US = os.path.join(PFR, 'pokefirered.gba')
ROM_FR = os.path.join(P, 'roms', 'Pokemon - Version Rouge Feu (France).gba')
ROM_VF = os.path.join(P, 'roms', 'Pokemon - Version Vert Feuille (France).gba')
ROM_US_LG = os.path.join(PFR, 'pokeleafgreen.gba')
G = Gen3(ROOT)
# version traitée : FRLG_VER=fr (Rouge Feu, défaut) ou lg (Vert Feuille : make leafgreen dans build/pokefirered)
VER = os.environ.get('FRLG_VER', 'fr')
SUF = '' if VER == 'fr' else '_lg'


def roms():
    if VER == 'lg':
        return open(ROM_US_LG, 'rb').read(), open(ROM_VF, 'rb').read()
    return open(ROM_US, 'rb').read(), open(ROM_FR, 'rb').read()


def symboles():
    """{nom: adresse ROM (décalage)} depuis build/pokefirered/syms.txt (arm-none-eabi-nm -n pokefirered.elf ;
    syms_lg.txt pour pokeleafgreen.elf)."""
    out = {}
    for l in open(os.path.join(PFR, 'syms%s.txt' % SUF)):
        p = l.split()
        if len(p) == 3 and p[0].startswith('08'):
            out[p[2]] = int(p[0], 16) - 0x08000000
    return out


def lire(rom, a, lim=4000):
    e = rom.find(b'\xff', a, a + lim)
    return rom[a:e] if e >= 0 else None
