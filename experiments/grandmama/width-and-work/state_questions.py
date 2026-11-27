"""Compute exact residual truth tables at fixed density and row cut."""
from itertools import combinations, product


def words(n,z):
    for pos in combinations(range(n),z):
        bits=['1']*n
        for j in pos: bits[j]='0'
        yield ''.join(bits)


def packet_keys(n,z):
    keys={}
    for w in words(n,z):
        rows=sorted(w[j:]+w[:j] for j in range(n))
        if rows[0] != w or len(set(rows))!=n: continue
        column=''.join(x[-1] for x in rows)
        keys[column]=int(w[::-1],2)
    return keys


def residuals(n,z,i,v,keys,cut):
    suffixes=list(words(n-i,z-v))
    rows=[]
    for prefix in words(i,v):
        rows.append(tuple(keys.get(prefix+q,1<<n)<cut for q in suffixes))
    return len(set(rows)),len(set(sum(row) for row in rows)),sum(map(sum,rows))


def verify_area(n):
    for bits in product("01",repeat=n):
        b=''.join(bits)
        z=b.count('0')
        p=sorted(range(n),key=lambda j:(b[j],j))
        # Invert the sorted-source listing to obtain source -> destination.
        dest=[p.index(j) for j in range(n)]
        d=[sum(t>=i for t in dest[:i]) for i in range(n+1)]
        area=sum(d)
        inv=sum(b[i]=='1' and b[j]=='0' for i in range(n) for j in range(i+1,n))
        peak=max(d)
        assert peak**2<=area<=peak*(n-peak) and inv==area
        visited=set()
        cycles=0
        for j in range(n):
            if j not in visited:
                cycles+=1
                while j not in visited:
                    visited.add(j)
                    j=dest[j]
        assert area%2==(n-cycles)%2


if __name__=="__main__":
    for n in range(1,11):
        verify_area(n)
    print("Area, crossing bounds, and cycle parity: all 2046 binary columns through n=10")
    n,z,i,v=12,6,6,3
    keys=packet_keys(n,z)
    observations=[]
    for cut in sorted({0,1<<n}|{val+1 for val in keys.values()}):
        c,m,yes=residuals(n,z,i,v,keys,cut)
        observations.append((cut,c,m,yes))
    print("n=12, z=6, scanned=6, scanned zeros=3. All completions have peak 3.")
    print("reversed integer cut / residual classes / distinct row sums / accepted")
    last=-1
    for cut,c,m,yes in observations:
        if c>last or cut==1<<n:
            print(cut,c,m,yes)
        last=max(last,c)
