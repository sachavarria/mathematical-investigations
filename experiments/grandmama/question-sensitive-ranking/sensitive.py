"""Cut-sensitive certificates for rooted binary circles. Python 3 and NumPy."""
from collections import deque
from functools import lru_cache
from math import comb
import numpy as np

def automaton(patterns):
    """Aho-Corasick with states leading to any forbidden output removed."""
    go=[[-1,-1]]
    terminal=[False]
    for p in patterns:
        i=0
        for bit in p:
            b=int(bit)
            if go[i][b]<0:
                go[i][b]=len(go)
                go.append([-1,-1])
                terminal.append(False)
            i=go[i][b]
        terminal[i]=True
    fail=[0]*len(go)
    queue=deque()
    for b,j in enumerate(go[0]):
        if j<0: go[0][b]=0
        else: queue.append(j)
    while queue:
        i=queue.popleft()
        terminal[i] |= terminal[fail[i]]
        for b,j in enumerate(go[i]):
            if j<0: go[i][b]=go[fail[i]][b]
            else:
                fail[j]=go[fail[i]][b]
                queue.append(j)
    ids={i:k for k,i in enumerate(i for i in range(len(go)) if not terminal[i])}
    return [(ids.get(go[i][0],-1),ids.get(go[i][1],-1)) for i in ids]

def avoidance(n,d=None):
    @lru_cache(maxsize=4096)
    def count(patterns):
        if not patterns: return 2**n if d is None else comb(n,d)
        if "" in patterns: return 0
        edges=automaton(patterns)
        N=len(edges)
        dtype=np.int64 if n<=62 else object
        if d is None:
            mat=np.zeros((N,N),dtype=dtype)
            for i,row in enumerate(edges):
                for j in row:
                    if j>=0: mat[i,j]+=1
            return int(np.trace(np.linalg.matrix_power(mat,n)))
        # Propagate paths, retaining the start state and the number of ones.
        table=np.zeros((d+1,N,N),dtype=dtype)
        table[0]=np.eye(N,dtype=dtype)
        for k in range(n):
            future=np.zeros_like(table)
            for i,row in enumerate(edges):
                for b,j in enumerate(row):
                    stop=min(d-b,k)+1
                    if j>=0 and stop>0:
                        future[b:b+stop,:,j]+=table[:stop,:,i]
            table=future
        return int(np.trace(table[d]))
    def evaluate(patterns):
        return count(tuple(sorted(set(patterns))))
    return evaluate

def cover(length,cut):
    """Prefix codes for the intervals [0,cut) and [cut,2^length)."""
    if cut<=0: return [],[""]
    if cut>=1<<length: return [""],[]
    while cut%2==0:
        cut//=2
        length-=1
    t=format(cut,f"0{length}b")
    yes=[t[:j]+"0" for j,b in enumerate(t) if b=="1"]
    no=[t[:j]+"1" for j,b in enumerate(t) if b=="0"]+[t]
    return yes,no

def cell(a,u,prior,count):
    """Rooted mass definitely below, possibly below, and total in this cell.
    prior is '1' for starts preceded by 1, or '' for every start."""
    n=len(a)
    F=[(u[:j]+"0")[::-1]+prior for j,b in enumerate(u) if b=="1"]
    base=count(F)
    if not base: return 0,0,0
    no_mark=count(F+[u[::-1]+prior])
    mass=base-no_mark
    if not mass: return 0,0,0
    h=len(u)
    if h==n:
        answer=mass*int(u[::-1]<a[::-1])
        return answer,answer,mass
    # Only n-h backwards bits remain unknown. The seam supplies reverse(u).
    cutoff=int(a[h:][::-1],2)+int(u[::-1]<a[:h][::-1])
    r=n-h
    if prior:
        r-=1
        cutoff-=1<<r
    yes,no=cover(r,cutoff)
    if not yes: return 0,0,mass
    if not no: return mass,mass,mass
    anchor=u[::-1]+prior
    low=count(F+[anchor+p for p in no])-no_mark
    high=base-count(F+[anchor+p for p in yes])
    return low,high,mass

def bounds(a,h,d=None,resolve_pairs=False):
    n=len(a)
    if not n or set(a)-set("01") or not 1<=h<=n or d is not None and not 0<=d<=n:
        raise ValueError("invalid query")
    # The two constant orbits have no cyclic 1-to-0 boundary.
    low=high=int("1" in a and d in (0,None))
    count=avoidance(n,d)
    stack=["0"]
    visited=0
    while stack:
        u=stack.pop()
        l,r,mass=cell(a,u,"1",count)
        visited+=1
        if r>l and len(u)<h:
            stack.extend((u+"0",u+"1"))
        else:
            if resolve_pairs and l<r:
                from pairs import pair_mass
                y,z=pair_mass(a,u,d)
                l+=y
                r-=z
            low+=l
            high+=r
    return low,high,visited

def gap_bounds(a,d,leaves):
    n=len(a)
    m=min(d,n-d)
    if m==0:
        value=int(("1" if d else "0")*n<a[::-1])
        return value,value
    count=avoidance(n,d)
    low=high=0
    for u in leaves:
        if d<=n-d:
            p="".join("0"*g+"1" for g in u)
            prior="1"
        else:
            p=("".join("0"+"1"*g for g in u)+"0")[:n]
            prior=""
        l,r,_=cell(a,p,prior,count)
        low+=l
        high+=r
    return low,high

if __name__=="__main__":
    import argparse
    cli=argparse.ArgumentParser()
    cli.add_argument("threshold")
    cli.add_argument("depth",type=int)
    cli.add_argument("--density",type=int)
    cli.add_argument("--pairs",action="store_true")
    args=cli.parse_args()
    print(bounds(args.threshold,args.depth,args.density,args.pairs))
