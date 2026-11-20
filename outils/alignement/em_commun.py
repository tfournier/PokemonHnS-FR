"""Outils communs du lot A (alignement Émeraude US <-> Émeraude FR).

Chemins relatifs à la racine du projet (deux niveaux au-dessus de ce fichier).
Ne modifie aucun fichier partagé : importe seulement gen3, hnsfr, style.
"""
import os, sys, re, json, glob, collections, pickle

P = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(P, 'outils'))
from gen3 import Gen3, nettoyer_kana   # noqa: E402
import hnsfr                            # noqa: E402
import style                            # noqa: E402

ROOT = os.path.join(P, 'build', 'upstream_orig')
MEM = os.path.join(P, 'memoires')
LOT = os.path.join(P, 'traductions', 'lots', 'A_emeraude')
TMP = os.environ.get('LOTA_TMP') or os.path.join(MEM, 'lotA')   # mémoires dérivées du lot A (petits pickles)

G = Gen3(ROOT)
CODE = re.compile(r'\{[^}]*\}')


def roms():
    us = open(os.path.join(MEM, 'emeraude_us.gba'), 'rb').read()
    fr = open(os.path.join(MEM, 'em_fr.gba'), 'rb').read()
    return us, fr


def charger_po():
    """{(msgctxt, msgid): dict(msgstr, source, fichier_po, occ, comment)}"""
    out = {}
    for f in sorted(glob.glob(os.path.join(P, 'traductions', '*.po'))):
        import polib
        for e in polib.pofile(f):
            if e.obsolete: continue
            m = re.search(r'source : ([^\n]*)', e.comment or '')
            out[(e.msgctxt or '', e.msgid)] = dict(
                msgstr=e.msgstr if 'fuzzy' not in e.flags else '', fuzzy='fuzzy' in e.flags,
                source=m.group(1).strip() if m else '', po=os.path.basename(f)[:-3],
                occ=[(p, int(l) if str(l).isdigit() else 0) for p, l in e.occurrences], comment=e.comment or '')
    return out


def deja_emeraude(info):
    return info['msgstr'] and info['source'].startswith('Émeraude FR officiel')


# ------------------------------------------------------------------ style
_GL = _ESP = None
def gl_esp():
    global _GL, _ESP
    if _GL is None:
        _GL = style.charger(os.path.join(P, 'traductions', 'glossaire.tsv'))
        _ESP = frozenset(style.cle(x) for x in json.load(open(os.path.join(MEM, 'ss_fr_msg.json'), encoding='utf-8'))['237'] if x.strip())
    return _GL, _ESP


def code_bytes(c):
    b = G.encode(c)
    return b if b is not None else c.encode()


def est_code(c):
    b = G.encode(c)
    return b is None or not b or b[0] >= 0xF7


def codes_octets(s):
    return collections.Counter(code_bytes(c) for c in CODE.findall(s) if est_code(c))


def graphie_codes(fr, en):
    """Remet la graphie anglaise des codes dont les octets sont identiques ({FONT 0} -> {FONT_SMALL})."""
    par_octets = {}
    for c in CODE.findall(en):
        par_octets.setdefault(code_bytes(c), c)
    def rep(m):
        c = m.group(0)
        return par_octets.get(code_bytes(c), c)
    return CODE.sub(rep, fr)


def officiel(fr_brut, en):
    """Texte Émeraude FR décodé -> passage au style SoulSilver + nettoyage + graphie des codes."""
    gl, esp = gl_esp()
    t = nettoyer_kana(fr_brut)
    t = graphie_codes(t, en)
    t = style.appliquer(t, gl, esp)
    t = nettoyer_kana(t)
    return t


def nombres(s):
    s = CODE.sub(' ', s)
    return sorted(re.findall(r'\d+', s))


def controle(en, fr, phrase=None):
    """Contrôles automatiques d'une paire alignée. Renvoie la liste des problèmes (vide = OK)."""
    pb = []
    if codes_octets(en) != codes_octets(fr): pb.append('codes')
    if nombres(en) != nombres(fr): pb.append('nombres')
    le = len(CODE.sub('X', en)); lf = len(CODE.sub('X', fr))
    if phrase is None: phrase = len(re.findall(r'[A-Za-z]+', CODE.sub('', en))) >= 3
    if phrase and le >= 8 and not (0.5 <= lf / le <= 2.2): pb.append('ratio %.2f' % (lf / le))
    if not phrase and le >= 3 and not (0.25 <= lf / le <= 4): pb.append('ratio %.2f' % (lf / le))
    for fin in ('\\n', '\\p', '\\l', ' '):
        if en.endswith(fin) and not fr.endswith(fin): pb.append('fin %r' % fin)
    if en.startswith(' ') != fr.startswith(' '): pb.append('debut espace')
    if re.search(r'[぀-ヿ]', fr): pb.append('kana')
    return pb


def decoder(rom, a, hint='', maxlen=2000):
    e = rom.find(b'\xff', a, a + maxlen)
    if e < 0: return None
    return G.decode(rom[a:e], hint)


def zone(path):
    """grande zone du jeu d'après le chemin du fichier source"""
    p = path
    if 'battle_frontier' in p or 'BattleFrontier' in p or 'battle_tower' in p or 'BattleTower' in p or 'frontier' in p.lower() \
            or 'Battle' in p and ('Dome' in p or 'Pike' in p or 'Arena' in p or 'Factory' in p or 'Palace' in p or 'Pyramid' in p) \
            or 'apprentice' in p or 'trainer_hill' in p or 'TrainerHill' in p or 'battle_tent' in p or 'BattleTent' in p:
        return 'Frontier'
    if 'contest' in p.lower(): return 'Concours'
    if 'tv' in os.path.basename(p).lower() or '/tv' in p or 'TV' in os.path.basename(p): return 'TV'
    if 'match_call' in p or 'MatchCall' in p or 'pokenav' in p: return 'Match Call/PokéNav'
    if p.startswith('data/maps/'):
        try:
            import functools
            return 'cartes FRLG' if _frlg(p.split('/')[2]) else 'cartes Hoenn/HnS'
        except Exception:
            return 'cartes'
    if p.startswith('data/'): return 'scripts/texte communs'
    if p.startswith('src/data/') or p.endswith('.party'): return 'données'
    return 'moteur (src)'


_MAPS = None
def _frlg(mapdir):
    """Vrai si la carte n'est pas compilée (cartes FRLG / inutilisées de l'upstream)."""
    global _MAPS
    if _MAPS is None:
        _MAPS = set()
        try:
            j = json.load(open(os.path.join(ROOT, 'data', 'maps', 'map_groups.json')))
            for grp in j.get('group_order', []):
                for m in j.get(grp, []): _MAPS.add(m)
        except Exception:
            pass
    return mapdir not in _MAPS


def ecrire(nom, liste):
    os.makedirs(LOT, exist_ok=True)
    liste = sorted(liste, key=lambda d: (d.get('fichier', ''), d.get('ligne', 0), d['msgid']))
    with open(os.path.join(LOT, nom), 'w', encoding='utf-8') as f:
        json.dump(liste, f, ensure_ascii=False, indent=1)
    return len(liste)


def entree(msgid, msgstr, source, info, preuve, note='', ctx=''):
    occ = info['occ'][0] if info and info['occ'] else ('', 0)
    d = {'msgid': msgid}
    if ctx: d['msgctxt'] = ctx
    d.update(msgstr=msgstr, source=source, fichier=occ[0], ligne=occ[1])
    if info and info['msgstr']: d['ancien'] = info['msgstr']
    d['preuve'] = preuve
    if note: d['note'] = note
    return d
