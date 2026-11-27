"""Exhaustive small tests against literal bit rotations, including the 000 reduction."""
from collections import Counter
from functools import lru_cache
from gap_rank import rank

def words(n):
    return [format(i,f"0{n}b")[::-1] for i in range(1<<n)]

def rots(w):
    return {w[i:]+w[:i] for i in range(len(w))}

def exhaustive(n):
    names=words(n)
    counts=Counter(min(rots(w)) for w in names)
    totals=[[0,0,0] for d in range(n+1)]
    calls=0
    for a in names:
        for d,total in enumerate(totals):
            assert rank(a,d)==tuple(total),(a,d,rank(a,d),total)
            calls+=1
        value=counts[a]
        total=totals[a.count("1")]
        total[0]+=value
        total[1]+=int(value>0)
        total[2]+=int(value==n)
    return calls

def family_tests():
    # Use the independently archived forward and reverse reductions, replacing only their oracle.
    import sys
    from pathlib import Path
    archive=Path(sys.argv[1]) if sys.argv[1:] else Path(__file__).resolve().parent.parent/"cut-ranking"
    sys.path.insert(0,str(archive))
    import family
    @lru_cache(None)
    def oracle(a,density):
        return rank(a,density)
    family.rank=oracle
    queries=0
    reverse_queries=0
    for m in range(2,8):
        names=words(m)
        total=0
        actual=Counter(min(rots(w)) for w in names)
        for a in names:
            assert family.rank_via_family(a)==total
            total+=actual[a]
            reverse_queries+=1
        for t in range(1,m):
            n=m+3*t
            masses={}
            for x in names:
                if x.count("1")==t:
                    orbit=rots(x.replace("1","1000"))
                    masses[min(orbit)]=len(orbit)
            probes={0,1,(1<<n)-1,(1<<n)//3}
            for w in masses:
                k=int(w[::-1],2)
                probes.update((k,max(0,k-1),min((1<<n)-1,k+1)))
            for key in probes:
                a=format(key,f"0{n}b")[::-1]
                expect=sum(v for w,v in masses.items() if w[::-1]<a[::-1])
                assert family.family_mass(a,m,t,3)==expect
                queries+=1
    return queries,reverse_queries

def fragments(k):
    # Reject/accept in that order inside each of 2^k disjoint prefix blocks.
    n=2*k+10
    a="00001"+"01"*k+"1"+"1011"
    previous=""
    for i in range(1<<k):
        middle="".join(("10" if (i>>j)&1 else "01") for j in reversed(range(k)))
        p="00001"+middle+"1"
        x,y=p+"0111",p+"1101"
        assert previous<x<y and y[::-1]<a[::-1]<x[::-1]
        for w in (x,y,a):
            assert w.count("1")==n//2 and min(rots(w))==w and len(rots(w))==n
        previous=y

if __name__=="__main__":
    for n in range(1,9):
        print(f"order {n}, all threshold/density pairs: {exhaustive(n)}",flush=True)
    print("000 ambient and converse queries:",family_tests())
    for k in range(9):
        fragments(k)
    print("Alternating interval witnesses checked for k=0..8")
