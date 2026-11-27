"""Stop at a requested fractional resolution. Return a cyclic interval for any window."""
from heapq import heappush,heappop
from pathlib import Path
import sys
from sensitive import avoidance,cell

def precision(a,K):
    if not a or set(a)-set("01") or not isinstance(K,int) or K<1:
        raise ValueError("expected a binary word and a positive integer K")
    n=len(a)
    period=1<<n
    depth=min(n,max(1,(max(1,K*n*(n-1)//2)-1).bit_length()))
    count=avoidance(n)
    heap=[]
    lo=hi=int("1" in a)
    visited=0
    def add(u):
        nonlocal lo,hi,visited
        l,r,_=cell(a,u,"1",count)
        lo+=l
        hi+=r
        visited+=1
        if r>l and len(u)<depth:
            heappush(heap,(l-r,u,l,r))
    add("0")
    while K*(hi-lo)>period:
        _,u,l,r=heappop(heap)
        lo-=l
        hi-=r
        add(u+"0")
        add(u+"1")
    return lo,hi,visited

def temporal(w,K,archive=None):
    if not w or set(w)-set("01") or not isinstance(K,int) or K<1:
        raise ValueError("expected a binary window and a positive integer K")
    if len(w)==1: return int(w),0
    archive=Path(archive) if archive else Path(__file__).resolve().parent.parent/"return-ranking"
    sys.path.insert(0,str(archive))
    from decode import predecessor
    for distance in range(len(w)+max(2,len(w)//2)):
        if all(w<w[j:]+w[:j] for j in range(1,len(w))):
            l,r,_=precision(w,K)
            return (l+distance)%(1<<len(w)),r-l
        w=predecessor(w)
    raise ArithmeticError("archived boundary bound exceeded")

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("window")
    p.add_argument("K",type=int)
    p.add_argument("--archive")
    args=p.parse_args()
    start,width=temporal(args.window,args.K,args.archive)
    print("First possible tick:",start)
    print("Forward interval width:",width)
