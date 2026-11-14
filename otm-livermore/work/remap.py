"""Re-time gen.py to a new take: align the old and new word lists (difflib on normalised tokens) and rewrite every word
index gen.py uses (ix(N), the YEARS / RULES / arrow / slip tuples) to the matching index in the new take.
Usage: python3 work/remap.py OLD_words.json NEW_words.json   (rewrites work/gen.py in place, prints the changes)"""
import difflib, json, re, sys

old = json.load(open(sys.argv[1])); new = json.load(open(sys.argv[2]))
def n(t): return re.sub(r"[^a-z0-9']", "", t.lower())
a, b = [n(w["text"]) for w in old], [n(w["text"]) for w in new]
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
M = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            M[i1 + k] = j1 + k
def m(i):
    if i in M:
        return M[i]
    lo = max([k for k in M if k < i], default=None)              # nearest aligned word before it, same offset
    return M[lo] + (i - lo) if lo is not None else i

src = open("work/gen.py").read()
changes = []
def sub(pat, fmt):
    global src
    def r(mo):
        i = int(mo.group("i")); j = m(i)
        if i != j:
            changes.append((mo.group(0), i, j, a[i] if i < len(a) else "?", b[j] if j < len(b) else "?"))
        return fmt(mo, j)
    src = re.sub(pat, r, src)
sub(r"ix\((?P<i>\d+)\)", lambda mo, j: f"ix({j})")
sub(r"\((?P<y>1[89]\d\d), (?P<i>\d+)\)", lambda mo, j: f"({mo.group('y')}, {j})")
sub(r'\("(?P<t>[A-Z][A-Z ,·%\'0-9]+)", (?P<i>\d+)\)', lambda mo, j: f'("{mo.group("t")}", {j})')
sub(r"\((?P<b>True|False), (?P<i>\d+)\)", lambda mo, j: f"({mo.group('b')}, {j})")
open("work/gen.py", "w").write(src)
bad = [c for c in changes if c[3] != c[4]]
print(len(changes), "indices moved;", len(bad), "landed on a different word:")
for c in bad:
    print("  ", c)
