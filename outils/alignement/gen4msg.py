"""Extract Gen 4 (HGSS) message banks from an NDS ROM into JSON {bank: [lines]}."""
import ndspy.rom, ndspy.narc, struct, json, sys, re
CM = '/home/claude/phg/tools/msgenc/charmap.txt'
chars, cmds = {}, {}
for line in open(CM, encoding='utf-8'):
    line = line.rstrip('\n').split('//')[0] if not line.startswith('//') else ''
    if '=' not in line: continue
    k, v = line.split('=', 1)
    try: code = int(k.strip(), 16)
    except ValueError: continue
    if v.startswith('{') and v.endswith('}'): cmds[code] = v[1:-1]
    else: chars.setdefault(code, v)
strvars = {c & 0xFF00 for c, n in cmds.items() if n.startswith('STRVAR_')}

def decode(u):
    out = []; j = 0
    while j < len(u):
        c = u[j]
        if c == 0xFFFF: break
        if c == 0xFFFE:
            code = u[j+1]; n = u[j+2]; args = u[j+3:j+3+n]
            if (code & 0xFF00) in strvars: name = 'STRVAR_%X %d' % (code >> 8, code & 0xFF)
            else: name = cmds.get(code, 'CMD_%04X' % code)
            out.append('{%s%s}' % (name, (' ' + ', '.join(map(str, args))) if args else ''))
            j += 3 + n; continue
        if c == 0xF100: out.append('{TRNAME}'); break
        out.append(chars.get(c, '[%04X]' % c)); j += 1
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

rom = ndspy.rom.NintendoDSRom.fromFile(sys.argv[1])
narc = ndspy.narc.NARC(rom.getFileByName(sys.argv[2]))
out = {}
for i, f in enumerate(narc.files):
    try: out[i] = bank(f)
    except Exception as e: out[i] = None
json.dump(out, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False)
print(len(out), 'banks', sum(len(v) for v in out.values() if v), 'lines')
