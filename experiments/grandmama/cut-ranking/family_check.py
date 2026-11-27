"""Use bit-level orbit counts, including cuts not in the code image."""
from collections import Counter
from functools import lru_cache
import family
from check import orbit,words
from cut_rank import rank

# Different ambient cuts can have the same pullback; share only the identical oracle call.
family.rank=lru_cache(None)(rank)
if __name__=="__main__":
    tested=0; density_calls=0
    for T in range(2,8):
        small=list(words(T))
        for t in range(1,T):
            canonical=Counter(min(orbit(q)) for q in small if q.count("1")==t)
            acc=0
            for a in sorted(small,key=lambda x:x[::-1]):
                assert family.rank(a,density=t)[0]==acc
                acc+=canonical[a]; density_calls+=1
            for h in (1,3,4):
                n=T+h*t
                mass=Counter()
                for q in small:
                    if q.count("1")!=t or q!=min(orbit(q)):
                        continue
                    # Build the original return stream (long = 1 then zeros), then canonicalize.
                    stream="".join("0" if c=="0" else "1"+"0"*h for c in q)
                    roots=orbit(stream)
                    assert min(roots)==family.expand(q,h)
                    mass[min(roots)]=len(roots)
                if n<=10:
                    keys=range(1<<n)
                else:
                    keys={0,(1<<n)-1,(1<<n)//3}
                    for w in mass:
                        k=int(w[::-1],2);keys.update((k,max(0,k-1),min((1<<n)-1,k+1)))
                ordered=sorted((int(w[::-1],2),v) for w,v in mass.items())
                for k in keys:
                    b=format(k,"0%db"%n)[::-1]
                    actual=sum(v for j,v in ordered if j<k)
                    assert family.family_mass(b,T,t,h)==actual,(T,t,h,b)
                    tested+=1
    print("Direct fixed-density threshold checks:",density_calls)
    print("Ambient two-return threshold checks:",tested)
    reverse_calls=0
    for T in range(1,8):
        small=list(words(T))
        expected=Counter(min(orbit(q)) for q in small)
        total=0
        for a in sorted(small,key=lambda w:w[::-1]):
            assert family.rank_via_family(a)==total
            total+=expected[a]
            reverse_calls+=1
    print("General threshold checks via fixed-marker reduction:",reverse_calls)
