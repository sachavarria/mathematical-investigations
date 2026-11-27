"""Exercise the dictionary branch directly, including overlaps and nonuniform leaf depths."""
from collections import Counter
from fractions import Fraction
from math import comb
from check import words,rots
from certificate import certificate,dictionary,interval_from_leaves

if __name__=="__main__":
    tests=exact_tests=0
    for n in range(2,10):
        names=words(n)
        for d in range(1,n):
            m=min(d,n-d)
            totals=Counter(min(rots(w)) for w in names if w.count("1")==d)
            for q in (Fraction(1,2),Fraction(1,5),Fraction(1,10)):
                leaves=list(dictionary(m,n-m,q))
                leafset=set(leaves)
                ambiguous=0
                for w,mass in totals.items():
                    gaps=tuple(map(len,w[:-1].split("1") if d<=n-d else w[1:].split("0")))
                    u=next(gaps[:i] for i in range(1,m+1) if gaps[:i] in leafset)
                    ambiguous+=mass*int(sum((gaps+gaps)[j:j+len(u)]==u for j in range(m))>1)
                target=0
                for j,a in enumerate(names):
                    if n<=5 or j in (0,1,len(names)//3,len(names)//2,len(names)-2,len(names)-1):
                        lo,hi=interval_from_leaves(a,d,leaves)
                        assert lo<=target<=hi<=comb(n,d) and hi-lo in (0,ambiguous)
                        if q==Fraction(1,2):
                            assert certificate(a,d,3)==(target,target)
                            exact_tests+=1
                        tests+=1
                    target+=totals[a]
    print("Dictionary intervals checked:",tests)
    print("Small-minority exact fallback checks:",exact_tests)
