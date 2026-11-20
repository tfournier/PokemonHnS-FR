#!/usr/bin/env python3
"""Test aller-retour de l'outillage : avec msgstr = msgid partout, la ROM doit être identique à la
ROM anglaise compilée sans aucune modification (même compilateur).

  test_aller_retour.py <dossier_projet>

1. construit la ROM anglaise de référence (aucun texte, aucune image, aucun correctif) ;
2. construit la ROM avec des .po où chaque msgstr = msgid (render/scan doivent tout restituer) ;
3. compare octet par octet.
"""
import os, sys, subprocess, tempfile, shutil, hashlib
P = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
sys.path.insert(0, os.path.join(P, 'outils'))
import polib
py = sys.executable
tmp = tempfile.mkdtemp(prefix='aller_retour_', dir=os.path.join(P, 'build'))
vide = os.path.join(tmp, 'vide'); ident = os.path.join(tmp, 'identite'); os.makedirs(vide); os.makedirs(ident)
for f in os.listdir(os.path.join(P, 'traductions')):
    if not f.endswith('.po'): continue
    po = polib.pofile(os.path.join(P, 'traductions', f))
    for e in po:
        e.msgstr = e.msgid; e.flags = [x for x in e.flags if x != 'fuzzy']
    po.save(os.path.join(ident, f))
roms = {}
for nom, d in (('reference', vide), ('identite', ident)):
    out = os.path.join(tmp, nom + '.gba')
    r = subprocess.run([py, '-I', os.path.join(P, 'outils', 'construire.py'), P, '--traductions', d,
                        '--sans-images', '--sans-correctifs', '--sortie', out], capture_output=True, text=True)
    print(r.stdout.strip().split('\n')[-3:])
    if r.returncode: print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit('échec de construction : ' + nom)
    roms[nom] = open(out, 'rb').read()
a, b = roms['reference'], roms['identite']
diff = sum(x != y for x, y in zip(a, b)) + abs(len(a) - len(b))
print('reference %s\nidentite  %s' % (hashlib.sha1(a).hexdigest(), hashlib.sha1(b).hexdigest()))
shutil.rmtree(tmp)
if diff:
    sys.exit('ÉCHEC : %d octets diffèrent' % diff)
print('OK : ROM identique')
