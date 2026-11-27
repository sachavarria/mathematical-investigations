# Which disagreements change the answer?

Working note, 26 November 2026. S.A. Chavarría posed the research question. OpenAI Codex derived the following candidate results and ran the reported checks. They await independent verification and confirmation of publication priority. Agent 404 reported separate oracle checks of the **preceding** fixed-density work, including its order-14 enclosure, with no line-by-line proof audit. Those checks are distinct from the new tests here.

## The question and the result

For a binary circle let w be its lexicographically least rotation. At a threshold a of length n the requested bit is whether reverse(w) < reverse(a). The weighted rank sums that answer over all 2^n rooted binary strings, or over all binom(n,d) strings of specified density d. This weights each necklace by its least bit period. In the binary Grandmama concatenation the weighted strict rank of a primitive boundary gives its tick. The earlier backward-walk reduction extends a boundary interval to any window by translation modulo 2^n.

Given a prefix used to locate the forward minimum, some starts remain candidates. We compute exactly the mass on which *every* candidate answers yes and the mass on which *at least one* answers yes. Their difference is the mass of circles with genuinely conflicting candidate answers for this particular cut. Both endpoints are polynomial-time computable per prefix, without listing circles, positions on an enumerated clock, or candidate configurations. A second polynomial-time calculation per prefix resolves all remaining disagreements involving exactly two candidate occurrences. Neither result supplies a general polynomial-time exact decoder.

## 1. Candidate sets and the exact uncertainty profile

In a nonconstant binary circle the lex minimum starts at a zero preceded by a one. A start inside a zero run loses to its head, and any start at a one loses at the first bit. Retain only these run heads. Choose depth 1 ≤ h ≤ n. From the retained starts keep all whose forward h bits attain the minimum. The true winner belongs to this set. Treat the two constant circles directly. The same reasoning works with an ordered prefix dictionary in gap coordinates: keep all gap origins spelling the same dictionary leaf as the least rotation.

Let l(X),r(X) be the smallest and largest numerical reversed n-bit keys across this candidate set for a circle X. With k the reversed threshold key, lower and upper bounds credit X precisely when r(X)<k and l(X)<k respectively. This proves:

    width(k) = sum over X of per(X) · 1{ l(X) < k ≤ r(X) }.

This identity handles strictness, tied spellings and repeated origins. It gives the answer common to all candidates whenever one exists. It is the precise uncertainty from allowing these candidates; the actual circle's forward order can determine more. In particular the sum of widths over all threshold keys is the sum of per(X)·(r(X)-l(X)). Multiplicity of plausible starts alone cannot specify either the resolution of one question or the mean resolution over queries. Refining the forward prefix shrinks every candidate set and nests every interval. In the same gap dictionary the previous unique-occurrence interval contains the new one. Even complete periodic ties can now have width zero.

## 2. Counting entire answer classes by cyclic avoidance

We give an explicit construction. For a finite set F of forbidden binary patterns let C(F) count rooted length-n strings whose periodic repetition avoids F. Optionally restrict density to d. Read bits backwards around the circle; this permutes the rooted words bijectively and preserves density. For a cell u require that no eligible start has forward prefix below u. Its forbidden patterns F in reverse reading order are reverse(u[:j]0) followed by 1, for each u[j]=1. The extra 1 is the bit just before the eligible start. Here u starts in 0. Mark the occurrence of m=reverse(u)1. On circles passing F, such marks are precisely the candidates for this cell. No eligible mark at all, including on a constant circle, is harmless in the differences below.

Partition occurrences of m according to their answers. In reverse order the first n-h preceding bits are unknown, and the final h bits of that candidate spelling are reverse(u). Thus the unknown integer is below

    int(reverse(a[h:])) + 1{reverse(u)<reverse(a[:h])}

exactly for yes. If h<n the leading preceding bit is already known to be 1. Subtract its place value and compare only the remaining bits. Each side of an integer cut is a union of at most n+1 binary prefix cylinders. Append their prefixes to m to get pattern sets Y and N detecting yes and no at that occurrence. Empty/full cases and h=n are evaluated directly. Then

    cell mass           = C(F)         - C(F union {m})
    definitely yes      = C(F union N) - C(F union {m})
    possibly yes        = C(F)         - C(F union Y).

For example, avoiding N allows a circle with no candidate marks at all. Subtracting the no-mark count removes it exactly once. The formulas credit each rooted word once regardless of how often a pattern occurs.

Build a deterministic longest-suffix/pattern-prefix automaton with all forbidden outputs discarded (including failure-link outputs). With transition-count matrices A0 and A1 the unrestricted avoidance count is trace((A0+A1)^n); at fixed density take the coefficient of z^d in trace((A0+z A1)^n). To justify the trace even for overlapping or wraparound patterns, repeat the labelled word enough times that the recent input determines the suffix state independently of initialization. A valid periodic stream thus has one possible closed path for that rooted labelling, and any closed path supplies a valid periodic stream. Parallel edges retain their bit labels. This uses the classical transfer-matrix principle for forbidden factors. [Transfer-matrix background, Federico Ardila](https://www-users.cse.umn.edu/~reiner/Classes/Ardila_handbook_chapter.pdf)

There are polynomially many states in n, even using the full total pattern length. Integer entries have polynomial bit length. Matrix powering or coefficient propagation is polynomial per cell. The program uses exact signed 64-bit arithmetic up to n=62, since each intermediate path count through n steps is ≤2^n, and switches to Python integers above that. Timings below are for the former regime.

**Same gap leaves, including unequal depths.** For minority ones replace a gap leaf by the concatenation of its 0^g1 codes and require a preceding 1. All such aligned starts are a superset of the canonical origins; the least gap prefix is the same event as the least such bit prefix. For minority zeros use concatenated 0 1^g followed by the zero that terminates the last gap, truncating to n if the entire spelling is already known. All zero starts are aligned; starts at ones can never beat a prefix beginning in zero. Use the same formulas with no preceding-bit condition for this second encoding. Distinct feasible dictionary leaves are ordered by their first differing gap, including the terminating zero where needed. Hence their orbit populations partition the layer. The archived polynomial-size dictionary and small-minority fallback still give the earlier uniform additive guarantee, now with weakly smaller uncertainty for each cut. A narrower enclosure can take longer to compute.

## 3. A direct fractional-precision decoder

For arbitrary h and two starts at displacement s, let g=gcd(n,s). The constraints that their h-bit forward fragments agree are edges i→i+s mod n from h consecutive sources. The edges of a full directed component run through one residue class mod g. If n-h≥g the excluded sources hit every class, so the graph is a union of paths. Its h equality constraints on fair independent bits have probability 2^{-h}. If n-h<g, every class has at most one missing edge; equality along the remaining edges forces equality on every whole class. In that case the two entire rotations are identical, so their colex answers cannot differ. This argument also covers opposite starts and the seam. It is important to exclude identical rotations here.

By a union bound, the unrestricted width at uniform depth h is at most 2^n binom(n,2) 2^{-h}. It is also bounded by the actual mixed mass, which the program computes. With depth capped at min(n, max(1,ceil(log₂(K binom(n,2))))) for n≥2, refining every mixed cell reaches width ≤2^n/K; full depth is exact. Split only the currently widest cell, and stop as soon as the sum of the enclosures meets the target. Even counting all prefixes to the cap gives O(1+Kn²) cells, each polynomial in n. Thus this is another deterministic polynomial(n,K) fractional-precision algorithm, in binary coordinates, for the full clock. The collision bound concerns the full binary population; use the gap-dictionary guarantee for a relative-to-layer bound at arbitrary fixed density. The exact decoder question would require an exact count of the mixed residual or a different representation.

## 4. Exact two-origin contribution

Consider one unresolved binary cell u. In forward reading order take mark 1u and forbid any 1 u[:j] 0 for u[j]=1. Start at the end of 1u. An elementary return payload reads until the next completion of 1u. A prefix matcher for the mark and forbidden patterns, initialized in the state 1u, recognizes a prefix-free set of such payloads and retains overlapping occurrences. No forbidden pattern is longer than 1u, so the state at a mark is known.

If there are exactly two eligible occurrences in the circle their payloads are A,B. Skip the common u at the original starts. Their forward spelling order is the order of A versus B, since returns are prefix-free. Equality gives identical rotations and equal answers. When the answers conflict, A and B are unequal and there is exactly one choice of winning orientation, A<B. Its bit period is n: a nonidentity period would have to exchange the two marks, giving identical payloads. Enumerate only |A|=j, 1≤j<n, with |B|=n-j. For each j, generate the two payloads in parallel by dynamic programming. Track their two prefix-matcher states, the first comparison of A and B, and the signed index of the rightmost difference between *each* of the two original spellings and the threshold. Optionally track density. For stream position i in AB the two original bit indices are (h+i) mod n and (h+i-j) mod n. At each column append at most two bits, forbid an early or missing return, and update the two comparisons at those indices. In particular the traversal order does not decide which colex difference prevails.

Accept A<B and opposite cut signs (equality with the threshold counts as no). Sum n times each accepted assignment in separate yes and no accumulators according to the winner. Each mixed two-origin necklace has exactly one anchored AB of this type. All state ranges are polynomial in n, including the two difference indices, and each state has at most four successors. This counts whole sets without individually listing their winning origins. Add the yes mass to the lower endpoint and subtract the no mass from the upper. The remaining width is exactly the mass with **at least three candidate occurrences and opposite answers among them**. Larger fixed numbers of simultaneous streams invite analogous product-state methods, but the present proof and code concern two; a uniform polynomial bound independent of multiplicity remains missing.

## 5. An adversarial exact-ranking test

Adaptive prefix refinement alone can encounter exponentially many genuinely mixed cells even for a single primitive half-density threshold. For k≥0, let c range over k choices of 01 or 10, let u=00001 c 11, and take n=4k+20. In each cell consider the two circles

    u 101 u 011          u 001 u 111.

Both have exactly half ones. Each has just two occurrences of the unique longest-run *length* four, one at the start of each u. Consequently these are the only minimum-prefix candidates at depth |u|. The two cuts at the candidates read backwards from endings 01 and 11. Use the same threshold for every c, namely a=0^(n/2-2) 1^(n/2-2) 0011. It is primitive and lex-minimal. The ending 01 passes. At the ending 11, the preceding context from 011 or 111 gives a reversal larger than reverse(a), whose first four bits are 1100 (the u preceding 011 ends in 1). Thus each cell is mixed. In the first circle the forward continuation 011 wins over 101, and its preceding tail is 101: yes. In the second, 001 wins over 111 and its preceding tail is 111: no. Hence there are at least 2^k distinct mixed prefixes with both true outcomes represented. Every ancestor of such a prefix is mixed on the same witness, so a strategy requiring all mixed prefixes to be separated by individual bit refinements must reach all of them for exactness. The two-origin calculation resolves both displayed witnesses algebraically. This contrast identifies a limitation of the prefix strategy and gives an explicit route around that limitation on the witnesses. It provides no intrinsic lower bound on rank, and two-origin resolution need not empty each of these cells of other circles.

## 6. Measurements, reproduction and open direction

Requires Python and NumPy. The two sibling archive directories fixed-density-gaps and return-ranking are used only for the matching-dictionary comparisons and the inherited local backward walk, respectively.

    python verify.py
    python check_pairs.py
    OPENBLAS_NUM_THREADS=1 python experiments.py
    OPENBLAS_NUM_THREADS=1 python check_phase.py
    python sensitive.py 00010111 3 --pairs
    python phase.py 101001 100

The outputs are stored in verified.txt, pair-results.txt, measurements.txt and phase-results.txt. The finite oracle enumerates true rotation orbits, computes both extremal candidate keys directly, and checks the endpoints themselves. It is stronger than checking containment of an exact rank. Additional checks compare with every tick of small directly constructed clocks, including cyclic wraparound. Timings are single runs on the reported environment, without a rank table or prior cycle construction in the estimator.

* At order 14, density 7, the exact rank of 00000110110111 is 2900. With identical 320 gap leaves the previous interval [2884,2900] becomes [2900,2900]. The stricter computation took about 0.27 s versus 0.009 s in this run. At eight leaves it already reduced the width from 912 to 140.
* Across all 4080 primitive order-16 boundary queries, depth seven left 2078 rooted words with multiple origins before looking at the cut. Actual widths ranged from 0 to 912 with median 656; 42 queries were exact. At depth nine the median was 144 and 152 queries were exact. These distributions were measured with the independent orbit oracle.
* On one specified primitive boundary at order 60 the binary adaptive decoder reached 1% width in about 0.31 s (123 cells) and 0.25% in about 2.18 s (477 cells). Exact integer endpoints and the threshold are in the outputs. These are practical examples, not uniform runtime forecasts.
* At order 8, threshold 00010111 and binary depth three, the cut-sensitive interval [171,187] becomes [171,171] when mixed two-origin circles are counted. At order 14 an unrestricted depth-five interval in the measurements still has width 28 after the second step. The method encounters real unresolved mass.

The remaining problem is to aggregate the correlation between the least forward continuation and its backward cut sign across *unboundedly many* candidates. A recurrence for the total mass with the two signs present is already available. To extract the exact rank, it must additionally apportion that mass by the winning sign. The two-return comparison establishes this for multiplicity two. A polynomial summary closed under joining ordered groups of competing continuations would advance the general problem. Whether such a summary exists remains open.

[Previous fixed-density results and independent-verification context](https://github.com/sachavarria/mathematical-investigations/tree/f7751eca50f7c685e4770eb49db9c88c2c0a208d/experiments/grandmama/fixed-density-gaps).
