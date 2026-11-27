"""Independent orbit oracle. No pattern matching or transfer matrices in the oracle."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import sys
from sensitive import bounds, gap_bounds

def orbits(n):
    seen=set()
    for i in range(1<<n):
        w=format(i,f"0{n}b")
        if w not in seen:
            orb={w[j:]+w[:j] for j in range(n)}
            seen.update(orb)
            yield min(orb),len(orb)

def candidates(w,h):
    n=len(w)
    starts=[i for i in range(n) if w[i-1]=="1" and w[i]=="0"]
    if not starts:
        return [w]
    twice=w+w
    best=min(twice[i:i+h] for i in starts)
    return [twice[i:i+n] for i in starts if twice[i:i+h]==best]

def profile(n,h,d=None):
    N=1<<n
    low=[0]*(N+1)
    high=[0]*(N+1)
    multi=0
    for w,mass in orbits(n):
        if d is not None and w.count("1")!=d: continue
        cand=candidates(w,h)
        keys=[int(v[::-1],2) for v in cand]
        low[max(keys)+1]+=mass
        high[min(keys)+1]+=mass
        if len(keys)>1: multi+=mass
    for i in range(1,N):
        low[i]+=low[i-1]
        high[i]+=high[i-1]
    return low,high,multi

def gap_oracle(a,d,leaves):
    n=len(a)
    leafset=set(leaves)
    l=r=0
    for w,v in orbits(n):
        if w.count('1')!=d: continue
        align=[w[i:]+w[:i] for i in range(n) if
               (w[i-1]=='1' if d<=n-d else w[i]=='0')]
        def gaps(x):
            return tuple(map(len,x[:-1].split("1") if d<=n-d else x[1:].split("0")))
        canon=gaps(w)
        leaf=next(canon[:i] for i in range(1,len(canon)+1) if canon[:i] in leafset)
        flags=[x[::-1]<a[::-1] for x in align if gaps(x)[:len(leaf)]==leaf]
        l+=v*all(flags)
        r+=v*any(flags)
    return l,r

def obstruction(k):
    n=4*k+20
    a="0"*(n//2-2)+"1"*(n//2-2)+"0011"
    for i in range(1<<k):
        c="".join("10" if i>>j&1 else "01" for j in range(k))
        u="00001"+c+"11"
        for x,y,expected in (("101","011",True),("001","111",False)):
            w=u+x+u+y
            origins=candidates(w,len(u))
            values=[v[::-1]<a[::-1] for v in origins]
            assert len(origins)==2 and any(values) and not all(values)
            assert (min(origins)[::-1]<a[::-1])==expected
            assert w.count("1")==n//2

if __name__=="__main__":
    archive=Path(sys.argv[1]) if sys.argv[1:] else Path(__file__).resolve().parent.parent/"fixed-density-gaps"
    sys.path.insert(0,str(archive))
    from certificate import dictionary,interval_from_leaves
    cases=0
    for n in range(1,11):
        N=1<<n
        ds=[None]+(list(range(n+1)) if n<=5 else [n//2])
        for d in ds:
            for h in sorted({1,min(3,n),n}):
                lo,hi,_=profile(n,h,d)
                keys=range(N) if n<=6 else sorted({0,1,N//3,N//2+1,N-2,N-1})
                for k in keys:
                    a=format(k,f"0{n}b")[::-1]
                    assert bounds(a,h,d)[:2]==(lo[k],hi[k]),(a,h,d)
                    cases+=1
    print("Binary interval comparisons:",cases,flush=True)
    cases=0
    for n in range(2,9):
        for d in range(1,n):
            m=min(d,n-d)
            for den in (2,8):
                leaves=list(dictionary(m,n-m,Fraction(1,den)))
                for k in sorted({0,1,(1<<n)//3,(1<<n)//2+1,(1<<n)-2,(1<<n)-1}):
                    a=format(k,f"0{n}b")[::-1]
                    new=gap_bounds(a,d,leaves)
                    old=interval_from_leaves(a,d,leaves)
                    assert new==gap_oracle(a,d,leaves),(a,d,new)
                    assert old[0]<=new[0]<=new[1]<=old[1]
                    cases+=1
    print("Matched-dictionary interval comparisons:",cases)
    for k in range(10): obstruction(k)
    print("Opposite-answer mixed-prefix witnesses: k=0..9")
