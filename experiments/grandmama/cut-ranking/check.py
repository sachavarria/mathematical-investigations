"""Compare all three answers with literal rotation orbits. Standard Python."""
from collections import Counter
from itertools import product
from math import isqrt
from cut_rank import rank, marker_machine, transcripts

def words(n):
    return ("".join(p) for p in product("01",repeat=n))
def orbit(w):
    return {w[j:]+w[:j] for j in range(len(w))}
def structural(n):
    cases = 0
    for w in words(n):
        circle=w*4; rots=orbit(w)
        for h in range(1,n+1):
            u=min(rots)[:h]
            marks=[j for j in range(n) if circle[j:j+h]==u]
            pairs=list(zip(marks,marks[1:]+[n+marks[0]]))
            short={circle[i+h:j+h] for i,j in pairs if 2*(j-i)<h}
            long={circle[i+h:j+h] for i,j in pairs if 2*(j-i)>=h}
            assert len(short)<=1 and all(s<z for s in short for z in long)
            if long:
                cuts=sorted(j%n for i,j in pairs if 2*(j-i)>=h)
                ends=cuts[1:]+[cuts[0]+n]
                payloads=[circle[i+h:j+h] for i,j in zip(cuts,ends)]
                start,step=marker_machine(u)
                for s in payloads:
                    state=start
                    for j,b in enumerate(s):
                        state=step(state,b)
                        assert (state==-2)==(j==len(s)-1) and state!=-1
                order=[payloads[i:]+payloads[:i] for i in range(len(cuts))]
                minimizers={j for j,p in zip(cuts,order) if p==min(order)}
                assert minimizers=={j for j in range(n) if circle[j:j+n]==min(rots)}
                token_period=len(set(map(tuple,order)))
                assert n*token_period==len(rots)*len(cuts)
            cases+=1
    return cases

def verify(n,exhaustive):
    tally=Counter(min(orbit(w)) for w in words(n))
    total=[0,0,0]; tested=calls=0
    chosen={0,1,2,2**n//5,2**n//3,2**n//2+1,2**n-2,2**n-1}
    for key,a in enumerate(sorted(words(n),key=lambda w:w[::-1])):
        if exhaustive or key in chosen:
            hs={1,n,isqrt(n-1)+1} if n<=5 else {isqrt(n-1)+1}
            for h in hs:
                ans=rank(a,h)
                assert ans==tuple(total),(a,h,ans,total)
                calls+=1
            tested+=1
        amount=tally[a]
        for j,value in enumerate((amount, int(amount>0), int(amount==n))):
            total[j]+=value
    return tested,calls
if __name__=="__main__":
    print("order,thresholds,rank_calls,word_marker_checks",flush=True)
    for n in range(1,12):
        print(n,*verify(n,n<=7),structural(n),sep=",",flush=True)
