"""Count primitive BWT columns with a prescribed LF itinerary and bounded crossing."""
from collections import defaultdict
from functools import lru_cache
from itertools import product
from math import comb


def cylinder(n, zeros, prefix, cap):
    """Return exact count and peak number of distinct stored states in a layer."""
    assert 0 <= zeros <= n and len(prefix) <= n and cap >= 0
    assert n >= 1 and set(prefix) <= set("01")
    factors = {prefix[i:j] for i in range(len(prefix)+1)
               for j in range(i, len(prefix)+1)}

    @lru_cache(None)
    def merge(left, right):
        text, overflow = left
        if overflow:
            return left
        more, extra = right
        for c in more:
            if text+c not in factors:
                return text, True
            text += c
        return text, extra

    empty = ("", False)
    letter = {b: ((b, False) if b in factors else ("", True)) for b in "01"}
    states = {(0, ()): 1}
    peak = 1
    for i in range(n):
        layer = defaultdict(int)
        for (used, paths), weight in states.items():
            for b in "01":
                v = used + (b == "0")
                if v > zeros or i+1-v > n-zeros or min(i+1, zeros)-v > cap:
                    continue
                target = used if b == "0" else zeros+i-used
                if target == 0:
                    target = n  # split the marked row into a source and a sink
                incoming = next((p for p in paths if p[1] == i), None)
                outgoing = next((p for p in paths if p[0] == target), None)
                if i == target or (incoming is not None and incoming == outgoing):
                    continue
                a, _, left = incoming or (i, i, empty)
                _, d, right = outgoing or (target, target, empty)
                key = merge(merge(left, letter[b]), right)
                rest = [p for p in paths if p != incoming and p != outgoing]
                rest.append((a, d, key))
                layer[v, tuple(sorted(rest))] += weight
        states = layer
        peak = max(peak, len(states))
    return sum(w for (_, ps), w in states.items()
               if len(ps) == 1 and ps[0][:2] == (0, n)
               and ps[0][2][0] == prefix), peak


def direct(n, z, s):
    """Explicit sorted rotations, independent of the frontier proof."""
    out = [0] * (min(z, n-z)+1)
    for bits in product("01", repeat=n):
        w = "".join(bits)
        if w.count("0") != z:
            continue
        rows = sorted(w[i:]+w[:i] for i in range(n))
        if rows[0] != w or len(set(rows)) != n or not w[::-1].startswith(s):
            continue
        d = sum(r[-1] == "1" for r in rows[:z])
        for j in range(d, len(out)):
            out[j] += 1
    return out


if __name__ == "__main__":
    checks = 0
    for n in range(1, 8):
        for z in range(n+1):
            for k in range(n+1):
                for bits in product("01", repeat=k):
                    s = "".join(bits)
                    for d, expected in enumerate(direct(n,z,s)):
                        assert cylinder(n,z,s,d)[0] == expected, (n,z,s,d)
                        checks += 1
    print("Sorted-rotation oracle comparisons:", checks)
    for n,z,s,d in [(16,8,"101",2),(32,16,"101",2),(64,32,"101",2),
                    (64,32,"101",3),(64,32,"10110",2)]:
        count, peak = cylinder(n,z,s,d)
        population = sum(comb(z,j)*comb(n-z,j) for j in range(d+1))
        print(n,z,s,d,"eligible columns",population,"accepted",count,"peak states",peak)
