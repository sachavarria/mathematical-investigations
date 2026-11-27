"""Support and additive integral of the unrestricted run-head uncertainty profile."""
from composition import locate
from sensitive import bounds

def support(n,h):
    H=max(2,h)
    if h<1 or n<4*H+4: raise ValueError("outside the proved shallow regime")
    return (1<<(n-1))+(1<<h)+1,(1<<n)-(1<<H)-2

def integrated(n,h,J):
    """Integer bounds for sum of widths over all 2^n threshold keys."""
    if n<1 or not 1<=h<=n or J<1: raise ValueError("invalid parameters")
    N=1<<n
    J=min(J,N)
    collision=min(N,((N*n*(n-1))//2)>>h)
    if n>=4*max(2,h)+4:
        first,last=support(n,h)
        count=last-first+1
        floor=count # positive integer mass on each interior threshold
    else:
        count=N
        floor=0
    upper=count*collision
    if upper<=2*N*((N+J-1)//J-1):
        return floor,upper
    edges=[i*N//J for i in range(J+1)]
    def value(k):
        if k==N: return N,N
        return bounds(format(k,f"0{n}b")[::-1],h)[:2]
    l,r=value(0)
    lo=hi=0
    for left,right in zip(edges,edges[1:]):
        L,U=value(right)
        interior=right-left-1
        lo+=r-l+interior*max(0,r-L)
        hi+=r-l+interior*(U-l)
        l,r=L,U
    return max(floor,lo),min(upper,hi)
