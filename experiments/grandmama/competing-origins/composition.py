"""Exact multiplicity slices and refined intervals. Uses the archived prefix-trie DP."""
from functools import lru_cache
from pathlib import Path
import sys
import numpy as np

def locate(archived,local):
    root=Path(__file__).resolve().parent.parent
    return str(root/archived if (root/archived).is_dir() else root/local)
sys.path+=[locate("cut-ranking","cutrank"),locate("question-sensitive-ranking","questionrank")]
from cut_rank import assignments,parses,transcripts
from pairs import returns
from sensitive import cell,avoidance,cover

def accepted(a,u,R,d=None):
    """Weighted yes mass by mark count 1,...,R. Zero index unused."""
    n,h=len(a),len(u)
    start,trans=returns(u)
    def step(q,b):
        z=trans[q,b]
        return -1 if z is None else -2 if z==start else z
    suffixes=["0"+a[j+1:]+u for j in range(h,n) if a[j]=="1"]
    if u[::-1]<a[:h][::-1]:
        suffixes.append(a[h:]+u)
    masses=[0]*(R+1)
    for suffix in suffixes:
        for b in range(1,len(suffix)+1):
            whole=parses(suffix[b:],start,step)
            if whole is None: continue
            for e in range(len(whole)+1,min(R,n//2)+1):
                for s,edges in transcripts(e):
                    if n*s%e: continue
                    ways=assignments(n,e,start,step,edges,suffix[:b],whole,d)
                    masses[e]+=ways*(n*s//e)
    return masses

def marked_trace(n,R,d,forbidden,mark):
    """Positive occurrence coefficients of a cyclic pattern-avoidance trace."""
    patterns=set(forbidden)|{mark}
    prefixes={p[:i] for p in patterns for i in range(len(p)+1)}
    states=sorted(q for q in prefixes if not any(q.endswith(p) for p in forbidden))
    ids={q:i for i,q in enumerate(states)}
    edges=[]
    for i,q in enumerate(states):
        for b in "01":
            word=q+b
            if any(word.endswith(p) for p in forbidden): continue
            dest=max((v for v in prefixes if word.endswith(v)),key=len)
            edges.append((i,ids[dest],int(word.endswith(mark)),int(b) if d is not None else 0))
    N=len(states)
    density=0 if d is None else d
    dtype=np.int64 if n<=62 else object
    table=np.zeros((R+1,density+1,N,N),dtype=dtype)
    table[0,0]=np.eye(N,dtype=dtype)
    for _ in range(n):
        future=np.zeros_like(table)
        for i,j,c,b in edges:
            if b<=density and c<=R:
                future[c:,b:,:,j]+=table[:R+1-c,:density+1-b,:,i]
        table=future
    return [int(np.trace(table[e,density])) for e in range(R+1)]

def refined(a,h,R,d=None):
    n=len(a)
    if not a or set(a)-set('01') or not 1<=h<=n or R<0 or d is not None and not 0<=d<=n:
        raise ValueError("invalid threshold, depth, multiplicity or density")
    count=avoidance(n,d)
    low=high=int("1" in a and d in (None,0))
    stack=["0"]
    while stack:
        u=stack.pop()
        l,r,m=cell(a,u,"1",count)
        if l<r and len(u)<h:
            stack.extend([u+"0",u+"1"])
            continue
        if l<r and R>=2:
            cap=min(R,n//2)
            F=[(u[:j]+"0")[::-1]+"1" for j,z in enumerate(u) if z=="1"]
            anchor=u[::-1]+"1"
            bits=n-h-1
            cut=int(a[h:][::-1],2)+int(u[::-1]<a[:h][::-1])-(1<<bits)
            yes,no=cover(bits,cut)
            def positive(extra):
                return sum(marked_trace(n,cap,d,F+extra,anchor)[1:])
            exact=sum(accepted(a,u,cap,d))
            l+=exact-positive([anchor+p for p in no])
            r+=exact-positive([])+positive([anchor+p for p in yes])
        low+=l
        high+=r
    return low,high

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("threshold")
    p.add_argument("depth",type=int)
    p.add_argument("origins",type=int)
    p.add_argument("--density",type=int)
    args=p.parse_args()
    print(refined(args.threshold,args.depth,args.origins,args.density))
