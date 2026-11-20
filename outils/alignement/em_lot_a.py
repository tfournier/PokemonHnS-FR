#!/usr/bin/env python3
"""Relance complète du lot A (Émeraude US <-> Émeraude FR).

  .venv/bin/python outils/alignement/em_lot_a.py
Variables : LOTA_TMP (dossier des mémoires intermédiaires, défaut memoires/lotA).
Étapes : em_pointeurs -> em_candidats -> em_tables -> em_approche -> em_sortie -> verifier.py
"""
import os, sys, subprocess
H = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(os.path.dirname(H))
py = sys.executable
for s in ('em_pointeurs.py', 'em_candidats.py', 'em_tables.py', 'em_approche.py', 'em_sortie.py'):
    print('==>', s, flush=True)
    subprocess.run([py, os.path.join(H, s)], check=True)
L = os.path.join(P, 'traductions', 'lots', 'A_emeraude')
fichiers = [os.path.join(L, f + '.json') for f in ('exact', 'contexte', 'tables', 'adapte', 'douteux')]
subprocess.run([py, os.path.join(P, 'outils', 'verifier.py'), os.path.join(P, 'build', 'upstream_orig')] + fichiers
               + ['--sortie', os.path.join(L, 'verifications.tsv')])
