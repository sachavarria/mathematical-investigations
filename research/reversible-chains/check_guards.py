"""Direct finite checks of the invariant guard construction. Uses only Python."""
from itertools import product, combinations


def step(state, mask):
    padded = (0, 0) + state
    return tuple(bit ^ ((mask >> (2 * padded[i + 1] + padded[i])) & 1)
                 for i, bit in enumerate(state))


def trajectory(initial, mask, length):
    state = initial
    output = []
    for _ in range(length):
        output.append(state[-1])
        state = step(state, mask)
    return tuple(output)


def main():
    checked = 0
    families = 0
    for length in range(1, 8):
        for mask, guard in ((2, 0), (4, 1)):
            traces = set()
            zero_end = set()
            for free in product(range(2), repeat=length):
                state = (0,) + tuple(bit for y in free for bit in (guard, y))
                successor = step(state, mask)
                assert successor[0] == 0
                assert successor[1::2] == (guard,) * length
                assert successor[2::2] == tuple(
                    y ^ z ^ guard for y, z in zip(free, (0,) + free[:-1]))
                trace = trajectory(state, mask, length)
                traces.add(trace)
                if free[-1] == 0:
                    zero_end.add(trace)
                checked += 1
            for count in range(length + 1):
                for times in combinations(range(length), count):
                    def project(population):
                        return {tuple(trace[t] for t in times)
                                for trace in population}
                    assert len(project(traces)) == 2 ** count
                    assert len(project(zero_end)) == 2 ** (count - (0 in times))
                    families += 1
    print(f"PASS {checked} guarded configurations; {families} time families.")


if __name__ == "__main__":
    main()
