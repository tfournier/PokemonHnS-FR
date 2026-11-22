import re, struct, sys
sys.path.insert(0, '/Users/tfournier/projets/github.com/tfournier/PokemonHnS-FR/outils')
from eclib import *
from gen3 import Gen3
us = open(P + '/memoires/emeraude_us.gba', 'rb').read()
fr = open(P + '/memoires/em_fr.gba', 'rb').read()
sym = Sym(PE + '/pokeemerald.nm')
G = Gen3(UP)
def find_groups(rom):
    a, _ = sym.addr('gEasyChatGroups')
    pat = b''.join(re.escape(b'') + b'(?:.{3}[\x08\x09])' + re.escape(us[a+8*i+4:a+8*i+8]) for i in range(22))
    hits = [m.start() for m in re.finditer(pat, rom, re.S)]
    return hits
def rd(rom, o, n=4): return int.from_bytes(rom[o:o+n], 'little')
def text(rom, p):
    e = rom.index(b'\xff', p); return G.decode(rom[p:e], '')
def tables(rom):
    base = find_groups(rom); assert len(base) == 1, base; base = base[0]
    T = {}
    for g in range(22):
        ptr = rd(rom, base + 8*g) - 0x08000000; n = rd(rom, base + 8*g + 4, 2)
        if g in (0, 18, 19, 21):
            T[g] = ('list', ptr, [rd(rom, ptr + 2*i, 2) for i in range(n)])
        else:
            T[g] = ('words', ptr, [(ptr + 12*i, text(rom, rd(rom, ptr + 12*i) - 0x08000000)) for i in range(n)])
    return base, T
if __name__ == '__main__':
    for name, rom in (('US', us), ('FR', fr)):
        base, T = tables(rom)
        print(name, 'gEasyChatGroups @%07X' % base)
        for g, i in ((8, 32), (5, 1)):
            ent = T[g][2][i]; p = rd(rom, ent[0]) - 0x08000000
            print('   group %s idx %d: entry @%07X text @%07X : %r' % (GROUPS[g], i, ent[0], p, ent[1]))
