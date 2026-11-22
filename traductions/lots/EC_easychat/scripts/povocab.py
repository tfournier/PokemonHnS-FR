import polib, glob, re, os
from eclib import *
def po_entries():
    d = {}
    for f in glob.glob(P + '/traductions/*.po'):
        for e in polib.pofile(f):
            for occ, ln in e.occurrences:
                d[(occ, int(ln) if ln else 0)] = e
    return d
def vocab():
    """(groupId, index) -> (en, fr_msgstr or None)"""
    pe = po_entries(); X = Consts(UP); V = {}
    for f in sorted(glob.glob(UP + '/src/data/easy_chat/easy_chat_group_*.h')):
        rel = os.path.relpath(f, UP); lines = open(f).read().split('\n'); cur = None
        for i, l in enumerate(lines, 1):
            m = re.search(r'\[EC_INDEX\((EC_WORD_[A-Z0-9_]+)\)\]', l)
            if m: cur = X.words[m.group(1)]
            m = re.search(r'\.text = COMPOUND_STRING\("(.*)"\)', l)
            if m and cur is not None:
                e = pe.get((rel, i))
                V[(cur >> 9, cur & 511)] = (m.group(1), e.msgstr if e and e.msgstr else None)
                cur = None
    return V
if __name__ == '__main__':
    V = vocab(); print(len(V), sum(1 for v in V.values() if v[1] is None))
    print([ (GROUPS[k[0]],k[1],v) for k,v in V.items() if v[1] is None][:20])
