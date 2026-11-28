"""Check the boundary-corrected mask-4 predictor independently by bit-parallel time evolution."""
from itertools import combinations
from math import comb
from random import Random


def predict(word, i, time):
    value = 0
    for j in range((i+1)//2, 0, -1):
        left = i-2*j
        boundary_bit = (word >> left) & 1 if left >= 0 else 0
        if j & time == j:
            value ^= 1-boundary_bit
        value &= (word >> (left+1)) & 1
    return value ^ ((word >> i) & 1)


def place(compact, positions):
    return sum(((compact >> j) & 1) << k for j,k in enumerate(positions))


def classes(values, positions, others):
    cols = [place(b,others) for b in range(1<<len(others))]
    return len({tuple(values[place(a,positions) | b] for b in cols)
                for a in range(1<<len(positions))})


def rank2(rows):
    pivots = {}
    for v in rows:
        while v:
            p = v.bit_length()-1
            if p not in pivots:
                pivots[p] = v
                break
            v ^= pivots[p]
    return len(pivots)


def main():
    scalar = midpoint = delayed = 0
    for m in range(1,12):
        mask = (1<<m)-1
        all_words = list(range(mask+1))
        states = all_words.copy()
        period = 1 << (m//2).bit_length()
        columns = []
        for t in range(2*period):
            if t and t <= period:
                assert (states == all_words) == (t == period), (t,m)
            for x,y in enumerate(states):
                for i in range(m):
                    assert predict(x,i,t) == (y>>i)&1,(m,t,i,x)
                    scalar += 1
            if m%2 and t<period:
                r = m//2
                j_count = sum(comb(t,j)%2 for j in range(1,r+1))
                vals = [y>>(m-1) for y in states]
                evens = list(range(0,m,2))
                odds = list(range(1,m,2))
                assert classes(vals,evens,odds)==1<<(j_count+1)
                assert classes(vals,odds,evens)==j_count+1
                assert max(classes(vals,list(range(c)),list(range(c,m)))
                           for c in range(m+1))<=2
                columns.append(vals)
                midpoint += 3
            states = [(v^((v<<1)&~(v<<2)))&mask for v in states]
        if columns:
            for length in range(len(columns)+1):
                for times in combinations(range(len(columns)),length):
                    dim = rank2([sum((comb(t,j)%2)<<j for j in range(m//2+1)) for t in times])
                    assert len({tuple(columns[t][x] for t in times) for x in all_words})==1<<dim
                    delayed += 1
    print("Scalar readouts (all states and sites, widths 1 through 11, two full periods):",scalar)
    print("Order-profile obligations, odd widths and all phases:",midpoint)
    print("Delayed-time families at odd widths through 11:",delayed)
    rng = Random(166)
    for m in [21,57,101]:
        for _ in range(50):
            x=rng.getrandbits(m)
            t=rng.getrandbits(200)
            y=x
            for _ in range(t%(1<<(m//2).bit_length())):
                y=(y^((y<<1)&~(y<<2)))&((1<<m)-1)
            assert predict(x,m-1,t)==(y>>(m-1))
    print("Seeded 200-bit time queries at lengths 21, 57, 101:",150)
    m,t=9,7
    states=list(range(1<<m))
    for _ in range(t):
        states=[(v^((v<<1)&~(v<<2)))&((1<<m)-1) for v in states]
    vals=[v>>(m-1) for v in states]
    for name,order in [('natural',list(range(m))),('reverse',list(reversed(range(m)))),
                       ('evens-first',list(range(0,m,2))+list(range(1,m,2))),
                       ('odds-first',list(range(1,m,2))+list(range(0,m,2)))]:
        print(name, [classes(vals,order[:c],order[c:]) for c in range(m+1)])
if __name__ == '__main__':
    main()
