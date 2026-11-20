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
    s = en[pos:e]
    if 3 <= len(s) <= 2000 and not s.translate(None, dele):
        # start: try the whole segment then shrink from the left if it fails to decode
        t = g.decode(s)
        if t and re.search(r'[A-Za-z]{3}', t):
            segs.append((pos, s, t))
    pos = e + 1
print('chaînes texte dans la ROM anglaise :', len(segs))

found = {}
for a, s, t in segs:
    ew = english_words(t)
    if not ew: continue
    if len(ew) == 1 and len(re.findall(r'[A-Za-z]+', t)) > 4:  # un seul mot anglais dans une phrase française
        continue
    if (s + b'\xff') in fr:
        found.setdefault(t, (a, ew))

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
for path in ('src/debug.c', 'src/battle_debug.c', 'src/text_input_strings.c'):
    for o in hnsfr.scan_file(root, path):
        b = g.encode(o.text)
        if b: occ[b].add(path + ' (exclu)')

rows = []
by = collections.Counter()
for t, (a, ew) in found.items():
    b = g.encode(t)
    src = sorted(occ.get(b, [])) if b else []
    cat = src[0].split('/')[0] + '/' + (src[0].split('/')[1] if '/' in src[0] else '') if src else '(source inconnue)'
    if src and src[0].endswith('.party'): cat = 'Dresseurs (.party)'
    elif src and src[0].endswith('.json'): cat = 'JSON (' + os.path.basename(src[0]) + ')'
    elif src and '(exclu)' in src[0]: cat = 'fichier exclu : ' + src[0]
    by[cat] += 1
    rows.append((cat, '0x%07X' % a, t, ' '.join(src[:3]), ' '.join(ew[:5])))
rows.sort()
with open(out, 'w', encoding='utf-8') as f:
    f.write('catégorie\tadresse_EN\ttexte\tsources\tmots_anglais\n')
    for r in rows: f.write('\t'.join(r) + '\n')
print('chaînes anglaises encore présentes :', len(rows))
for k, v in by.most_common(): print('  %-45s %d' % (k, v))
