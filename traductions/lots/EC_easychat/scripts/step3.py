import pickle, collections, struct, bisect, sys
from eclib import *
import vocab as VV
us, fr, sym = VV.us, VV.fr, VV.sym
gs = pickle.load(open('groups.pkl', 'rb'))
_, TUS = VV.tables(us); _, TFR = VV.tables(fr)
E = Consts(PE)
def valid(w):
    if w == 0xFFFF: return True
    g, i = w >> 9, w & 511
    if g >= 22: return False
    kind, _, lst = TFR[g]
    return (i in lst) if kind == 'list' else i < len(lst)
def word_fr(w):
    if w == 0xFFFF: return '_'
    g, i = w >> 9, w & 511
    kind, _, lst = TFR[g]
    if kind == 'words': return lst[i][1]
    return '<%s:%s>' % (GROUPS[g], E.name(w))
# deltas
from step2 import anchors_around
DELTA = {}
def delta(symaddr):
    if symaddr in DELTA: return DELTA[symaddr]
    an = anchors_around(symaddr)
    b = [x[1] for x in an if x[0] <= symaddr][-2:]; a = [x[1] for x in an if x[0] > symaddr][:2]
    DELTA[symaddr] = (b, a); return DELTA[symaddr]
PREF = {'src/battle_tower.c': 'sRecordTrainer', 'src/easy_chat.c': 'sDefault|sBerry|sMystery'}
import re
out = []
for g in gs:
    if not g['us']: g['fr'] = None; continue
    hits = g['us']
    if len(hits) > 1:
        if g['file'] in PREF:
            hits = [h for h in hits if re.match(PREF[g['file']], sym.at(h)[0])]
        g['ambig'] = True
    g['hits_kept'] = hits
    h = hits[0]
    name, off, sz, sa = sym.at(h)
    b, a = delta(sa)
    d = b[-1] if b else a[0]
    g['sym'] = name; g['symoff'] = off; g['delta_ok'] = bool(b and a and b[-1] == a[0]); g['d'] = d
    n = len(g['toks'])
    fw = list(struct.unpack('<%dH' % n, fr[h + d:h + d + 2*n]))
    g['fr'] = fw; g['fr_valid'] = all(valid(w) for w in fw)
    g['fr_addr'] = h + d
pickle.dump(gs, open('groups3.pkl', 'wb'))
c = collections.Counter((g['file'], g.get('sym','-') if g['fr'] else 'none', g['fr_valid'] if g['fr'] else None, g.get('delta_ok')) for g in gs)
for k, v in sorted(c.items(), key=str): print(v, k)
