from time import perf_counter
from check import profile
from unique import unique_mass
from composition import refined
from profile_tools import integrated

if __name__=="__main__":
    a="00000110110111"
    for R in range(1,6):
        t=perf_counter()
        print("Threshold",a,"depth 3, maximum origins",R,refined(a,3,R),"seconds",round(perf_counter()-t,3),flush=True)
    for n in (12,16,20,24):
        a=("00010111"*4)[:n-1]+"1"
        t=perf_counter()
        print("Unique least return at depth 1",n,a,unique_mass(a,"0"),unique_mass("1"*n,"0"),
              "seconds",round(perf_counter()-t,3),flush=True)
    for n,h,J in [(12,2,64),(16,3,64),(32,3,64)]:
        lo,hi=integrated(n,h,J)
        exact=profile(n,h)[1] if n<=16 else None
        print("Integrated width",n,h,J,lo,hi,"exact",exact,flush=True)
