#!/usr/bin/env python3
"""Contrôles automatiques des traductions (.po ou lot JSON).

  verifier.py <source_upstream> <fichiers .po ou .json…> [--sortie rapport/verifications.tsv]
              [--patch memoires/hns_fr_patch.gba] [--glossaire traductions/glossaire.tsv]

Un lot JSON est une liste d'objets {"msgid", "msgstr", "msgctxt"?, "source"?, "fichier"?}.

Contrôles (une ligne du rapport par problème) :
  CODES      codes de contrôle {…} différents de l'anglais (nombre, type, arguments)
  ESPACE     espace initiale / suffixe non conservé, fin \\n \\p \\l ou $ non conservée
  KANA       caractère japonais dans le français
  CARACTERE  caractère que la charmap ne sait pas encoder
  LARGEUR    ligne de dialogue de plus de 198 px (police normale)
  LONGUEUR   champ fixe trop long (classe, type, objet, capacité, talent, Dresseur…)
  GLOSSAIRE  terme en capitales dont le glossaire donne une autre graphie
  FRAGMENT   texte venant du patch FR qui ne commence pas à un début de chaîne dans sa ROM
  ANGLAIS    traduction identique à l'anglais (hors noms propres/sigles)
"""
import os, re, sys, json, collections, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen3 import Gen3
import hnsfr

MAXW = 198
FENETRE = 216   # largeur de la fenêtre de dialogue (27 tuiles) : tolérance pour les textes officiels
KANA = re.compile(r'[぀-ヿ一-鿿]')
CODE = re.compile(r'\{[^}]*\}')
# champs à longueur fixe : (motif de la ligne source, longueur max, nom)
CHAMPS = [
    (re.compile(r'types_info\.h$'), re.compile(r'\.name\s*='), 8, 'type'),
    (re.compile(r'types_info\.h$'), re.compile(r'\.generic\s*='), 16, 'generic'),
    (re.compile(r'.'), re.compile(r'\.categoryName\s*='), 12, 'catégorie Pokédex'),
    (re.compile(r'.'), re.compile(r'\.speciesName\s*='), 12, 'espèce'),
    (re.compile(r'items\.h$'), re.compile(r'\.name\s*=\s*ITEM_NAME'), 20, 'objet'),
    (re.compile(r'items\.h$'), re.compile(r'\.pluralName\s*='), 22, 'objet (pluriel)'),
    (re.compile(r'moves_info\.h$'), re.compile(r'\.name\s*='), 16, 'capacité'),
    (re.compile(r'abilities\.h$'), re.compile(r'\.name\s*='), 16, 'talent'),
    (re.compile(r'battle_main\.c$|trainer_class'), re.compile(r'\.name\s*=|\[TRAINER_CLASS_\w+\]\s*=\s*\{\s*_\('), 12, 'classe de Dresseur'),
    (re.compile(r'battle_frontier_trainers\.h$|battle_tent\.h$'), re.compile(r'\.trainerName\s*='), 7, 'Dresseur Frontier'),
    (re.compile(r'trainer_hill\.h$'), re.compile(r'\.nickname\s*='), 10, 'surnom Mont Dresseurs'),
    (re.compile(r'trainer_hill\.h$'), re.compile(r'\.name\s*='), 7, 'Dresseur Mont Dresseurs'),
]


_EN = None
def anglais(t):
    """mots anglais (dictionnaire système moins les mots présents dans SoulSilver FR)."""
    global _EN
    if _EN is None:
        P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        frw = set()
        for lines in json.load(open(os.path.join(P, 'memoires', 'ss_fr_msg.json'), encoding='utf-8')).values():
            for l in lines or []: frw.update(w.lower() for w in re.findall(r"[A-Za-zÀ-ÿ]+", l))
        enw = {l.strip() for l in open('/usr/share/dict/words', errors='ignore') if len(l.strip()) >= 3 and l.strip().islower()}
        enw |= {'you', 'the', 'and', 'your', 'this', 'what', 'with', 'have', 'will', 'are', 'was'}
        _EN = enw - frw - {'pokemon', 'pokedex', 'ok'}
    t = re.sub(r'\{[^}]*\}|\\[nlp]', ' ', t)
    return [w for w in re.findall(r"[A-Za-z]+", t) if w.lower() in _EN]


def codes(s):
    return collections.Counter(CODE.findall(s))


def lignes(s):
    return re.split(r'\\[nlp]', s)


class Verif:
    def __init__(self, root, patch=None, glossaire=None):
        self.root = root
        self.g = Gen3(root)
        self.cm = hnsfr.Charmap(root)
        self.patch = open(patch, 'rb').read() if patch and os.path.exists(patch) else None
        self.gl = {}
        if glossaire and os.path.exists(glossaire):
            import style
            self.gl = style.charger(glossaire)
            self.style = style
        self._src = {}

    def ligne_source(self, path, line):
        """ligne de l'original upstream (git show du tag) pour reconnaître le champ."""
        if path not in self._src:
            try:
                tag = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'upstream.txt')).read().strip()
                txt = subprocess.run(['git', 'show', '%s:%s' % (tag, path)], cwd=self.root, capture_output=True, text=True).stdout
            except Exception:
                txt = ''
            if not txt and os.path.exists(os.path.join(self.root, path)):
                txt = open(os.path.join(self.root, path), encoding='utf-8', errors='replace').read()
            self._src[path] = txt.split('\n')
        L = self._src[path]
        return L[line - 1] if 0 < line <= len(L) else ''

    def est_code(self, c):
        """vrai code de contrôle (FC…, FD…, boutons F8/F9) et non glyphe ({SUPER_E}, {PKMN}, flèches…)."""
        b = self.g.encode(c)
        return b is None or not b or b[0] >= 0xF7

    def code_bytes(self, c):
        b = self.g.encode(c)
        return b if b is not None else c

    def champ(self, occs):
        for path, line in occs or []:
            try: line = int(line)
            except (TypeError, ValueError): continue
            src = self.ligne_source(path, line)
            for fre, lre, n, nom in CHAMPS:
                if fre.search(path) and lre.search(src):
                    return n, nom
            if path.endswith('.party'):
                return 10, 'nom de Dresseur'
        return None

    def check(self, msgid, msgstr, occs=(), comment='', domaine=''):
        pb = []
        if not msgstr: return pb
        source = (re.search(r'source : ([^\n]*)', comment or '') or [None, ''])[1]
        # codes
        a = collections.Counter(self.code_bytes(c) for c in CODE.findall(msgid) if self.est_code(c))
        b = collections.Counter(self.code_bytes(c) for c in CODE.findall(msgstr) if self.est_code(c))
        if a != b:
            a, b = codes(msgid), codes(msgstr)
            manque = list((a - b).elements()); trop = list((b - a).elements())
            pb.append(('CODES', 'manque %s ; en trop %s' % (manque[:4], trop[:4])))
        # espaces / suffixes / fins
        if msgid.startswith(' ') != msgstr.startswith(' '):
            pb.append(('ESPACE', 'espace initiale différente'))
        for fin in ('\\n', '\\p', '\\l', ' '):
            if msgid.endswith(fin) and not msgstr.endswith(fin):
                pb.append(('ESPACE', 'fin %r non conservée' % fin))
        # kana / caractères
        if KANA.search(msgstr):
            pb.append(('KANA', ''.join(sorted(set(KANA.findall(msgstr))))))
        bad = self.cm.invalid(msgstr)
        if '$' in msgstr and '$' not in msgid:
            bad = list(bad) + ['$ (= 0xFF, fin de chaîne)']
        if bad:
            pb.append(('CARACTERE', repr(sorted(set(bad))[:6])))
        # largeur (dialogues : textes multi-lignes ou domaine dialogues)
        dialogue = bool(re.search(r'\\[nlp]', msgid)) or domaine == 'dialogues'
        if dialogue and not re.search(r'\{(DYNAMIC|CLEAR_TO|CLEAR|FONT|SHIFT)', msgstr):
            wmax_en = max(self.g.largeur(l) for l in lignes(msgid))
            officiel = 'officiel' in source
            for l in lignes(msgstr):
                w = self.g.largeur(l)
                if w > (FENETRE if officiel else MAXW) and w > wmax_en:
                    pb.append(('LARGEUR', '%d px : %s' % (w, l[:50]))); break
        # champs fixes
        ch = self.champ(occs)
        if ch:
            n, nom = ch
            enc = self.g.encode(msgstr)
            if enc is not None and len(enc) > n:
                pb.append(('LONGUEUR', '%s : %d > %d' % (nom, len(enc), n)))
        # glossaire
        if self.gl and re.search(r'[a-zà-ÿ]{2}', CODE.sub('', msgstr).replace('é', '')):
            t = self.style.appliquer(msgstr, self.gl)
            if t != msgstr:
                diff = [w for w in re.findall(r"[A-ZÀ-Þé][A-ZÀ-Þé'’.\- ]+", msgstr) if w not in t][:3]
                pb.append(('GLOSSAIRE', 'graphie glossaire différente : %s' % diff))
        # fragment du patch FR
        if self.patch is not None and source.startswith('patch FR') or self.patch is not None and source.startswith('relu'):
            enc = self.g.encode(msgstr)
            if enc:
                pat = enc + b'\xff'; i = self.patch.find(pat); ok = False; vu = False
                while i >= 0:
                    vu = True
                    if i == 0 or self.patch[i - 1] in (0xFF, 0x00) or not (0xA1 <= self.patch[i - 1] <= 0xEE or 0x01 <= self.patch[i - 1] <= 0x1F):
                        ok = True; break
                    i = self.patch.find(pat, i + 1)
                if vu and not ok:
                    pb.append(('FRAGMENT', 'toujours précédé d’une lettre dans la ROM du patch FR (morceau d’une autre chaîne)'))
                len_en, len_fr = len(msgid), len(msgstr)
                if len_en >= 8 and not (0.45 <= len_fr / len_en <= 2.6):
                    pb.append(('FRAGMENT', 'ratio de longueur %.2f' % (len_fr / len_en)))
                ma, mf = CODE.sub('', msgid)[:1], CODE.sub('', msgstr)[:1]
                if ma and mf and ma.isupper() and mf.islower():
                    pb.append(('FRAGMENT', 'minuscule initiale (anglais en majuscule)'))
        # identique à l'anglais
        if msgstr == msgid and anglais(msgid):
            pb.append(('ANGLAIS', 'traduction identique à l’anglais'))
        return pb


def main():
    args = sys.argv[1:]
    def opt(n, d=None):
        if n in args:
            i = args.index(n); v = args[i + 1]; del args[i:i + 2]; return v
        return d
    P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = opt('--sortie', os.path.join(P, 'rapport', 'verifications.tsv'))
    patch = opt('--patch', os.path.join(P, 'memoires', 'hns_fr_patch.gba'))
    gl = opt('--glossaire', os.path.join(P, 'traductions', 'glossaire.tsv'))
    root, files = args[0], args[1:]
    V = Verif(root, patch, gl)
    rows = []; tot = collections.Counter(); n = 0
    for f in files:
        if f.endswith('.po'):
            import polib
            ents = [(e.msgid, e.msgstr, e.occurrences, e.comment or '', e.msgctxt or '') for e in polib.pofile(f)
                    if e.msgstr and 'fuzzy' not in e.flags and not e.obsolete]
            dom = os.path.basename(f)[:-3]
        else:
            ents = [(d['msgid'], d.get('msgstr', ''), [(d['fichier'], d.get('ligne', 0))] if d.get('fichier') else [],
                     'source : ' + (d.get('source') or ''), d.get('msgctxt', '')) for d in json.load(open(f, encoding='utf-8'))]
            dom = ''
        for mid, mstr, occ, com, ctx in ents:
            n += 1
            d = dom or (hnsfr.domain(occ[0][0]) if occ else '')
            for k, msg in V.check(mid, mstr, occ, com, d):
                tot[k] += 1
                src = (re.search(r'source : ([^\n]*)', com) or [None, ''])[1]
                rows.append((k, os.path.basename(f), src, mid.replace('\t', ' '), mstr.replace('\t', ' '), msg))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as fo:
        fo.write('controle\tfichier\tsource\tmsgid\tmsgstr\tdetail\n')
        for r in sorted(rows): fo.write('\t'.join(r) + '\n')
    print('entrées vérifiées : %d ; problèmes : %d' % (n, len(rows)))
    for k, v in tot.most_common(): print('  %-10s %d' % (k, v))
    return 1 if rows else 0


if __name__ == '__main__':
    sys.exit(main())
