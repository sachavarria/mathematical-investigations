# Counting temporal records with a fixed number of missing windows

Research note, 25 November 2026. Independently derived result. Publication priority unconfirmed.

## Question and conventions

Fix a labelled alphabet of size q ≥ 2. A cyclic word of length L is balanced at every scale if each word of length m occurs either floor(L/q^m) or ceil(L/q^m) times in the circular record, for every 1 ≤ m ≤ L. This is precisely the Nellore–Ward definition. Identify rotations only. Write B(q,n,d) for the count at L=q^n−d and D(q,n)=(q!)^(q^(n−1))/q^n for the classical full-length count. The deficit d is positive.

The information experiment has a public deterministic cycle and an unknown uniform phase. A window identifies a set of phases, its size equal to the window multiplicity. Equalizing these sizes to the two nearest integers attains the smallest possible worst-case ambiguity simultaneously at every window length. The mathematical objective here is to count systems with this property. At length n the phase is unique. No assumption of computational hardness or secure encryption enters.

For a concrete security quantity, suppose the phase itself is the secret and an observer gets one noiseless contiguous m-window. Write L=a q^m+b, with 0≤b<q^m. Exactly b windows have a+1 preimages and the others have a. The observer's optimal single-guess success probability is min(q^m,L)/L: each distinct observation contributes exactly 1/L. The remaining Shannon entropy in bits is [b(a+1)log₂(a+1)+(q^m−b)a log₂(a)]/L, with 0 log₂0=0. Thus the observer's information is known exactly, even though the number of distinct public systems producing this leakage profile is a separate enumerative question.

## Problem selection and novelty audit

The de Bruijn Sequence and Universal Cycle Constructions research-problems catalogue explicitly marks some neighbouring questions solved and lists the following without that designation. The catalogue provides evidence of open status. Search cannot rule out an unindexed or newly published solution. Complexity targets below make the decoding questions precise: polynomial time and space in n, for a fixed binary alphabet, with a canonical origin and without an exponentially precomputed table.

| Candidate | Existing work and remaining target | Session tractability and verification | Significance and broader principle |
|---|---|---|---|
| Count all-scale balanced necklaces at lengths q^n−d for fixed deficit | Nellore–Ward construct them. Catalogue problem 8 asks their number. Binary d=2 has prior work. | High for a restricted family. Compare exhaustive necklaces, full graph cofactors and a smaller formula. | Counts optimally balanced temporal records. A local defect might encode the global object. |
| Rank the binary Grandmama (PCR2) sequence from an n-bit window | Catalogue 10 lists PCR2 separately from solved PCR3. Efficient forward generation is known. | Medium. Test ranks against a canonical full cycle at small n. | Distinguishes identifiability of a phase from efficient inference of that phase. |
| Unrank the binary PCR4 sequence from a phase index | Catalogue 10. Concatenation construction is marked solved under problem 4. Efficient random access remains listed. | Medium. Try subtree sizes of the necklace ordering, verify every index against generation. | Would connect local generation with global access. |
| Rank the binary prefer-same cycle | Catalogue 10; Sala, Sawada and Alhakim give an efficient successor rule. | Medium–low. Run-length classes suggest a representation. Test all windows against direct traversal. | Can temporal persistence be exploited for synchronization? |
| Find a simple local successor rule for the greedy binary XNOR cycle | Catalogue 6; Wang, Wong and Zhang give the greedy construction. Seek polynomial work and space per successor without storing visited windows. | Medium for conjecture discovery, lower for proof. Compare complete cycles and prove the last-edge tree condition. | Would turn apparent historical dependence into a bounded-memory rule. |
| Ternary minimum discrepancy at order n ≥ 3 | Catalogue 15 states the broader conjecture; Álvarez et al. settled binary minimum discrepancy. Ask whether ternary minimum equals n for all n ≥ 3 under their discrepancy definition. | Lower. Verify proposed constructions on all cyclic intervals, then prove their discrepancy bounds. | Controls imbalance on time intervals rather than across window types. |

I selected enumeration because three independent representations are available and because it can give a theorem for unbounded n. I excluded binary minimum discrepancy and the binary two-deletion identity as novelty targets. Searches covered balanced cut-down sequences, arbitrary-length analogs, cycle-length enumeration, near-Hamiltonian de Bruijn cycles, binary shift-register enumeration, and generalized de Bruijn words. The latter phrase covers several inequivalent definitions. The finite kernel below extends the same matrix-tree and exact-mixing method explicitly used for binary d=2 in the MathOverflow answer. Its mathematical contribution lies in the all-scale classification and the general fixed-deficit law.

## Theorem 1. Exact fixed-deficit kernel and limiting law

Fix q,d, put r=max(1,ceil(log_q d)), k=n−1, and assume k ≥ r. Form a finite set of pairs (U,s) as follows.

1. U is a set of d distinct r-letter words. For every m<r, m≥1, the counts of their length-m prefixes must be floor(d/q^m) or ceil(d/q^m), including zero counts.
2. s is a permutation of U. The last r−1 letters of u must equal the first r−1 of s(u). At r=1 this imposes no restriction.

Let S be the row permutation matrix with entry 1 at (u,s(u)). Read the first letters of u,s(u),s²(u),… to obtain a periodic stream. Let v_u be its first k letters. They begin with u, so the v_u are distinct. Define a d by d rational matrix

    G[u,w] = sum over 0 ≤ t < k of q^(−t−1)
             times [the suffix of v_u of length k−t equals the prefix of v_w of that length].

Then the exact answer is

    B(q,n,d) / D(q,n) = (q−1)^(−d) sum_(U,s) det(I − (I−S)G).       (1)

For every fixed q,d the ratio converges to the rational constant

    sum_(U,s) product over cycles C of s of 1/(q^|C|−1).             (2)

More strongly, on each residue class of k modulo lcm(1,...,d), the ratio in (1) is a polynomial in q^(−k) of degree at most d−1 with rational coefficients, throughout k≥r. In an individual summand the degree is at most d minus the number of cycles of s. Thus the fixed-deficit law includes both the limiting constant and the form of all finite-window corrections.

### Proof

Use the directed graph with vertices all k-letter words and edges all n-letter words. Each edge shifts one place and appends a symbol. A cyclic record with distinct n-windows traverses each used edge once. Its omitted edges therefore have equal in- and out-degrees at every vertex. For m≤n, shorter-window counts in the record are obtained from the full counts q^(n−m) by subtracting the counts of omitted edge prefixes. Thus their balance is equivalent to prefix balance in the deficit (subtract the two rounding endpoints from the integer full count). At scale r, balance forces distinct omitted r-prefixes since d≤q^r, including equality when d=q^r. At lengths from r through n these distinct prefixes guarantee all omitted prefix counts are zero or one. At lengths above n, uniqueness in the surviving record follows from uniqueness of n-windows. This accounts for every scale.

The d omitted k-prefix vertices are consequently distinct. Conservation forces the suffix vertices to be the same set, also without repetitions. Successor along an omitted edge is therefore a permutation. Reading first letters along its orbits recovers the entire omitted n-word at each vertex, because successive vertices overlap in k−1 letters. Project to the first r letters to obtain (U,s). Conversely any admissible (U,s) reconstructs precisely these omitted edges by reading n letters from its streams. This gives a bijection at the level of possible balanced omitted edge sets. A deletion leaving no Euler tour will receive zero weight automatically.

Let M=q^k, P be the full row-stochastic shift matrix, A=q(I−P) the out-Laplacian and J the matrix whose entries are 1/M. Degrees are q everywhere. The directed matrix-tree theorem gives the number of trees directed to any fixed root as det(A+J)/M: balance gives equal cofactors and J acts as identity on constants. The same formula holds for the deleted balanced graph, including zero for disconnection. Each selected vertex loses one outgoing edge and retains positive degree. The BEST theorem counts Euler tours with specified first edge as a rooted-tree count times the product of (outdegree−1)! over vertices. Fixing any one used edge counts each cyclic tour once. All edges have distinct labels. Thus the factorial-product ratio after deletion is (q−1)^(−d). In the full graph P^k=J because k freshly sampled letters overwrite the state. This also proves the quoted full count: on the sum-zero space P is nilpotent, so det(A+J)=q^(M−1), and BEST gives q^(M−1)((q−1)!)^M/M=D(q,n).

Let E embed the d defect vertices as coordinate columns. The deleted Laplacian is A−E(I−S)Eᵀ. The determinant lemma gives tree-count ratio det(I−(I−S)Eᵀ(A+J)^(−1)E). On constants the inverse is identity. On sum-zero vectors it is q^(−1) times the sum of P^t for 0≤t<k, by the finite geometric series. The difference between this inverse and that finite sum divided by q is a scalar multiple of J, which disappears after multiplication by I−S in the compressed expression. For t<k, a transition from v_u to v_w has probability q^(−t) exactly when the stated overlap holds and zero otherwise. This proves (1).

For overlaps of length at least r, equality holds exactly for w=s^t(u), since the r-prefixes are distinct. If one replaced all overlaps by this rule and extended the sum to infinity, one would obtain G∞=(qI−S)^(−1). For a shorter overlap of length h, 1≤h<r, the exact test is equality of the first h letters of the streams starting at s^(k−h)(u) and w. Its correction to G∞ has prefactor q^(−k) q^(h−1). The omitted infinite tail is q^(−k) S^k G∞. Consequently G=G∞+q^(−k)H, where H is rational and depends only on k modulo the order of s (and on the fixed pair). Each permutation order divides lcm(1,...,d). Multilinearity bounds the polynomial degree by the rank of (I−S)H, hence by d minus the number of cycles. Taking the constant term gives det((q−1)(qI−S)^(−1)); det(qI−S) is the product of q^|C|−1 by permutation cycles. The BEST factor cancels the numerator, proving (2) and the polynomial law. ∎

## Corollary. A closed limit for one to q missing windows

For 1≤d≤q, r=1 and every permutation of every d-symbol subset qualifies. The finite formula uses G=sum_(0≤t<k) S^t/q^(t+1). In particular, with (q)_d=q(q−1)…(q−d+1),

    lim B(q,n,d)/D(q,n) = (q)_d q^(d(d−1)/2) / product_(i=1 to d)(q^i−1).

Indeed the permutation cycle index makes (2) equal to (q)_d times the coefficient of z^d in exp(sum_(j≥1) z^j/[j(q^j−1)]). Expanding 1/(q^j−1) geometrically turns this series into F(z)=product_(h≥1)(1−z/q^h)^(−1). The identity (1−z/q)F(z)=F(z/q) gives its coefficients recursively and yields the displayed expression. For example q=d=3 gives 81/208. The finite count for q=n=d=3 is 148608, against 373248 full-length cycles. Their ratio is 43/108. 

## Verification, failed extensions and scope

Run `python3 verify.py` beside this note, using the standard library. There are two independent finite checks. One enumerates raw words, factors out rotations and tests every window count including unobserved words. The other enumerates missing edge sets and evaluates the full graph cofactor using exact rational elimination. Only the latter check shares the BEST theorem with the proof. All 21 cases with 1≤d≤q in the script pass the full cofactor check, including nine checked by exhaustive words. Five more binary cases with d>q pass the general overlap kernel against exhaustive words. Selected results:

| q | n | counts in increasing deficit order |
|---|---|---|
| 2 | 3 | 4, 3, 2, 1 for d=1,…,4 |
| 2 | 4 | 32, 20, 12, 9, 6 for d=1,…,5 |
| 3 | 2 | 36, 24, 8 |
| 3 | 3 | 559872, 435456, 148608 |
| 4 | 2 | 27648, 20736, 10368, 2592 |

The naïve claim that missing windows always permute distinct *letters* fails already for the binary necklace 00011. At n=3 its missing words are 010, 101, 111. Two start in 1. Passing to distinct two-letter contexts repairs exactly this failure. Another tempting inference is that every admissible permutation gives a positive number of records. In the binary graph at n=2, deleting the alternating two-cycle leaves two disconnected loops, and the corresponding determinant vanishes. The uniform prior on phase matters to the entropy interpretation. The enumeration itself has no probability assumption.

The binary d=2 sequence 1,3,20 at n=2,3,4 agrees with the corrected pre-existing count and does not establish novelty. All arithmetic in the script is exact. Neither Lean nor Lake was available on the executable path. The general theorem has a written proof and finite executable tests, not a proof-assistant certificate. There is no asserted efficient method for recovering the phase given a succinctly specified cycle, or lower bound for doing so. For large d even enumerating (U,s) is expensive. The theorem controls dependence on n at fixed deficit.

## Source register and priority assessment

1. A. Nellore and R. Ward, *Arbitrary-Length Analogs to de Bruijn Sequences*, CPM 2022. Definition, existence, construction, and small counting data. The authors also distribute an enumeration script. [Paper](https://doi.org/10.4230/LIPIcs.CPM.2022.9) · [Code](https://github.com/nelloreward/pkl)
2. *De Bruijn Sequences and Universal Cycle Constructions*, research-problems catalogue, especially items 6, 8, 10 and 15. Distinguishes open questions from several explicitly marked solved. [Catalogue](https://debruijnsequence.org/db/db/db/problems)
3. Fredricksen, *A survey of full length nonlinear shift register cycle algorithms*, SIAM Review 24 (1982), §2c, and Timothy Chow's question with jvvk's subsequent solution. The posted answer corrects the quoted binary two-defect formula and explicitly uses the determinant lemma and exact mixing. This is the closest located proof. [Question and answer](https://mathoverflow.net/questions/227666/cycles-of-length-2n-2-in-the-de-bruijn-graph)
4. *The enumeration of shift register sequences*, Journal of Combinatorial Theory A (1983). Studies distinct-window binary cycles by length; this condition alone generally permits uneven shorter-window counts. [Paper](https://www.sciencedirect.com/science/article/pii/0097316583900043)
5. Álvarez, Becher, Mereb, Pajor and Soto, *De Bruijn Sequences with Minimum Discrepancy*. Settles the binary minimum-discrepancy question, an important exclusion when selecting candidates. [Paper](https://arxiv.org/abs/2407.17367)
6. *Generalized De Bruijn Words, Invertible Necklaces, and the Burrows–Wheeler Transform*, MFCS 2025. Its permutation blocks describe a different class. A shared name or the appearance of permutations is insufficient to transfer its counting theorem. [Paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol345-mfcs2025/html/LIPIcs.MFCS.2025.48/LIPIcs.MFCS.2025.48.html)
7. *Robust Positioning Patterns with Low Redundancy*. A competing recoverability direction imposing robustness to corrupted observations. Its objectives differ from exact counts of noiseless all-scale balanced records. [Paper](https://doi.org/10.1137/19M1253472)

I found no statement of the general fixed-deficit limiting constant or residue-class polynomial law in the material located. The determinant tools are classical; absence of a search hit cannot establish priority. In particular, checking older shift-register literature for an equivalent generating function remains worthwhile. This is a finite-regime answer to an explicit enumerative problem and a link between short-memory overlap and temporal ambiguity. It establishes no one-way function or computational separation.

## Next research question

For fixed q and increasing d, how does the limiting constant (2) grow or decay? In particular, at d=q^r all r-letter contexts are used, so admissible permutations are precisely shift-compatible cycle covers on those contexts. Can their weighted cycle index, with weight 1/(q^j−1) per j-cycle, be evaluated recursively in r? This is a precise bridge from the fixed-deficit theorem to a regime in which the missing information itself grows. The first target is a recursion or asymptotic bound for binary d=2^r.
