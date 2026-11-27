"""Count an entire unknown shared-history family using at most one ordinary rank query."""
LETTERS=tuple("0"*(5-j)+"1"*j+"0" for j in range(1,6))
A,B0,B1,X0,X1=LETTERS

def block(s,b):
    return A+"".join(B1 if x=="1" else B0 for x in s)+(X1 if b=="1" else X0)

def encode(s,q):
    P="".join(block(s,b) for b in q)
    return "0"+P[:-1]

def digits(i,n):
    return format(i,f"0{n}b") if n else ""

def lower_bound(size,predicate):
    lo,hi=0,size
    while lo<hi:
        mid=(lo+hi)//2
        if predicate(mid): hi=mid
        else: lo=mid+1
    return lo

def family_mass(a,m,D,rank):
    """rank(q) is the unrestricted weighted strict rank at length m."""
    L=6*(D+2)
    if m<1 or D<0 or len(a)!=L*m or set(a)-set("01"):
        raise ValueError("inconsistent family/cut")
    leading=(a[1:]+"0")[::-1][:L]
    total=0
    for b,layer in (("0",1),("1",(1<<m)-1)):
        def key(i):
            return block(digits(i,D)[::-1],b)[::-1]
        i=lower_bound(1<<D,lambda i:key(i)>=leading)
        total+=i*layer
        if i==1<<D or key(i)!=leading: continue
        s=digits(i,D)[::-1]
        if b=="0":
            total+=int(encode(s,"0"*m)[::-1]<a[::-1])
        else:
            # Plain q keys are sorted by the colex order of their aligned encodings.
            j=lower_bound(1<<m,lambda j:encode(s,digits(j,m)[::-1])[::-1]>=a[::-1])
            selected=(1<<m) if j==1<<m else rank(digits(j,m)[::-1])
            total+=selected-int(encode(s,"0"*m)[::-1]<a[::-1])
    return L*total

def rank_via_family(a,D,oracle):
    """Recover ordinary weighted colex rank from the all-histories family oracle."""
    m=len(a)
    s="0"*D
    L=6*(D+2)
    value,rem=divmod(oracle(encode(s,a),m,D),L)
    assert rem==0
    # With the smallest filler, all other fillers have a larger tail block
    # for the same terminal bit. All terminal-zero necklaces are constant zero.
    if a[-1]=="1":
        value-=(1<<D)-1
    return value
