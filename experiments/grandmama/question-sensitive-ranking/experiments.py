from pathlib import Path
import sys,time,platform
from fractions import Fraction
from random import Random
import numpy as np
from sensitive import bounds,gap_bounds
from verify import profile,orbits

def run():
    archive=Path(sys.argv[1]) if sys.argv[1:] else Path(__file__).resolve().parent.parent/"fixed-density-gaps"
    sys.path.insert(0,str(archive))
    from certificate import dictionary,interval_from_leaves
    print(platform.machine(),platform.python_version(),"NumPy",np.__version__,flush=True)
    print("order 14, matched gap dictionaries: denominator leaves old new old_s new_s",flush=True)
    a="00000110110111"
    for den in (2,8,32,128):
        leaves=list(dictionary(7,7,Fraction(1,den)))
        t=time.perf_counter()
        old=interval_from_leaves(a,7,leaves)
        t1=time.perf_counter()
        new=gap_bounds(a,7,leaves)
        print(den,len(leaves),old,new,round(t1-t,4),round(time.perf_counter()-t1,4),flush=True)
    print("all primitive boundary questions, order 16: depth boundaries multi_origin_mass min Q1 median Q3 max exact",flush=True)
    n=16
    queries=[int(w[::-1],2) for w,v in orbits(n) if v==n]
    for h in (3,5,7,9):
        lo,hi,multi=profile(n,h)
        widths=sorted(hi[k]-lo[k] for k in queries)
        print(h,len(queries),multi,*[widths[(len(widths)-1)*i//4] for i in range(5)],widths.count(0),flush=True)
    print("binary transfer, uniform full cycle: n h primitive_threshold L U width_percent cells seconds",flush=True)
    rng=Random(404)
    for n in (24,32,48,60):
        x=format(rng.getrandbits(n),f"0{n}b")
        a=min(x[i:]+x[:i] for i in range(n))
        assert all(a!=a[i:]+a[:i] for i in range(1,n))
        for h in (6,9,11):
            t=time.perf_counter()
            l,r,c=bounds(a,h)
            print(n,h,a,l,r,round(100*(r-l)/(1<<n),6),c,round(time.perf_counter()-t,4),flush=True)
    print("pairs refinement, uniform full cycle: a h base refined base_s refined_s",flush=True)
    for a in ("00010111","00000110110111","000100100011"):
        for h in (3,5):
            t=time.perf_counter()
            old=bounds(a,h)[:2]
            t1=time.perf_counter()
            new=bounds(a,h,resolve_pairs=True)[:2]
            print(a,h,old,new,round(t1-t,4),round(time.perf_counter()-t1,4),flush=True)
if __name__=="__main__":
    run()
