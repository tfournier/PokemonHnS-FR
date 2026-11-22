import pickle, struct, re, collections, difflib, os, sys, csv
from eclib import *
import vocab as VV
from povocab import vocab as povocab
from manuel import MANUEL
import frlgvocab as FL
X = Consts(UP); E = Consts(PE)
us, fr, sym = VV.us, VV.fr, VV.sym
frl = FL.frl; pfr = FL.rom
_, TU = VV.tables(us); _, TF = VV.tables(fr); TL = FL.table(FL.hits[0])
PO = povocab()
# names (Emerald internal species / moves)
def names(rom, a, size, n):
    out = []
    for i in range(n):
        b = rom[a + size*i:a + size*(i+1)]; e = b.find(b'\xff'); out.append(VV.G.decode(b[:e if e >= 0 else size], ''))
    return out
sa, _ = sym.addr('gSpeciesNames'); ma, _ = sym.addr('gMoveNames')
SP_US = names(us, sa, 11, 412); SP_FR = names(fr, sa + 31536, 11, 412)
MV_US = names(us, ma, 13, 355); MV_FR = names(fr, ma + 31536, 13, 355)
def dec(vals, T, SP, MV, po=False):
    out = []
    for w in vals:
        if w == 0xFFFF: continue
        g, i = w >> 9, w & 511
        if g in (0, 21): out.append(SP[i])
        elif g in (18, 19): out.append(MV[i])
        elif po:
            v = PO.get((g, i)); out.append((v[1] or ('[%s]' % v[0])) if v else '??')
        else: out.append(T[g][2][i][1])
    return ' '.join(out)
def valid_in(T, w):
    if w == 0xFFFF: return True
    g, i = w >> 9, w & 511
    if g >= 22: return False
    return (i in T[g][2]) if T[g][0] == 'list' else i < len(T[g][2])
def to_token(w, empty):
    """Emerald-numbered value -> expansion token, checked"""
    if w == 0xFFFF: return empty
    g, i = w >> 9, w & 511
    if g in (18, 19):
        n = E.rmoves[i]
        if X.moves.get(n) != i: n = X.rmoves[i]
        assert X.moves[n] == i <= 354
        return 'EC_MOVE%s(%s)' % ('' if g == 18 else '2', n[5:])
    if g in (0, 21):
        n = E.rspecies[i]; assert n in X.species, n
        return 'EC_POKEMON%s(%s)' % ('' if g == 0 else '_NATIONAL', n[8:])
    n = E.rwords[w]; assert X.words[n] == w, n
    return n
def manual_value(t):
    if t == '_': return 0xFFFF
    if '(' in t: return E.value('EC_' + t)
    return E.words['EC_WORD_' + t]
gs = pickle.load(open('groups4.pkl', 'rb'))
tt = {g['line']: g for g in pickle.load(open('tt2.pkl', 'rb'))}
# trainer tower: resolve repeated hits in sequence inside the floor
prev = None
for g in pickle.load(open('tt2.pkl', 'rb')):
    pass
rows = []; repl = collections.defaultdict(dict)   # file -> {start: (end, newtok)}
stat = collections.Counter(); tstat = collections.defaultdict(collections.Counter)
prev_tt = None
for g in gs:
    f = g['file']; toks = g['toks']; n = len(toks)
    emptystyle = next((t for t in toks if t in ('-1', '0xFFFF')), 'EC_EMPTY_WORD')
    xv = [X.value(t) for t in toks]
    en_vals = [E.value(t) for t in toks]
    src = None; T = TF; frv = None; ctx = ''
    if f == 'src/trainer_tower_sets.c':
        t = tt[g['line']]
        hits = [h for h in t['pfr_hits'] if FL.Sym('pfr.nm').at(h)[0] == t['tt_sym']] if False else t['pfr_hits']
        floor_hits = [h for h in hits if prev_tt is None or h > prev_tt] or hits
        h = min(floor_hits) if len(hits) > 1 else hits[0]
        prev_tt = h
        frv = list(struct.unpack('<%dH' % n, frl[h - 34860:h - 34860 + 2*n]))
        T = TL; src = 'officiel Rouge Feu FR @%07X' % (h - 34860); ctx = t['tt_sym']
        # Rouge Feu FR et Émeraude FR n'ont pas le même mot à STATUS 0 / STATUS 14 : on garde le sens
        REMAP = {(2 << 9) | 14: E.words['EC_WORD_AWFUL'], (2 << 9) | 0: (2 << 9) | 14}
        if any(w in REMAP for w in frv): src += ' (mot adapté au vocabulaire Émeraude)'
        frv = [REMAP.get(w, w) for w in frv]
        if all(w == 0xFFFF for w in frv):
            rows.append(dict(file=f, line=g['line'], source='NON TRAITÉ : étage inutilisé (%s), vide dans Rouge Feu FR' % ctx, en=dec(en_vals, TU, SP_US, MV_US), fr_off='', fr_po='', old_fr_po='', tokens=''))
            stat['non traité (étage mort)'] += 1; tstat[f]['non traité (étage mort)'] += 1; continue
        en_dec = dec(en_vals, TU, SP_US, MV_US)
    elif (f, g['line']) in MANUEL:
        frv = [manual_value(x) for x in MANUEL[(f, g['line'])]]; assert len(frv) == n, (f, g['line'])
        src = 'composé (HnS)'; en_dec = dec(en_vals, TU, SP_US, MV_US) if None not in en_vals else ' '.join(toks)
    elif g.get('fr') is not None:
        frv = g['fr']; src = 'officiel Émeraude FR @%07X (%s+%d)' % (g['fr_addr'], g['sym'], g['symoff']); ctx = g['sym']
        en_dec = dec(en_vals, TU, SP_US, MV_US)
    else:
        rows.append(dict(file=f, line=g['line'], source='NON TRAITÉ', en=' '.join(toks), fr_off='', fr_po='', old_fr_po='', tokens=''))
        stat['non traité'] += 1; tstat[f]['non traité'] += 1; continue
    assert all(valid_in(T, w) or valid_in(TF, w) or (src.startswith('compos') and w >> 9 in (0, 21)) for w in frv), (f, g['line'])
    newtoks = [to_token(w, emptystyle) for w in frv]
    # check Emerald-FR vocabulary decode (that's what HnS will show) and FRLG one for the tower
    fr_off = dec(frv, T, SP_FR, MV_FR); fr_em = dec(frv, TF, SP_FR, MV_FR)
    fr_po = dec(frv, None, SP_FR, MV_FR, po=True)
    old = dec([v for v in xv], None, SP_FR, MV_FR, po=True) if all(v >> 9 not in (0, 21) for v in xv if v != 0xFFFF) else ''
    changed = newtoks != toks and [X.value(t) for t in newtoks] != xv
    kind = src.split()[0]
    stat[kind + (' modifié' if changed else ' identique')] += 1; tstat[f][kind + (' modifié' if changed else ' identique')] += 1
    if changed:
        for (s, e, t), nt in zip(g['items'], newtoks): repl[f][s] = (e, nt)
    rows.append(dict(file=f, line=g['line'], source=src, en=en_dec, fr_off=fr_off if fr_off == fr_em else fr_off + '  [vocab. Émeraude : ' + fr_em + ']', fr_po=fr_po, old_fr_po=old, tokens=', '.join(newtoks)))
# Quiz Lady answers
qa = sym.addr('sQuizLadyQuizAnswers')[0]
lines = open(UP + '/src/data/lilycove_lady.h').read().split('\n')
txt = open(UP + '/src/data/lilycove_lady.h').read()
for k in range(16):
    af = struct.unpack('<H', fr[qa + 17288 + 2*k:qa + 17288 + 2*k + 2])[0]
    m = list(re.finditer(r'\.answer = (EC_WORD_[A-Z0-9_]+)', txt))[k]
    old = m.group(1); new = to_token(af, None)
    ln = txt.count('\n', 0, m.start()) + 1
    ch = new != old
    stat['réponse quiz ' + ('modifiée' if ch else 'identique')] += 1
    if ch: repl['src/data/lilycove_lady.h'][m.start(1)] = (m.end(1), new)
    rows.append(dict(file='src/data/lilycove_lady.h', line=ln, source='officiel Émeraude FR @%07X (sQuizLadyQuizAnswers+%d)' % (qa + 17288 + 2*k, 2*k), en=dec([E.words[old]], TU, SP_US, MV_US), fr_off=dec([af], TF, SP_FR, MV_FR), fr_po=dec([af], None, SP_FR, MV_FR, po=True), old_fr_po=dec([E.words[old]], None, SP_FR, MV_FR, po=True), tokens=new))
# patch
patch = []
for f in sorted(repl):
    orig = open(UP + '/' + f, encoding='utf-8').read(); new = orig
    for s in sorted(repl[f], reverse=True):
        e, nt = repl[f][s]; new = new[:s] + nt + new[e:]
    assert orig.count('\n') == new.count('\n')
    a = orig.splitlines(keepends=True); b = new.splitlines(keepends=True)
    d = list(difflib.unified_diff(a, b, 'a/' + f, 'b/' + f, n=3))
    patch.append('diff --git a/%s b/%s\n' % (f, f) + ''.join(d))
open(P + '/code/easy-chat-fr.patch', 'w', encoding='utf-8').write(''.join(patch))
with open('tables.tsv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=['file', 'line', 'source', 'en', 'fr_off', 'fr_po', 'old_fr_po', 'tokens'], delimiter='\t')
    w.writeheader(); [w.writerow(r) for r in rows]
pickle.dump(rows, open('rows.pkl', 'wb'))
for k, v in sorted(stat.items()): print(v, k)
for f in tstat: print(f, dict(tstat[f]))
