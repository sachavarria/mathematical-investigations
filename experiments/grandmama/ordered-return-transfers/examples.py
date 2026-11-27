from transfer import bounded
from verify import history,orbits,payloads
from collections import Counter
if __name__=="__main__":
    for a in ("00000110110111","1"*14):
        print(a,bounded(a,2))
    for n in (8,14,18,20):
        hist=Counter()
        for w,v in orbits(n):
            if len(set(w))>1:
                hist[len(history(w)[0])-1]+=v
        print("Direct orbit mass by stopping level, n =",n,sorted(hist.items()))
    a="00011101"
    for w in ("00101011","00101101"):
        starts=[i for i in range(len(w)) if w[i-1]=="1" and w[i]=="0"]
        keys=[int((w[i:]+w[:i])[::-1],2) for i in starts]
        print(w,payloads(w),keys,"winning answer:",w[::-1]<a[::-1])
