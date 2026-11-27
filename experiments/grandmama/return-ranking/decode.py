"""Rank a binary Grandmama window from its bits; no cycle or rank table."""
from return_rank import ranks

def is_representative(w):
    return all(w <= w[i:]+w[:i] for i in range(1,len(w)))

def predecessor(w):
    # Invert PCR2 (First 1): the flip predicate depends only on the shared tail.
    tail=w[:-1]
    prefix=tail.rstrip("0")
    test="0"*(len(tail)-len(prefix))+"1"+prefix
    incoming=int(w[-1]) ^ int(is_representative(test))
    return str(incoming)+tail

def decode(w):
    if not w or set(w)-set("01"):
        raise ValueError("expected a nonempty binary word")
    if len(w)==1:
        return int(w)
    origin=w
    for distance in range(len(w)+max(2,len(w)//2)):
        if all(w < w[i:]+w[:i] for i in range(1,len(w))):
            return (ranks(w)[0]+distance) % (1<<len(w))
        w=predecessor(w)
    raise ArithmeticError("gap bound failed for "+origin)

def check():
    from collections import Counter
    for n in range(1,10):
        N=1<<n
        words=[format(i,'0%db'%n) for i in range(N)]
        masses=Counter(min(w[i:]+w[:i] for i in range(n)) for w in words)
        clock="".join(w[:masses[w]] for w in sorted(masses,key=lambda w:w[::-1]))
        words=[(clock*2)[i:i+n] for i in range(N)]
        for i,w in enumerate(words):
            assert predecessor(w)==words[i-1]
            assert decode(w)==i
        print(n,N)
if __name__=="__main__":
    import sys
    if sys.argv[1:]==['--check']:
        check()
    else:
        print(decode(sys.argv[1]))
