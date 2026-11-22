import pickle, struct, collections, bisect, re
from eclib import *
rom = open(PF + '/pokefirered.gba', 'rb').read()
fr = open(P + '/roms/Pokemon - Version Rouge Feu (France).gba', 'rb').read()
print(fr[0xA0:0xB0])
sym = Sym('pfr.nm')
gs = pickle.load(open('tt1.pkl', 'rb'))
src = open(UP + '/src/trainer_tower_sets.c').read().split('\n')
def anchors_around(addr, span=0x6000):
    out = []
    i0 = bisect.bisect_left(sym.a, addr + 0x08000000 - span); i1 = bisect.bisect_right(sym.a, addr + 0x08000000 + span)
    for i in range(i0, i1):
        a = sym.a[i] - 0x08000000; sz = sym.sz[i]
        if sz < 24: continue
        b = rom[a:a+24]
        if len(set(b)) < 6 or rom.count(b) != 1: continue
        j = fr.find(b)
        if j < 0 or fr.find(b, j + 1) >= 0: continue
        out.append((a, j - a, sym.n[i]))
    return out
prev = None; mism = 0; D = {}
for g in gs:
    floor = [l for l in src[:g['line']] if l.startswith('static const struct TrainerTowerFloor')][-1].split()[4]
    hits = g['pfr_hits']
    if len(hits) > 1:
        cand = [h for h in hits if sym.at(h)[0] == floor]; hits = cand or hits
    h = hits[0]
    name, off, sz, sa = sym.at(h)
    if name != floor: mism += 1; print('floor mismatch', g['line'], floor, name)
    if sa not in D:
        an = anchors_around(sa)
        D[sa] = ([x[1] for x in an if x[0] <= sa][-2:], [x[1] for x in an if x[0] > sa][:2])
    b, a = D[sa]
    g["tt_sym"] = name; g["tt_d"] = -34860; g['tt_dok'] = bool(b and a and b[-1] == a[0])
    g['tt_hit'] = h
print('mism', mism)
print(collections.Counter((tuple(v[0]), tuple(v[1])) for v in D.values()))
pickle.dump(gs, open('tt2.pkl', 'wb'))
