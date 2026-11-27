from collections import Counter
from composition import accepted,refined
from unique import unique_mass
from profile_tools import support,integrated
from itertools import groupby

def words(n):
    return (format(i,f"0{n}b") for i in range(1<<n))
def circles(n,h,d=None):
    seen=set()
    for x in words(n):
        if x in seen or d is not None and x.count("1")!=d: continue
        rotations=[x[j:]+x[:j] for j in range(n)]
        seen.update(rotations)
        w=min(rotations)
        starts=[j for j in range(n) if w[j-1]=="1" and w[j]=="0"]
        if not starts:
            yield w,None,[],[],False,len(set(rotations))
            continue
        cyc=w*3
        u=w[:h]
        marks=[j for j in starts if cyc[j:j+h]==u]
        gaps=[cyc[j+h:k+h] for j,k in zip(marks,marks[1:]+[n])]
        keys=[int(cyc[j:j+n][::-1],2) for j in marks]
        yield w,u,keys,gaps,gaps.count(min(gaps))==1,len(set(rotations))

def test_counts():
    calls=intervals=0
    for n in range(2,10):
        keys=range(1<<n) if n<=5 else sorted({0,1,(1<<n)*3//5,(1<<n)*7//8,(1<<n)-1})
        for h in sorted({1,min(3,n)}):
            for d in (None,n//2):
                population=list(circles(n,h,d))
                prefixes={w[:h] for w in words(n) if w[0]=="0"}
                for k in keys:
                    a=format(k,f"0{n}b")[::-1]
                    for u in prefixes:
                        exact=[0]*(n//2+1)
                        special=0
                        for w,cell,xs,_,single,mass in population:
                            if cell==u and w[::-1]<a[::-1]:
                                exact[len(xs)]+=mass
                                special+=mass*single
                        assert accepted(a,u,n//2,d)==exact,(a,u,d)
                        assert unique_mass(a,u,d)==special,(a,u,d,special)
                        calls+=1
                    for R in sorted({2,3,n//2}):
                        l=r=0
                        for w,_,xs,_,_,mass in population:
                            if len(xs)<=R:
                                l+=mass*(w[::-1]<a[::-1])
                                r+=mass*(w[::-1]<a[::-1])
                            else:
                                l+=mass*(max(xs)<k)
                                r+=mass*(min(xs)<k)
                        assert refined(a,h,R,d)==(l,r),(a,h,R,d,l,r)
                        intervals+=1
    print("Multiplicity-vector and unique-minimum comparisons each:",calls,flush=True)
    print("Refined interval checks:",intervals,flush=True)

def profile(n,h):
    N=1<<n
    changes=Counter()
    total=0
    for w,_,xs,_,_,mass in circles(n,h):
        if xs:
            l,r=min(xs),max(xs)
            changes[l+1]+=mass
            changes[r+1]-=mass
            total+=mass*(r-l)
    width=0
    positives=[]
    for k in range(N):
        width+=changes[k]
        if width: positives.append(k)
    return positives,total

if __name__=="__main__":
    test_counts()
    cells=0
    for n in range(12,19):
        for h in range(1,(n-4)//4+1):
            pos,_=profile(n,h)
            a,b=support(n,h)
            assert pos==list(range(a,b+1))
            cells+=1<<n
    print("Individual support classifications in proved regime:",cells,flush=True)
    pos,_=profile(13,5)
    print("Outside regime, internal zero-width keys at (13,5):",
          sorted(set(range(min(pos),max(pos)+1))-set(pos)))
    for n in range(2,10):
        for h in range(1,min(4,n)+1):
            _,v=profile(n,h)
            lo,hi=integrated(n,h,8)
            assert lo<=v<=hi
            assert integrated(n,h,1<<n)==(v,v)
    print("All-key integral and enclosure comparisons passed for n=2..9, h<=4.")
