from verify import orbits,candidates
from sensitive import bounds

def direct(a,h,d):
    l=r=0
    for w,mass in orbits(len(a)):
        if d is not None and w.count("1")!=d: continue
        xs=candidates(w,h)
        flags=[x[::-1]<a[::-1] for x in xs]
        if len(xs)==2:
            flags=[min(xs)[::-1]<a[::-1]]
        l+=mass*all(flags)
        r+=mass*any(flags)
    return l,r

if __name__=="__main__":
    cases=0
    for n in range(2,11):
        keys=range(1<<n) if n<=6 else [0,1,(1<<n)//3,(1<<n)//2+1,(1<<n)-2,(1<<n)-1]
        for h in sorted({1,min(3,n),min(4,n)}):
            for k in keys:
                a=format(k,f"0{n}b")[::-1]
                for d in (None,n//2):
                    actual=bounds(a,h,d,True)[:2]
                    assert actual==direct(a,h,d),(a,h,d,actual,direct(a,h,d))
                    cases+=1
    print("Two-origin interval comparisons:",cases)
