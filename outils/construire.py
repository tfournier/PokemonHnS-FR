#!/usr/bin/env python3
"""Construit la ROM française à partir du code upstream + traductions + images + correctifs.

  construire.py <dossier_projet> [--source <clone upstream existant>] [--jobs N]
                [--traductions <dossier .po>] [--sans-images] [--sans-correctifs] [--sortie <rom.gba>]
                [--patch-emeraude]
  (patch distribué : sur Heart & Soul anglais seulement ; --patch-emeraude produit en plus celui sur
   Émeraude US, gardé au cas où mais non distribué)
  (--sortie : construction de test, ni rapport ni patchs ; utilisé par test_aller_retour.py)

Étapes : copie propre du code upstream à la version de upstream.txt, images (avec contrôle
d'empreinte), correctifs de code, textes, compilation (`make hns`), puis patchs.
Si un texte français dépasse la taille d'un champ fixe (noms d'objets, de types…), il est
remis en anglais et listé dans rapport/trop_longs.txt pour être raccourci dans le .po.
"""
import os, sys, re, subprocess, shutil, hashlib, glob
sys.path.insert(0, os.path.dirname(__file__))
import hnsfr

P = os.path.abspath(sys.argv[1])
args = sys.argv[2:]
src = args[args.index('--source') + 1] if '--source' in args else None
jobs = args[args.index('--jobs') + 1] if '--jobs' in args else str(os.cpu_count() or 4)
podir = os.path.abspath(args[args.index('--traductions') + 1]) if '--traductions' in args else os.path.join(P, 'traductions')
sans_images = '--sans-images' in args          # test aller-retour : textes seuls
sans_code = '--sans-correctifs' in args
sortie = os.path.abspath(args[args.index('--sortie') + 1]) if '--sortie' in args else None
patch_emeraude = '--patch-emeraude' in args
tag = open(os.path.join(P, 'upstream.txt')).read().strip()
work = os.path.join(P, 'build', 'upstream')
rep = os.path.join(P, 'rapport'); os.makedirs(rep, exist_ok=True)
URL = 'https://github.com/PokemonHnS-Development/pokehns-expansion'

def run(cmd, cwd=None, check=True, out=None):
    r = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), stdout=out or subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True)
    if check and r.returncode != 0:
        print(r.stdout[-3000:] if r.stdout else ''); sys.exit('échec : %s' % cmd)
    return r

# 1. code upstream propre
if not os.path.isdir(os.path.join(work, '.git')):
    os.makedirs(os.path.dirname(work), exist_ok=True)
    if src:
        run(['git', 'clone', '-q', src, work])
    else:
        run(['git', 'clone', '-q', '--depth', '1', '--branch', tag, URL, work])
run(['git', 'fetch', '-q', '--depth', '1', 'origin', 'tag', tag], cwd=work, check=False)
run(['git', 'checkout', '-q', '-f', tag], cwd=work)
run(['git', 'reset', '-q', '--hard', tag], cwd=work)
run(['git', 'clean', '-q', '-fd', '-e', 'build', '-e', 'tools'], cwd=work)
print('upstream :', tag)

# 2. images (on vérifie que l'original upstream n'a pas changé depuis notre traduction)
emp = {}
for line in open(os.path.join(P, 'images', 'EMPREINTES_ORIGINAUX.txt')):
    h, f = line.split(None, 1); emp[f.strip()] = h
warn = []
for f, h in ({} if sans_images else emp).items():
    cur = os.path.join(work, f)
    if os.path.exists(cur) and hashlib.sha1(open(cur, 'rb').read()).hexdigest() != h:
        warn.append(f); continue          # upstream a modifié l'image : on garde la leur, à retraduire
    shutil.copy(os.path.join(P, 'images', f), cur)
if not sortie: open(os.path.join(rep, 'images_a_revoir.txt'), 'w').write('\n'.join(warn) + '\n')
print('images : %d copiées, %d à revoir' % (len(emp) - len(warn), len(warn)))

# 3. correctifs de code
for pt in ([] if sans_code else sorted(glob.glob(os.path.join(P, 'code', '*.patch')))):
    r = run(['git', 'apply', pt], cwd=work, check=False)
    print('correctif %s : %s' % (os.path.basename(pt), 'OK' if r.returncode == 0 else 'NE S’APPLIQUE PLUS'))

# 4. textes
st, pb = hnsfr.apply(work, podir, os.path.join(rep, 'textes.txt') if not sortie else None)
print('textes :', dict(st))

# 5. compilation, avec repli en anglais des textes trop longs
trop = []
ERR = re.compile(r'^(src/[^:]+):(\d+):\d+: error: (excess elements in array initializer|initializer-string for array)', re.M)
for tour in range(6):
    r = run(['make', 'hns', '-j' + jobs], cwd=work, check=False)
    open(os.path.join(rep, 'compilation.log' if not sortie else 'compilation_test.log'), 'w').write(r.stdout)
    if r.returncode == 0: break
    bad = sorted(set((m.group(1), int(m.group(2))) for m in ERR.finditer(r.stdout)))
    if not bad:
        print(r.stdout[-3000:]); sys.exit('échec de compilation (voir rapport/compilation.log)')
    up = hnsfr.scan  # reverting: restore the original upstream line content for each failing line
    for f, ln in bad:
        orig = run(['git', 'show', '%s:%s' % (tag, f)], cwd=work).stdout.split('\n')
        cur = open(os.path.join(work, f), encoding='utf-8').read().split('\n')
        trop.append('%s:%d  %s' % (f, ln, cur[ln-1].strip()))
        cur[ln-1] = orig[ln-1]
        open(os.path.join(work, f), 'w', encoding='utf-8').write('\n'.join(cur))
else:
    sys.exit('échec de compilation')
print('trop longs remis en anglais :', len(trop))
if sortie:
    shutil.copy(os.path.join(work, 'pokehns.gba'), sortie); print('ROM :', sortie); sys.exit(0)
open(os.path.join(rep, 'trop_longs.txt'), 'w', encoding='utf-8').write('\n'.join(trop) + '\n')
out = os.path.join(P, 'build', 'pokehns_fr.gba')
shutil.copy(os.path.join(work, 'pokehns.gba'), out)
print('ROM :', out)

# 6. patchs (ROM de base fournie par l'utilisateur dans memoires/, jamais distribuée)
mem = os.path.join(P, 'memoires'); dist = os.path.join(P, 'dist'); os.makedirs(dist, exist_ok=True)
nom = 'PokemonHnS_%s_FR' % tag.replace('Release-', '')
cibles = [('hns_en.gba', 'sur_HnS_anglais')] + ([('emeraude_us.gba', 'sur_Emeraude_US')] if patch_emeraude else [])
for base, suffixe in cibles:
    b = os.path.join(mem, base)
    if os.path.exists(b):
        dst = os.path.join(dist, '%s_%s.ups' % (nom, suffixe))
        run([sys.executable, '-I', os.path.join(os.path.dirname(__file__), 'ups.py'), b, out, dst])
        import ups_appliquer
        if ups_appliquer.appliquer(open(b, 'rb').read(), open(dst, 'rb').read()) != open(out, 'rb').read():
            sys.exit('patch %s : la ROM obtenue diffère de la ROM construite' % dst)
        print('patch :', dst, '(vérifié : appliqué à %s, il redonne la ROM construite)' % base)
