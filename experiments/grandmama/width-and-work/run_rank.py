"""Width-bounded complete weighted colex rank. Standard library, exact integers."""
from functools import lru_cache
from itertools import groupby, product
from math import comb


@lru_cache(None)
def orders(r):
    """Ordered equality classes of r labelled positions, numbered from zero."""
    if r == 0:
        return ((),)
    out = []
    for previous in orders(r-1):
        groups = max(previous, default=-1)+1
        for j in range(groups):
            out.append(previous+(j,))
        for j in range(groups+1):
            out.append(tuple(x+(x >= j) for x in previous)+(j,))
    return tuple(out)


@lru_cache(maxsize=8192)
def assignments(total, multiplicities, intervals):
    """Positive strictly increasing values with individually bounded ranges."""
    if any(lo > hi for lo, hi in intervals):
        return 0
    if sum((j+1)*m for j,m in enumerate(multiplicities)) > total:
        return 0
    states = [{0:1}] + [{} for _ in intervals]
    for value in range(1, total+1):
        for j in reversed(range(len(intervals))):
            lo, hi = intervals[j]
            if lo <= value <= hi:
                nxt = states[j+1]
                add = multiplicities[j]*value
                for used, count in states[j].items():
                    if used+add <= total:
                        nxt[used+add] = nxt.get(used+add,0)+count
    return states[-1].get(total,0)


def primitive(n, z, cap, end):
    """Primitive minima with reversed integer strictly below end, fixed zero count."""
    if end <= 0:
        return 0
    if n == 1:
        return int(1-z < end)
    if z == 0 or z == n:
        return 0
    cut = format(end, f"0{n}b") if end < 1<<n else None
    if cut and cut[0] == '0':  # a mixed least rotation ends in one
        return 0
    lengths = [] if cut is None else [sum(1 for _ in g) for _,g in groupby(cut)]
    count = 0
    for r in range(1,min(cap,z,n-z)+1):
        for zero, one in product(orders(r),repeat=2):
            shape = tuple(zip((-x for x in zero),one))
            if any(shape >= shape[j:]+shape[:j] for j in range(1,r)):
                continue
            types = (zero,one)
            totals = (z,n-z)
            mult = [tuple(t.count(j) for j in range(max(t)+1)) for t in types]
            bounds = [[(1,totals[b]) for _ in m] for b,m in enumerate(mult)]
            def ways():
                return (assignments(z,mult[0],tuple(bounds[0]))
                        * assignments(n-z,mult[1],tuple(bounds[1])))
            if cut is None:
                count += ways()
                continue
            positions = [(bit,types[bit][j]) for j in reversed(range(r)) for bit in (1,0)]
            for (bit,cl),q in zip(positions,lengths):
                lo,hi = bounds[bit][cl]
                bounds[bit][cl] = (lo,min(hi,q-1)) if bit else (max(lo,q+1),hi)
                count += ways()
                if not lo <= q <= hi:
                    break
                bounds[bit][cl]=(q,q)
    return count


def rank(word, cap, zeros=None):
    """Cap applies to the primitive packet, including for proper powers."""
    n = len(word)
    if not n or set(word)-set("01") or cap < 0 or (zeros is not None and not 0<=zeros<=n):
        raise ValueError("invalid threshold, cap or zero count")
    key = int(word[::-1],2)
    ans = 0
    for p in range(1,n+1):
        if n%p: continue
        repetitions = n//p
        if zeros is not None and zeros%repetitions: continue
        scale = ((1<<n)-1)//((1<<p)-1)
        end = (key+scale-1)//scale
        layers = range(p+1) if zeros is None else (zeros//repetitions,)
        ans += p*sum(primitive(p,z,cap,end) for z in layers)
    return ans


def oracle(n):
    data = []
    for x in range(1<<n):
        w = format(x, f"0{n}b")
        rows = sorted(set(w[i:]+w[:i] for i in range(n)))
        u = rows[0][:len(rows)]
        width = sum(u[j-1:j] == '1' and u[j]=='0' for j in range(1,len(u))) + (u[-1]=='1' and u[0]=='0')
        data.append((w.count("0"),width,int(rows[0][::-1],2)))
    return data


if __name__ == "__main__":
    checks=0
    for n in range(1,8):
        data=oracle(n)
        for x in range(1<<n):
            w=format(x,f"0{n}b")
            for d in range(n//2+1):
                for z in [None,*range(n+1)]:
                    expected=sum(key<int(w[::-1],2) and wid<=d and (z is None or z==zw)
                                 for zw,wid,key in data)
                    assert rank(w,d,z)==expected,(n,w,d,z,expected)
                    checks+=1
    print("All weighted rank comparisons through n=7:",checks)
    for n,z,d in [(64,32,1),(64,32,2),(64,32,3)]:
        q=("00101101"*(n//8))
        print("n",n,"z",z,"primitive-width cap",d,"rank",rank(q,d,z),"threshold",q)
