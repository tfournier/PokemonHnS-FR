#!/usr/bin/env python3
"""Lot B : paires (banque, index, anglais HGSS, français SoulSilver) contrôlées banque par banque.

  ss_paires.py --phg <clone partiel de pret/pokeheartgold> --travail <dossier de sortie>
               [--rom "roms/Pokemon Argent SoulSilver FR.nds"]

Clone partiel conseillé (quelques Mo) :
  git clone --depth 1 --filter=blob:none --sparse https://github.com/pret/pokeheartgold.git phg
  cd phg && git sparse-checkout set --no-cone '/files/msgdata/msg/*' '/tools/msgenc/charmap.txt' \
      '/files/msgdata/NARC_msg.txt' '/files/poketool/trainer/*'

Sorties dans --travail :
  ss_en.json, ss_fr.json   banques {banque: [lignes]} au format pret (vrais \n \r \f, {STRVAR_1 t, i, x})
  ss_paires.json           [[banque, index, en, fr], ...] (lignes vides / « garbage » exclues)
  ss_banques.tsv           qualité par banque : nombres de lignes EN/FR, taux de codes et de nombres cohérents
"""
import os, re, sys, json, glob, collections

P = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def opt(args, n, d=None):
    if n in args:
        i = args.index(n); v = args[i + 1]; del args[i:i + 2]; return v
    return d


def banques_en(phg):
    out = {}
    for f in glob.glob(os.path.join(phg, 'files/msgdata/msg/msg_*.json')):
        b = int(re.match(r'msg_(\d+)', os.path.basename(f)).group(1))
        d = json.load(open(f, encoding='utf-8'))
        L = []
        for m in d['messages']:
            t = m.get('en_US', '')
            if isinstance(t, list): t = ''.join(t)
            L.append(t)
        out[b] = L
    tr = json.load(open(os.path.join(phg, 'files/poketool/trainer/trainers.json'), encoding='utf-8'))['trainers']
    out[729] = [t['name'] for t in tr]
    return out


STRV = re.compile(r'\{STRVAR_(\w+) (\d+), (\d+)(?:, (\d+))?\}')
CODE = re.compile(r'\{[^}]*\}')
NUM = re.compile(r'\d+')


def cles(s):
    return collections.Counter((m.group(1), m.group(2), m.group(3)) for m in STRV.finditer(s))


def nombres(s):
    return sorted(NUM.findall(CODE.sub('', s)))


def main():
    args = sys.argv[1:]
    phg = opt(args, '--phg'); trav = opt(args, '--travail')
    rom = opt(args, '--rom', os.path.join(P, 'roms', 'Pokemon Argent SoulSilver FR.nds'))
    os.makedirs(trav, exist_ok=True)
    import gen4msg, ndspy.rom, ndspy.narc
    gen4msg.charger_charmap(os.path.join(phg, 'tools/msgenc/charmap.txt'))
    gen4msg.FORMAT = 'pret'
    narc = ndspy.narc.NARC(ndspy.rom.NintendoDSRom.fromFile(rom).getFileByName('a/0/2/7'))
    fr = {}
    for i, f in enumerate(narc.files):
        try: fr[i] = gen4msg.bank(f)
        except Exception: fr[i] = None
    en = banques_en(phg)
    json.dump(en, open(os.path.join(trav, 'ss_en.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(fr, open(os.path.join(trav, 'ss_fr.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    paires = []; rows = []
    for b in sorted(set(en) | set(fr)):
        E, F = en.get(b) or [], fr.get(b) or []
        n = ok_c = ok_n = 0
        for i, (e, f) in enumerate(zip(E, F)):
            if not e.strip() or not f.strip(): continue
            n += 1
            c = cles(e) == cles(f); ok_c += c
            ne = nombres(e); nf = nombres(f); ok_n += (ne == nf)
            paires.append([b, i, e, f])
        rows.append((b, len(E), len(F), n, ok_c / n if n else 1, ok_n / n if n else 1))
    json.dump(paires, open(os.path.join(trav, 'ss_paires.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    with open(os.path.join(trav, 'ss_banques.tsv'), 'w', encoding='utf-8') as fo:
        fo.write('banque\tlignes_en\tlignes_fr\tpaires\tcodes_ok\tnombres_ok\n')
        for r in rows: fo.write('%d\t%d\t%d\t%d\t%.3f\t%.3f\n' % r)
    print(len(paires), 'paires ;', sum(1 for r in rows if r[1] != r[2]), 'banques de taille différente')


if __name__ == '__main__':
    main()
