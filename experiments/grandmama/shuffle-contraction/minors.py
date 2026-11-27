"""Two ways to sum the cycle cofactor for a residual quota/twist instance."""
from fractions import Fraction
from shuffles import lf,twisted
from itertools import product

def cofactor(matrix):
    a=[[Fraction(int(i==j))-matrix[i][j] for j in range(1,len(matrix))]
       for i in range(1,len(matrix))]
    det=Fraction(1)
    for i in range(len(a)):
        j=next((j for j in range(i,len(a)) if a[j][i]),None)
        if j is None: return Fraction(0)
        if j!=i:
            a[i],a[j]=a[j],a[i]
            det=-det
        pivot=a[i][i]
        det*=pivot
        for j in range(i+1,len(a)):
            ratio=a[j][i]/pivot
            for k in range(i+1,len(a)): a[j][k]-=ratio*a[i][k]
    return det

def twist(j,h):
    return h if j==0 else j-1 if j<=h else j

def signed_minor_sum(gaps,h):
    n=sum(b for b,_ in gaps)
    z=sum(c for _,c in gaps)
    ends={}
    i=j=0
    for b,c in gaps:
        i+=b;j+=c;ends[i]=j
    answer=0
    for subset in range(0,1<<n,2):  # exclude cofactor root 0
        target=[bool(subset>>twist(j,h)&1) for j in range(n)]
        prefix=[0]
        for selected in target: prefix.append(prefix[-1]+selected)
        dp={0:1}
        for i in range(n):
            future={}
            chosen=bool(subset>>i&1)
            for used,mass in dp.items():
                ones=i-used
                for bit,j in ((0,used),(1,z+ones)):
                    if bit==0 and used==z or bit==1 and ones==n-z: continue
                    v=used+(bit==0)
                    if i+1 in ends and v!=ends[i+1] or chosen!=target[j]: continue
                    inv=(prefix[z+ones]-prefix[z]) if chosen and bit==0 else 0
                    future[v]=future.get(v,0)+(-mass if inv%2 else mass)
            dp=future
        parity=subset.bit_count()+(prefix[h+1]-prefix[1] if target[0] else 0)
        answer+=(-1 if parity%2 else 1)*dp.get(z,0)
    return answer

def switch_sum(gaps,h):
    n=sum(b for b,_ in gaps)
    z=sum(c for _,c in gaps)
    mean=[[Fraction(0) for _ in range(n)] for _ in range(n)]
    i=low=0
    choices=1
    for size,quota in gaps:
        high=z+i-low
        if quota==0 or quota==size:
            start=high if quota==0 else low
            for k in range(size): mean[i+k][twist(start+k,h)]=1
        elif (size,quota)==(2,1):
            choices*=2
            for row in (i,i+1):
                for col in (low,high): mean[row][twist(col,h)]=Fraction(1,2)
        else: raise ValueError("wide mixed interval")
        i+=size;low+=quota
    result=choices*cofactor(mean)
    assert result.denominator==1
    return int(result)

if __name__=="__main__":
    from random import Random
    rng=Random(404)
    tests=switches=0
    for n in range(1,10):
        for _ in range(30):
            cuts=sorted({0,n}|{j for j in range(1,n) if rng.random()<0.4})
            gaps=tuple((j-i,rng.randrange(j-i+1)) for i,j in zip(cuts,cuts[1:]))
            h=rng.randrange(n)
            expect=twisted(gaps,h)
            assert signed_minor_sum(gaps,h)==expect,(gaps,h)
            tests+=1
            if all(c in (0,b) or (b,c)==(2,1) for b,c in gaps):
                assert switch_sum(gaps,h)==expect
                switches+=1
    print("Signed-minor / switch cofactor checks:",tests,switches)
    print("32 independent switches, twist 0:",switch_sum(((2,1),)*32,0))
    # Three equally likely stable shuffles of a zero and two ones.
    mat=[[Fraction(0) for _ in range(3)] for _ in range(3)]
    for b in ("011","101","110"):
        for i,j in enumerate(lf(b)): mat[i][j]+=Fraction(1,3)
    print("Three-way block: actual count",twisted(((3,1),),0),"mean-matrix prediction",3*cofactor(mat))
