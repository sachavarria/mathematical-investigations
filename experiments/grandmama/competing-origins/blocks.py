"""Reference counter parameterized by the frequency of the least elementary return."""
from functools import lru_cache
from itertools import product
from math import comb,prod
from composition import returns,parses,transcripts
from cut_rank import match_step

def shapes(cap,k):
    """k ordered lists of nonminimum slots, plus the common minimum slot 0."""
    def extend(left,rows,size):
        if not left:
            yield rows,size
            return
        for length in range(cap-k-size+2):
            yield from extend(left-1,rows+[tuple(range(size,size+length))],size+length)
    if k<=cap:
        yield from extend(k,[],1)

def systems(rows,edges,size):
    """Resolve every required block comparison into slot equalities and strict edges."""
    options=[]
    for i,j,same in edges:
        a,b=rows[i],rows[j]
        pairs=list(zip(a,b))
        if same:
            if len(a)!=len(b): return
            options.append([(pairs,[])])
        else:
            cases=[(pairs[:v],[pair]) for v,pair in enumerate(pairs)]
            if len(a)<len(b): cases.append((pairs,[]))
            options.append(cases)
    for cases in product(*options):
        parent=list(range(size))
        def root(x):
            while parent[x]!=x:
                x=parent[x]
            return x
        for eq,_ in cases:
            for i,j in eq:
                parent[root(j)]=root(i)
        names=[root(i) for i in range(size)]
        strict={(names[i],names[j]) for _,lt in cases for i,j in lt}
        if all(i!=j for i,j in strict):
            yield names,strict

def symmetric(start,step,n,d,sequence,edges,pivot,tail,fixed):
    multiplicity={i:sequence.count(i) for i in set(sequence)}
    pins={}
    for i,w in zip(sequence[pivot+1:],fixed):
        if i in pins and pins[i]!=w: return 0
        pins[i]=w
    pivot=sequence[pivot]
    if pivot in pins and not pins[pivot].endswith(tail): return 0
    if pivot in pins: pivot=None
    # Keep the root explicit, even if pinned. Other fixed classes are charged once here.
    root_pin=pins.pop(0,None)
    constraints=[]
    if root_pin is not None: constraints.append((0,"=",root_pin))
    if pins: constraints.append((0,"<",min(pins.values())))
    remaining=set(multiplicity)-pins.keys()
    special={0}
    if pivot is not None: special.add(pivot)
    strict=set()
    for i,j in edges:
        if i in pins and j in pins:
            if pins[i]>=pins[j]: return 0
        elif i in pins:
            special.add(j);constraints.append((j,">",pins[i]))
        elif j in pins:
            special.add(i);constraints.append((i,"<",pins[j]))
        else:
            special.update((i,j));strict.add((i,j))
    for i in special-{0}: strict.add((0,i))
    special=sorted(special)
    index={x:j for j,x in enumerate(special)}
    allmask=(1<<len(special))-1
    pair=[(1<<index[i],1<<index[j]) for i,j in strict]
    tests=[(1<<index[i],op,w) for i,op,w in constraints]
    pbit=(1<<index[pivot]) if pivot is not None else 0
    ordinary=remaining-set(special)
    weights=sorted({multiplicity[i] for i in ordinary})
    counts=tuple(sum(multiplicity[i]==w for i in ordinary) for w in weights)
    def charge(mask,counts):
        return sum(w*c for w,c in zip(weights,counts))+sum(multiplicity[i] for j,i in enumerate(special) if mask>>j&1)
    n-=sum(multiplicity[i]*len(w) for i,w in pins.items())
    if d is not None: d-=sum(multiplicity[i]*w.count("1") for i,w in pins.items())
    @lru_cache(None)
    def rec(mask,counts,depth,state,suffix,signs,budget,ones):
        if budget<0 or ones is not None and not 0<=ones<=budget: return 0
        used=charge(mask,counts)
        if not used: return int(budget==0)
        if state==-2:
            if budget or mask&1 and any(counts) or any(mask&i and mask&j for i,j in pair): return 0
            if mask&pbit and suffix!=len(tail): return 0
            for (bit,op,w),s in zip(tests,signs):
                if mask&bit:
                    value=s or ((depth>len(w))-(depth<len(w)))
                    if not {"=":value==0,"<":value<0,">":value>0}[op]: return 0
            return 1
        rest=budget-used
        if rest<0: return 0
        total=0
        left=mask
        while True:
            right=mask^left
            if not any(right&i and left&j for i,j in pair):
                for c0 in product(*(range(c+1) for c in counts)):
                    if right&1 and any(c0): continue
                    c1=tuple(c-a for c,a in zip(counts,c0))
                    groups=[]
                    for b,m,c in (("0",left,c0),("1",right,c1)):
                        use=charge(m,c)
                        z=step(state,b) if use else None
                        ss=tuple((s or (1 if depth>=len(w) else (b>w[depth])-(b<w[depth]))) if m&bit else 0
                                 for (bit,_,w),s in zip(tests,signs))
                        groups.append(((m,c,depth+1,z,match_step(tail,suffix,b) if m&pbit else 0,ss),use))
                    (arg0,n0),(arg1,n1)=groups
                    if arg0[3]==-1 or arg1[3]==-1: continue
                    factor=prod(comb(c,a) for c,a in zip(counts,c0))
                    lengths=(0,) if not n0 else (rest,) if not n1 else range(rest+1)
                    rem=None if ones is None else ones-n1
                    for l in lengths:
                        alloc=(None,) if rem is None else range(max(0,rem-rest+l),min(l,rem)+1)
                        for w in alloc:
                            v=rec(*arg0,l,w)
                            if v: total+=factor*v*rec(*arg1,rest-l,None if rem is None else rem-w)
            if not left: break
            left=(left-1)&mask
        return total
    ans=rec(allmask,counts,0,start,0,(0,)*len(tests),n,d)
    rec.cache_clear()
    return ans

def block_mass(a,u,k,d=None):
    """Strict accepted rooted mass in one cell with minimum return occurring exactly k times."""
    n,h=len(a),len(u)
    if k<1 or not 1<=h<=n or u[0]!="0": raise ValueError("invalid parameters")
    start,T=returns(u)
    def step(q,b):
        z=T[q,b]
        return -1 if z is None else -2 if z==start else z
    suffixes=["0"+a[j+1:]+u for j in range(h,n) if a[j]=="1"]
    if u[::-1]<a[:h][::-1]: suffixes.append(a[h:]+u)
    cuts=[]
    for v in suffixes:
        for b in range(1,len(v)+1):
            fixed=parses(v[b:],start,step)
            if fixed is not None: cuts.append((v[:b],fixed))
    result=0
    for rows,size in shapes(n//2,k):
        slots=[i for row in rows for i in (0,*row)]
        for s,edges in transcripts(k):
            if n*s%k: continue
            for names,strict in systems(rows,edges,size):
                seq=[names[i] for i in slots]
                for tail,fixed in cuts:
                    pivot=len(seq)-len(fixed)-1
                    if pivot>=0:
                        result+=n*s//k*symmetric(start,step,n,d,seq,strict,pivot,tail,fixed)
    return result
