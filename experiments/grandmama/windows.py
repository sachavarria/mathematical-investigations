"""Exhaustive diagnostic. Compare window's least rotation to its host block."""
from itertools import product

def necklace(w):
    return min(w[i:]+w[:i] for i in range(len(w)))

def root(w):
    return next(w[:i] for i in range(1,len(w)+1) if w[:i]*(len(w)//i)==w)

def measure(n):
    words = map(''.join, product('01', repeat=n))
    reps = sorted({necklace(w) for w in words}, key=lambda w:w[::-1])
    clock = ''.join(root(w) for w in reps)
    hosts = [w for w in reps for _ in root(w)]
    windows = [(clock+clock)[i:i+n] for i in range(len(clock))]
    assert len(set(windows)) == len(hosts) == 2**n
    return sum(necklace(w)==host for w,host in zip(windows,hosts)), len(windows)

if __name__ == '__main__':
    for n in range(2,13):
        print(n,*measure(n))
