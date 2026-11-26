"""Run with Python 3.9+; standard library only. All arithmetic is exact."""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb, factorial
from collections import Counter


def det(rows):
    a = [list(map(F, row)) for row in rows]
    value = F(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            value = -value
        value *= a[i][i]
        for j in range(i + 1, len(a)):
            if a[j][i]:
                ratio = a[j][i] / a[i][i]
                for h in range(i + 1, len(a)):
                    a[j][h] -= ratio * a[i][h]
    return value


def count_formula(q, n, d):
    k = n - 1
    total = F(0)
    for p in permutations(range(d)):
        # I - (I-S) sum S^t/q^(t+1)
        a = [[int(i == j) for j in range(d)] for i in range(d)]
        for i in range(d):
            j = i
            for t in range(k):
                weight = F(1, q ** (t + 1))
                a[i][j] -= weight
                j = p[j]
                a[i][j] += weight
        total += det(a)
    full = factorial(q) ** (q**k) // q**n
    answer = full * comb(q, d) * total / (q - 1)**d
    assert answer.denominator == 1
    return int(answer)


def direct_words(q, n, d):
    length = q**n - d
    hits = 0
    for w in product(range(q), repeat=length):
        if w != min(w[i:] + w[:i] for i in range(length)):
            continue
        cyclic = w + w
        for m in range(1, length + 1):
            lo, rem = divmod(length, q**m)
            counts = Counter(cyclic[i:i+m] for i in range(length))
            if (lo and len(counts) < q**m) or any(
                not lo <= c <= lo + bool(rem) for c in counts.values()
            ):
                break
        else:
            hits += 1
    return hits


def direct_graph(q, n, d):
    # Try every deletion set. Check flow and actual prefix counts, then use
    # the full tree cofactor. No permutation classification or small kernel.
    size = q**(n-1)
    total = 0
    for gone in combinations(range(q**n), d):
        if Counter(e//q for e in gone) != Counter(e%size for e in gone):
            continue
        if any(max(Counter(e//q**(n-m) for e in gone).values(), default=0)
               > 1 for m in range(1, n+1)):
            continue
        a = [[0]*size for _ in range(size)]
        degree = [0]*size
        for e in range(q**n):
            if e in gone:
                continue
            u, v = e//q, e%size
            degree[u] += 1
            a[u][u] += 1
            a[u][v] -= 1
        weight = det([row[1:] for row in a[1:]])
        for deg in degree:
            weight *= factorial(deg-1)
        total += weight
    return int(total)


if __name__ == '__main__':
    for q, n in [(2,2),(2,3),(2,4),(3,2),(3,3),(4,2),(5,2)]:
        for d in range(1, q+1):
            result = count_formula(q,n,d)
            assert result == direct_graph(q,n,d)
            words = q**(q**n-d) <= 40000
            if words:
                assert result == direct_words(q,n,d)
            print(q, n, d, result, 'graph+words' if words else 'graph')


def limit_from_windows(q, d, n):
    """General fixed-deficit construction, using its exact finite kernel."""
    r = 1
    while q**r < d:
        r += 1
    k = n-1
    assert k >= r
    contexts = list(product(range(q), repeat=r))
    total = F(0)
    for labels in combinations(contexts, d):
        for m in range(1,r):
            counts = Counter(w[:m] for w in labels)
            lo, rem = divmod(d,q**m)
            if (lo and len(counts)<q**m) or any(
                not lo <= c <= lo+bool(rem) for c in counts.values()
            ):
                break
        else:
            for p in permutations(range(d)):
                if any(labels[i][1:] != labels[p[i]][:-1] for i in range(d)):
                    continue
                vertices = []
                for i in range(d):
                    v = []
                    for _ in range(k):
                        v.append(labels[i][0])
                        i = p[i]
                    vertices.append(tuple(v))
                g = [[sum(F(1,q**(t+1)) for t in range(k)
                          if u[t:] == v[:k-t]) for v in vertices]
                     for u in vertices]
                total += det([[int(i == j)-g[i][j]+g[p[i]][j]
                               for j in range(d)] for i in range(d)])
    full = factorial(q)**(q**k)//q**n
    return F(full, (q-1)**d)*total


if __name__ == '__main__':
    for q,n,d in [(2,3,3),(2,3,4),(2,4,3),(2,4,4),(2,4,5)]:
        small = limit_from_windows(q,d,n)
        brute = direct_words(q,n,d)
        assert small == brute
        print(q,n,d,brute,'general kernel+words')
