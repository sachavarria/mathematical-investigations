"""Reproduce the finite obligations added in the 27 November proof review."""
from collections import Counter
from itertools import combinations, permutations, product
from math import factorial, prod
from pathlib import Path
import sys

here = Path(__file__).resolve().parent
for candidate in [here.parent / "morphology-of-order", here.parent / "orderdraft", here]:
    if (candidate / "check_joint.py").is_file():
        sys.path.insert(0, str(candidate))
        break
from check_joint import Cell


def literal_table(n):
    """Construct by rooted binary words, least rotations and actual last columns."""
    answer = Counter()
    cells = set()
    for bits in product("01", repeat=n):
        word = "".join(bits)
        cells.add(tuple(word[i:i+2].count("0") for i in range(0,n,2)))
        rotations = sorted(word[i:]+word[:i] for i in range(n))
        if rotations[0] != word or len(set(rotations)) != n:
            continue
        last = "".join(row[-1] for row in rotations)
        signature = tuple(last[i:i+2].count("0") for i in range(0,n,2))
        for k in range(n+1):
            answer[signature, word[::-1][:k]] += 1
    return sorted(cells), answer


def all_prefixes(n):
    cells, oracle = literal_table(n)
    tested = positive = 0
    for quota in cells:
        cell = Cell(n, quota)
        for k in range(n+1):
            for bits in product("01", repeat=k):
                s = "".join(bits)
                count = cell.count(s)
                assert count == oracle[quota,s]
                tested += 1
                positive += count > 0
    print("n", n, "cells", len(cells), "all cell/prefix pairs", tested,
          "positive", positive, "zero", tested-positive)


def border_coefficients(vertices, edges):
    """Compute exact formal coefficients by the Leibniz formula, root zero."""
    r, m = vertices-1, len(edges)
    matrix = [[None]*(r+m) for _ in range(r+m)]
    for j,(a,b) in enumerate(edges):
        x, y = j, m+j
        if a:
            matrix[a-1][r+j] = y, 1
        if a != b:
            if a:
                matrix[r+j][a-1] = x, -1
            if b:
                matrix[r+j][b-1] = x, 1
        matrix[r+j][r+j] = y, 1
    terms = Counter()
    for col in permutations(range(r+m)):
        entries = [matrix[i][j] for i,j in enumerate(col)]
        if None in entries:
            continue
        inversions = sum(a>b for i,a in enumerate(col) for b in col[i+1:])
        terms[tuple(sorted(label for label,sign in entries))] += (
            (-1)**inversions * prod(sign for label,sign in entries))
    return {monomial:c for monomial,c in terms.items() if c}, factorial(r+m)


def tree_monomials(vertices, edges):
    r, m = vertices-1, len(edges)
    required = set(range(1,vertices))
    answer = {}
    for chosen in combinations(range(m),r):
        outgoing = dict(edges[e] for e in chosen)
        if set(outgoing) != required:
            continue
        for start in required:
            v = start
            for _ in range(r):
                v = outgoing.get(v,0)
            if v:
                break
        else:
            answer[chosen+tuple(range(m,2*m))] = 1
    return answer


if __name__ == "__main__":
    for n in (7,8):
        all_prefixes(n)
    count = orders = 0
    for vertices in range(1,4):
        types = list(product(range(vertices), repeat=2))
        for m in range(4):
            for edges in product(types, repeat=m):
                coeff, cost = border_coefficients(vertices, edges)
                assert coeff == tree_monomials(vertices, edges), (vertices, edges)
                count += 1
                orders += cost
    print("formal bordered determinants", count, "Leibniz permutations", orders)
