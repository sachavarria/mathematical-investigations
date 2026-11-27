"""First-return frequency slices via polynomially many literal run-head prefixes."""
from pathlib import Path
import sys
root=Path(__file__).resolve().parent.parent
sys.path.append(str(root/"competing-origins" if (root/"competing-origins").is_dir() else root/"originrank"))
from composition import accepted
from transfer import base

def slices(a,R,d=None):
    n=len(a)
    if not n or set(a)-set("01") or R<1 or d is not None and not 0<=d<=n:
        raise ValueError("invalid input")
    values=[0]*(R+1)
    for p in base(n):
        if len(p)==n:
            w="0"+p[:-1]
            if w[::-1]<a[::-1] and (d is None or d==w.count("1")): values[1]+=n
        else:
            counts=accepted(a,"0"+p,R,d)
            for t in range(1,R+1): values[t]+=counts[t]
    return values
