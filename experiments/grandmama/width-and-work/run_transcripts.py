"""Single-exponential primitive-width weighted colex ranking; no third-party packages."""
from functools import lru_cache
from itertools import groupby
from math import gcd


def primitive_transcripts(r):
    # Prenecklace extension, as used in the archived fixed-density counter.
    def walk(j, period, edges):
        if j == r:
            if period == r:
                yield edges
            return
        source = j-period
        yield from walk(j+1, period, edges+((source, j, True),))
        yield from walk(j+1, j+1, edges+((source, j, False),))
    yield from walk(1, 1, ())


def boxes(r, key):
    # Disjoint first unequal run cases. Intervals for zero length then one length.
    n = len(key)
    if key[0] == "0":
        return
    bounds = [[1,n,1,n] for _ in range(r)]
    for j, (_, group) in enumerate(groupby(key)):
        if j == 2*r:
            break
        q = sum(1 for _ in group)
        i = r-1-j//2
        low = 2 if j%2 == 0 else 0
        if low == 2:
            bounds[i][3] = q-1
        else:
            bounds[i][0] = q+1
        if bounds[i][low] <= bounds[i][low+1]:
            yield tuple(map(tuple, bounds))
        bounds[i][low] = bounds[i][low+1] = q


def assignments(z, o, restrictions, edges):
    r = len(restrictions)
    full = (1<<r)-1
    states = {(0,0,0): 1}
    for a in range(z-r+1,0,-1):
        for b in range(1,o-r+2):
            allowed = sum(1<<i for i,(lo,hi,low,high) in enumerate(restrictions)
                          if lo<=a<=hi and low<=b<=high)
            if not allowed:
                continue
            layer = dict(states)
            for (done,zeros,ones), count in states.items():
                available = allowed & ~done
                subset = available
                while subset:
                    size = subset.bit_count()
                    newz,newo = zeros+size*a,ones+size*b
                    if newz <= z and newo <= o:
                        ok = True
                        for src,dest,equal in edges:
                            has_src = (subset>>src)&1
                            has_dest = (subset>>dest)&1
                            if equal and has_src != has_dest:
                                ok = False
                                break
                            if not equal and has_dest and not ((done>>src)&1):
                                ok = False
                                break
                        if ok:
                            state = (done|subset, newz, newo)
                            layer[state] = layer.get(state,0)+count
                    subset = (subset-1)&available
            states = layer
    return states.get((full,z,o),0)


@lru_cache(maxsize=2048)
def primitive(n,z,d,end):
    if end <= 0:
        return 0
    if n == 1:
        return int(1-z<end)
    o = n-z
    total = 0
    for r in range(1, min(z,o,d)+1):
        cases = tuple(boxes(r, format(end, f"0{n}b"))) if end < 1<<n else (((1,n,1,n),)*r,)
        for edges in primitive_transcripts(r):
            for restrictions in cases:
                total += assignments(z,o,restrictions,edges)
    return total


def rank_key(n,z,d,key):
    """Fixed zero count z and cap d on the primitive root. key is the reversed integer cutoff."""
    if n<1 or not (0<=z<=n) or d<0 or not (0<=key<=1<<n):
        raise ValueError("invalid input")
    result = 0
    for rep in range(1,gcd(n,z)+1):
        if n%rep or z%rep:
            continue
        p = n//rep
        scale = ((1<<n)-1)//((1<<p)-1)
        end = (key+scale-1)//scale
        result += p*primitive(p,z//rep,d,end)
    return result


def direct(w):
    rotations = sorted(set(w[i:]+w[:i] for i in range(len(w))))
    u = rotations[0][:len(rotations)]
    width = sum(u[j-1]=="1" and u[j]=="0" for j in range(len(u)))
    return width,int(rotations[0][::-1],2)


if __name__ == "__main__":
    total = 0
    for n in range(1,9):
        population = [[] for _ in range(n+1)]
        for x in range(1<<n):
            w = format(x,f"0{n}b")
            population[w.count('0')].append(direct(w))
        for z,layer in enumerate(population):
            for d in range(min(z,n-z)+1):
                for key in range((1<<n)+1):
                    assert rank_key(n,z,d,key)==sum(u<=d and t<key for u,t in layer)
                    total += 1
        print("order",n,"cumulative density/cap/threshold checks",total)
