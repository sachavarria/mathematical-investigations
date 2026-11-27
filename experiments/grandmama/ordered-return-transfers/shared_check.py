from shared import encode,family_mass,rank_via_family
from verify import orbits,history,base
from bisect import bisect_left
from random import Random
from time import perf_counter

def index(table):
    keys=sorted(table)
    sums=[0]
    for k in keys: sums.append(sums[-1]+table[k])
    return lambda k:sums[bisect_left(keys,k)]

if __name__=="__main__":
    calls=reverse=0
    rng=Random(404)
    for m in range(1,7):
        orbs=list(orbits(m))
        rank=index({w[::-1]:v for w,v in orbs})
        for D in range(4):
            L=6*(D+2)
            n=L*m
            table={}
            samples={0,(1<<n)-1}
            for i in range(1<<D):
                s=format(i,f"0{D}b") if D else ""
                for q,v in orbs:
                    w=encode(s,q)
                    rots={w[j:]+w[:j] for j in range(n)}
                    assert min(rots)==w and len(rots)==L*v
                    assert w[::-1] not in table
                    table[w[::-1]]=len(rots)
                    k=int(w[::-1],2)
                    samples.update([k,k-1,k+1])
            f=index(table)
            for _ in range(20): samples.add(rng.getrandbits(n))
            for k in samples:
                a=format(k,f"0{n}b")[::-1]
                probes=[]
                def small(x):
                    probes.append(x)
                    return rank(x[::-1])
                assert family_mass(a,m,D,small)==f(a[::-1])
                assert len(probes)<=1
                calls+=1
            for i in range(1<<m):
                a=format(i,f"0{m}b")[::-1]
                assert rank_via_family(a,D,lambda x,m,D:f(x[::-1]))==rank(a[::-1])
                reverse+=1
    print("All-histories ambient cut checks:",calls)
    print("Converse single-query rank checks:",reverse)
    q1,q2,a="00101011","00101101","00011101"
    for s in ("","0110","0"*16,"10"*32):
        assert (encode(s,q1)[::-1]<encode(s,a)[::-1])==False
        assert (encode(s,q2)[::-1]<encode(s,a)[::-1])==True
    print("Eight-bit opposite winning answers preserved at D=0,4,16,64.")
    D=128
    threshold=encode("10"*64,a)
    probes=[]
    tiny=index({w[::-1]:v for w,v in orbits(8)})
    def query(x):
        probes.append(x)
        return tiny(x[::-1])
    start=perf_counter()
    result=family_mass(threshold,8,D,query)
    print("D=128; threshold length:",len(threshold),"mass:",result,"ordinary rank queries:",probes,
          "seconds:",round(perf_counter()-start,4))
