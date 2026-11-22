import struct, collections, pickle
from eclib import *
X = Consts(UP); E = Consts(PE)
us = open(P + '/memoires/emeraude_us.gba', 'rb').read()
sym = Sym(PE + '/pokeemerald.nm')
FILES = ['src/data/battle_frontier/battle_frontier_trainers.h', 'src/data/battle_frontier/battle_tent.h',
 'src/data/battle_frontier/trainer_hill.h', 'src/data/battle_frontier/apprentice.h', 'src/data/trade.h',
 'src/data/lilycove_lady.h', 'src/mauville_old_man.c', 'src/battle_tower.c', 'src/battle_pike.c',
 'src/easy_chat.c', 'src/scrcmd.c', 'src/ereader_helpers.c', 'src/trainer_tower_sets.c']
res = []
for f in FILES:
    txt, gs = parse_groups(UP + '/' + f)
    stat = collections.Counter(); syms = collections.Counter()
    for g in gs:
        toks = [t for _, _, t in g['items']]
        xv = [X.value(t) for t in toks]
        assert None not in xv, (f, g['line'], toks)
        ev = [E.value(t) for t in toks]
        g['file'] = f; g['toks'] = toks
        if None in ev:
            g['us'] = None; stat['nonEM'] += 1
        else:
            b = struct.pack('<%dH' % len(ev), *ev)
            hits = []; i = us.find(b)
            while i >= 0:
                if i % 2 == 0: hits.append(i)
                i = us.find(b, i + 1)
            g['us'] = hits
            if not hits: stat['notfound'] += 1
            elif len(hits) == 1: stat['unique'] += 1; syms[sym.at(hits[0])[0]] += 1
            else: stat['multi'] += 1; syms['multi:' + ','.join(sym.at(h)[0] for h in hits[:3])] += 1
        res.append(g)
    print(f, len(gs), dict(stat)); print('   ', dict(syms))
pickle.dump(res, open('groups.pkl', 'wb'))
