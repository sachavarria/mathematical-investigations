# From an observed word to a temporal landmark

26 November 2026. Investigation prompted and directed by S.A. Chavarría; mathematical development, code and interface with ChatGPT (Astra). Working derivation. No independent verification or priority claim.

Use the zero-based binary Grandmama cycle of order n≥2, starting at the first emitted bit of the colex necklace concatenation. Each necklace is represented by its lexicographically least rotation. Each contributes its shortest repeating unit, once. Sources: [Grandmama construction and successor rule](https://doi.org/10.1016/j.ejc.2018.03.006), [decoding and Granddaddy comparison](https://debruijnsequence.org/db/rank). This note concerns partial decoding.

## Recognition and an exact reduction

Call a tick an anchor if a length-n primitive necklace block starts there. Its observed forward n-bit window is then its own least rotation and is primitive. Conversely every such word occurs at its own block start and the de Bruijn property precludes its appearance elsewhere. The test is exact. Merely rotating the observed word to canonical form loses the distinction between being at an anchor and bearing a resemblance to one.

Move backward from an observed word until the first anchor a; call the distance j. Backward stepping needs no inverse table. For a word ub with final bit b, try 0u and 1u with the published forward successor rule. Exactly one leads to ub since the successor permutes the states in one cycle. One backward step costs O(n) using that rule. Primitivity and least rotation can also be checked in O(n) using period testing and minimum rotation (or directly in quadratic time). The experimental interface uses a table to keep the interaction instantaneous, not to benchmark succinct decoding.

Let C(a) be the sum of the primitive periods of all representatives strictly preceding a in colex order. The absolute phase is C(a)+j modulo 2^n. This formula also applies when the observed tick belongs to a short block after a: identifying that particular short host is unnecessary. A table for C is exponentially large. A uniform polynomial-time algorithm for C on primitive anchors would give an average-polynomial-time phase decoder under uniform phase, by the following bound. Conversely a rank oracle immediately evaluates C(a) on these inputs. This does not establish worst-case polynomial equivalence.

## Mean cost, independent of block order

Write N=2^n. Consecutive anchors have forward gaps g_i=n+t_i, where t_i counts the bits emitted by short blocks in the gap. Their total T equals the number of nonprimitive n-bit words: every short orbit of size p accounts for p words and emits p bits. The distances to the preceding anchor in a gap are exactly 0 through g_i−1, counting ties at distance zero. Thus, under uniform phase,

    E[j] = (n−1)/2 + (nT + sum_i t_i²)/(2N).

Every proper period of an n-word repeated from a shorter root divides n and is at most floor(n/2). Hence T ≤ sum_{p=1}^{floor(n/2)} 2^p < 2·2^{n/2}. Since sum t_i² ≤ T², the additive excess is bounded by 2 + n·2^(−n/2). This is an asymptotic (n−1)/2 + O(1) theorem. The argument also applies to other orders of these same emitted blocks whenever their concatenation is de Bruijn. Recognizing an anchor only costs comparisons on the word at hand. Turning it into an absolute time requires a global weighted count; allowable preprocessing and its storage must accompany any ranking-time claim.

For prime n the only short blocks are the constant bits, adjacent across the cyclic seam. The largest gap is exactly n+2 and the backward search terminates within n+1 steps on every input. Thus for prime orders worst-case polynomial ranking reduces to C on primitive necklaces. Nonconstant blocks then have weight n; the remaining obstacle amounts to counting preceding primitive representatives in colex order (with the constant-zero prefix contribution).

## Experiment and open question

Run python3 anchors.py in this directory (uses windows.py). The program generates all windows, compares detected anchors to annotated block starts, and checks the mean identity independently from measured gaps. Every binary order 2 through 16 passes. For all these orders the largest gap equals n+max(2,n/p), where p is the least prime divisor of n. At composite orders n/p is the largest proper divisor. A primitive root of any such length exists, giving the corresponding lower bound, and the two constant blocks give the seam lower bound. The upper bound for composite n is conjectural. The important obstruction to test is a consecutive run of short blocks with total emitted length larger than either of these individual obstructions. Another experiment would sort admissible orders by their gap second moments. Agreement on a mean cost need not imply agreement on the worst case.

## Two kinds of access, two representations

In the atlas's [Experiment 007](https://sachavarria.github.io/The-Morphology-of-Information-/#experiment007), some admissible graphs lie outside the permitted component. The second pane uses the exact adjacency lists and motif counts generated by S.A. Chavarría's [Experiment 009 implementation](https://github.com/sachavarria/The-Morphology-of-Information-/blob/main/experiment009.py); the artist's original atlas and motion studies are separate works. From graph 1, switches reach six graphs, triangle reversals added to switches reach fifteen, and allowing up to three replacements reaches all twenty-one. The first two rules reach zero motif-bearing graphs from graph 1. The ring placement is a display coordinate with no metric significance. The drawing depicts possible transitions, not transition probabilities or time spent.

Grandmama is connected. Uniform distribution on its phases gives zero conditional uncertainty about phase after seeing the full window. In a binary counter the analogous ranking map is just reading a binary numeral. In a cyclic group generated by g, with transition x↦gx and start 1, ranking x is exactly the discrete logarithm; its difficulty depends on group, encoding and computational model. Granddaddy supplies a still closer control: a known efficient decoder for another necklace concatenation. Dense labelled layouts and tables can reveal the answer by spending preprocessing and display space. The object deliberately permits this reveal. Perceptibility is an empirical question about the participant; no human timing or perceptual study was conducted.

The full-block certificate arose by changing the representation from a scatterplot of failed rotation guesses to marked block starts and the lengths of the intervals between them. The subsequent interactive display makes the criterion inspectable; no discovery is attributed to user interaction that has not happened yet.
