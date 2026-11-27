"""Exact fixed-density colex rank by gap values. Standard library only."""
def least_feasible_key(key, ones, forced_index, forced_bit):
    """First key >= input with the given weight and specified bit."""
    n=len(key)
    def can_fill(start,left):
        forced=int(forced_bit) if start<=forced_index else 0
        free=n-start-int(start<=forced_index)
        return 0<=left-forced<=free
    pivot=None
    used=0
    for i,bit in enumerate(key):
        if bit=="0" and (i!=forced_index or forced_bit=="1") and can_fill(i+1,ones-used-1):
            pivot=(i,ones-used-1)
        if i==forced_index and bit!=forced_bit:
            break
        used+=int(bit)
    else:
        if used==ones:
            return key
    if pivot is None:
        return None
    i,left=pivot
    output=list(key[:i]+"1")
    for j in range(i+1,n):
        bit=forced_bit if j==forced_index else "0" if can_fill(j+1,left) else "1"
        output.append(bit)
        left-=int(bit)
    return "".join(output)

def transcripts(m):
    def visit(j,k,edges):
        if j==m:
            p=m-k
            if m%p==0:
                yield p,edges
            return
        yield from visit(j+1,k+1,edges+[(k,j,True)])
        yield from visit(j+1,0,edges+[(k,j,False)])
    yield from visit(1,0,[])

def count_assignments(m,B,descending,edges,cut,pivot):
    """Place labelled slots at successive integer levels; track the gap sum."""
    full=(1<<m)-1
    states={(0,0):1}
    levels=range(B,-1,-1) if descending else range(B+1)
    for v in levels:
        eligible=full
        if cut is not None:
            for i in range(pivot,m):
                ok=v==cut[i] if i>pivot else (v>cut[i] if descending else v<cut[i])
                if not ok:
                    eligible^=1<<i
        future=dict(states)    # choose no slots at this value
        for (done,weight),ways in states.items():
            avail=eligible & (full^done)
            group=avail
            while group:
                used=weight+v*group.bit_count()
                ok=used<=B
                for i,j,equal in edges:
                    if equal and bool(group>>i&1)!=bool(group>>j&1):
                        ok=False
                        break
                    if not equal and group>>j&1 and not done>>i&1:
                        ok=False
                        break
                if ok:
                    state=(done|group,used)
                    future[state]=future.get(state,0)+ways
                group=(group-1)&avail
        states=future
    return states.get((full,B),0)

def rank(a,d):
    """Strict colex totals in order (weighted mass, necklaces, Lyndon words)."""
    n=len(a)
    if not n or set(a)-set("01") or not 0<=d<=n:
        raise ValueError("expected a nonempty binary threshold and valid density")
    if d in (0,n):
        accepted=int(("1" if d else "0")*n<a[::-1])
        return accepted,accepted,accepted*int(n==1)
    descending=d<=n-d
    m=min(d,n-d)
    B=n-m
    key=least_feasible_key(a[::-1],d,0 if descending else n-1,"1" if descending else "0")
    cut=None
    if key is not None:
        aligned=key[::-1]
        gaps=aligned[:-1].split("1") if descending else aligned[1:].split("0")
        cut=tuple(map(len,gaps))
    result=[0,0,0]
    for period,edges in transcripts(m):
        if n*period%m:
            continue
        for pivot in (range(m) if cut is not None else (None,)):
            ways=count_assignments(m,B,descending,edges,cut,pivot)
            bits=n*period//m
            result[0]+=bits*ways
            result[1]+=ways
            result[2]+=(bits==n)*ways
    return tuple(result)

if __name__=="__main__":
    import sys
    print(rank(sys.argv[1],int(sys.argv[2])))
