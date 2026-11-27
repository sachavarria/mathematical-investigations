"""Ordered, length-truncated series for colex cuts, with arbitrary-precision counts."""
from functools import lru_cache
import numpy as np

class Cut:
    def __init__(self,a):
        if not a or set(a)-set("01"):
            raise ValueError("nonempty binary threshold required")
        self.a=a
        self.n=len(a)
        self.reference=a[1:]+"0"
        self.zero_matrix=np.zeros((self.n+1,self.n+1),dtype=object)
        self.identity=np.eye(self.n+1,dtype=object)
        self.zero=(self.zero_matrix,)*3
        self.one=(self.identity,self.identity,self.zero_matrix)
        self.monomials={}

    def word(self,w):
        if w in self.monomials: return self.monomials[w]
        T,E,L=(self.zero_matrix.copy() for _ in range(3))
        for i in range(self.n-len(w)+1):
            j=i+len(w)
            target=self.reference[i:j][::-1]
            T[i,j]=1
            E[i,j]=int(w[::-1]==target)
            L[i,j]=int(w[::-1]<target)
        self.monomials[w]=(T,E,L)
        return T,E,L

    def mass(self,F):
        _,E,L=F
        return int(L[0,self.n]+(self.a[0]=="1")*E[0,self.n])

def add(A,B):
    return tuple(x+y for x,y in zip(A,B))

def sub(A,B):
    return tuple(x-y for x,y in zip(A,B))

def cat(A,B):
    T,E,L=A
    t,e,l=B
    return T@t,E@e,T@l+L@e

def inv_series(F):
    """I+F+F^2+... for strictly upper triangular F."""
    N=len(F)
    out=np.eye(N,dtype=object)
    for i in range(N-2,-1,-1):
        out[i,i+1:]=F[i,i+1:]@out[i+1:,i+1:]
    return out

def star(F):
    T,E,L=F
    t,e=inv_series(T),inv_series(E)
    return t,e,t@L@e

def base(n):
    return sorted("0"*i+"1"*j+"0" for i in range(n-1) for j in range(1,n-i))

def split(x,p):
    b=0
    while x.startswith(p):
        b+=1
        x=x[len(p):]
    return b,x

class Path:
    """One supplied history. No higher-level alphabet is materialized here."""
    def __init__(self,cut,pivots):
        self.cut=cut
        self.pivots=tuple(pivots)
        self.alphabet=base(cut.n)
        if not self.pivots or any(not p or len(p)>cut.n for p in self.pivots):
            raise ValueError("invalid pivot length")
        for i,p in enumerate(self.pivots):
            y=p
            for k in reversed(range(i)):
                b,y=split(y,self.pivots[k])
                if not y or y<=self.pivots[k] or (k==i-1 and b==0):
                    raise ValueError("invalid grouped pivot")
            if y not in self.alphabet: raise ValueError("invalid base letter")
        self.memo={}

    def greater(self,i,x):
        key=(i,x)
        if key in self.memo: return self.memo[key]
        C=self.cut
        if i==0:
            G=C.zero
            for w in self.alphabet:
                if w>x: G=add(G,C.word(w))
        else:
            p=self.pivots[i-1]
            b,y=split(x,p)
            greater_old=self.greater(i-1,p)
            prefixes=C.zero
            for k in range(b):
                prefixes=add(prefixes,C.word(p*k))
            G=add(cat(prefixes,greater_old),cat(C.word(p*b),self.greater(i-1,y)))
        self.memo[key]=G
        return G

    def contribution(self):
        """First unique terminal, pure repeat, and all unique mass at this history."""
        C=self.cut
        i=len(self.pivots)-1
        p=self.pivots[i]
        G=self.greater(i,p)
        rest=star(G)
        all_unique=C.n*C.mass(cat(C.word(p),rest))
        first=all_unique
        if i and split(p,self.pivots[i-1])[0]==1:
            inherited=star(self.greater(i-1,self.pivots[i-1]))
            first-=C.n*C.mass(cat(C.word(p),inherited))
        repeat=0
        if C.n%len(p)==0 and C.n>len(p):
            repeat=len(p)*C.mass(C.word(p*(C.n//len(p))))
        return first,repeat,all_unique

def bounded(a,depth):
    """Exact mass resolved at or before depth. Enumerate pivots only for path discovery."""
    C=Cut(a)
    levels=[[0,0] for _ in range(depth+1)]
    def visit(past,alphabet):
        i=len(past)
        for p in alphabet:
            if past and not p.startswith(past[-1]): continue
            f,r,_=Path(C,past+(p,)).contribution()
            levels[i][0]+=f
            levels[i][1]+=r
            # A tied, impure pivot must leave room for a strictly greater letter.
            if i<depth and 2*len(p)<C.n:
                nxt=[p*k+x for x in alphabet if x>p
                     for k in range((C.n-len(x))//len(p)+1)]
                if nxt: visit(past+(p,),nxt)
    visit((),base(C.n))
    return int("1" in a),levels

if __name__=="__main__":
    import sys
    print(bounded(sys.argv[1],int(sys.argv[2])))
