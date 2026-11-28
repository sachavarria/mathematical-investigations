"""Exact residual-state census. Python 3 standard library, all data synthetic."""
import csv
from pathlib import Path

QUESTIONS = ('last', 'xor', 'pair', 'times', 'odd', 'changes')
ORDERS = ('forward', 'reverse', 'even_odd')


def positions(n, order):
    if order == 'forward':
        return tuple(range(n))
    if order == 'reverse':
        return tuple(reversed(range(n)))
    if order == 'even_odd':
        return tuple(range(0, n, 2)) + tuple(range(1, n, 2))
    raise ValueError(order)


def read_permutation(n, order):
    # Visit configurations in lex order of observed bits, first observation first.
    configurations = [0]
    for i in positions(n, order):
        configurations = [y for x in configurations for y in (x, x | (1 << i))]
    return configurations


def step(x, mask, n):
    a, b = x << 1, x << 2
    toggle = 0
    for pair in range(4):
        if (mask >> pair) & 1:
            toggle |= (a if pair & 2 else ~a) & (b if pair & 1 else ~b)
    return (x ^ toggle) & ((1 << n) - 1)


def scalar(x, mask, n):
    state = [(x >> i) & 1 for i in range(n)]
    result = 0
    for i, own in enumerate(state):
        a = state[i-1] if i >= 1 else 0
        b = state[i-2] if i >= 2 else 0
        result |= (own ^ ((mask >> (2*a+b)) & 1)) << i
    return result


def widths(outputs, permutation):
    layer = [outputs[i] for i in permutation]
    counts = [len(set(layer))]
    while len(layer) > 1:
        names = {}
        parents = []
        for j in range(0, len(layer), 2):
            children = layer[j], layer[j+1]
            parents.append(names.setdefault(children, len(names)))
        counts.append(len(names))
        layer = parents
    return counts[::-1]


def literal_widths(outputs, permutation, n):
    table = bytes(outputs[i] for i in permutation)
    return [len({table[j:j+size] for j in range(0, len(table), size)})
            for size in (1 << (n-i) for i in range(n+1))]


def truth_tables(current, n):
    shift = n-1
    final = [x >> shift for x in current]
    previous = [(x >> (shift-1)) & 1 for x in current]
    odd_mask = sum(1 << i for i in range(1,n,2))
    odd = [(x & odd_mask).bit_count()%2 for x in current]
    changes = [(ini >> shift) ^ (((ini ^ x) & odd_mask).bit_count()%2)
               for ini,x in enumerate(current)]
    return (final, [a^b for a,b in zip(previous, final)],
            [2*a+b for a,b in zip(previous, final)],
            [2*(x >> shift)+b for x,b in enumerate(final)], odd, changes)


def census(n, directory):
    perm = {o: read_permutation(n, o) for o in ORDERS}
    names = [q+'_'+o for q in QUESTIONS for o in ORDERS]
    outfile = directory / f'census-{n}.csv'
    count = 0
    with outfile.open('w', newline='') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['mask','time','endpoint_support']+names)
        for mask in range(16):
            current = list(range(1 << n))
            update = [step(x, mask, n) for x in current]
            assert len(set(update)) == len(update)
            assert all(y == scalar(x, mask, n) for x,y in enumerate(update))
            for t in range(2*n+1):
                tables = truth_tables(current,n)
                support = sum(1<<j for j in range(n)
                              if any(tables[0][x]!=tables[0][x^(1<<j)]
                                     for x in range(1<<n)))
                entry = [mask,t,format(support,f'0{n}b')]
                for q, table in zip(QUESTIONS,tables):
                    for o in ORDERS:
                        profile=widths(table,perm[o])
                        if n <= 8:
                            assert profile==literal_widths(table,perm[o],n)
                        if q=='last' and n==8 and t==7 and o=='forward' and mask in (4,8):
                            assert profile[n//2]=={4:2,8:9}[mask]
                        if q in ('odd','changes') and t==1:
                            A = ((mask >> 2) ^ mask) & 1
                            C = mask.bit_count()%2
                            if o=='even_odd':
                                exponent = A + (n//2-1)*C
                                assert profile[n//2]==1<<exponent
                            if o=='forward': assert max(profile)<=4
                        if q=='changes' and t==1 and mask in (6,14):
                            assert sum(table)==1<<(n-1)
                            assert all(any(table[x]!=table[x^(1<<j)] for x in range(1<<n))
                                       for j in range(n))
                        entry.append(f'{profile[n//2]}/{max(profile)}')
                        count+=1
                writer.writerow(entry)
                current=[update[x] for x in current]
    print(f'n={n}: {16*(2*n+1)} rule/time rows, {count} exact cut profiles')


if __name__=='__main__':
    for size in (6,8,10,12):
        census(size,Path(__file__).parent)
