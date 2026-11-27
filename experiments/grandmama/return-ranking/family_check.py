from collections import Counter
from itertools import product
from math import comb

def key(w):
    return w[::-1]

def neck(w):
    rs = {w[j:]+w[:j] for j in range(len(w))}
    return min(rs), len(rs)

def words(n):
    return map(''.join,product('01',repeat=n))

def check_self_embedding(m,h):
    u='0'*h
    def encode(w):
        raw=''.join(('101' if c=='0' else '111')+u for c in w)
        return u+raw[:-h]
    vs=list(words(m))
    assert sorted(vs,key=key)==sorted(vs,key=lambda v:key(encode(v)))
    for q in vs:
        rep, period=neck(q)
        assert neck(encode(q)) == (encode(rep), (h+3)*period)

def check_aggregation(t,s,h):
    u='0'*h; n=t*(h+1)+s
    found={}
    for bits in words(t+s):
        if bits.count('1') != t:continue
        payload=''.join('0' if b=='0' else '1'+u for b in bits)
        rep,per=neck(payload)
        assert rep.endswith('01') and key(rep)<key('0'*(n-2)+'11')
        found[rep]=per
    assert sum(found.values())*(s+t)==n*comb(s+t,t)

for m in range(1,8):
    for h in range(2,7):
        check_self_embedding(m,h)
for h in range(3,7):
    for t in range(1,6):
        for s in range(t,t+3):
            check_aggregation(t,s,h)
print('All 35 embedding tests and 60 weighted-aggregation tests passed.')
