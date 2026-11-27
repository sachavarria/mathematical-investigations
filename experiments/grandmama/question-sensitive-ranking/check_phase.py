from verify import orbits
from phase import precision,temporal
from pathlib import Path
import sys,time
if __name__=="__main__":
    archive=Path(sys.argv[1]) if sys.argv[1:] else Path(__file__).resolve().parent.parent/"return-ranking"
    cases=0
    for n in range(1,9):
        clock="".join(w[:v] for w,v in sorted(orbits(n),key=lambda x:x[0][::-1]))
        for i in range(1<<n):
            w=(clock*2)[i:i+n]
            for K in (3,100,1<<(n+1)):
                start,width=temporal(w,K,archive)
                assert (i-start)%(1<<n)<=width and K*width<=1<<n
                cases+=1
    print("Full-clock cyclic interval checks:",cases)
    a="000000001101010100001101100101011000010010001110100000010111"
    for K in (100,400):
        t=time.perf_counter()
        print("Order 60, K =",K,"(L,U,cells)",precision(a,K),"seconds",round(time.perf_counter()-t,4))
