"""Reference checks for tree.md. Pure Python, no imports from the clock implementation."""
from bisect import bisect_left
from itertools import product


def word_list(n):
    return ["".join(x) for x in product("01", repeat=n)]


def weight(w):
    rotations = {w[i:] + w[:i] for i in range(len(w))}
    return len(rotations) if min(rotations) == w else 0


def key(w):
    return int(w[::-1], 2)


def zero_test(n, suffix, primitive):
    if not suffix:
        return True
    score = weight("0" * (n-len(suffix)) + suffix)
    return score == n if primitive else score != 0


def next_rep(n, threshold, primitive):
    if threshold >= 2**n:
        return 2**n
    digits = format(threshold, f"0{n}b")
    if zero_test(n, digits[::-1], primitive):
        return threshold
    for i in reversed(range(n)):
        if digits[i] == "1":
            continue
        prefix = digits[:i] + "1"
        if not zero_test(n, prefix[::-1], primitive):
            continue
        while len(prefix) < n:
            prefix += "0" if zero_test(n, ("0"+prefix[::-1]), primitive) else "1"
        return int(prefix, 2)
    return 2**n


def main():
    cumulative = {}
    for n in range(1, 13):
        words = sorted(word_list(n), key=key)
        ws = list(map(weight, words))
        ordinary, weighted, primitive = [0], [0], [0]
        ordinary_keys = [i for i,v in enumerate(ws) if v]
        primitive_keys = [i for i,v in enumerate(ws) if v==n]
        for v in ws:
            ordinary.append(ordinary[-1]+bool(v))
            weighted.append(weighted[-1]+v)
            primitive.append(primitive[-1]+(v==n))
        cumulative[n] = ordinary,weighted,primitive
        for use_primitive, keys in [(False,ordinary_keys),(True,primitive_keys)]:
            terminal = keys + [2**n]
            for length in range(1,n+1):
                for s in word_list(length):
                    start = key(s) << (n-length)
                    expected = terminal[bisect_left(terminal,start)] < start + 2**(n-length)
                    assert zero_test(n,s,use_primitive) == expected
            for t in range(2**n+1):
                assert next_rep(n,t,use_primitive) == terminal[bisect_left(terminal,t)]
        for t in range(2**n+1):
            i = next_rep(n,t,False)
            skipped = []
            while i<2**n and ws[i] != n:
                skipped.append(ws[i])
                i = next_rep(n,i+1,False)
            assert len(skipped)<=2 and weighted[i]-sum(skipped)==weighted[t]
            counts, masses = {}, {}
            for d in range(1,n+1):
                if n%d:
                    continue
                factor = (2**n-1)//(2**d-1)
                cut = (t+factor-1)//factor
                rd,cd,pd = (row[cut] for row in cumulative[d])
                counts[d] = rd-sum(v for e,v in counts.items() if d%e==0)
                masses[d] = cd-sum(v for e,v in masses.items() if d%e==0)
                assert counts[d]==pd and masses[d]==d*pd
            assert sum(masses[d]//d for d in masses)==ordinary[t]
            assert sum(d*counts[d] for d in counts)==weighted[t]
        print("order",n,"all cutoffs verified")
    masses = [sum(weight(x+y) for x in word_list(6)) for y in ["001011","001101"]]
    assert masses == [90,114]
    for m in range(2,8):
        roots = [w for w in word_list(m) if weight(w)==m]
        # C indexed by integer reversed key. Difference C(x+y) to C(x_next+y)
        # is a single unit in this key (y is its high half).
        all_words = sorted(word_list(2*m), key=key)
        c=[0]
        for w in all_words:
            c.append(c[-1]+weight(w))
        for x in roots:
            for y in roots:
                value=weight(x+y)
                assert (value==0 if x>y else value==m if x==y else value==2*m)
                threshold=key(x+y)
                assert c[threshold+1]-c[threshold]==value
    print("midpoint matrix checks and order-12 collision passed")


if __name__ == "__main__":
    main()
