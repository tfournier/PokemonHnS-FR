#!/usr/bin/env python3
"""Lot B : noms (Dresseurs Johto/Kanto, classes, lieux, objets, capacités, talents, espèces) d'après SoulSilver FR.

  ss_noms.py --travail <dossier de ss_paires.py> --phg <clone partiel pret/pokeheartgold>

Dresseurs : chaque Dresseur de trainers_hns.party / trainers_frlg.party est rapproché des Dresseurs HGSS
(files/poketool/trainer/trainers.json, index = ligne de la banque 729 des noms FR) de même nom anglais,
départagés par la classe et l'équipe. Écrit cand_noms.json et cand_douteux_noms.json dans --travail.
"""
import os, re, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ss_commun import *   # noqa

UP = os.path.join(P, 'build', 'upstream_orig')
MAXLEN = {'nom de Dresseur': 10, 'classe de Dresseur': 12, 'objet': 20, 'capacité': 16, 'talent': 16, 'espèce': 12}
GENERIQUES = {'GRUNT', 'SCIENTIST', '{B_RIVAL_NAME}', 'RIVAL', 'CHAMPION'}


def opt(args, n, d=None):
    if n in args:
        i = args.index(n); v = args[i + 1]; del args[i:i + 2]; return v
    return d


def lire_party(path):
    txt = open(os.path.join(UP, path), encoding='utf-8').read()
    out = []
    parts = re.split(r'^=== (\w+) ===\s*$', txt, flags=re.M)
    for k in range(1, len(parts), 2):
        cid, body = parts[k], parts[k + 1]
        name = re.search(r'^Name:[ \t]*(.*?)[ \t]*$', body, re.M)
        cls = re.search(r'^Class:[ \t]*(.*?)[ \t]*$', body, re.M)
        mons = []
        for blk in re.split(r'\n\s*\n', body):
            l = blk.strip().split('\n')[0].strip()
            if not l or ':' in l.split('@')[0] and not re.search(r'\(', l): continue
            if re.match(r'^(Name|Class|Pic|Gender|Music|Double|AI|Items|Mugshot|Starting|Party|Copy)', l): continue
            sp = l.split('@')[0].strip()
            m = re.search(r'\(([^()]+)\)\s*(\([MF]\))?\s*$', sp)
            if m and m.group(1) not in ('M', 'F'): sp = m.group(1)
            sp = re.sub(r'\s*\([MF]\)\s*$', '', sp)
            mons.append(re.sub(r'[^A-Z]', '', sp.upper()))
        line = txt[:txt.find('=== %s ===' % cid)].count('\n') + 1
        out.append({'id': cid, 'name': name.group(1) if name else '', 'class': cls.group(1) if cls else '', 'mons': set(mons),
                    'path': path, 'line': line})
    return out


def cle_classe(c):
    c = re.sub(r'^TRAINERCLASS_', '', c.upper().replace(' ', '_'))
    c = re.sub(r'_(HNS|FRLG|GS|M|F|EARLY|LATE|1|KANTO)\b', '', c)
    c = re.sub(r'_(HNS|FRLG|GS|M|F|EARLY|LATE|1|KANTO)\b', '', c)
    eq = {'COOLTRAINER': 'ACE_TRAINER', 'POKEMANIAC': 'POKE_MANIAC', 'OFFICER': 'POLICEMAN', 'ROCKET_ADMIN': 'EXECUTIVE',
          'CHANNELER': 'MEDIUM', 'SCHOOL_KID': 'SCHOOL_KID', 'PSYCHIC': 'PSYCHIC', 'BOSS': 'ROCKET_BOSS'}
    c = eq.get(c, c)
    return re.sub(r'[^A-Z]', '', c)


def classes_compatibles(a, b):
    a, b = cle_classe(a), cle_classe(b)
    return a == b or b.startswith(a) or a.startswith(b)


def entree(e, msgstr, preuve, note, src='SoulSilver FR officiel', ctx=None):
    o = {'msgid': e.msgid}
    if ctx is not None: o['msgctxt'] = ctx
    elif e.msgctxt: o['msgctxt'] = e.msgctxt
    occ = [x for x in e.occurrences if ctx is None or x[0] == ctx] or e.occurrences
    o.update({'msgstr': msgstr, 'source': src, 'fichier': occ[0][0] if occ else '',
              'ligne': int(occ[0][1]) if occ and str(occ[0][1]).isdigit() else 0})
    if e.msgstr: o['ancien'] = e.msgstr
    o['preuve'] = preuve
    if note: o['note'] = note
    o['_source_po'] = source_po(e.comment) or 'non traduit'
    return o


def main():
    args = sys.argv[1:]
    trav = opt(args, '--travail'); phg = opt(args, '--phg')
    en = json.load(open(os.path.join(trav, 'ss_en.json'), encoding='utf-8'))
    fr = json.load(open(os.path.join(trav, 'ss_fr.json'), encoding='utf-8'))
    G = gen3()
    tr = json.load(open(os.path.join(phg, 'files/poketool/trainer/trainers.json'), encoding='utf-8'))['trainers']
    hg = []
    for i, t in enumerate(tr):
        hg.append({'i': i, 'name': t['name'].replace('{TRNAME}', '').strip(), 'class': t['class'],
                   'mons': {re.sub(r'[^A-Z]', '', p['species'].replace('SPECIES_', '')) for p in t['party']},
                   'fr': fr['729'][i].replace('{TRNAME}', '').strip()})
    parnom = collections.defaultdict(list)
    for h in hg: parnom[h['name'].upper()].append(h)
    po = {}
    for d, e in charger_po():
        po.setdefault(e.msgid, []).append((d, e))
    noms, douteux = [], []
    stats = collections.Counter()

    # ------------------------------------------------------------------ Dresseurs
    hns = lire_party('src/data/trainers_hns.party') + lire_party('src/data/trainers_frlg.party')
    choix = collections.defaultdict(list)   # nom EN → [(fr, preuve, fichier)]
    for t in hns:
        n = t['name']
        if not n or n.upper() in GENERIQUES or '{' in n: continue
        cands = parnom.get(n.upper(), [])
        if not cands:
            stats['dresseur_sans_homonyme_hgss'] += 1; continue
        def score(h):
            s = 0
            if classes_compatibles(t['class'], h['class']): s += 2
            if t['mons'] and h['mons']: s += 3 * len(t['mons'] & h['mons']) / len(t['mons'] | h['mons'])
            return s
        cands = sorted(cands, key=score, reverse=True)
        frs = {h['fr'] for h in cands}
        best = cands[0]
        ok_classe = classes_compatibles(t['class'], best['class'])
        if len(frs) == 1:
            conf = 'sûr' if ok_classe else 'nom seul'
        elif score(best) > (score(cands[1]) if len(cands) > 1 else 0) and ok_classe:
            conf = 'départagé'
        else:
            conf = 'ambigu'
        choix[n].append({'fr': best['fr'], 'conf': conf, 'preuve': '729:%d — %s (%s, équipe %s)' % (
            best['i'], best['fr'], best['class'].replace('TRAINERCLASS_', ''), '/'.join(sorted(best['mons']))[:60]),
            'hns': '%s (%s, %s)' % (t['id'], t['class'], t['path'].split('/')[-1]), 'path': t['path'], 'line': t['line'],
            'alts': sorted(frs)})
    def verdict(L, fr1):
        """raison de douter pour un groupe de Dresseurs, ou ''."""
        frs = {y['fr'] for y in L}
        enc = G.encode(fr1)
        if len(frs) > 1: return 'plusieurs noms SS : %s' % ', '.join(sorted(frs))
        if not enc or len(enc) > 10: return 'nom trop long (%s > 10)' % (len(enc) if enc else '?')
        if any(y['conf'] == 'ambigu' for y in L): return 'homonymes HGSS aux noms FR différents : %s' % ', '.join(L[0]['alts'])
        if any(y['conf'] == 'nom seul' for y in L): return 'classe HGSS différente : simple homonyme'
        return ''
    for n, L in choix.items():
        ents = po.get(n)
        if not ents: continue
        d, e = ents[0]
        frs = collections.Counter(x['fr'] for x in L)
        fr1 = frs.most_common(1)[0][0]
        x = next(x for x in L if x['fr'] == fr1)
        occ_files = {o[0] for o in e.occurrences}
        hoenn = sorted(f for f in occ_files if not re.search(r'trainers_(hns|frlg)\.party$', f))
        src_po = source_po(e.comment)
        if e.msgstr == fr1: continue
        note = '; '.join(sorted({'%s → %s' % (y['hns'], y['conf']) for y in L}))[:300]
        paths = sorted({y['path'] for y in L})
        v = verdict(L, fr1)
        if not hoenn and not v and 'officiel' not in src_po:
            noms.append(entree(e, fr1, x['preuve'], note)); stats['dresseur'] += 1; continue
        if not hoenn and 'SoulSilver' in src_po:
            o = entree(e, fr1, x['preuve'], note + ' ; le .po a déjà « %s » (SoulSilver FR officiel) : homonyme mal choisi ?' % e.msgstr)
            douteux.append(o); stats['dresseur_ss_existant_different'] += 1; continue
        # sinon : une entrée par fichier Johto/Kanto (msgctxt = chemin), sûre ou douteuse selon ce fichier
        for path in paths:
            Lp = [y for y in L if y['path'] == path]
            fp = collections.Counter(y['fr'] for y in Lp).most_common(1)[0][0]
            vp = verdict(Lp, fp)
            xp = next(y for y in Lp if y['fr'] == fp)
            notep = '; '.join(sorted({'%s → %s' % (y['hns'], y['conf']) for y in Lp}))[:300]
            if hoenn: notep += ' ; msgid aussi utilisé dans %s : contexte par fichier' % ', '.join(hoenn)[:200]
            elif len(paths) > 1: notep += ' ; noms différents selon le fichier'
            o = entree(e, fp, xp['preuve'], notep + (' ; ' + vp if vp else ''), ctx=path)
            if o['fichier'] != path:   # occurrence absente du .po : on pointe sur le Dresseur lui-même
                o['fichier'] = path; o['ligne'] = xp['line'] + 1
                o['note'] += ' ; occurrence %s:%d absente des références du .po' % (path, xp['line'] + 1)
            (douteux if vp else noms).append(o); stats['dresseur_ctx' + ('_douteux' if vp else '')] += 1

    # ------------------------------------------------------------------ banques de noms
    def table(b):
        t = collections.defaultdict(set)
        for a, f in zip(en[str(b)], fr[str(b)]):
            if a.strip() and f.strip(): t[norm(a)].add(f.strip())
        return t
    T = {k: table(b) for k, b in (('objet', 222), ('capacité', 750), ('talent', 720), ('espèce', 237), ('lieu', 279), ('classe', 730), ('type', 735))}
    CLASSE_EQ = {'pkmn trainer': 'pkmn trainer', 'cooltrainer': 'ace trainer', 'pokemaniac': 'poke maniac', 'officer': 'policeman',
                 'rocket': 'team rocket', 'rocket admin': 'executive', 'pkmn breeder': 'pkmn breeder',
                 'boss': 'rocket boss', 'pkmn ranger': 'pkmn ranger'}

    def champ(e):
        for path, line in e.occurrences:
            try: src = open(os.path.join(UP, path), encoding='utf-8', errors='replace').read().split('\n')[int(line) - 1]
            except Exception: continue
            if path.endswith('items.h') and re.search(r'\.name\s*=', src): return 'objet'
            if path.endswith('moves_info.h') and re.search(r'\.name\s*=', src): return 'capacité'
            if path.endswith('abilities.h') and re.search(r'\.name\s*=', src): return 'talent'
            if 'species_info' in path and re.search(r'\.speciesName\s*=', src): return 'espèce'
            if path.endswith('region_map_sections.json'): return 'lieu'
            if path == 'src/battle_main.c' and re.search(r'TRAINER_CLASS_\w+\]\s*=', src): return 'classe'
        return None
    MAXK = {'objet': 20, 'capacité': 16, 'talent': 16, 'espèce': 12, 'classe': 12, 'lieu': 16}
    for msgid, ents in po.items():
        d, e = ents[0]
        if not dans_perimetre(e): continue
        k = champ(e)
        if not k: continue
        key = norm(msgid.replace('{PKMN}', 'PKMN'))
        if k == 'classe': key = CLASSE_EQ.get(key, key)
        fset = T[k].get(key)
        if not fset: stats['%s_absent_ss' % k] += 1; continue
        f = sorted(fset)[0]
        f = f.replace('₧₦', '{PKMN}')
        if k == 'espèce': f = f.upper()
        b = {'objet': 222, 'capacité': 750, 'talent': 720, 'espèce': 237, 'lieu': 279, 'classe': 730}[k]
        idxs = [i for i, (a, g) in enumerate(zip(en[str(b)], fr[str(b)])) if norm(a) == key]
        preuve = '%d:%d — %s' % (b, idxs[0], fr[str(b)][idxs[0]]) if idxs else str(b)
        note = '' if key == norm(msgid) else 'équivalence de classe HGSS : %s' % en[str(b)][idxs[0]]
        if k == 'lieu':
            # région de la section : Johto/Kanto/Sinnoh seulement (les noms Hoenn suivent Émeraude)
            note = (note + ' ; ' if note else '') + 'nom de lieu SS'
        o = entree(e, f, preuve, note)
        enc = G.encode(f)
        if len(fset) > 1:
            o['note'] = (note + ' ; ' if note else '') + 'plusieurs graphies SS : %s' % ' | '.join(sorted(fset)); douteux.append(o)
        elif enc is None or len(enc) > MAXK[k]:
            o['note'] = (note + ' ; ' if note else '') + 'trop long (%s > %d)' % (len(enc) if enc else '?', MAXK[k]); douteux.append(o)
        else:
            noms.append(o)
        stats[k] += 1
    print(dict(stats))
    json.dump(noms, open(os.path.join(trav, 'cand_noms.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(douteux, open(os.path.join(trav, 'cand_douteux_noms.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('noms', len(noms), 'douteux', len(douteux))


if __name__ == '__main__':
    main()
