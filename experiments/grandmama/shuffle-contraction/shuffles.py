"""Exact full-rank reference via stable shuffles and path contraction. Standard library."""
from itertools import combinations,product
from math import comb,prod
from functools import lru_cache

def lf(bits):
    z=bits.count("0")
    counts=[0,z]
    image=[]
    for c in bits:
        b=int(c)
        image.append(counts[b])
        counts[b]+=1
    return image

def one_cycle(image):
    i=image[0]
    visited=1
    while i!=0:
        visited+=1
        i=image[i]
    return visited==len(image)

def layouts(n,z,s):
    """Embeddings of a simple LF path, in the forced relative row order."""
    order=sorted(range(1,len(s)+1),key=lambda j:s[:j][::-1])
    zeros=[j for j in order if s[j-1]=="0"]
    ones=[j for j in order if s[j-1]=="1"]
    for low in combinations(range(1,z),len(zeros)):
        for high in combinations(range(z,n),len(ones)):
            loc=[0]*(len(s)+1)
            for j,i in zip(zeros+ones,low+high):
                loc[j]=i
            yield loc

def quotas(n,z,s,loc):
    used=count=0
    gaps=[]
    for i,j,b in sorted(zip(loc[:-1],loc[1:],s)):
        before=j if b=="0" else i-(j-z)
        size=i-used
        quota=before-count
        if not 0<=quota<=size: return None
        if size: gaps.append((size,quota))
        used,count=i+1,before+(b=="0")
    if not 0<=z-count<=n-used: return None
    if n>used: gaps.append((n-used,z-count))
    return tuple(gaps)

def interleavings(size,zeros):
    for subset in combinations(range(size),zeros):
        word=["1"]*size
        for j in subset: word[j]="0"
        yield "".join(word)

@lru_cache(maxsize=8192)
def twisted(gaps,h):
    total=0
    for strings in product(*(interleavings(b,c) for b,c in gaps)):
        perm=lf("".join(strings))
        perm=[h if j==0 else j-1 if j<=h else j for j in perm]
        total+=one_cycle(perm)
    return total

def primitive_cylinder(n,s,zeros=None):
    if not 1<=len(s)<=n or set(s)-set("01"): raise ValueError("invalid cylinder")
    if len(s)==n:
        w=s[::-1]
        return int((zeros is None or w.count("0")==zeros)
                   and all(w<w[j:]+w[:j] for j in range(1,n)))
    total=0
    for z in range(1,n) if zeros is None else (zeros,):
        if not 0<z<n: continue
        for loc in layouts(n,z,s):
            gaps=quotas(n,z,s,loc)
            if gaps is None: continue
            h=loc[-1]-sum(i<loc[-1] for i in loc[:-1])
            total+=twisted(gaps,h)
    return total

def rank(a,zeros=None):
    """Weighted strict rank by primitive root length. zeros is optional fixed zero count."""
    n=len(a)
    if not n or set(a)-set("01") or zeros is not None and not 0<=zeros<=n:
        raise ValueError("invalid query")
    key=int(a[::-1],2)
    total=0
    for p in range(1,n+1):
        if n%p: continue
        power=n//p
        if zeros is not None and zeros%power: continue
        z=None if zeros is None else zeros//power
        scale=((1<<n)-1)//((1<<p)-1)
        end=(key+scale-1)//scale
        digits=format(end,f"0{p}b")
        for j,b in enumerate(digits):
            if b=="1":
                total+=p*primitive_cylinder(p,digits[:j]+"0",z)
    return total
