from shuffles import lf,one_cycle,layouts,quotas,primitive_cylinder,rank
from itertools import product,combinations
from collections import Counter
from math import comb,prod

def bits(n):
    return map("".join,product("01",repeat=n))

def rotation(w,i): return w[i:]+w[:i]

def bwt(w):
    rows=sorted(rotation(w,i) for i in range(len(w)))
    return "".join(r[-1] for r in rows)

def explicit_path(n,z,s):
    buckets=Counter()
    for b in bits(n):
        if b.count("0")!=z or not one_cycle(lf(b)): continue
        loc=[0]
        for c in s:
            if b[loc[-1]]!=c: break
            loc.append(lf(b)[loc[-1]])
        if len(loc)==len(s)+1: buckets[tuple(loc)]+=1
    return buckets

def witness(m,choices):
    ell=(3*m).bit_length()
    def tag(i):
        return "".join("0110" if b=="0" else "1010" for b in format(i,f"0{ell}b"))
    def block(i): return "0001"+tag(i)+"11"
    root="00001"+tag(0)+"111"
    tail="".join(block(3*i+2) for i in range(m))
    w=root+"".join(block(3*i+(1 if c=="0" else 3)) for i,c in enumerate(choices))+tail
    return w,tail,len(block(0))

if __name__=="__main__":
    bin_checks=full_checks=path_checks=0
    for n in range(1,9):
        roots=Counter(min(rotation(w,i) for i in range(n)) for w in bits(n))
        for w,v in roots.items():
            if v==n:
                b=bwt(w);perm=lf(b);row=0;label=""
                assert one_cycle(perm)
                for _ in range(n):
                    label+=b[row];row=perm[row]
                assert row==0 and label==w[::-1]
        current=[0]*(n+1)
        for key in range(1<<n):
            a=format(key,f"0{n}b")[::-1]
            if n<=7 or key in (0,1,83,149,184,255):
                assert rank(a)==sum(current)
                full_checks+=1
                for z in range(n+1):
                    assert rank(a,z)==current[z]
                    bin_checks+=1
            current[a.count("0")]+=roots[a]
    from shuffles import twisted
    for n in range(3,8):
        for k in range(1,n):
            for s in bits(k):
                for z in range(1,n):
                    truth=explicit_path(n,z,s)
                    for loc in layouts(n,z,s):
                        g=quotas(n,z,s,loc)
                        t=loc[-1]-sum(i<loc[-1] for i in loc[:-1])
                        value=0 if g is None else twisted(g,t)
                        assert value==truth.pop(tuple(loc),0)
                        path_checks+=1
                    assert not truth
    print("Unrestricted / fixed-zero rank comparisons:",full_checks,bin_checks)
    print("Individual pinned layouts checked, including impossible layouts:",path_checks)
    for m in range(1,10):
        histories=set()
        for choices in bits(m):
            w,tail,B=witness(m,choices)
            assert w.count("1")*2==len(w)
            # Sort the literal rotations independently of the contraction.
            indices=sorted(range(len(w)),key=lambda j:rotation(w,j))
            assert indices[0]==0
            inv={j:i for i,j in enumerate(indices)}
            path=tuple(inv[len(w)-j] for j in range(1,len(tail)+1))
            for i,c in enumerate(choices):
                assert path[len(tail)-i*B-1]==2+2*i+int(c=="0")
            histories.add(path)
        assert len(histories)==1<<m
        print("Probe blocks, order, contracted edges, distinct histories:",m,len(w),len(tail),len(histories))
    for w in ("00101011","00101101"):
        b=bwt(w)
        print(w,"BWT",b,"LF",lf(b),"strict answer at 00011101",w[::-1]<"00011101"[::-1])
