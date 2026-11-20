"""Extrait les banques de messages Gen 4 (HGSS) d'une ROM NDS en JSON {banque: [lignes]}.

  gen4msg.py <rom.nds> <chemin NARC, ex. a/0/2/7> <sortie.json> [--charmap tools/msgenc/charmap.txt]
             [--format pret]

Charmap : celle de pret/pokeheartgold (tools/msgenc/charmap.txt). Par défaut on cherche
$P/../phg/tools/msgenc/charmap.txt puis la variable d'environnement PHG_CHARMAP.

Format des codes :
  - par défaut (format historique de memoires/ss_fr_msg.json) : {STRVAR_1 1 0, 0}, retours écrits « \\n », « \\r », « \\f » ;
  - --format pret : {STRVAR_1 1, 0, 0} comme les JSON de pret/pokeheartgold.
Les noms compressés (0xF100, banque 729 des noms de Dresseurs) sont décodés (caractères de 9 bits)
et précédés de {TRNAME} comme dans pret.
"""
import ndspy.rom, ndspy.narc, struct, json, sys, os

chars, cmds, strvars = {}, {}, set()


def charger_charmap(path):
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n').split('//')[0] if not line.startswith('//') else ''
        if '=' not in line: continue
        k, v = line.split('=', 1)
        try: code = int(k.strip(), 16)
        except ValueError: continue
        if v.startswith('{') and v.endswith('}'): cmds[code] = v[1:-1]
        else: chars.setdefault(code, v)
    strvars.update(c & 0xFF00 for c, n in cmds.items() if n.startswith('STRVAR_'))


FORMAT = 'ancien'


def decode(u):
    out = []; j = 0
    while j < len(u):
        c = u[j]
        if c == 0xFFFF: break
        if c == 0xFFFE:
            code = u[j+1]; n = u[j+2]; args = u[j+3:j+3+n]
            if (code & 0xFF00) in strvars:
                if FORMAT == 'pret':
                    name = 'STRVAR_%X %s' % (code >> 8, ', '.join(map(str, [code & 0xFF] + list(args))))
                    out.append('{%s}' % name); j += 3 + n; continue
                name = 'STRVAR_%X %d' % (code >> 8, code & 0xFF)
            else: name = cmds.get(code, 'CMD_%04X' % code)
            out.append('{%s%s}' % (name, (' ' + ', '.join(map(str, args))) if args else ''))
            j += 3 + n; continue
        if c == 0xF100:   # chaîne compressée : caractères de 9 bits
            out.append('{TRNAME}')
            cont = 0; bits = 0
            for w in u[j+1:]:
                cont |= (w & 0x7FFF) << bits; bits += 15
                fin = False
                while bits >= 9:
                    ch = cont & 0x1FF; cont >>= 9; bits -= 9
                    if ch == 0x1FF: fin = True; break
                    out.append(chars.get(ch, '[%04X]' % ch))
                if fin: break
            break
        ch = chars.get(c, '[%04X]' % c)
        if FORMAT == 'pret' and ch in ('\\n', '\\r', '\\f'): ch = {'\\n': '\n', '\\r': '\r', '\\f': '\f'}[ch]
        out.append(ch); j += 1
    return ''.join(out)


def bank(data):
    count, key = struct.unpack_from('<HH', data)
    lines = []
    for i in range(1, count + 1):
        off, ln = struct.unpack_from('<II', data, 4 + 8 * (i - 1))
        ak = (765 * i * key) & 0xFFFF; ak |= ak << 16
        off ^= ak; ln ^= ak
        u = list(struct.unpack_from('<%dH' % ln, data, off))
        k = (i * 596947) & 0xFFFF
        for t in range(ln):
            u[t] ^= k; k = (k + 18749) & 0xFFFF
        lines.append(decode(u))
    return lines


def main():
    global FORMAT
    args = sys.argv[1:]
    cm = None
    if '--charmap' in args:
        i = args.index('--charmap'); cm = args[i + 1]; del args[i:i + 2]
    if '--format' in args:
        i = args.index('--format'); FORMAT = args[i + 1]; del args[i:i + 2]
    if cm is None:
        P = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        cm = os.environ.get('PHG_CHARMAP') or os.path.join(P, '..', 'phg', 'tools', 'msgenc', 'charmap.txt')
    charger_charmap(cm)
    rom = ndspy.rom.NintendoDSRom.fromFile(args[0])
    narc = ndspy.narc.NARC(rom.getFileByName(args[1]))
    out = {}
    for i, f in enumerate(narc.files):
        try: out[i] = bank(f)
        except Exception: out[i] = None
    json.dump(out, open(args[2], 'w', encoding='utf-8'), ensure_ascii=False)
    print(len(out), 'banks', sum(len(v) for v in out.values() if v), 'lines')


if __name__ == '__main__':
    main()
