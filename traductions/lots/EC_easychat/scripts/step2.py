import pickle, collections, struct, bisect
from eclib import *
us = open(P + '/memoires/emeraude_us.gba', 'rb').read()
fr = open(P + '/memoires/em_fr.gba', 'rb').read()
sym = Sym(PE + '/pokeemerald.nm')
if __name__ == '__main__':
  gs = pickle.load(open('groups.pkl', 'rb'))
  targets = sorted(set(sym.at(g['us'][0])[3] for g in gs if g['us']) | set(sym.at(h)[3] for g in gs if g['us'] for h in g['us']))
# anchors: every symbol (any) of size>=24 in rodata/text: first 24 bytes unique in US and in FR
def anchors_around(addr, span=0x4000):
    out = []
    i0 = bisect.bisect_left(sym.a, addr + 0x08000000 - span); i1 = bisect.bisect_right(sym.a, addr + 0x08000000 + span)
    for i in range(i0, i1):
        a = sym.a[i] - 0x08000000; sz = sym.sz[i]
        if sz < 24: continue
        b = us[a:a+24]
        if len(set(b)) < 6: continue
        if us.count(b) != 1: continue
        j = fr.find(b)
        if j < 0 or fr.find(b, j + 1) >= 0: continue
        out.append((a, j - a, sym.n[i]))
    return out
if __name__ == "__main__":
    res = {}
    for t in targets:
        name = sym.at(t)[0]
        an = anchors_around(t)
        before = [x for x in an if x[0] <= t][-3:]; after = [x for x in an if x[0] > t][:3]
        print('%-34s US %07X  before %s  after %s' % (name, t, [(x[2], x[1]) for x in before], [(x[2], x[1]) for x in after]))
    