"""Retrouve dans une ROM traduite le bloc qui correspond à un bloc de la ROM US : on cherche le pointeur US,
puis le même code autour de ce pointeur dans l'autre ROM (fenêtres de 10 octets uniques, décalage majoritaire)."""
import struct
from collections import Counter

def ptrs(rom, adr):
    p = struct.pack('<I', 0x08000000 + adr); out = []; i = rom.find(p)
    while i >= 0:
        out.append(i); i = rom.find(p, i + 1)
    return out

def counterpart(us, fr, adr, before=400):
    """renvoie [(pointeur US, emplacement FR, adresse FR pointée)] pour les pointeurs ROM voisins de
    l'emplacement estimé (le pool de littéraux peut être décalé de quelques mots) : à confirmer à l'œil"""
    res = []
    for p in ptrs(us, adr):
        C = Counter()
        for off in range(-before, 40, 2):
            pat = us[p + off:p + off + 10]; i = fr.find(pat)
            if i >= 0 and fr.find(pat, i + 1) < 0: C[i - (p + off)] += 1
        if C:
            q0 = p + C.most_common(1)[0][0]
            for q in range(q0 - 8, q0 + 12, 4):
                v = struct.unpack_from('<I', fr, q)[0]
                if 0x08000000 <= v < 0x0A000000: res.append((p, q, v - 0x08000000))
    return res
