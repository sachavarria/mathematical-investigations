"""Additional cross-check of the older algorithm with non-default marker lengths."""
from collections import Counter
from pathlib import Path
import sys
from check import words,rots

if __name__=="__main__":
    archive=Path(sys.argv[1]) if sys.argv[1:] else Path(__file__).resolve().parent.parent/"cut-ranking"
    sys.path.insert(0,str(archive))
    from cut_rank import rank
    cases=0
    for n in range(8,11):
        names=words(n)
        mass=Counter(min(rots(w)) for w in names)
        for h in (1,2,3,4,5,6,7,n):
            for a in (names[len(names)//3],names[-2]):
                for d in {1,n//2,n-1}:
                    small=[v for w,v in mass.items() if w.count("1")==d and w[::-1]<a[::-1]]
                    assert rank(a,h,d)==(sum(small),len(small),small.count(n))
                    cases+=1
    print("Additional marker-scale/density/threshold checks:",cases)
