#!/usr/bin/env python3
"""Recherche les textes anglais de la ROM de référence encore présents dans la ROM construite.

  controle_anglais.py <source_upstream> <rom_anglaise> <rom_construite> <sortie.tsv> [--json]

Méthode : on découpe la ROM anglaise en chaînes Gen 3 (terminées par 0xFF), on garde celles qui
se décodent en texte et contiennent au moins un mot anglais (dictionnaire système, privé des
mots qui existent aussi en français dans les textes officiels SoulSilver FR), puis on cherche la
même suite d'octets dans la ROM construite. Chaque chaîne trouvée est rattachée, si possible, à
son fichier source (msgid des .po, noms de cartes JSON, Dresseurs .party).
"""
import os, re, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen3 import Gen3

root, en_path, fr_path, out = sys.argv[1:5]
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
g = Gen3(root)
en = open(en_path, 'rb').read()
fr = open(fr_path, 'rb').read()

# octets autorisés dans un texte (lettres, chiffres, ponctuation, codes de contrôle)
ok = bytes(range(0x00, 0x100))
allowed = set(range(0x00, 0x20)) | set(range(0x2D, 0x30)) | set(range(0x51, 0x52)) | \
    set(range(0x5A, 0x5E)) | set(range(0xA1, 0xF8)) | {0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0x34, 0x35, 0x36, 0x68}
dele = bytes(sorted(allowed))

# vocabulaire anglais sans les mots français homographes
fr_words = set()
ss = json.load(open(os.path.join(P, 'memoires', 'ss_fr_msg.json'), encoding='utf-8'))
for lines in ss.values():
    for l in lines or []:
        for w in re.findall(r"[A-Za-zÀ-ÿ]+", l):
            fr_words.add(w.lower())
for w in ('pokemon', 'pokedex', 'pokenav', 'pc', 'pp', 'hp', 'ok', 'tv', 'lv', 'no', 'non', 'oui'):
    fr_words.add(w)
en_words = set()
for l in open('/usr/share/dict/words', encoding='utf-8', errors='ignore'):
    w = l.strip()
    if len(w) >= 3 and w.islower():
        en_words.add(w)
en_words |= {"you're", "i'm", "it's", "don't", "can't", "won't", "that's", "let's", "there's", "isn't",
             "you", "the", "and", "your", "this", "what", "with", "have", "will", "are", "was"}
en_only = en_words - fr_words


def english_words(t):
    t = re.sub(r'\{[^}]*\}|\\[nlp]', ' ', t)
    ws = re.findall(r"[A-Za-z][a-z']+|[A-Z]{3,}", t)
    return [w for w in ws if w.lower().strip("'") in en_only or w.lower() in en_only]


segs = []
pos = 0
while True:
    e = en.find(b'\xff', pos)
    if e < 0: break
    a = e
    while a > pos and e - a < 2000 and en[a - 1] in allowed: a -= 1
    while a < e and en[a] == 0: a += 1          # espaces de remplissage
    s = en[a:e]
    if len(s) >= 3:
        t = g.decode(s)
        if t and re.search(r'[A-Za-z]{3}', t):
            segs.append((a, s, t))
    pos = e + 1
print('chaînes texte dans la ROM anglaise :', len(segs))

def at_boundary(rom, i):
    return i == 0 or rom[i - 1] in (0xFF, 0x00) or rom[i - 1] not in allowed

def present(b):
    """Adresse de la chaîne dans la ROM construite (ou None)."""
    pat = b + b'\xff'; i = fr.find(pat)
    while i >= 0:
        if at_boundary(fr, i): return i
        i = fr.find(pat, i + 1)
    return None


# zones de la ROM construite (fichier .map de l'éditeur de liens, s'il correspond à cette ROM)
import bisect
symboles = []
carte = os.path.join(os.path.dirname(os.path.abspath(fr_path)), 'upstream', 'pokehns.map')
if os.path.exists(carte):
    obj = None
    for l in open(carte, encoding='utf-8', errors='ignore'):
        m = re.match(r'\s+\.\S+\s+0x(08[0-9a-f]{6})\s+0x[0-9a-f]+\s+(\S+\.o)\s*$', l)
        if m: obj = m.group(2); continue
        m = re.match(r'\s+0x(08[0-9a-f]{6})\s+(\S+)\s*$', l)
        if m: symboles.append((int(m.group(1), 16) - 0x08000000, m.group(2), obj or '?'))
    symboles.sort()
adresses = [x[0] for x in symboles]


def zone(i):
    if i is None or not symboles: return ''
    k = bisect.bisect_right(adresses, i) - 1
    return '%s (%s)' % (symboles[k][1], symboles[k][2]) if k >= 0 else ''

found = {}
for a, s, t in segs:
    ew = english_words(t)
    if not ew: continue
    if len(ew) == 1 and len(re.findall(r'[A-Za-z]+', t)) > 4:  # un seul mot anglais dans une phrase française
        continue
    ifr = present(s)
    if ifr is not None:
        found.setdefault(t, (a, ew, ifr))

# rattachement aux sources
import hnsfr
occ = collections.defaultdict(set)
for o in hnsfr.scan(root):
    b = g.encode(o.text)
    if b: occ[b].add(o.path)
for dp, dn, fn in os.walk(os.path.join(root, 'src', 'data')):
    for f in fn:
        p = os.path.join(dp, f); rel = os.path.relpath(p, root)
        if f.endswith('.party'):
            for m in re.finditer(r'^Name: *(.+)$', open(p, encoding='utf-8').read(), re.M):
                b = g.encode(m.group(1).strip())
                if b: occ[b].add(rel)
        elif f.endswith('.json'):
            for m in re.finditer(r'"name"\s*:\s*"([^"]+)"', open(p, encoding='utf-8').read()):
                b = g.encode(m.group(1))
                if b: occ[b].add(rel)
import glob
for path in ['src/debug.c', 'src/battle_debug.c', 'src/text_input_strings.c'] + [os.path.relpath(x, root) for x in glob.glob(os.path.join(root, 'src/data/credits*'))]:
    for o in hnsfr.scan_file(root, path):
        b = g.encode(o.text)
        if b: occ[b].add(path + ' (exclu)')

for b, paths in occ.items():
    if len(b) < 3: continue
    t = g.decode(b)
    if not t or t in found: continue
    ew = english_words(t)
    if not ew or (len(ew) == 1 and len(re.findall(r'[A-Za-z]+', t)) > 4): continue
    ifr = present(b) if (b + b'\xff') in en else None
    if ifr is not None:
        found[t] = (en.find(b + b'\xff'), ew, ifr)

rows = []
by = collections.Counter()
BINAIRE = re.compile(r'^(gMetatiles|gMetatileAttributes|gTileset|gTiles|sTiles|gBattleAnim|gObjectEventPic|gTrainerFrontPic|gTrainerBackPic|gMonFrontPic|gMonBackPic|gMonIcon)|_Tiles?$|Gfx|Tilemap|Pal')
for t, (a, ew, ifr) in found.items():
    b = g.encode(t)
    src = sorted(occ.get(b, [])) if b else []
    cat = src[0].split('/')[0] + '/' + (src[0].split('/')[1] if '/' in src[0] else '') if src else '(source inconnue)'
    if src and src[0].endswith('.party'): cat = 'Dresseurs (.party)'
    elif src and src[0].endswith('.json'): cat = 'JSON (' + os.path.basename(src[0]) + ')'
    elif src and '(exclu)' in src[0]: cat = 'fichier exclu : ' + src[0]
    z = zone(ifr)
    if not src:   # sans source dans le code : données binaires (tuiles…) ou texte à examiner
        cat = 'données binaires (%s)' % z.split(' ')[0] if z and BINAIRE.search(z.split(' ')[0]) else '(source inconnue)'
    by[cat] += 1
    rows.append((cat, '0x%07X' % a, t, ' '.join(src[:3]), ' '.join(ew[:5]), '0x%07X' % ifr, z))
rows.sort()
with open(out, 'w', encoding='utf-8') as f:
    f.write('catégorie\tadresse_EN\ttexte\tsources\tmots_anglais\tadresse_FR\tzone_FR\n')
    for r in rows: f.write('\t'.join(r) + '\n')
print('chaînes anglaises encore présentes :', len(rows))
for k, v in by.most_common(): print('  %-45s %d' % (k, v))
