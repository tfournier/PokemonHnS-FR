import pickle, struct, re, collections
from eclib import *
import vocab as VV
from povocab import po_entries
us, fr, sym = VV.us, VV.fr, VV.sym
gs = pickle.load(open('groups3.pkl', 'rb'))
pe = po_entries()
# resolve multi-hits by sequence
byfile = collections.defaultdict(list)
for g in gs: byfile[g['file']].append(g)
for f, L in byfile.items():
    prev = None
    for g in L:
        if not g.get('hits_kept'): continue
        if len(g['hits_kept']) > 1 and prev is not None:
            cand = [h for h in g['hits_kept'] if h > prev]
            h = min(cand) if cand else g['hits_kept'][0]
            if h != g['hits_kept'][0]:
                g['fr'] = list(struct.unpack('<%dH' % len(g['toks']), fr[h + g['d']:h + g['d'] + 2*len(g['toks'])]))
                g['fr_addr'] = h + g['d']; g['sym'], g['symoff'] = sym.at(h)[:2]
            g['us_hit'] = h
        else:
            g['us_hit'] = g['hits_kept'][0]
        prev = g['us_hit']
# structural check: frontier + tents: names
def name_at(rom, o, n=8):
    b = rom[o:o+n]; e = b.find(b'\xff'); return VV.G.decode(b[:e if e >= 0 else n], '')
lines = {}
for f in ['src/data/battle_frontier/battle_frontier_trainers.h', 'src/data/battle_frontier/battle_tent.h', 'src/data/battle_frontier/trainer_hill.h', 'src/data/battle_frontier/apprentice.h']:
    for i, l in enumerate(open(UP + '/' + f), 1):
        m = re.search(r'\.(?:trainerName|name) = _\("(.*)"\)', l)
        if m: lines[(f, i)] = m.group(1)
bad = 0; checked = 0
for g in gs:
    if g['file'] not in ('src/data/battle_frontier/battle_frontier_trainers.h', 'src/data/battle_frontier/battle_tent.h') or not g.get('us_hit') or g['sym'] not in ('gBattleFrontierTrainers','gSlateportBattleTentTrainers','gVerdanturfBattleTentTrainers','gFallarborBattleTentTrainers'): continue
    sa = sym.addr(g['sym'])[0]; off = g['us_hit'] - sa
    idx, fo = divmod(off, 52); k = (fo - 12) // 12
    # find source trainer name preceding the group
    ln = max(l for (f, l) in lines if f == g['file'] and l < g['line'])
    en_src = lines[(g['file'], ln)]
    en_rom = name_at(us, sa + idx*52 + 4); fr_rom = name_at(fr, sa + g['d'] + idx*52 + 4)
    e = pe.get((g['file'], ln)); fr_po = e.msgstr if e else None
    checked += 1
    ok = en_src.upper() == en_rom.upper() and (fr_po is None or fr_po.upper() == fr_rom.upper())
    if not ok:
        bad += 1
        if bad < 25: print(g['file'], g['line'], g['sym'], idx, k, en_src, en_rom, fr_po, fr_rom)
    g['en_name'] = en_src; g['fr_name'] = fr_rom
print('checked', checked, 'bad', bad)
pickle.dump(gs, open('groups4.pkl', 'wb'))
