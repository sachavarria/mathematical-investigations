"""Deterministic truth-table controls. Coordinate zero is the least significant bit."""
from itertools import combinations

def step(x,n,rule):
    mask=(1<<n)-1
    left = (x<<1) if rule in ('linear','mixed') else 0
    interaction = ((x<<1)&(x<<2)) if rule in ('product','mixed') else 0
    return (x^left^interaction)&mask

def columns(n,rule):
    trajectories=[[] for _ in range(n)]
    for x in range(1<<n):
        y=x
        for col in trajectories:
            col.append(y>>(n-1))
            y=step(y,n,rule)
    assert len({step(x,n,rule) for x in range(1<<n)})==1<<n
    return trajectories

def support(col,n):
    return [j for j in range(n) if any(col[x]!=col[x^(1<<j)] for x in range(1<<n))]

def classes(col,n,i):
    # First i low-index cells arrive before the remaining cells.
    return len({tuple(col[a|(b<<i)] for b in range(1<<(n-i))) for a in range(1<<i)})

def mask_rows(n,t):
    return sum(1<<(n-1-j) for j in range(n) if j&t==j)

def linear_checks(n):
    cols=columns(n,'linear')
    for t,col in enumerate(cols):
        mask=mask_rows(n,t)
        assert col==[(x&mask).bit_count()%2 for x in range(1<<n)]
        assert len(support(col,n))==2**t.bit_count()
    for k in range(n+1):
        for family in combinations(range(n),k):
            answers={tuple(cols[t][x] for t in family) for x in range(1<<n)}
            assert len(answers)==1<<k

def graph(m):
    def answer(x,y):
        # The paths s -> v_j -> t have indicators x_j and y_j.
        return any(x>>j&1 and y>>j&1 for j in range(m))
    size=1<<m
    blocked={tuple(bool(answer(x,y)) for y in range(size)) for x in range(size)}
    order=[(j,c) for j in range(m) for c in range(2)]
    data=[]
    for value in range(size*size):
        x=sum(((value>>i)&1)<<j for i,(j,c) in enumerate(order) if c==0)
        y=sum(((value>>i)&1)<<j for i,(j,c) in enumerate(order) if c==1)
        data.append(bool(answer(x,y)))
    profile=[classes(data,2*m,i) for i in range(2*m+1)]
    assert len(blocked)==size and max(profile)<=3
    return len(blocked),profile

if __name__=="__main__":
    n=8
    linear_checks(n)
    print("Linear chain: all 256 states, 8 times and 256 possible time families verified.")
    print("Graph: blocked midpoint states and interleaved profile, m=6:",graph(6))
    for rule in ('linear','mixed','product'):
        cols=columns(n,rule)
        print(rule, "n=8: t / support / exact residual states / parity-control states at cut 4")
        for t,col in enumerate(cols):
            mask=sum(1<<j for j in support(col,n))
            parity=[(x&mask).bit_count()%2 for x in range(1<<n)]
            assert sum(col)==sum(parity)==128
            print(t,format(mask,"08b"),classes(col,n,4),classes(parity,n,4))
