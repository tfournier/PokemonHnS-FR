#!/usr/bin/env python3
"""Amorçage des fichiers .po (à lancer une seule fois, ou pour une nouvelle version).

Sources, par ordre de priorité :
  1. Pokémon Émeraude FR officiel  (moteur : menus, combats…)        -> traduit
  2. Pokémon SoulSilver FR officiel (dialogues de Johto/Kanto)         -> traduit
  3. Patch FR actuel de Heart & Soul (texte relu à la main par son auteur) -> traduit
  4. SoulSilver, correspondance approchée                              -> « fuzzy » (à relire)

Usage : amorcer.py <source_upstream> <memoires/> <sortie traductions/>
  memoires/ doit contenir : hns_en.gba (ROM anglaise officielle), hns_fr_patch.gba (ROM avec le
  patch FR actuel), patch_fr.bps (ce patch), tm_em_bytes.pkl, tm_ss_pairs.pkl
"""
import sys, os, re, pickle, collections, unicodedata, struct
sys.path.insert(0, os.path.dirname(__file__))
from gen3 import Gen3
import hnsfr
import polib

root, mem, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
g = Gen3(root)
MAXW = 198

# ------------------------------------------------------------------ helpers
def norm(s):
    s = re.sub(r'\{[^}]*\}', ' ', s)
    s = re.sub(r'\\[nlprf]', ' ', s).replace('\n', ' ').replace('\r', ' ').replace('\x0c', ' ')
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()

def textlike(s):
    t = re.sub(r'\{[^}]*\}|\\[nlp]', '', s or '')
    return len(re.findall(r'[A-Za-zÀ-ÿ]', t)) >= 2

def is_dialogue_like(msgid):
    return bool(re.search(r'\\[nlp]', msgid)) or g.largeur(msgid) > MAXW

# ------------------------------------------------------------------ load
pot = hnsfr.scan(root)
occ_by_id = collections.defaultdict(list)
for o in pot:
    if hnsfr.wanted(o.text): occ_by_id[o.text].append(o)
msgids = list(occ_by_id)
print('textes', len(msgids))

en = open(os.path.join(mem, 'hns_en.gba'), 'rb').read()
fr = open(os.path.join(mem, 'hns_fr_patch.gba'), 'rb').read()

# bytes changed by the current FR patch
def bps_changed(path, size):
    d = open(path, 'rb').read()
    def rd(i):
        v = 0; s = 1
        while True:
            x = d[i]; i += 1; v += (x & 0x7f) * s
            if x & 0x80: return v, i
            s <<= 7; v += s
    i = 4; _, i = rd(i); _, i = rd(i); ml, i = rd(i); i += ml
    K = bytearray(size); out = 0; end = len(d) - 12
    while i < end:
        v, i = rd(i); cmd, ln = v & 3, (v >> 2) + 1
        if cmd == 1:
            K[out:out+ln] = b'\x01' * ln; i += ln
        elif cmd in (2, 3):
            _, i = rd(i)
        out += ln
    return K
K = bps_changed(os.path.join(mem, 'patch_fr.bps'), len(fr))

# ------------------------------------------------------------------ 3. current FR patch
import ahocorasick
A = ahocorasick.Automaton(); enc = {}
for m in msgids:
    b = g.encode(m)
    if b and len(b) >= 2:
        enc[m] = b
        A.add_word((b + b'\xff').decode('latin1'), m)
A.make_automaton()
addrs = collections.defaultdict(list)
for endpos, m in A.iter(en.decode('latin1')):
    a = endpos - len(enc[m])
    if a == 0 or en[a-1] in (0xFF, 0x00) or a % 4 == 0:
        addrs[m].append(a)
targets = {a for v in addrs.values() for a in v}
ptrs = collections.defaultdict(list)
for p in range(len(en) - 3):
    if en[p+3] not in (0x08, 0x09): continue
    v = struct.unpack_from('<I', en, p)[0] - 0x08000000
    if v in targets: ptrs[v].append(p)

def fr_at(t):
    e = fr.find(b'\xff', t, t + 2000)
    return fr[t:e] if e > 0 else None

fan, fan_doute = {}, {}
for m, al in addrs.items():
    votes = collections.Counter()
    for a in al:
        hit = False
        for p in ptrs.get(a, []):
            v = struct.unpack_from('<I', fr, p)[0]
            if 0x08000000 <= v < 0x0A000000:
                b = fr_at(v - 0x08000000)
                if b is not None: votes[b] += 1; hit = True
        if not hit and any(K[a:a+len(enc[m])+1]):
            b = fr_at(a)
            if b is not None: votes[b] += 1
    if not votes: continue
    best, n = votes.most_common(1)[0]
    t = g.decode(best, m)
    if not (t and textlike(t)) or norm(t) == norm(m): continue
    # sanity: a one-word label that becomes a sentence is a wrong pointer
    words_en = len(re.findall(r"[A-Za-z]+", re.sub(r'\{[^}]*\}', '', m)))
    words_fr = len(re.findall(r"[A-Za-zÀ-ÿ]+", re.sub(r'\{[^}]*\}', '', t)))
    suspicious = (words_en <= 2 and words_fr >= words_en + 3) or len(t) > 3 * len(m) + 10
    if n < 0.6 * sum(votes.values()) or suspicious:
        fan_doute[m] = t
    else:
        fan[m] = t
print('patch FR actuel :', len(fan), ' douteux :', len(fan_doute))

# ------------------------------------------------------------------ 1. Emerald FR
tm_em = pickle.load(open(os.path.join(mem, 'tm_em_bytes.pkl'), 'rb'))
em = {}
for m, b in enc.items():
    f = tm_em.get(b)
    if f:
        t = g.decode(f, m)
        if t and textlike(t): em[m] = t
print('Émeraude FR :', len(em))

# ------------------------------------------------------------------ 2. SoulSilver FR
pairs = pickle.load(open(os.path.join(mem, 'tm_ss_pairs.pkl'), 'rb'))
ss_votes = collections.defaultdict(collections.Counter); ss_en = {}
for b_, i_, e_, f_ in pairs:
    if not re.search('[A-Za-z]{3}', e_) or b_ == 802: continue
    n = norm(e_)
    if len(n) >= 4:
        ss_votes[n][f_] += 1; ss_en.setdefault(n, e_)
PRIO = {222, 237, 750, 720, 279, 730, 735}   # banques de noms officielles : prioritaires
ss_prio = {}
for b_, i_, e_, f_ in pairs:
    if b_ in PRIO:
        n = norm(e_)
        if len(n) >= 2: ss_prio.setdefault(n, (e_, f_))
ss_idx = dict(ss_prio)
for n, c in ss_votes.items():
    if n in ss_idx: continue
    (f_, k), = c.most_common(1)
    wen = len(n.split()); wfr = len(norm(f_).split())
    if len(c) > 1 and k < 0.6 * sum(c.values()): continue      # traductions contradictoires
    if wen <= 2 and wfr > wen + 1: continue                      # libellé court devenu phrase
    ss_idx[n] = (ss_en[n], f_)

REPL = {'«': '“', '»': '”', '‘': '’', '–': '-', '—': '-', ' ': ' ', ' ': ' ', '…': '…', 'Œ': 'Œ'}
HNS_FMT = re.compile(r'\{(PAUSE|PLAY|COLOR|HIGHLIGHT|SHADOW|FONT|CLEAR|SKIP|PALETTE|MUSIC|SOUND|WAIT|PAUSE_UNTIL_PRESS)')

def ss_convert(ss_en, ss_fr, hid):
    if HNS_FMT.search(hid): return None
    ph_h = re.findall(r'\{[^}]*\}', hid)
    tok_en = re.findall(r'\{[^}]*\}', ss_en.replace('\n', ' '))
    tok_fr = re.findall(r'\{[^}]*\}', ss_fr)
    if any(not t.startswith('{STRVAR') for t in tok_en + tok_fr): return None
    if len(tok_en) != len(ph_h): return None
    mp = {}
    for a, b in zip(tok_en, ph_h):
        if mp.get(a, b) != b: return None
        mp[a] = b
    out = ss_fr
    for a, b in mp.items(): out = out.replace(a, b)
    if re.search(r'\{STRVAR', out): return None
    for a, b in REPL.items(): out = out.replace(a, b)
    out = re.sub(r'(\\[rf])+$', '', out)
    out = re.sub(r'\\[rf]', r'\\p', out)
    if is_dialogue_like(hid) or (re.search(r'\\[nlp]', out) and DIALOGUE.get(hid)):
        out = g.reformater(out, MAXW)
    else:
        if re.search(r'\\[nlp]', out): return None
    if hnsfr.Charmap.invalid(CM, out): return None
    return out

CM = hnsfr.Charmap(root)
DIALOGUE = {m: hnsfr.domain(occ_by_id[m][0].path) == 'dialogues' for m in msgids}
ss_exact, ss_fuzzy = {}, {}
from rapidfuzz import process, fuzz
keys = list(ss_idx)
for m in msgids:
    n = norm(m)
    if len(n) < 4: continue
    if n in ss_idx:
        t = ss_convert(ss_idx[n][0], ss_idx[n][1], m)
        if t: ss_exact[m] = t
        continue
    if m in em or len(n) < 12: continue
    r = process.extractOne(n, keys, scorer=fuzz.ratio, score_cutoff=92)
    if r and re.findall(r'\d+', n) == re.findall(r'\d+', r[0]):
        t = ss_convert(ss_idx[r[0]][0], ss_idx[r[0]][1], m)
        if t: ss_fuzzy[m] = (t, r[1], ss_idx[r[0]][0])
print('SoulSilver exact :', len(ss_exact), ' approché :', len(ss_fuzzy))

# ------------------------------------------------------------------ style SoulSilver
import style, json
gl_path = os.path.join(outdir, 'glossaire.tsv')
if not os.path.exists(gl_path):
    os.makedirs(outdir, exist_ok=True); style.construire(os.path.join(mem, 'ss_fr_msg.json'), gl_path)
GL = style.charger(gl_path)
ESP = frozenset(style.cle(x) for x in json.load(open(os.path.join(mem, 'ss_fr_msg.json')))['237'] if x.strip())
for d in (fan, em, fan_doute):
    for k in list(d): d[k] = style.appliquer(d[k], GL, ESP)

# ------------------------------------------------------------------ write
os.makedirs(outdir, exist_ok=True)
files = {d: polib.POFile() for d in ('dialogues', 'menus', 'donnees')}
for f in files.values():
    f.metadata = {'Project-Id-Version': 'pokehns-fr', 'Language': 'fr', 'MIME-Version': '1.0',
                  'Content-Type': 'text/plain; charset=UTF-8', 'Content-Transfer-Encoding': '8bit'}
stats = collections.Counter()
for m in msgids:
    occs = occ_by_id[m]
    dom = hnsfr.domain(occs[0].path)
    e = polib.POEntry(msgid=m, occurrences=[(o.path, str(o.line)) for o in occs[:6]])
    if m in em:
        e.msgstr = em[m]; e.comment = 'source : Émeraude FR officiel'; stats['Émeraude FR'] += 1
        if m in fan and norm(fan[m]) != norm(em[m]): e.comment += '\npatch FR actuel : ' + fan[m]
    elif m in ss_exact:
        e.msgstr = ss_exact[m]; e.comment = 'source : SoulSilver FR officiel'; stats['SoulSilver FR'] += 1
        if m in fan and norm(fan[m]) != norm(ss_exact[m]): e.comment += '\npatch FR actuel : ' + fan[m]
    elif m in fan:
        e.msgstr = fan[m]; e.comment = 'source : patch FR actuel'; stats['patch FR actuel'] += 1
        if m in ss_fuzzy: e.comment += '\nSoulSilver (approché) : ' + ss_fuzzy[m][0]
    elif m in fan_doute:
        e.msgstr = fan_doute[m]; e.flags.append('fuzzy'); e.comment = 'source : patch FR actuel (correspondance douteuse, à vérifier)'
        stats['à relire (douteux)'] += 1
    elif m in ss_fuzzy:
        e.msgstr = ss_fuzzy[m][0]; e.flags.append('fuzzy')
        e.comment = 'source : SoulSilver FR, correspondance approchée (%d %%) avec « %s »' % (ss_fuzzy[m][1], ss_fuzzy[m][2].replace('\n', ' ')[:120])
        stats['à relire (approché)'] += 1
    else:
        stats['non traduit'] += 1
    files[dom].append(e)
for d, f in files.items():
    f.save(os.path.join(outdir, d + '.po'))
for k, v in stats.most_common(): print('%-22s %d' % (k, v))
