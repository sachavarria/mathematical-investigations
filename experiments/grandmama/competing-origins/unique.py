"""Polynomial per known prefix, unbounded number of origins, unique least outgoing return."""
from functools import lru_cache
from math import comb
from composition import returns,parses
from cut_rank import match_step

def unique_mass(a,u,d=None):
    n,h=len(a),len(u)
    if not 1<=h<=n or u[0]!="0": raise ValueError("expected a nonempty run-head prefix")
    start,T=returns(u)
    def step(q,b):
        z=T[q,b]
        return -1 if z is None else -2 if z==start else z
    total=0
    suffixes=["0"+a[j+1:]+u for j in range(h,n) if a[j]=="1"]
    if u[::-1]<a[:h][::-1]: suffixes.append(a[h:]+u)
    for suffix in suffixes:
        for b in range(1,len(suffix)+1):
            fixed=parses(suffix[b:],start,step)
            if fixed is None: continue
            wall=min(fixed,default=None)
            tail=suffix[:b]
            budget=n-len(suffix)+b
            ones=None if d is None else d-suffix[b:].count("1")
            @lru_cache(None)
            def solve(f,root,pivot,depth,q,k,cmp,length,weight):
                if weight is not None and not 0<=weight<=length: return 0
                # pivot=1 distinct, 2 designates the root itself
                size=f+int(root)+int(pivot==1)
                if not size: return int(length==0)
                if q==-2:
                    return int(length==0 and (not root or (size==1 and (wall is None or cmp<0)))
                               and (not pivot or k==len(tail)))
                rest=length-size
                if rest<0: return 0
                ways=0
                for f0 in range(f+1):
                    for rb in ("01" if root else "-"):
                        for pb in ("01" if pivot==1 else rb if pivot==2 else "-"):
                            if rb=="1" and (f0 or pb=="0"): continue
                            groups=[]
                            for bit,fbit in (("0",f0),("1",f-f0)):
                                rt=rb==bit
                                pv=pivot if pb==bit else 0
                                count=fbit+int(rt)+int(pv==1)
                                dest=step(q,bit) if count else None
                                sign=cmp if rt else 0
                                if rt and wall is not None and not sign:
                                    if depth>=len(wall): sign=1
                                    elif bit!=wall[depth]: sign=-1 if bit<wall[depth] else 1
                                groups.append(((fbit,rt,pv,depth+1,dest,
                                                match_step(tail,k,bit) if pv else 0,sign),count))
                            (left,c0),(right,c1)=groups
                            if left[4]==-1 or right[4]==-1: continue
                            lengths=(0,) if not c0 else (rest,) if not c1 else range(rest+1)
                            rem=None if weight is None else weight-c1
                            for l in lengths:
                                wl=(None,) if rem is None else range(max(0,rem-rest+l),min(l,rem)+1)
                                for w in wl:
                                    x=solve(*left,l,w)
                                    if x: ways+=comb(f,f0)*x*solve(*right,rest-l,None if rem is None else rem-w)
                return ways
            # The pivot can be the root, or it is preceded by the root and f free slots.
            # All distinct returns to 1u have length at least one; there are <=n/2 run heads.
            if len(fixed)+1<=n//2:
                total+=solve(0,True,2,0,start,0,0,budget,ones)
            for f in range(n//2-len(fixed)-1):
                total+=solve(f,True,1,0,start,0,0,budget,ones)
            solve.cache_clear()
    return n*total
