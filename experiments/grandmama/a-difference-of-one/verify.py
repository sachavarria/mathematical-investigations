"""Independent exhaustive rotation-orbit tally. Run python3 verify.py."""
from itertools import product
from collections import Counter

def ranks(n):
    weights=Counter()
    for seq in product("01",repeat=n):
        w="".join(seq)
        weights[min(w[i:]+w[:i] for i in range(n))]+=1
    a="0"*(n-1)+"1"
    b="0"*(n-2)+"11"
    rank=lambda w:sum(v for k,v in weights.items() if k[::-1]<w[::-1])
    keys=sorted(weights,key=lambda s:s[::-1])
    cycle="".join(w[:weights[w]] for w in keys)
    assert weights[a]==weights[b]==n
    assert rank(a)==1 and len(cycle)==2**n
    for w in (a,b):
        assert (cycle*2)[rank(w):rank(w)+n]==w
    d=rank(b)-rank(a)
    if n>=16: assert min(d,2**n-d)*128>2**n
    return rank(a),rank(b),d
if __name__=="__main__":
    print("order,first_tick,second_tick,forward_interval")
    for n in range(3,17):
        print(n,*ranks(n),sep=",")
