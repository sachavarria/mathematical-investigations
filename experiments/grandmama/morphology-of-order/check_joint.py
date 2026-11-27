"""Exact BWT itinerary/connectivity counts by pair quotas and Euler tours."""
from collections import Counter
from itertools import product


def determinant(rows):
    """Integer fraction-free elimination. The empty determinant is one."""
    a = [row.copy() for row in rows]
    sign = previous = 1
    for j in range(len(a) - 1):
        pivot_row = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot_row is None:
            return 0
        if pivot_row != j:
            a[j], a[pivot_row] = a[pivot_row], a[j]
            sign *= -1
        pivot = a[j][j]
        for i in range(j + 1, len(a)):
            for k in range(j + 1, len(a)):
                a[i][k] = (pivot * a[i][k] - a[i][j] * a[j][k]) // previous
        previous = pivot
    return sign * a[-1][-1] if a else 1


def cells(n):
    sizes = (2,) * (n // 2) + (1,) * (n % 2)
    return product(*(range(size + 1) for size in sizes))


class Cell:
    def __init__(self, n, quotas):
        self.n = n
        z = sum(quotas)
        starts = [0, z]
        self.z = z
        self.head = []
        self.tail = [None] * n
        self.out = []
        for group, quota in enumerate(quotas):
            size = min(2, n - 2 * group)
            targets = []
            for c, amount in enumerate((quota, size - quota)):
                targets.extend(range(starts[c], starts[c] + amount))
                starts[c] += amount
            bundles = [targets] if size == 2 and quota == 1 else [[t] for t in targets]
            for bundle in bundles:
                v = len(self.out)
                self.head.extend([v] * len(bundle))
                for e in bundle:
                    self.tail[e] = v
                self.out.append(bundle)

    def count(self, prefix):
        """Number of single-cycle completions whose LF trace begins with prefix."""
        n = self.n
        if len(prefix) > n:
            raise ValueError("prefix longer than cycle")
        # Trace starts AFTER incoming edge 0. Its own color is read last.
        if len(prefix) == n:
            if int(prefix[-1]) != int(0 >= self.z):
                return 0
            prefix = prefix[:-1]
        used = {0}
        e = 0
        for c in prefix:
            candidates = [j for j in self.out[self.head[e]] if (j >= self.z) == int(c)]
            if not candidates or candidates[0] in used:
                return 0
            e = candidates[0]
            used.add(e)
        # Contract the path of distinct edges 0,...,e to one marked edge.
        edges = [(self.tail[j], self.head[j]) for j in range(n) if j not in used]
        edges.append((self.tail[0], self.head[e]))
        vertices = sorted({v for u, v in edges} | {u for u, v in edges})
        renumber = {v: i for i, v in enumerate(vertices)}
        lap = [[0] * len(vertices) for _ in vertices]
        for u, v in edges:
            i, j = renumber[u], renumber[v]
            lap[i][i] += 1
            lap[i][j] -= 1
        return determinant([row[1:] for row in lap[1:]])


def rank(n, zeros, threshold):
    """Strict primitive necklace rank by reversed canonical key, at fixed zeros."""
    cuts = [threshold[:j] + "0" for j, c in enumerate(threshold) if c == "1"]
    return sum(cell.count(s) for q in cells(n) if sum(q) == zeros
               for cell in [Cell(n, q)] for s in cuts)


def canonical_oracle(n):
    """Enumerate primitive necklaces via literal rotations, then sort their BWT rows."""
    result = Counter()
    reversed_keys = []
    for bits in product("01", repeat=n):
        w = "".join(bits)
        rows = sorted(w[i:] + w[:i] for i in range(n))
        if w != rows[0] or len(set(rows)) != n:
            continue
        last = "".join(row[-1] for row in rows)
        q = tuple(last[i:i+2].count("0") for i in range(0,n,2))
        rev = w[::-1]
        reversed_keys.append((w.count("0"), rev))
        for k in range(n + 1):
            result[q,rev[:k]] += 1
    return result, reversed_keys


def symbolic_matrix_check():
    """Evaluate the two-occurrence lift against literal arborescence monomials."""
    from itertools import combinations
    from math import prod
    from random import Random
    rng = Random(404)
    tested = 0
    for v in range(1,6):
        for _ in range(35):
            m = rng.randrange(1,9)
            edges = [(rng.randrange(v),rng.randrange(v)) for j in range(m)]
            x, y, z = [[rng.randrange(-3,4) for j in range(m)] for t in range(3)]
            r = v - 1
            mat = [[0]*(r+m) for j in range(r+m)]
            for j,(u,w) in enumerate(edges):
                if u:
                    mat[u-1][r+j] = x[j]
                    mat[r+j][u-1] += y[j]
                if w:
                    mat[r+j][w-1] -= y[j]
                mat[r+j][r+j] = z[j]
            total = 0
            for subset in combinations(range(m),r):
                chosen = set(subset)
                successor = {edges[j][0]: edges[j][1] for j in chosen}
                if set(successor) != set(range(1,v)):
                    continue
                tree = True
                for u in successor:
                    end = u
                    for k in range(r):
                        if end == 0:
                            break
                        end = successor[end]
                    if end:
                        tree = False
                        break
                if tree:
                    total += prod(x[j]*y[j] if j in chosen else z[j] for j in range(m))
            assert determinant(mat) == (-1)**r * total, (v,edges)
            tested += 1
    print("two-occurrence lift versus direct signed tree polynomial:", tested)


if __name__ == "__main__":
    total = ranks = 0
    for n in range(1,9):
        expected, keys = canonical_oracle(n)
        # Test all cut prefixes in all cells through n=6, including impossible paths.
        # At 7 and 8 test every actual prefix globally against every cell.
        words = (["".join(w) for k in range(n+1) for w in product("01", repeat=k)]
                 if n <= 6 else sorted({word for q,word in expected}))
        checked = 0
        for q in cells(n):
            cell = Cell(n, q)
            for s in words:
                assert cell.count(s) == expected[q,s], (n, q, s)
                checked += 1
        if n <= 6:
            for z in range(n+1):
                for bits in product("01", repeat=n):
                    threshold = "".join(bits)
                    target = sum(d == z and key < threshold for d, key in keys)
                    assert rank(n,z,threshold) == target
                    ranks += 1
        print(f"order {n}: {checked} cell/prefix checks, {len(keys)} primitive necklaces")
        total += checked
    c = Cell(64,(1,)*32)
    print("all-mixed cell, order 64:", [(p, c.count(p)) for p in ("", "1", "11", "101", "10101")])
    print(f"total: {total} cell/prefix counts; {ranks} complete fixed-density primitive ranks")
    symbolic_matrix_check()
