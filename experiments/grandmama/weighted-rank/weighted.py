"""Exact binary Grandmama prefix weights. Standard Python, no dependencies."""
from collections import defaultdict
from itertools import product


def words(k):
    for bits in product("01", repeat=k):
        yield "".join(bits)


def weight(w):
    rotations = [w[i:] + w[:i] for i in range(len(w))]
    return len(set(rotations)) if w == min(rotations) else 0


def unique_count(u, a):
    """Count words starting with u whose every other cyclic h-factor exceeds u."""
    n, h = len(a), len(u)
    # q = length of longest suffix matching a proper prefix of u.
    transitions = {}
    for q in range(h):
        context = u[:q]
        active = [k for k in range(q+1) if context.endswith(u[:k])]
        for bit in "01":
            extended = context + bit
            new_q = max(k for k in range(h) if extended.endswith(u[:k]))
            bad = [k for k in active if bit < u[k] or (k == h-1 and bit == u[k])]
            transitions[q, bit] = new_q, bad
    states = {(0, False): 1}
    for i in range(n+h-1):
        choices = u[i] if i < h else u[i-n] if i >= n else "01"
        following = defaultdict(int)
        for (q, less), multiplicity in states.items():
            for bit in choices:
                new_q, bad = transitions[q, bit]
                if any(1 <= i-k < n for k in bad):
                    continue
                new_less = less if i >= n or bit == a[i] else bit < a[i]
                following[new_q, new_less] += multiplicity
        states = following
    return sum(count for (_, less), count in states.items() if less)


def tied_words(n, h):
    for d in range(1, n):
        groups = list(range(n))
        for i in range(h):
            left, right = groups[i], groups[(i+d) % n]
            groups = [left if g == right else g for g in groups]
        labels = sorted(set(groups))
        assert len(labels) == n-h
        positions = [labels.index(g) for g in groups]
        for values in words(len(labels)):
            w = "".join(values[j] for j in positions)
            doubled = w+w
            if all(doubled[j:j+h] != w[:h] for j in range(1, d)):
                yield w


def count(a):
    n = len(a)
    if n < 2 or set(a)-set("01"):
        raise ValueError("expected at least two binary digits")
    h = n//2
    unique = n * sum(unique_count(u, a) for u in words(h))
    tied = sum(weight(w) for w in tied_words(n, h) if w[::-1] < a[::-1])
    return unique, tied


if __name__ == "__main__":
    import sys
    parts = count(sys.argv[1])
    print("unique weight, tied weight, absolute prefix weight:", *parts, sum(parts))
