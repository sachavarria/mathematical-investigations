# Circular runs and the width of a stable shuffle

Candidate derivation and internal audit by Codex, 27 November 2026. The instrument displays an invariant of a rotation packet that also bounds the number of endpoints in an exact counting calculation.

## From boundary marks to live paths

For a last column b of length n with z zeros, let P be the stable-sort permutation and v(i) the zeros among its first i entries. After constructing the first i edges of P the source set is [0,i). The targets already occupied are [0,v(i)) and [z,z+i−v(i)). The number of occupied targets outside the source set is consequently

    d(i) = min(i,z) − v(i).

Below the cut i=z this count increases by one on a one. Above that cut it decreases by one on a zero. The maximum D is therefore the number of ones among the first z entries of b. For a primitive necklace these are precisely the sorted rotation rows starting in zero and ending in one. Reading around the original circle, each such row identifies a distinct transition 1→0. Thus the maximum crossing count equals the number of circular zero runs for a mixed primitive word. The transition formulation includes the constant primitive words at length one, with peak zero. For a periodic rooted window the instrument uses the packet of its primitive root.

## Counting with a bounded peak

Fix an itinerary s of k bits, a density z and a peak limit D. The following transfer counts exactly those single-cycle columns with that itinerary and peak at most D. Redirect target 0 to a fresh sink n. A completed permutation is a single cycle precisely when the split graph is one path from 0 to n. Construct rows in order. For the next bit, its raw target is v on zero and z+i−v on one. Reject any choice exceeding its quota or peak limit. Splice the new directed edge into the paths ending at its source and beginning at its target, when present. Reject a closed cycle immediately. At completion retain just paths spelling a word that starts with s. Every retained column occurs once.

There is no need to store the whole text on a partly built path. Store its longest prefix t that occurs as a contiguous factor of s, together with one bit recording whether any text remains after t. Empty text is allowed. This summary composes under concatenation. If the left summary already overflows, no extension can repair its first failed prefix. Otherwise append characters from the right summary until the first failure. If that summary overflows before the merge detects a failure, its first omitted character necessarily makes the merged prefix fail too: a suffix of a factor must itself be a factor. Acceptance is equivalent to t=s, including k=0. This discards text that cannot affect the comparison, even if its path eventually joins another path in a different order.

At a fixed (i,v), the possible starts and ends of nonempty paths are known from the source and target sets. Splitting row zero adds at most one pair of endpoints. The transfer thus retains a matching of at most D+1 starts to ends and one text summary per matched pair. There are at most M=2(1+k(k+1)/2) summaries. A layer has at most

    (D+1) (D+1)! M^(D+1)

states: v has at most D+1 feasible values. Each state has two possible extensions with polynomial processing and integer weights of at most n+1 bits. This proves fixed-parameter tractability in the *combined* parameters D and k. For a full-length query it gives polynomial time for each fixed D, with an exponent that can depend on D. General columns can have growing D; this does not improve the archived unrestricted bound. In particular the visual width belongs to a packet, whereas a ranking query must count a population of packets. The width of one displayed packet cannot predict the cost of that entire query.

## Finite checks

The [program](frontier.py) checks every length through seven, every zero count, every binary prefix including the empty prefix, and every relevant peak cap against a direct oracle sorting rotations. At n=64, z=32 and D=3 there are 24,848,641 possible last columns before the connectivity and itinerary tests, because the count with peak j is binom(z,j)binom(n−z,j). Of these, 451 are single-cycle and have itinerary beginning 101. The largest transfer layer in that calculation had 210 states. Layer size is not elapsed time or the total number of states processed. [Reproduction output](frontier-results.txt)
