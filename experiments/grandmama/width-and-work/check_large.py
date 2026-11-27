"""Direct composition oracle for the order-64 primitive-width examples."""
from itertools import combinations
from run_rank import rank

def compositions(n,r):
    for cuts in combinations(range(1,n),r-1):
        edges=(0,)+cuts+(n,)
        yield tuple(b-a for a,b in zip(edges,edges[1:]))

def main():
    n=64
    test="00101101"*8
    key=test[::-1]
    accepted=[0]*4
    mass=[0]*4
    for p in (2,4,8,16,32,64):
        for r in range(1,min(3,p//2)+1):
            for zero in compositions(p//2,r):
                for one in compositions(p//2,r):
                    blocks=["0"*a+"1"*b for a,b in zip(zero,one)]
                    w="".join(blocks)
                    if any("".join(blocks[j:]+blocks[:j])<=w for j in range(1,r)):
                        continue
                    mass[r]+=p
                    accepted[r]+=p*((w*(n//p))[::-1]<key)
    for d in range(1,4):
        assert sum(accepted[:d+1])==rank(test,d,32)
        assert sum(mass[:d+1])==rank("1"*n,d,32)
        print("cap",d,"total mass",sum(mass[:d+1]),"strictly below cut",sum(accepted[:d+1]))
if __name__=='__main__': main()
