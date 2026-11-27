# Ordered transfers for recurrent minima

Research question by S.A. Chavarría. Derivations, code and finite audit by OpenAI Codex, 26 November 2026. Candidate mathematical contributions pending independent verification and priority review. Agent 404's reported independent verification concerned earlier work.

This note concerns the strict weighted colex rank of length-n binary necklaces represented by their **lexicographically** least rotations. The weight is the number of distinct bit rotations. The earlier Grandmama reduction uses this rank at a primitive boundary and a polynomial-time backward walk. General polynomial-time exact rank and decoding remain open. All earlier files are preserved.

## 1. Audit of the preceding results

I reread the [competing-origin proof and code](https://github.com/sachavarria/mathematical-investigations/tree/d306f8b38ebf80cb8b15e7f562ed47f0525e556b/experiments/grandmama/competing-origins) and reran both its test programs. Both outputs reproduced byte for byte. The audit targeted the following distinctions.

* At e origins, an accepting prenecklace transcript makes e-1 comparisons, branching only on equality or a strict increase. Each binary prefix subset has two child subsets and there are 3^e subset/split pairs. Polynomial budgets, the suffix pivot, depth and the shared return state give the claimed 6^e poly(n) cost up to polynomial factors. Period weighting uses ns/e, where s is the token period. Counting tied origins as independent winners would overcount periodic words.
* With t copies of the minimum, equality in the block construction joins slots in the same column of at most t different tails. The distinguished strict-edge endpoints are O(t); only unpinned equality classes of multiplicity 1 through t need the ordinary census. This is polynomial **for fixed t**. The number of possible census vectors can grow as (r+1)^t. A short description of one vector is different from a polynomial bound on the number of vectors. No uniform polynomial-time conclusion follows from that proof.
* For the depth-h binary agreement certificate, the stated support is for the full population, before algebraic tie resolution. With H=max(h,2), n≥4H+4 and N=2^n, positive width means N/2+2^h < k ≤ N-2^H-2 for the reversed key k. At the low end, a head containing a one in its first h bits loses to a longer zero run unless it is the sole head. At the high end, matching a second h-prefix would force a zero beyond the last zero; at h=1 adjacent zeros cannot both be heads. The witnesses with two ones and with two zeros attain the endpoint keys, and the third circle's two candidate keys overlap both spans. The low endpoint itself is exact; the high endpoint is mixed. In addition to the previous exhaustive checks I recomputed the three spans directly on 120 instances through h=40, including the minimum allowed n. Neither the proof nor these witnesses imply this support at a single prescribed density.
* The opposite-sign pair bound after exact R-way resolution uses e-1≥R opposite-sign pairs when e>R. Overlapping equal fragments whose constraint graph contains a complete cycle cannot simply be treated as independent. In the circular consecutive-source setting, once the missing sources occupy fewer than gcd(n,s) positions, each residue cycle has at most one edge missing and the full rotations coincide. Only the forest case contributes disagreement.

I found no defect in those bounds under their stated assumptions. The improvements below use the special structure of binary run heads.

## 2. A polynomial base alphabet and an FPT improvement

Use every cyclic 1-to-0 transition as a landmark, at its 0. After skipping that common initial 0, an elementary first return to the end of 10 has form 0^i 1^j 0, i≥0 and j≥1. The ones before the final zero form a single run, because an earlier 10 would have ended the payload. Conversely every such word is legal. These words form a prefix code C0. At length ≤n there are n(n-1)/2 possibilities. For w=0V the payload stream is P=V0. To compare canonical marked starts, compare their circular payload streams. The two constant circles are handled separately.

**Theorem.** Over the whole binary population, the exact weighted rank contributions with minimum elementary-return frequencies 1 through T can be computed in 6^T poly(n) bit operations, also at prescribed density. No specified minimum and no bound on total run heads are required. This is FPT in minimum frequency for these slices; the earlier n^{O(t)} result applied more broadly to a supplied arbitrary prefix.

**Proof.** Enumerate the polynomial base alphabet. For p of length <n, let u=0p. Having least elementary payload p is exactly the event that the least run-head prefix of length |u| is u. Indeed prefix-freeness makes every other first payload smaller or larger within the comparison with p, and equality designates exactly an occurrence of p. Thus multiplicity in the new literal prefix cell is the frequency of p. Apply the previous 6^T poly(n) counter at u. The cells are disjoint on circles, even though their lengths vary. If |p|=n there is one head, the spelling is 0 followed by p without its last bit, and its least period is n. Sum these contributions. The explicit routine is landmark.py. Taking T=O(log n) gives a polynomial-time slice encompassing unbounded numbers of competitors. Knowing the observed window's own frequency does not constrain the entire ranked population.

## 3. Eliminating a minimum with ordered products

Let C be a prefix code of nonempty bit words. Ignore words longer than n. Fix the least symbol p actually present on a circle, and put G={x∈C:x>p}. If every token equals p the circle is a pure repetition. Otherwise circularly group the payloads into codewords p^b x for b≥0 and x∈G. This is again prefix-free: the first non-p token completes a group. Among the marked origins the least rotation is a group head, since a start inside a run of p loses when its shorter initial run reaches a larger token. Ordered comparison of group words is by **descending** b, then by ascending x. The actual bit spelling at the winner is unchanged. This is related to standard free-monoid elimination; the order-sensitive counting and stopping rules below are the points of application. [Background on Lazard elimination and Lyndon factorization](https://www-lipn.univ-paris13.fr/~duchamp/Conferences/CAP23/Slides%20%26%20Docs/Duchamp/CAP23-GHED_v22.pdf)

Write C_{i+1}=p_i^*(C_i)_{>p_i}. If we take another actual minimum, its spelling begins with at least one copy of p_i, since some group has b>0. Thus the pivot words in a genuine history are nested proper prefixes. A bit period preserves all the group boundaries inductively: initially it preserves all 10 occurrences, then it preserves the distinction between p and larger tokens. In particular a unique pivot yields bit weight n. A pure circle of copies of a pivot p has bit weight |p|, since its only final boundaries occur at multiples of |p|.

### What must survive an anchored product

Set a'=a[1:]+0. Both P=V0 and a' end in 0. The original word 0V is below a in colex iff P is below a' in colex, or they agree and a starts in 1. For any language F and offsets i,j, keep upper triangular matrices T,E,L. Their entries count spellings of length j-i in F, respectively all, equal to a'[i:j], or strictly below that segment in colex. At a fixed placement, once the forward anchor has been imposed, these three numbers suffice for every concatenation context. For unambiguous concatenation the exact rules are

    T(FG) = T(F) T(G)
    E(FG) = E(F) E(G)
    L(FG) = T(F) L(G) + L(F) E(G).

The right factor decides whenever it differs; when it agrees, the decision passes to the left. Summing over the split position accounts for variable lengths. For positive-length codewords G the series are nilpotent in this truncation, and the unambiguous star satisfies

    T(G*) = (I-T(G))^{-1}
    E(G*) = (I-E(G))^{-1}
    L(G*) = T(G*) L(G) E(G*).

The final formula locates the rightmost differing token against its own assigned substring. This sums all multiplicities without census variables. Only addition of disjoint languages, unambiguous products, and explicitly justified subtraction are used.

This signature has a contextual interpretation. With a strictly smaller right context, all T completions pass. With an equal right context and a rejecting left comparison, L pass; with an equal right context and an accepting left comparison, L+E pass. Whenever these three testing contexts are available, they recover the three numbers, so any summary supporting all three tests must distinguish differing triples. Some individual thresholds allow fewer contexts. The signature is for an **anchored** language and preserves order of multiplication. It is not by itself a selector of the canonical origin.

### A polynomial operator for a supplied history of any depth

For x=p_i^b y in C_{i+1}, the language of group tokens strictly above x is the following disjoint union:

    (C_{i+1})_{>x} = (union over 0 ≤ j < b of p_i^j) (C_i)_{>p_i}
                      union p_i^b (C_i)_{>y}.

This follows from descending run length and the tie comparison of the terminator. For a supplied p_0,...,p_d compute the transfer of (C_d)_{>p_d} recursively by this identity. At the base sum actual elementary words. A call introduces the previous pivot and a single stripped tail; pivot subproblems can be reused. Every pivot seeds at most one tail chain through each earlier level, so there are O((d+1)^2) distinct level/word subproblems. Exponents are ≤n, each matrix has (n+1)^2 polynomial-bit entries, and d≤n. Thus the computation is polynomial even for an explicitly supplied history of growing depth. It does not materialize the higher alphabets. This result concerns a specified history, whose discovery or summation is a separate cost.

Let p be the terminal pivot and G the computed language of larger final tokens. The anchored unique-winner language is pG*, and n times its accepted count is the weighted contribution. Earlier minima are present because p contains their spellings at their proper nested boundaries. No earlier smaller symbols are possible in this grammar. For disjoint stopping classes, stop as soon as a minimum is unique or the stream is pure. For a unique terminal p with immediate predecessor p_old, an earlier unique stop has been included iff the old minimum occurs only once. Frequencies are nonincreasing, and any earlier pure stop is incompatible with forming the next group. When p begins with two or more copies of p_old, no subtraction is needed. When it begins with exactly one copy, subtract the accepted count for p (C_old)_{>p_old}^*, since every trailing group must then have exponent zero to keep the parent unique. Multiply the difference by n. Separately add a pure repetition of p, if present and of exponent at least two, weighted by |p|. Its ancestors had at least two occurrences. The single-copy pure case was already counted as unique.

**Whole-class consequence.** For each fixed d the contribution of *all* histories stopping by depth d is polynomial-time computable without bounding any pivot frequency at earlier levels. Here the initial pivots are unknown. To find them one may enumerate the length-truncated alphabets: |C0|=O(n²), and |C_{i+1}|≤(n+1)|C_i| along a fixed path. Enumerating the possible pivot paths through depth d therefore costs at most n^{O((d+1)^2)} times polynomial transfer work. This is an XP upper bound in unknown stopping depth, not an FPT or polynomial bound uniform in d. transfer.py separates the supplied-path operator from the discovery routine. Run depth twice, at the actual cut and at the all-ones threshold, to obtain the exact resolved yes mass and the entire resolved nonconstant population. Thus one can certify when the slice exhausts the population on an individual order.

At order 14, query 00000110110111, the disjoint (new unique, pure repeated) weighted contributions at depths 0,1,2 are (11410,23), (1064,63), (98,7). Add the constant zero's 1 to get 12666. At that order depth two exhausts the population. At order 20 a direct orbit audit finds genuine depth-four mass. No fixed universal stopping depth follows.

## 4. An exponential family of unknown shared histories with a one-query residual

Fix m≥1 and D≥0. Use five length-six members of C0, of form 0^{5-j}1^j0 with j=1,...,5, called A,B0,B1,X0,X1 respectively. Both forward and reversed lexical order increase in this list. For arbitrary s of D bits define a block

    H_s(b) = A B_{s[0]} ... B_{s[D-1]} X_b.

All blocks have length f=6(D+2). From q of length m form P by concatenating its H_s blocks, and E_s(q)=0 followed by P without its last bit. Consider the family of bit necklaces so encoded, over **all** 2^D choices of the shared s. The history is not provided to the counter.

**Embedding proof.** All initial heads are exactly the ends of the 10 returns, reanchored by the initial 0. The lex winner starts with A in its payload stream. At those heads block order is the order of the corresponding q bits. Therefore E_s(q) is canonical iff q is. Reversal preserves the ordering of aligned encodings at fixed s: removing their common last 0 and adding a common final 0 in the reversed comparison leaves the same answer, and the terminating X bits determine the first differing reversed block. Distinct s yield disjoint necklaces since the A-heads and their common history can be recovered. Period is f times the token period of q: any bit symmetry must preserve the A-heads. There are (D+2)m eligible binary origins and the least elementary return occurs m times. At successive eliminations, the minimum A B_{s[0]}...B_{s[i-1]} occurs m times for i=0,...,D. Indeed the next letter after each occurrence is the specified filler, and remaining single B or X letters are larger. For m≥2 none of these stages has a unique minimum or is pure before the indicated eliminations. Taking D=m gives polynomial encoding length and arbitrarily many ties at arbitrarily many levels.

**Forward reduction, valid at every ambient cut a, including nonimages.** For each possible last q bit b compare the first f bits of reverse(a[1:]+0) against reverse(H_s(b)). The latter is strictly increasing in the reversed D-bit integer key of s. Binary search therefore counts all s on the strictly smaller side in O(D+1) comparisons and detects an exact tie. For each strictly smaller s, the entire terminal-bit layer contributes. At b=0 the only canonical q is the all-zero word and has token mass 1. At b=1 the total token mass is 2^m-1. Strictly larger comparisons contribute zero. Only one pair (b,s) can tie: the reversed block uniquely identifies both. If b=0 directly test E_s(0^m). If b=1, binary search the ordinary m-bit reversed keys for the first aligned E_s(q) at least a in colex. A general strict weighted rank at that key gives the full accepted mass for s (use 2^m past the end). Subtract the accepted all-zero contribution to retain the b=1 layer. Multiply the final token count by f. The algorithm uses polynomial work in the explicit input and at most **one** ordinary oracle query. The first block comparison uses the normalized threshold; the final aligned search uses the original ambient threshold, including its strict-equality convention.

**Converse.** Given a general m-bit cut a, ask the all-histories family oracle once at E_{0^D}(a). The all-zero filler is the least possible history at a fixed terminal bit, so no other history can contribute from the same terminal-bit layer. If a ends in zero, the family mass divided by f already equals the original rank. If a ends in one, every other filler contributes its one all-zero token orbit; subtract 2^D-1 after dividing by f. This establishes exact one-query equivalence for this *restricted family*. It is neither a complexity lower bound nor a reduction from arbitrary restricted-family counting to a hypothetical unrestricted ambient colex oracle. In particular it does not prove that arbitrary families with different, nonshared continuations admit this compression.

For D=128 and m=8, an ambient threshold 6240 bits long summing over all 2^128 unknown histories left just the ordinary query 00011101. This is an illustration of a polynomial reduction, not a timing claim for general ranking.

## 5. Relational audit and remaining obstruction

At the eight-bit cut 00011101 (key 184), the original orbit 00101011 has outgoing payloads 010,10,110 and candidate keys 212,154,166. The orbit 00101101 has the same payloads in order 010,110,10 and keys 180,150,210. Both have the same least return and two yes votes. The first winning key rejects and the second accepts. In the unique-return transfer the left anchor is the same in both cases, while the ordered right product differs. Individual monomials evaluate to the correct opposite answers. The embeddings preserve those answers at common encoded cuts, even through 64 filler levels. The example rules out the multiset-plus-vote-count summary. It does not establish a universal lower bound on sufficient statistics.

A shared history can be discarded from all strict branches once its backward comparison has been accounted for. An unresolved equality branch can still carry *the entire original ranking question*. Counting that branch requires the relationship of the winner to its preceding spelling. This gives a precise way to separate compression of exponentially many histories from compression of the remaining ordering information.

**Next exact target.** Eliminate a family of distinct terminators with different pasts while summing over the possible next minimal pivot. The polynomial operator above evaluates a supplied pivot and its strict upper language. Its recursion does not yet sum those operators over an unrestricted pivot family without enumerating histories. A useful closure property would have to preserve the ordered comparison at the same anchor, and pass the one-query embedding test. The best general exact upper bound established in this archive remains the candidate 2^{O(sqrt(n))} bound.

## Reproduction

Python 3 and NumPy, with the sibling archive directories competing-origins, cut-ranking and question-sensitive-ranking available. No external service or generative assets are used.

    OPENBLAS_NUM_THREADS=1 python verify.py
    OPENBLAS_NUM_THREADS=1 python deep_check.py
    OPENBLAS_NUM_THREADS=1 python shared_check.py
    OPENBLAS_NUM_THREADS=1 python examples.py
    python transfer.py 00000110110111 2

verified.txt, deep-results.txt, shared-results.txt and examples.txt contain the outputs. The small-order checker compares disjoint stopping masses and density slices with literal rotation orbits. The deeper checker explicitly constructs truncated alphabets and performs a different left-to-right dynamic program rather than using the recursive strict-upper operator. The shared-history checker constructs bit orbits and tests cuts on and off their image, equality, neighbors, and the converse. Finite checks and internal proofs are distinct from independent verification.
