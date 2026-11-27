"""Primitive Eulerian edge necklaces for a contracted binary stable shuffle."""
from fractions import Fraction
from itertools import combinations, product
from math import factorial, gcd, prod
from functools import reduce


def pieces(gaps, h):
    """Return (source, bit, destination, multiplicity) in original emission order."""
    vertices = [u for u, (size, _) in enumerate(gaps) for _ in range(size)]
    start = [0, sum(z for _, z in gaps)]
    edges = []
    aligned = True
    for u, (size, zeros) in enumerate(gaps):
        for bit, count in enumerate((zeros, size - zeros)):
            prev = None
            n_pieces = 0
            for raw in range(start[bit], start[bit] + count):
                j = h if raw == 0 else raw - 1 if raw <= h else raw
                if prev is None or j != prev + 1 or vertices[j] != vertices[prev]:
                    edges.append([u, bit, vertices[j], 0])
                    n_pieces += 1
                edges[-1][3] += 1
                prev = j
            aligned &= n_pieces <= 1
            start[bit] += count
    return edges, aligned


def determinant(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    value = Fraction(1)
    for i in range(len(a)):
        pivot = next((k for k in range(i, len(a)) if a[k][i]), None)
        if pivot is None:
            return 0
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            value *= -1
        value *= a[i][i]
        for row in a[i+1:]:
            ratio = row[i] / a[i][i]
            for j in range(i+1, len(a)):
                row[j] -= ratio * a[i][j]
    assert value.denominator == 1
    return int(value)


def mobius(d):
    sign = 1
    p = 2
    while p*p <= d:
        if d % p == 0:
            d //= p
            if d % p == 0:
                return 0
            sign = -sign
        p += 1
    return -sign if d > 1 else sign


def euler_bound(gaps, h):
    edges, aligned = pieces(gaps, h)
    n = sum(s for s, _ in gaps)
    g = reduce(gcd, (c for _, _, _, c in edges))
    total = 0
    for d in range(1, g+1):
        if g % d or not (mu := mobius(d)):
            continue
        degree = [size//d for size, _ in gaps]
        lap = [[di if i == j else 0 for j in range(len(gaps))]
               for i, di in enumerate(degree)]
        for u, _, v, count in edges:
            lap[u][v] -= count//d
        tree_count = determinant([row[1:] for row in lap[1:]])
        numerator = (n//d)*tree_count*prod(factorial(x-1) for x in degree)
        denominator = prod(factorial(c//d) for _, _, _, c in edges)
        assert numerator % denominator == 0
        total += mu * (numerator//denominator)
    assert total % n == 0
    return total//n, aligned


def literal(gaps,h):
    pools = [list(combinations(range(size), z)) for size,z in gaps]
    zeros = sum(z for _,z in gaps)
    answer = 0
    for selections in product(*pools):
        word = [int(i not in selection) for (size,_),selection in zip(gaps,selections)
                for i in range(size)]
        k = [0,zeros]
        perm = []
        for c in word:
            j = k[c]
            perm.append(h if j==0 else j-1 if j<=h else j)
            k[c] += 1
        orbit = set()
        j = 0
        while j not in orbit:
            orbit.add(j)
            j = perm[j]
        answer += len(orbit)==len(word)
    return answer


def signatures(n):
    if n == 0:
        yield ()
    for size in range(1,n+1):
        for rest in signatures(n-size):
            for z in range(size+1):
                yield ((size,z),) + rest


if __name__ == '__main__':
    first = None
    for n in range(1,8):
        tested = exact = strict = 0
        for gaps in signatures(n):
            for h in range(n):
                forecast, aligned = euler_bound(gaps,h)
                actual = literal(gaps,h)
                assert forecast == actual if aligned else forecast >= actual
                tested += 1
                exact += aligned
                strict += forecast > actual
                if forecast > actual and first is None:
                    first = (gaps,h,forecast,actual)
        print(f'n={n}: {tested} signatures; {exact} aligned; {strict} strict upper bounds')
    print('First strict relaxation:',first)
    for gaps,h in [(((3,1),),0),(((3,1),),1),(((40,20),(40,20)),0)]:
        print(gaps,h,euler_bound(gaps,h))


def pinned_examples(n, k):
    """Extract positive pinned instances from literal one-cycle binary columns."""
    records = {}
    for w in product((0,1),repeat=n):
        z = w.count(0)
        seen = [0,z]
        perm = []
        for b in w:
            perm.append(seen[b])
            seen[b] += 1
        row = 0
        trace = []
        while row not in trace:
            trace.append(row)
            row = perm[row]
        if len(trace)!=n:
            continue
        loc = trace[:k+1]
        cuts = set(loc[:-1])
        gaps = []
        chunk = []
        for i,b in enumerate(w):
            if i in cuts:
                if chunk: gaps.append((len(chunk),chunk.count(0)))
                chunk = []
            else:
                chunk.append(b)
        if chunk: gaps.append((len(chunk),chunk.count(0)))
        h = loc[-1]-sum(i<loc[-1] for i in cuts)
        key = (z,tuple(loc))
        if key not in records:
            records[key] = (tuple(gaps),h,0)
        g,h0,count = records[key]
        assert g==tuple(gaps) and h0==h
        records[key] = (g,h,count+1)
    aligned = tight = 0
    for g,h,count in records.values():
        upper,exact = euler_bound(g,h)
        assert count==literal(g,h) and upper>=count
        aligned += exact
        tight += upper==count
    return len(records),aligned,tight


def border_check(gaps, h):
    """Compare integral evaluations of the bordered matrix and the tree minor."""
    edges,_ = pieces(gaps,h)
    v = len(gaps)-1
    m = len(edges)
    matrix = [[0]*(v+m) for _ in range(v+m)]
    lap = [[0]*v for _ in range(v)]
    for e,(u,_,w,weight) in enumerate(edges):
        x = weight*(e+2)
        y = e+3
        i = v+e
        matrix[i][i] = y
        if u:
            matrix[u-1][i] = y
            matrix[i][u-1] -= x
            lap[u-1][u-1] += x
            if w: lap[u-1][w-1] -= x
        if w: matrix[i][w-1] += x
    assert determinant(matrix) == prod(range(3,m+3))*determinant(lap)


if __name__ == '__main__':
    for k in (2,4,6):
        print('order 9, fixed path length', k, 'positive layouts, aligned, bound tight:',
              pinned_examples(9,k))
    for n in range(1,5):
        for gaps in signatures(n):
            for h in range(n):
                border_check(gaps,h)
    print('Bordered determinant identity: integer evaluations for every signature through n=4.')
    print('Mixed overcount: gaps ((3,2),), twist 1, literal and relaxation:',
          literal(((3,2),),1),euler_bound(((3,2),),1)[0])
