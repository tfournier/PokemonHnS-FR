import pickle, struct, collections
from eclib import *
E = Consts(PE)
rom = open(PF + '/pokefirered.gba', 'rb').read()
sym = Sym('pfr.nm')
gs = [g for g in pickle.load(open('groups4.pkl', 'rb')) if g['file'] == 'src/trainer_tower_sets.c']
c = collections.Counter(); prev = None
for g in gs:
    ev = [E.value(t) for t in g['toks']]
    if None in ev: print('noval', g['line'], g['toks']); continue
    b = struct.pack('<%dH' % len(ev), *ev); hits = []; i = rom.find(b)
    while i >= 0:
        if i % 2 == 0: hits.append(i)
        i = rom.find(b, i + 1)
    g['pfr_hits'] = hits
    c[(len(hits), sym.at(hits[0])[0] if hits else None)] += 1
print(c)
pickle.dump(gs, open('tt1.pkl', 'wb'))
