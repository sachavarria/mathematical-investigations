"""Binary strict colex prefix counts via prefix-code tries. Python standard library."""
from functools import lru_cache
from itertools import product
from math import isqrt

def words(n):
    for s in product("01", repeat=n):
        yield "".join(s)

def rotations(w):
    return [w[i:] + w[:i] for i in range(len(w))]

def match_step(pattern, q, bit):
    trial = pattern[:q] + bit
    return max(i for i in range(len(pattern)+1) if trial.endswith(pattern[:i]))

def marker_machine(u):
    """-1 rejects, -2 finishes one grouped return, otherwise (q, age)."""
    h = len(u)
    cap = (h+1)//2
    base = {}
    for q in range(h+1):
        active = [i for i in range(h) if u[:q].endswith(u[:i])]
        for b in "01":
            base[q,b] = -1 if any(b < u[i] for i in active) else match_step(u,q,b)
    def step(state,b):
        q, age = state
        z = base[q,b]
        elapsed = min(age+1,cap)
        if z == h:
            return -2 if elapsed == cap else (h,0)
        return -1 if z == -1 else (z,elapsed)
    return (h,0),step

def parses(text,start,step):
    """Suffixes that parse into complete tokens. Return None on failure."""
    state = start
    result = []
    left = 0
    for j,b in enumerate(text):
        state = step(state,b)
        if state == -1:
            return None
        if state == -2:
            result.append(text[left:j+1])
            left = j+1
            state = start
    return result if left == len(text) else None

def transcripts(e):
    """Accepting paths of the prenecklace extension test, including the period."""
    def visit(j,k,edges):
        if j == e:
            p = e-k
            if e%p == 0:
                yield p,edges
            return
        yield from visit(j+1,k+1,edges+((k,j,True),))
        yield from visit(j+1,0,edges+((k,j,False),))
    yield from visit(1,0,())

def assignments(n,e,start,step,edges,fixed_suffix,whole,density=None):
    """Count tuples at exact total length using a binary prefix trie."""
    pivot = e-1-len(whole)
    exact = {pivot+1+i:w for i,w in enumerate(whole)}
    transition = {(q,b):match_step(fixed_suffix,q,b)
                  for q in range(len(fixed_suffix)+1) for b in "01"}
    @lru_cache(None)
    def solve(mask,depth,state,q,budget,ones_left):
        if ones_left is not None and not 0 <= ones_left <= budget:
            return 0
        if not mask:
            return int(budget == 0)
        has_pivot = bool(mask & (1<<pivot))
        fixed = [(i,w) for i,w in exact.items() if mask & (1<<i)]
        pending = [(i,j,same) for i,j,same in edges if mask>>i&1 and mask>>j&1]
        if state == -2:
            return int(budget==0 and all(same for _,_,same in pending)
                       and (not has_pivot or q==len(fixed_suffix))
                       and all(len(w)==depth for _,w in fixed))
        budget -= mask.bit_count()
        if budget < 0 or any(len(w)<=depth for _,w in fixed):
            return 0
        total = 0
        zeros = mask
        while True:
            ones = mask ^ zeros
            allowed = all((w[depth]=="0")==bool(zeros>>i&1) for i,w in fixed)
            for i,j,same in pending:
                if (ones>>i&1 and zeros>>j&1) or (same and zeros>>i&1 and ones>>j&1):
                    allowed = False
                    break
            lo = step(state,"0") if zeros else None
            hi = step(state,"1") if ones else None
            if allowed and lo!=-1 and hi!=-1:
                q0 = transition[q,"0"] if zeros>>pivot&1 else 0
                q1 = transition[q,"1"] if ones>>pivot&1 else 0
                splits = (0,) if not zeros else (budget,) if not ones else range(budget+1)
                for left in splits:
                    rest = None if ones_left is None else ones_left-ones.bit_count()
                    allocations = (None,) if rest is None else range(max(0,rest-(budget-left)),min(left,rest)+1)
                    for low_ones in allocations:
                        high_ones = None if rest is None else rest-low_ones
                        a = solve(zeros,depth+1,lo,q0,left,low_ones)
                        if a:
                            total += a * solve(ones,depth+1,hi,q1,budget-left,high_ones)
            if not zeros:
                break
            zeros = (zeros-1)&mask
        return total
    answer = solve((1<<e)-1,0,start,0,n,density)
    solve.cache_clear()
    return answer

def rank(a,h=None,density=None):
    if not a or set(a)-set("01"):
        raise ValueError("a must be a nonempty binary word")
    n = len(a)
    h = isqrt(n-1)+1 if h is None else h
    if not 1<=h<=n:
        raise ValueError("marker length out of range")
    if density is not None and not 0<=density<=n:
        raise ValueError("density out of range")
    result = [0,0,0]
    cap = (h+1)//2
    for u in words(h):
        p = next(i for i in range(1,h+1) if u[i:]==u[:-i])
        if 2*p<h and n%p==0:
            w = u[:p]*(n//p)
            if w == min(rotations(w)) and w[::-1]<a[::-1] and (density is None or w.count("1")==density):
                result[0]+=p; result[1]+=1; result[2]+=int(p==n)
        start,step = marker_machine(u)
        masks = ["0"+a[j+1:]+u for j in range(h,n) if a[j]=="1"]
        if u[::-1]<a[:h][::-1]:
            masks.append(a[h:]+u)
        for suffix in masks:
            for b in range(1,len(suffix)+1):
                whole = parses(suffix[b:],start,step)
                if whole is None:
                    continue
                # Total lengths of these trailing tokens are already fixed.
                available = n-len(suffix)+b
                limit = (available-max(b,cap))//cap+1
                for free_and_pivot in range(1,limit+1):
                    e = len(whole)+free_and_pivot
                    for symbol_period,edges in transcripts(e):
                        if n*symbol_period%e:
                            continue
                        ways = assignments(n,e,start,step,edges,suffix[:b],whole,density)
                        per = n*symbol_period//e
                        result[0] += per*ways
                        result[1] += ways
                        result[2] += ways*int(per==n)
    return tuple(result)

if __name__=="__main__":
    import sys
    print(rank(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else None))
