"""Exact binary colex prefix counts using first returns to the least h-factor.

Run 'python return_rank.py 00010111' for the three strict prefix counts.
Reference implementation for verification, with deliberately explicit state.
"""
from collections import defaultdict
from itertools import product
from math import ceil, log2, sqrt


def binary_words(length):
    for word in product("01", repeat=length):
        yield "".join(word)


def local_transitions(u):
    """Disallow all length-h cyclic factors below u. State h signals an occurrence."""
    h = len(u)
    table = {}
    for q in range(h+1):
        context = u[:q]
        active = [k for k in range(h) if context.endswith(u[:k])]
        for bit in "01":
            if any(bit < u[k] for k in active):
                continue
            extended = context + bit
            table[q, bit] = max(k for k in range(h+1) if extended.endswith(u[:k]))
    return table


def least_linear_period(u):
    return next(d for d in range(1, len(u)+1) if u[d:] == u[:-d])


def schedules(n, h, p):
    """Gap zero is anchored in the word. Negative lengths denote short returns."""
    # Iterative to avoid an implementation-dependent recursion limit in a long short-gap run.
    stack = [(n, ())]
    while stack:
        remaining, prefix = stack.pop()
        if remaining == 0:
            yield prefix
            continue
        for d in range((h+1)//2, remaining+1):
            stack.append((remaining-d, prefix+(d,)))
        if 2*p < h and p <= remaining:
            stack.append((remaining-p, prefix+(-p,)))


def update_comparison(old, position, bit, a):
    # Magnitude encodes one plus the rightmost differing position seen so far.
    if bit == a[position] or abs(old) > position:
        return old
    sign = 1 if bit > a[position] else -1
    return sign * (position+1)


def normalize_order(keys):
    order = {value: i for i, value in enumerate(sorted(set(keys)))}
    return tuple(order[key] for key in keys)


def fixed_return_allowed(word, transitions, h):
    q = h
    for j, bit in enumerate(word):
        q = transitions.get((q, bit), -1)
        if q < 0 or (q == h) != (j+1 == len(word)):
            return False
    return True


def schedule_counts(a, u, transitions, gaps):
    h, n = len(u), len(a)
    long_slots, labels = [], []
    short_word, comparison, start = "", 0, 0
    for gap in gaps:
        if gap > 0:
            labels.append(len(long_slots))
            long_slots.append((gap, start))
        else:
            labels.append(-1)
            short_word = u[gap:]
            for j, bit in enumerate(short_word):
                comparison = update_comparison(comparison, (h+start+j) % n, bit, a)
        start += abs(gap)
    if short_word and not fixed_return_allowed(short_word, transitions, h):
        return 0, 0, 0

    lengths = [d for d, _ in long_slots]
    if short_word:
        lengths.append(len(short_word))
    # Each key contains local automaton states, relative orders of prefixes, and
    # the signed rightmost difference. Process all payloads one column at a time.
    states = {((h,)*len(long_slots), (0,)*len(lengths), comparison): 1}
    for j in range(max(lengths)):
        after = defaultdict(int)
        for (local, order, old_cmp), count in states.items():
            options = []
            for (d, _), q in zip(long_slots, local):
                if j >= d:
                    options.append([("", q)])
                    continue
                choices = []
                for bit in "01":
                    next_q = transitions.get((q, bit), -1)
                    if next_q >= 0 and (next_q == h) == (j+1 == d):
                        choices.append((bit, next_q))
                options.append(choices)
            for move in product(*options):
                new_cmp = old_cmp
                for (d, t), (bit, _) in zip(long_slots, move):
                    if j < d:
                        new_cmp = update_comparison(new_cmp, (h+t+j) % n, bit, a)
                column = [bit for bit, _ in move]
                if short_word:
                    column.append(short_word[j:j+1])
                ranks = normalize_order(tuple(zip(order, column)))
                new_local = tuple(q for _, q in move)
                after[new_local, ranks, new_cmp] += count
        states = after
        if not states:
            break

    weighted = necklaces = lyndon = 0
    for (_, order, cmp), count in states.items():
        if cmp >= 0:
            continue
        symbols = tuple(order[i] for i in labels)
        rotations = {symbols[i:]+symbols[:i] for i in range(len(symbols))}
        if min(rotations) != symbols:
            continue
        symbol_period = len(rotations)
        bit_period = sum(abs(g) for g in gaps[:symbol_period])
        weighted += count * bit_period
        necklaces += count
        if bit_period == n:
            lyndon += count
    return weighted, necklaces, lyndon


def ranks(a, h=None):
    """Return (weighted prefix mass, necklace strict rank, Lyndon strict rank)."""
    n = len(a)
    if not n or set(a)-set("01"):
        raise ValueError("A nonempty binary threshold is required")
    if h is None:
        h = min(n, max(1, ceil(sqrt(n*log2(n+1)))))
    if not 1 <= h <= n:
        raise ValueError("The factor length h must be between 1 and n")
    totals = [0, 0, 0]
    for u in binary_words(h):
        transitions = local_transitions(u)
        period = least_linear_period(u)
        for gaps in schedules(n, h, period):
            counts = schedule_counts(a, u, transitions, gaps)
            for i, count in enumerate(counts):
                totals[i] += count
    return tuple(totals)


if __name__ == "__main__":
    import sys
    print(ranks(sys.argv[1], int(sys.argv[2]) if len(sys.argv)>2 else None))
