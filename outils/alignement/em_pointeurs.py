#!/usr/bin/env python3
"""Carte des pointeurs Émeraude US -> Émeraude FR par « marche parallèle ».

1. Ancres : fenêtres de 16 octets uniques (pointeurs masqués à tout décalage) communes aux deux ROM.
2. Depuis chaque ancre (et chaque paire de pointeurs découverte), on avance en parallèle dans les deux
   ROM tant que les octets sont identiques ; une différence expliquée par un pointeur (4 octets finissant
   par 08/09 dans les deux ROM, alignés ou non : scripts de carte, msgbox/loadword…) est enregistrée
   (cible US -> cible FR) et la marche continue ; la paire de cibles devient une nouvelle graine.
   Une différence courte suivie d'une resynchronisation au même décalage (champ de longueur fixe : nom
   dans une table) est enregistrée comme segment et la marche continue.
Sortie : $TMP/em_ptr.pkl = {'ptr': {cible_us: Counter(cible_fr)}, 'src': {cible_us: [emplacements US]},
                            'seg': [(adr_us, adr_fr, longueur)]}
"""
import os, sys, pickle, collections, struct, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from em_commun import roms, TMP

us, fr = roms()
N = len(us)
A = np.frombuffer(us, np.uint8); B = np.frombuffer(fr, np.uint8)


def masque(arr):
    m = arr.copy()
    hit = np.nonzero((arr[3:] == 8) | (arr[3:] == 9))[0]
    for k in range(4): m[hit + k] = 0
    return m


t0 = time.time()
MA, MB = masque(A), masque(B)
mu, mf = MA.tobytes(), MB.tobytes()
W = 16
idx = {}; dup = set()
for i in range(0, N - W, 8):
    w = mu[i:i + W]
    if w.count(0) > 6 or w.count(255) > 6 or len(set(w)) < 5: continue
    if w in idx: dup.add(w)
    else: idx[w] = i
for w in dup: idx.pop(w, None)
seeds = []
seenf = {}
for j in range(0, N - W):
    i = idx.get(mf[j:j + W])
    if i is not None:
        if i in seenf: seenf[i] = None
        else: seenf[i] = j
anch = sorted((i, j) for i, j in seenf.items() if j is not None)
print('ancres', len(anch), '%.0fs' % (time.time() - t0), file=sys.stderr)


def ptr(rom, j):
    if j < 0 or j + 4 > N or rom[j + 3] not in (8, 9): return None
    v = struct.unpack_from('<I', rom, j)[0] - 0x08000000
    return v if 0 <= v < N else None


NONE = np.iinfo(np.int32).min
dl = np.full(N, NONE, np.int32)        # décalage FR-US des positions US parcourues
pairs = collections.defaultdict(collections.Counter)
srcs = collections.defaultdict(list)
segs = []
queue = collections.deque(anch)
CH = 4096
MINRES = int(os.environ.get("EM_MINRES", "2"))
TEXTE = set(range(0x00, 0xF7)) - {0x08, 0x09}


def fin_texte(rom, x, lim=48):
    """fin (position du FF) d'un texte commençant avant x, ou None si pas du texte"""
    e = rom.find(b'\xff', x, x + lim)
    if e < 0: return None
    if any(c not in TEXTE for c in rom[x:e]): return None
    return e


nwalk = 0
while queue:
    u, f = queue.popleft()
    if u < 0 or f < 0 or u >= N or f >= N or dl[u] != NONE: continue
    nwalk += 1
    D = f - u
    while u < N and f < N:
        L = min(CH, N - u, N - f)
        if L <= 0: break
        c = dl[u:u + L] != NONE
        stop = int(np.argmax(c)) if c.any() else L
        d = np.nonzero(A[u:u + stop] != B[f:f + stop])[0]
        if len(d) == 0:
            dl[u:u + stop] = D
            if stop < L: break      # déjà parcouru
            u += L; f += L; continue
        i = int(d[0])
        dl[u:u + i] = D
        u += i; f += i
        # pointeur ?
        ok = False
        for j in range(3, -1, -1):
            pu, pf = ptr(us, u - j), ptr(fr, f - j)
            if pu is not None and pf is not None and us[u - j:u] == fr[f - j:f]:
                pairs[pu][pf] += 1; srcs[pu].append(u - j)
                if dl[pu] == NONE: queue.append((pu, pf))
                dl[u - j:u - j + 4] = D
                u += 4 - j; f += 4 - j; ok = True; break
        if ok: continue
        # champ texte de longueur fixe complété par des 00 (tables de noms) : même décalage après
        eu, ef = fin_texte(us, u), fin_texte(fr, f)
        if eu is not None and ef is not None and (us[eu + 1] == 0 or fr[ef + 1] == 0):
            nu, nf = eu + 1, ef + 1
            while nu < N and us[nu] == 0 and nu - u < 64: nu += 1
            while nf < N and fr[nf] == 0 and nf - f < 64: nf += 1
            if nu - u == nf - f:
                segs.append((u, f, nu - u, 'pad')); dl[u:nu] = D
                u, f = nu, nf; continue
        # champ de longueur fixe : resynchronisation au même décalage
        for k in range(1, 33):
            a = mu[u + k:u + k + 16]; b = mf[f + k:f + k + 16]
            if a == b and 16 - a.count(0) - a.count(255) >= MINRES:
                segs.append((u, f, k, 'sync')); dl[u:u + k] = D
                u += k; f += k; ok = True; break
        if not ok: break
cov = dl != NONE
print('marches', nwalk, 'cibles', len(pairs), 'segments', len(segs), 'couverture %.1f%%' % (100 * cov.mean()),
      '%.0fs' % (time.time() - t0), file=sys.stderr)
os.makedirs(TMP, exist_ok=True)
pickle.dump({'ptr': dict(pairs), 'src': dict(srcs), 'seg': segs, 'anch': anch}, open(os.path.join(TMP, 'em_ptr.pkl'), 'wb'))
np.save(os.path.join(TMP, 'em_delta.npy'), dl)
