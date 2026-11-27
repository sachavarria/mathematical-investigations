# A complete colex cut on a population of bounded crossing width

Candidate contribution, 27 November 2026. The width cap in this statement is a restriction on the population being counted. Independent review and confirmation of publication priority remain open.

The [transcript refinement](run-transcripts.md) improves the dependence on D to a single exponential. This first proof isolates why numerical lengths can be aggregated and supplies a different verification algorithm.

## Statement

A length-n binary word is considered on a circle with a marked starting position. Its necklace is the set of its distinct rotations. Its canonical spelling is the least of these rotations in ordinary lexicographic order. Its primitive root is the shortest block whose repetitions give the canonical spelling. The packet width is the number of circular 1-to-0 transitions in this root. It is zero for a constant word. The connection to BWT crossings and its antecedent are described in the [source register](literature.md).

Given an arbitrary n-bit threshold, count all rooted words whose canonical spelling precedes it when both are read backwards, and whose packet width is at most D. An optional fixed zero count is allowed. This strict weighted rank can be computed in

    2^{O(D log(D+2))} poly(n) bit operations.

The polynomial degree is independent of D and of the threshold. Each distinct rotation is counted once, so the weight of a necklace is its primitive period. The earlier explicit frontier proof gave a bound polynomial for each fixed D on such a full comparison, with the exponent depending on D. This result takes the threshold all the way to its last bit without that dependence. It does not restrict the number of runs in the threshold.

## Idea

Consider the two zero runs in 00010111. The start of the three-zero run wins the competition with the start of the one-zero run. This competition would have the same outcome for any two positive lengths with the same strict order. The numerical lengths matter again when imposing density or comparing to a specified threshold. These two uses can be separated. First decide the canonical starting position from the order relations, including ties. Then count all integer lengths that satisfy those relations and the requested comparison. Run-pair encoding and its block comparison already occur in Sawada, Williams and Wong. The proposed advance is the parameterized count across numerical realizations. [Prior work and scope](literature.md)

## Proof

Fix a mixed primitive length p and its zero count z. There are some r alternating zero and one runs, with 1≤r≤min(D,z,p−z), in its canonical spelling. Write this spelling as the concatenation of blocks 0^{a_j}1^{b_j}, j from 1 to r, with all lengths positive. A rotation beginning with one loses to a zero start. A rotation starting strictly inside a zero run loses to the start of that same run, which keeps a zero at the first position where the two spellings differ. Thus only the r block starts compete.

At a block start a longer zero run wins. If the zero lengths tie, a shorter one run wins, because it reaches the next zero first. For the last run of a full equal-length comparison one cannot exhaust one spelling strictly before the other after all preceding runs agreed. Thus the canonical and primitive conditions together say that the sequence of pairs (−a_j,b_j) is strictly smaller lexicographically than each of its nontrivial cyclic shifts. Equality under a nontrivial shift gives a proper power. Conversely any period of a mixed circle sends zero-run starts to zero-run starts, and hence gives equality for a block shift. For r=1 there are no competing block starts.

Enumerate two ordered partitions of the r labelled positions, one for the a's and one for the b's. A part denotes equal lengths. Parts are arranged from smallest to largest. The ordered partitions determine every block comparison, so discard the pairs that fail the strict rotation test. Each valid numerical canonical spelling belongs to just one surviving pair of ordered partitions. Conversely each numerical realization of a surviving pair is a primitive canonical spelling. There is no division by r.

To count the realizations below a p-bit reversed cutoff, first inspect its first bit. A mixed candidate begins with one when read backwards, so a cutoff beginning in zero gives no contribution. Otherwise the two reversed strings start in the same bit. Read their runs together. At the first unequal length, a shorter run of ones, or a longer run of zeros, makes the candidate smaller. In a proposed first-difference case impose equality to the corresponding cutoff lengths at all earlier runs and this one strict inequality at the current run. These cases are disjoint. If all runs encountered before either string ends have equal lengths, equal total bit length forces the two strings to end together and be identical. This gives no contribution to a strict cut. In particular it suffices to inspect at most 2r cutoff runs. There are no restrictions on the uninspected suffix. The cases of cutoff zero and a cutoff above the largest p-bit integer are interpreted as empty and full.

Within each case, a length class has an allowed integer interval, possibly a singleton or empty. Zero and one lengths can now be counted independently at fixed z. Suppose the zero length classes in increasing order have multiplicities m₁,...,m_h. Select distinct positive integers t₁<...<t_h from their intervals with Σm_j t_j=z. Scanning possible values t from 1 to z, keep a table indexed by the number j of classes already assigned and the used total. Each value may be skipped or assigned to the next class if its interval contains t. Assignment adds m_{j+1}t to the total. Any solution determines exactly one history of these choices. Apply the same calculation to the one lengths with total p−z and multiply. Summing over the first-difference cases and the surviving orders counts precisely the primitive minima below the cut.

Finally let K be the integer value of the reversed n-bit threshold. A primitive length p dividing n contributes p rooted words for each eligible primitive necklace. Repeating its spelling multiplies its reversed integer by (2^n−1)/(2^p−1), so the primitive strict cutoff is the ceiling of K divided by that multiplier. At fixed full zero count, the repetition number must divide it. Count the one-letter primitive roots directly. These cases exhaust all proper powers, and their caps apply to the primitive packet throughout.

There are at most r^r ordered partitions for one bit, since ordered class indices are in {1,...,r}. Each of at most 2r cases per retained pair uses two tables with O(rp) entries per value and at most p values. All row counts have polynomial bit length: for a feasible order and partial total they count positive length assignments, bounded for example by (p+1)^r. Polynomial overhead covers creating the orders, canonical comparisons, all densities, and all divisors. Summing over r proves the bound. ▪

## How much of a complete query was counted?

At order 64 and zero count 32, use the threshold obtained by repeating 00101101 eight times. The counts below refer to primitive-packet widths, including proper powers.

| Width cap | Rooted words in the restricted population | Rooted words below the complete strict cut |
|---|---:|---:|
| 1 | 126 | 2 |
| 2 | 34,846 | 1,122 |
| 3 | 4,767,622 | 279,914 |

The half-density population has binomial(64,32)=1,832,624,140,942,590,534 words. The last line gives an exact comparison on a small part of it. A low-width observation alone provides no right to discard the rest when assigning its global temporal position. The general exact bound has not improved.

The [reference program](run_rank.py) passed 7,734 comparisons with direct rotation orbits at every threshold through n=7, each tested cap, and fixed or unrestricted density. A [different enumerator](check_large.py) reproduces all six order-64 table entries by assigning the actual lengths, constructing bitstrings and comparing them. The latter oracle is intentionally slower and uses the proved restriction to zero-run starts. [Small-order results](run-results.txt) · [Large-order results](large-results.txt)
