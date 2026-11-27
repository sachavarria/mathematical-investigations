# Binary colex ranking and Grandmama decoding

26 November 2026. S.A. Chavarría posed the research question. Agent 404 independently reproduced earlier finite findings and emphasized that polynomial-time ranking was unresolved. Codex (GPT-6.2 Astra and internal collaborators) developed and cross-checked the work here. The new method is a candidate original contribution pending independent verification and confirmation of publication priority.

**Status.** The binary case admits the following working upper bound for exact counting and decoding: 2^{O(sqrt(n log(n+1)))} bit operations. The reference implementation can use subexponential space. The previous algorithm retained a polynomial-space advantage. We have not established polynomial time, practical superiority on small orders, or a lower bound on general polynomial-time algorithms.

- [First-return construction, proof and cost](return-codes.md)
- [Quasinecklace subtree weights, transfer matrices and reductions](tree.md)
- [Exact rank counters](return_rank.py) and [arbitrary-window decoder](decode.py)
- [Original interactive counting instrument, redesigned in place](../weighted-rank/Index-Study.html). Its measured operations are those of the index and residual scan. The research counter is separate.

## What the tree tells us

The concatenation tree traversed in RCL order emits canonical representatives in the required colex order. The contribution of a complete consecutive subtree equals the sum of its representative periods. Having its endpoints gives that sum via the difference of two weighted ranks; efficient traversal alone does not supply it. We have no polynomial-time subtree-mass formula for that tree. The Gabrić–Sawada suffix generation tree is a different tree. Its suffix parameters and the word buffer serve different roles. Substituting the small integer parameters for that buffer in a subtree-mass memoization loses information. The explicitly verified example and scope of the associated matrix obstruction are in tree.md. The paper's stated open problem concerns efficient colex ranking and unranking, including alphabets beyond the binary case treated here.

## Why the remaining enumeration matters

For the marker u=0^h with h≥3, two legal first-return words are the single 0 and the word consisting of 1 followed by h zeros. Choose t≥1 long words and s≥1 short words, so T=t+s and n=t(h+1)+s. Every circular arrangement yields a necklace whose least rotation ends in 01 because all its ones are isolated. Hence every such necklace lies strictly before the primitive threshold 0^(n−2)11. There are at least binom(T,t)/T distinct cyclic schedules (each orbit has at most T elements). Taking t=floor(n/(h+2)) and s=n−t(h+1) gives s≥t and, for h on the order of log n, superpolynomially many genuinely contributing schedules. A method that visits them all cannot be polynomial on this family.

Yet their **aggregate mass** is exactly (n/T)·binom(T,t). For a token necklace of least token period j, the least bit period is nj/T, by the marker-to-marker period argument in the proof. Summing j over all token necklaces counts every one of the binom(T,t) arrangements once. Thus precisely the family on which enumeration breaks down can be aggregated when the threshold includes the whole family. The consequential next question is how to preserve that compression when an arbitrary threshold cuts *through* a family of nonidentical return words. There is also the cost of enumerating markers themselves. A successful recurrence must control both costs.

In a useful stress test, let h≥2, u=0^h and let the two equal-length return words be 101u and 111u (length L=h+3). Encode a binary m-word q by concatenating its return words and moving the final u to the front. Every occurrence of u is a marker at one of the designated boundaries. A comparison of rotations at marked starts is a comparison of token words, and comparisons at other starts cannot produce the minimum. Thus canonicality is preserved and period scales by L. Colex comparisons of encodings are also exactly colex comparisons of q: all raw encodings share the trailing u moved to the front, and the two equal-length codewords are colex ordered. On this restricted family the weighted count below an encoded threshold equals L times the smaller-order weighted count. This is a test for a recursive aggregation strategy, not a claim of computational hardness.

## Verification

Using Python 3 in this directory:

    python3 return_rank.py 00010111
    python3 decode.py 101001
    python3 return_check.py
    python3 decode.py --check
    python3 tree_check.py
    python3 structural_check.py
    python3 family_check.py

The first line returns (171, 24, 20): weighted prefix mass, preceding necklaces and preceding Lyndon words. The second returns tick 15 at order six. The rank verifier compares all thresholds through order 7, then selected thresholds through order 12, against rotation-orbit enumeration. The decoder verifier constructs the full clock independently and checks every window through order 9, including the cyclic seam. The internal structural audit checks 81,810 word/marker-length pairs through order 13. The family checks test the two restricted identities. These finite checks are separate from the asymptotic proof.

## Sources

- Daniel Gabrić and Joe Sawada, [Necklaces and Lyndon words in colexicographic order](https://arxiv.org/html/2607.05324v1), especially §§2–4 and 6.
- [Concatenation trees and the PCR constructions](https://debruijnsequence.org/db/db/db/concat), and the [PCR2 successor rule](https://debruijnsequence.org/db/db/db/shift). The reference decoder inverts the PCR2 flip from the known tail; its straightforward rotation test is quadratic in bit operations for a single word.
- P. B. Dragon et al., [Grandmama construction](https://doi.org/10.1016/j.ejc.2018.03.006).
- Kociumaka, Radoszewski and Rytter, [lexicographic ranking](https://doi.org/10.1137/15M1043248). Lexicographic and colexicographic ordering of lex-minimal representatives pose different counting questions.
