"""Rebuild results with python3 check.py. No external dependencies."""
from weighted import words, weight, count


def verify(n):
    keys = sorted(words(n), key=lambda w: w[::-1])
    # Construct independently via full rotation orbits of all words.
    mass = dict.fromkeys(keys, 0)
    for w in keys:
        rep = min(w[i:]+w[:i] for i in range(n))
        mass[rep] += 1
    phase = 0
    anchors = []
    tested = 0
    for i, w in enumerate(keys):
        if n <= 8 or i in {0, 1, len(keys)//3, len(keys)//2+5, len(keys)-1}:
            assert sum(count(w)) == phase, (n, w, phase)
            tested += 1
        if mass[w] == n:
            anchors.append(phase)
        phase += mass[w]
    assert phase == 2**n
    max_gap = max(b-a for a,b in zip(anchors, anchors[1:]+[anchors[0]+phase]))
    p = next(d for d in range(2,n+1) if n%d == 0)
    assert max_gap == n+max(2,n//p)
    print(n, tested, len(anchors), max_gap, sep=",", flush=True)

if __name__ == "__main__":
    print("order,thresholds_verified,anchors,max_gap")
    for n in range(2, 15):
        verify(n)
