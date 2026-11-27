from itertools import product
from time import monotonic

def audit(word,h):
    n=len(word); z=word*2
    rot=[z[i:i+n] for i in range(n)]
    u=min(rot)[:h]
    marks=[i for i,r in enumerate(rot) if r[:h]==u]
    gaps=[(j-i)%n or n for i,j in zip(marks,marks[1:]+marks[:1])]
    cyc=word*4
    payloads=[cyc[i+h:i+h+d] for i,d in zip(marks,gaps)]
    distinct=set(payloads)
    assert all(not v.startswith(w) for w in distinct for v in distinct if v!=w)
    p=next(p for p in range(1,h+1) if u[p:]==u[:-p])
    assert all(d==p and v==u[-p:] for d,v in zip(gaps,payloads) if 2*d<h)
    prs=[payloads[i:]+payloads[:i] for i in range(len(payloads))]
    expected=[i for i,w in enumerate(rot) if w==min(rot)]
    actual=[i for i,w in zip(marks,prs) if w==min(prs)]
    assert actual==expected
    per=len(set(rot)); sp=len(set(map(tuple,prs)))
    assert sum(gaps[:sp])==per
for n in range(1,14):
   tot=0
   for bits in product('01',repeat=n):
       w=''.join(bits)
       for h in list(dict.fromkeys([1,2,n//2,max(1,n-2),n])):
           if 1<=h<=n: audit(w,h);tot+=1
   print(n,tot,flush=True)
