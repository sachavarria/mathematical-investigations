"""Signed transfer for fixed-density primitive BWT columns. Python standard library."""
from collections import Counter, defaultdict
from itertools import product


def evaluate(n, zeros, prefix, cap=None):
    """Count one-cycle columns starting with prefix at row zero, with peak <= cap."""
    if n < 1 or not 0 <= zeros <= n or not set(prefix) <= {'0', '1'} or len(prefix) > n:
        raise ValueError("invalid cylinder")
    k = len(prefix)
    transitions = [[q+1 if bit == int(c) else None for bit in (0, 1)]
                   for q,c in enumerate(prefix)]
    return transfer(n, zeros, transitions, cap)


def strict(n, zeros, threshold, cap=None):
    """Primitive rank below a reversed integer key, in one automaton evaluation."""
    if not 0 <= threshold <= 2**n:
        raise ValueError("invalid threshold")
    if threshold == 0:
        return 0,0,0
    if threshold == 2**n:
        return evaluate(n,zeros,"",cap)
    digits = [int(c) for c in f"{threshold:0{n}b}"]
    transitions = []
    for q, digit in enumerate(digits):
        row = []
        for bit in (0,1):
            if bit < digit:
                row.append(n)
            elif bit > digit or q == n-1:
                row.append(None)
            else:
                row.append(q+1)
        transitions.append(row)
    return transfer(n, zeros, transitions, cap)


def transfer(n, zeros, transitions, cap):
    """Transient states increase; state k accepts, k+1 marks a selected vertex."""
    cap = min(zeros, n-zeros) if cap is None else cap
    k = len(transitions)
    selected = k+1
    states = {(0, 0, ()): 1}  # used zeros, parity of selected preceding ones, boundary colors
    peak = 1
    visits = 0
    for i in range(n):
        after = defaultdict(int)
        for (v, parity, packed), weight in states.items():
            boundary = dict(packed)
            known = 0 if i == 0 else boundary.get(i)
            for bit in (0, 1):
                nv = v + (bit == 0)
                if nv > zeros or i+1-nv > n-zeros or min(i+1, zeros)-nv > cap:
                    continue
                dest = v if bit == 0 else zeros+i-v
                for q in (known,) if known is not None else range(k+2):
                    visits += 1
                    arrive = transitions[q][bit] if q < k else q
                    if arrive is None:
                        continue
                    edge = boundary.copy()
                    if i != 0:
                        if i in edge:
                            del edge[i]
                        else:
                            edge[i] = q
                    if dest == 0:
                        if arrive != k:
                            continue
                    elif dest in edge:
                        if edge.pop(dest) != arrive:
                            continue
                    else:
                        edge[dest] = arrive
                    take = q == selected
                    odd = take and not (bit == 0 and parity == 1)
                    key = nv, parity ^ int(take and bit == 1), tuple(sorted(edge.items()))
                    after[key] += -weight if odd else weight
        states = {key: val for key, val in after.items() if val}
        peak = max(peak, len(states))
    if any(v != zeros or ports for v, _, ports in states):
        raise AssertionError("unfinished boundary")
    return sum(states.values()), peak, visits


def primitive_reference(n):
    counts = Counter()
    for bits in product("01", repeat=n):
        w = ''.join(bits)
        if any(w >= w[i:]+w[:i] for i in range(1,n)):
            continue
        z = w.count('0')
        runs = sum(w[i-1] == '1' and w[i]=='0' for i in range(1,n))
        runs += w[-1]=='1' and w[0]=='0'
        for d in range(runs,min(z,n-z)+1):
            for k in range(n+1):
                counts[z,w[::-1][:k],d] += 1
    return counts


def all_queries(n):
    counts = primitive_reference(n)
    tests = 0
    for k in range(n+1):
        for bits in product('01',repeat=k):
            s = ''.join(bits)
            for z in range(n+1):
                for d in range(min(z,n-z)+1):
                    got = evaluate(n,z,s,d)[0]
                    assert got == counts[z,s,d], (n,z,s,d,got,counts[z,s,d])
                    tests += 1
    return tests


def full_rank(n, zeros, key, cap=None):
    """Rank weighted by primitive orbit length. Peak cap applies to primitive roots."""
    total = 0
    for p in range(1,n+1):
        if n % p != 0 or zeros % (n//p) != 0:
            continue
        scale = (2**n-1)//(2**p-1)
        total += p*strict(p, zeros//(n//p), (key+scale-1)//scale, cap)[0]
    return total


def check_weighted(n):
    reference = Counter()
    for bits in product('01',repeat=n):
        z = bits.count('0')
        w = ''.join(bits)
        rows = sorted({w[i:]+w[:i] for i in range(n)})
        root = rows[0][:len(rows)]
        runs = sum(root[i-1]=='1' and root[i]=='0' for i in range(len(root)))
        for d in range(runs,min(z,n-z)+1):
            reference[z,d,int(rows[0][::-1],2)] += 1
    count = 0
    for z in range(n+1):
        for d in range(min(z,n-z)+1):
            accum = 0
            for key in range(2**n+1):
                assert full_rank(n,z,key,d) == accum, (n,z,d,key,accum)
                accum += reference[z,d,key]
                count += 1
    return count


if __name__ == '__main__':
    for n in range(1,8):
        print("order",n,"all density/prefix/cap queries",all_queries(n), flush=True)
    for n in range(1,8):
        print("weighted rank queries at order",n,check_weighted(n),flush=True)
    for args in [(12,6,"101",6),(20,10,"1",3),(32,16,"1",3),(64,32,"101",2),
                 (12,6,"10101",3),(20,10,"",5)]:
        print("input",args,"count, peak nonzero states, attempted label transitions",evaluate(*args),flush=True)
    from random import Random
    from run_rank import rank as run_rank
    rng = Random(2711)
    for n in (8,10,13,16,20,24):
        matches = []
        for _ in range(2):
            cutoff = rng.randrange(2**(n-1), 2**n)
            word = f"{cutoff:0{n}b}"[::-1]
            a = run_rank(word,2,n//2)
            assert full_rank(n,n//2,cutoff,2) == a
            matches.append((word,a))
        print('run-order cross-check',n,'cap 2',matches)
