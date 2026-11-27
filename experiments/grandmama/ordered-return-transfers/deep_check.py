"""Audit the transfer on deeper histories by explicitly generating the truncated alphabets."""
from transfer import Cut,Path,base,cat
from verify import history
from shared import encode,A,B0
from random import Random

def brute_star(n,p,letters,a):
    # Concatenate explicit letters left-to-right. Update the sign using the actual bits.
    ref=a[1:]+"0"
    mem=[{} for _ in range(n+1)]
    def sign(w,target):
        return (w[::-1]>target[::-1])-(w[::-1]<target[::-1])
    mem[len(p)][sign(p,ref[:len(p)])]=1
    for i in range(len(p),n):
        for word in letters:
            j=i+len(word)
            if j>n: continue
            delta=sign(word,ref[i:j])
            for old,v in mem[i].items():
                s=delta or old
                mem[j][s]=mem[j].get(s,0)+v
    return n*(mem[n].get(-1,0)+(a[0]=="1")*mem[n].get(0,0))

if __name__=="__main__":
    rng=Random(71)
    checks=0
    for n,depth in [(20,3),(25,4),(30,5)]:
        alph=base(n)
        pivots=[]
        previous=[]
        for i in range(depth+1):
            p="0010"+"010"*i
            assert p in alph
            pivots.append(p)
            greater=[v for v in alph if v>p and len(v)+len(p)<=n]
            for a in ("1"*n,format(rng.getrandbits(n),f"0{n}b"),("00010111"*5)[:n]):
                path=Path(Cut(a),pivots)
                first,pure,all_unique=path.contribution()
                expect=brute_star(n,p,greater,a)
                assert all_unique==expect
                old=brute_star(n,p,previous,a) if i else 0
                assert first==expect-old
                checks+=1
            previous=[v for v in alph if v>p]
            alph=[p*k+x for x in previous for k in range((n-len(x))//len(p)+1)]
    print("Explicit-alphabet, independent star and inherited-unique comparisons:",checks)
    # Delayed equal-frequency paths in a genuinely nested code.
    for D in (1,3,8):
        w=encode("0"*D,"00101011")
        path,_=history(w)
        assert path[:D+1]==tuple(A+B0*i for i in range(D+1))
    print("Persistent ties checked through D=8 on the order-eight witness.")

    cut=Cut("00011101")
    for w,expected in (("00101011",0),("00101101",1)):
        from verify import payloads
        F=cut.one
        for token in payloads(w): F=cat(F,cut.word(token))
        assert cut.mass(F)==expected
    print("Ordered monomial products separate both eight-bit witnesses.")
