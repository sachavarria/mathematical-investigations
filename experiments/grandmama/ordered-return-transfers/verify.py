"""Direct orbit classification using circular lists, independent of the transfer recurrence."""
from collections import defaultdict
from itertools import product
from transfer import Cut,Path,bounded,base,split
from landmark import slices
from shared import encode,A,B0

def orbits(n):
    seen=set()
    for i in range(1<<n):
        x=format(i,f"0{n}b")
        if x in seen: continue
        group={x[j:]+x[:j] for j in range(n)}
        seen.update(group)
        yield min(group),len(group)

def payloads(w):
    n=len(w)
    marks=[i for i in range(n) if w[i-1]=="1" and w[i]=="0"]
    return [(w*3)[j+1:k+1] for j,k in zip(marks,marks[1:]+[n])]

def history(w):
    slots=payloads(w)
    path=[]
    while slots:
        p=min(slots)
        path.append(p)
        if slots.count(p)==1: return tuple(path),0
        if all(v==p for v in slots): return tuple(path),1
        assert slots[0]==p and slots[-1]!=p
        grouped=[]
        k=0
        for v in slots:
            if v==p: k+=1
            else:
                grouped.append(p*k+v)
                k=0
        slots=grouped
    return (),-1

def bridge_check(n,h):
    N=1<<n
    H=max(h,2)
    pad=n-3*h-H-4
    low="0"*h+"1"+"0"*(n-h-2)+"1"
    high="0"+"1"*(H-1)+"0"+"1"*(n-H-1)
    mid="0"*h+"1"*(H+1)+"0"*(2*h+2+pad)+"1"
    spans=[]
    for w in (low,mid,high):
        rots=[w[j:]+w[:j] for j in range(n) if w[j-1]+w[j]=="10"]
        u=min(rots)[:h]
        keys=[int(v[::-1],2) for v in rots if v.startswith(u)]
        spans.append((min(keys),max(keys)))
    assert spans[0][0]==N//2+2**h and spans[-1][-1]==N-2**H-2
    spans.sort()
    endpoint=spans[0][1]
    for l,r in spans[1:]:
        assert l<=endpoint
        endpoint=max(endpoint,r)

if __name__=="__main__":
    layers=paths=counts=embeds=0
    for n in range(2,11):
        population=[(w,v,*history(w)) for w,v in orbits(n) if "0" in w and "1" in w]
        ks=range(1<<n) if n<=5 else {0,1,3*(1<<n)//4,7*(1<<n)//8,(1<<n)-1}
        for key in ks:
            a=format(key,f"0{n}b")[::-1]
            true=defaultdict(lambda:[0,0])
            for w,v,path,kind in population:
                if w[::-1]<a[::-1]: true[path][kind]+=v
            for path in {p for _,_,p,_ in population}:
                assert Path(Cut(a),path).contribution()[:2]==tuple(true[path]),(n,a,path)
                paths+=1
            c,levels=bounded(a,2)
            assert c==int(key>0)
            for j,entry in enumerate(levels):
                expect=[sum(v[b] for p,v in true.items() if len(p)==j+1) for b in (0,1)]
                assert entry==expect,(n,a,j,entry,expect)
                layers+=1
            for d in (None,n//2):
                R=min(n//2,4)
                expect=[0]*(R+1)
                for w,v,path,_ in population:
                    t=payloads(w).count(path[0])
                    if t<=R and w[::-1]<a[::-1] and (d is None or w.count("1")==d):
                        expect[t]+=v
                assert slices(a,R,d)==expect,(a,R,d)
                counts+=1
    for m in range(1,8):
        for D in (0,1,3,m):
            for q,v in orbits(m):
                x=encode("0"*D,q)
                orbit={x[i:]+x[:i] for i in range(len(x))}
                assert min(orbit)==x and len(orbit)==(6*(D+2))*v
                if m>1:
                    path,_=history(x)
                    assert path[:D+1]==tuple(A+B0*i for i in range(D+1))
                for j in range(1<<m):
                    a=format(j,f"0{m}b")
                    assert (x[::-1]<encode("0"*D,a)[::-1])==(q[::-1]<a[::-1])
                    embeds+=1
    for h in range(1,41):
        for extra in (0,1,17):
            bridge_check(4*max(2,h)+4+extra,h)
    print("Supplied-path (first unique,pure) comparisons:",paths)
    print("Whole-depth output comparisons:",layers)
    print("Global least-frequency vectors, including fixed density:",counts)
    print("Delay-embedding representative/threshold comparisons:",embeds)
    print("Shallow-theorem three-witness endpoint and overlap checks: 120")
