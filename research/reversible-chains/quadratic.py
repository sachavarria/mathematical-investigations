"""Exact one-step scalar-parity response width from local quadratic coefficients."""
from itertools import product


def bits(mask):
    while mask:
        unit = mask & -mask
        yield unit.bit_length()-1
        mask ^= unit


def relations(vectors):
    """Rank and a basis of dependencies among the given binary vectors."""
    pivots = {}
    null = []
    for j,v in enumerate(vectors):
        combination = 1<<j
        while v:
            pivot = v.bit_length()-1
            if pivot not in pivots:
                pivots[pivot] = (v,combination)
                break
            other,coeff = pivots[pivot]
            v ^= other
            combination ^= coeff
        if not v:
            null.append(combination)
    return len(pivots),null


def predicted(n,rule,observed,read):
    prefix = list(bits(read))
    index = {site:j for j,site in enumerate(prefix)}
    slopes = [0]*len(prefix)
    linear = 0
    edges = []
    c = rule&1
    left = c^((rule>>2)&1)
    second = c^((rule>>1)&1)
    nonlinear = rule.bit_count()%2
    for i in bits(observed):
        for j,term in ((i,1),(i-1,left),(i-2,second)):
            if term and j in index:
                linear ^= 1<<index[j]
        if nonlinear and i>=2:
            a,b = i-1,i-2
            if a in index and b in index:
                edges.append((index[a],index[b]))
            elif a in index:
                slopes[index[a]] ^= 1<<b
            elif b in index:
                slopes[index[b]] ^= 1<<a
    r,kernel = relations(slopes)
    def polar(k):
        w = 0
        for a,b in edges:
            w ^= ((k>>a)&1)<<b
            w ^= ((k>>b)&1)<<a
        return w
    coefficients = [polar(k) for k in kernel]
    if any((w&k).bit_count()%2 for w in coefficients for k in kernel):
        return 2<<r
    system=[]
    for k,w in zip(kernel,coefficients):
        value = (linear&k).bit_count()
        value += sum(((k>>a)&1)*((k>>b)&1) for a,b in edges)
        system.append(w | ((value%2)<<len(prefix)))
    h = relations(coefficients)[0]
    if relations(system)[0]>h:
        return 2<<r
    return (2<<r)-(1<<(r-h))


def direct(n,rule,observed,read):
    rows={}
    for x in range(1<<n):
        y=0
        for i in range(n):
            a = x>>(i-1)&1 if i>=1 else 0
            b = x>>(i-2)&1 if i>=2 else 0
            y |= (((x>>i)&1)^((rule>>(2*a+b))&1))<<i
        rows.setdefault(x&read,[]).append((y&observed).bit_count()%2)
    return len({tuple(row) for row in rows.values()})


if __name__=="__main__":
    checks=0
    for n in range(1,6):
        for rule,obs,cut in product(range(16),range(1<<n),range(1<<n)):
            a=predicted(n,rule,obs,cut)
            assert a==direct(n,rule,obs,cut),(n,rule,obs,cut,a)
            checks+=1
    print("Exact one-step cut widths vs literal rows:",checks)
    for n in (6,24,96):
        odds=sum(1<<i for i in range(1,n,2))
        evens=((1<<n)-1)^odds
        print("n",n,"odd-site parity, even-first state counts (mask order 0..15):",
              [predicted(n,r,odds,evens) for r in range(16)])
