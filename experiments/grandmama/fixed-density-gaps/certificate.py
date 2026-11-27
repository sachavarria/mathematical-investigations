"""Deterministic additive interval for fixed-density weighted colex rank."""
from fractions import Fraction
from math import comb
from gap_rank import least_feasible_key,rank

def dictionary(m,B,q):
    """Ordered gap-prefix partition; skip gap values impossible at total B."""
    n=m+B
    probabilities=[Fraction(m,n)*Fraction(B,n)**v for v in range(B+1)]
    stack=[((),Fraction(1))]
    while stack:
        u,mass=stack.pop()
        if mass<=q or len(u)==m:
            yield u
            continue
        for v in range(B-sum(u)+1):
            stack.append((u+(v,),mass*probabilities[v]))

def anchored(m,B,u,descending,cut):
    """Count canonical gap arrays with this unique minimum prefix, before cut and total."""
    r=len(u)
    def smaller(v,w):
        return v>w if descending else v<w
    transitions={}
    for k in range(r+1):
        active=[j for j in range(r) if j<=k and (j==0 or u[k-j:k]==u[:j])]
        for v in range(B+1):
            if any(smaller(v,u[j]) for j in active):
                transitions[k,v]=-1
            else:
                word=u[:k]+(v,)
                transitions[k,v]=max(j for j in range(min(r,len(word))+1)
                                      if j==0 or word[-j:]==u[:j])
    def compare(old,i,v):
        if cut is None:
            return True
        return old if v==cut[i] else smaller(v,cut[i])
    states={(0,0,cut is None):1}
    for i in range(m+r-1):
        future={}
        for (state,used,below),amount in states.items():
            choices=(u[i],) if i<r else (u[i-m],) if i>=m else range(B-used+1)
            for v in choices:
                z=transitions[state,v]
                if z<0 or (z==r)!=(i==r-1):
                    continue
                w=used+(v if i<m else 0)
                if w>B:
                    continue
                key=(z,w,compare(below,i,v) if i<m else below)
                future[key]=future.get(key,0)+amount
        states=future
    return (sum(v for (_,w,b),v in states.items() if w==B and b),
            sum(v for (_,w,_),v in states.items() if w==B))

def interval_from_leaves(a,d,leaves):
    n=len(a)
    desc=d<=n-d
    m=min(d,n-d)
    key=least_feasible_key(a[::-1],d,0 if desc else n-1,"1" if desc else "0")
    if key is None:
        total=comb(n,d)
        return total,total
    w=key[::-1]
    cut=tuple(map(len,w[:-1].split("1") if desc else w[1:].split("0")))
    low=resolved=0
    for u in leaves:
        yes,all_words=anchored(m,n-m,u,desc,cut)
        low+=n*yes
        resolved+=n*all_words
    return low,low+comb(n,d)-resolved

def certificate(a,d,K):
    if not a or set(a)-set("01") or not 0<=d<=len(a) or not isinstance(K,int) or K<1:
        raise ValueError("expected binary threshold, valid density and positive integer K")
    n=len(a)
    m=min(d,n-d)
    denominator=K*n*(n+1)*m**3
    if m==0 or m<2*(denominator-1).bit_length():
        x=rank(a,d)[0]
        return x,x
    interval=interval_from_leaves(a,d,dictionary(m,n-m,Fraction(1,denominator)))
    assert (interval[1]-interval[0])*K<=comb(n,d)
    return interval
