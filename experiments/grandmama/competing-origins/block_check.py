from check import circles
from blocks import block_mass
from unique import unique_mass
from time import perf_counter

if __name__=="__main__":
    cases=0
    for n in range(2,13):
        N=1<<n
        keys=range(N) if n<=5 else [N//2+1,3*N//4,7*N//8,N-1]
        for h in sorted({1,min(3,n)}):
            for d in (None,n//2):
                population=list(circles(n,h,d))
                for key in keys:
                    a=format(key,f"0{n}b")[::-1]
                    for u in sorted({entry[1] for entry in population if entry[1]}):
                        expected=[0]*(n//2+1)
                        for w,v,_,g,_,mass in population:
                            if u==v and w[::-1]<a[::-1]:
                                expected[g.count(min(g))]+=mass
                        for k in range(1,n//2+1):
                            ans=block_mass(a,u,k,d)
                            assert ans==expected[k],(a,u,d,k,ans,expected[k])
                            if k==1: assert ans==unique_mass(a,u,d)
                            cases+=1
    print("Least-return multiplicity slice comparisons:",cases)
    a="00000110110111"
    for h in (1,3):
        for u in sorted({v for _,v,*_ in circles(len(a),h) if v}):
            print("cut",a,"cell",u,"accepted mass at least-return frequencies 1,2,3:",
                  [block_mass(a,u,k) for k in (1,2,3)])
