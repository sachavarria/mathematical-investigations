"""Exhaustive independent oracle and deterministic larger examples; Python stdlib."""
from collections import Counter
from itertools import product
from return_rank import ranks


def oracle(n):
    words = ["".join(w) for w in product("01", repeat=n)]
    masses = Counter(min(w[i:]+w[:i] for i in range(n)) for w in words)
    cumulative = [0, 0, 0]
    result = {}
    for w in sorted(words, key=lambda v: v[::-1]):
        result[w] = tuple(cumulative)
        mass = masses[w]
        for i, value in enumerate((mass, int(mass>0), int(mass==n))):
            cumulative[i] += value
    return result


def verify(n):
    reference = oracle(n)
    if n <= 7:
        tested = reference.keys()
    else:
        all_words = sorted(reference)
        tested = {all_words[i] for i in (0, 1, len(all_words)//3, len(all_words)//2+1, -2, -1)}
        if n == 8:
            tested.add("00010111")
    hs = sorted({None, 2, min(n, 4), n}, key=lambda x: 0 if x is None else x) if 2 <= n <= 6 else [None]
    for w in tested:
        for h in hs:
            assert ranks(w,h) == reference[w], (n,w,h,ranks(w,h),reference[w])
    print(n,len(tested),len(hs),sep=",",flush=True)


if __name__ == "__main__":
    print("order,thresholds,factor_lengths")
    for n in range(1,13):
        verify(n)
