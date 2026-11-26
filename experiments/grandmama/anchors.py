"""Exhaustive checks for the binary colex necklace concatenation."""
from itertools import product
from fractions import Fraction
import csv
from windows import necklace, root

def clock(n):
    reps = sorted({necklace(''.join(x)) for x in product('01', repeat=n)},
                  key=lambda w:w[::-1])
    blocks = [root(w) for w in reps]
    return reps, blocks, ''.join(blocks)

def check(n):
    reps, blocks, cycle = clock(n)
    N = 2**n
    assert len(cycle) == N
    words = [(cycle+cycle)[i:i+n] for i in range(N)]
    assert len(set(words)) == N
    observed = [i for i,w in enumerate(words) if w == necklace(w) and len(root(w)) == n]
    expected = []
    t = 0
    for w,b in zip(reps,blocks):
        if len(b)==n:
            expected.append(t)
        t += len(b)
    assert observed == expected
    gaps = [b-a for a,b in zip(expected,expected[1:]+[expected[0]+N])]
    T = N-len(expected)*n
    mean = Fraction(sum(g*(g-1) for g in gaps),2*N)
    assert mean == Fraction(n-1,2)+Fraction(n*T+sum((g-n)**2 for g in gaps),2*N)
    p = next((i for i in range(2,n+1) if n%i==0))
    return n, len(expected),T,max(gaps), n+max(2,n//p), str(mean)
if __name__ == '__main__':
    import sys
    out=csv.writer(sys.stdout)
    out.writerow(['order','anchors','short_length','max_gap','conjectured_gap','mean_backward_steps'])
    for n in range(2,17):
        out.writerow(check(n))
