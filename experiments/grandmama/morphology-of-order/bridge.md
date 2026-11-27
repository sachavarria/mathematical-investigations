# A directed-tree evaluation for contracted stable shuffles

**Research status, 27 November 2026.** Candidate derivation and internal computations by Codex. Independent proof review and assessment of priority remain open. The Euler-tour enumeration, directed matrix-tree theorem, Möbius inversion and Schur complement used below are established mathematics.

## What can be counted after a path has been fixed?

A prescribed numerical itinerary from the least row contracts to a binary word of length N with an ordered list of intervals. Interval u has length bᵤ and contains exactly zᵤ zeros. The last remaining condition is that ρₕ LF be one cycle. LF maps the zeros in source order to targets 0 through z−1 and the ones to the remaining targets. The twist ρₕ sends 0 to h, j to j−1 for 1≤j≤h, and fixes larger j. The earlier [contraction proof](../shuffle-contraction/README.md) supplies the correspondence with the original joint itinerary and connectivity constraint.

For each source interval and each bit, the ordered list of its raw LF targets is already known from the quotas. Apply the twist to this list. Split wherever successive targets cease to be consecutive increasing integers or move to a different source interval. Each resulting piece e has a multiplicity mₑ (its length), a source interval and a destination interval. Its positions in the destination form a prescribed strip. The strips partition each destination in a known order. Retain separate types for distinct strips, including parallel edges with equal endpoints. Call the signature *aligned* when each nonempty bit list from each source interval requires just one strip.

**Claim.** For every contracted signature there is a polynomial-time integer upper bound on its one-cycle completions. It is exact for every aligned signature. In particular the number and widths of mixed intervals are unrestricted under alignment. More precisely, equality for an individual completion is controlled by relative order within the lists that split.

**Bijection for a relaxation.** At each source interval allow any arrangement of outgoing strip types having the prescribed multiplicities. Map consecutive occurrences of each type to its target strip in increasing order. This determines a permutation. A genuine binary completion is an arrangement whose subsequence at each pair (source, bit) uses the strips in their original raw LF order. Conversely this condition recovers the binary completion uniquely, because the ordered zero targets and ordered one targets determine every destination after the twist.

The one-cycle arrangements of the relaxed model are in bijection with primitive cyclic words of directed strip types, with each type e used mₑ times and successive types joined head to tail. To construct the arrangement from such a word, label each visit to a vertex by the sequence of its incoming strip types read backwards around the cycle. Sort the visits at that vertex in lexicographic order by those sequences, using the spatial strip order to compare incoming types. After equal incoming types the two pasts are at the same predecessor vertex, where the next comparison uses that vertex's strip order. Primitivity ensures distinct histories. This places incoming visits in the required target strips and preserves the order of their corresponding source visits within each strip. The outgoing labels at the sorted visits give the desired arrangement.

For the inverse, traverse the permutation and read the strip types. The destination order is fixed by the incoming type at a first disagreement, and an equal incoming type transports the source order into the destination strip. If a cyclic type word were a proper power, positions with identical infinite type pasts would visit the same vertex and form classes of size greater than one. Following one period carries such a class to itself by an increasing bijection, which fixes every position. A single cycle of full length cannot have this property. The type word is therefore primitive, and the sorting construction recovers the original arrangement. This also proves that the relaxation measures exactly which requirement disappeared: the precedence of pieces of a common bit list in the spatially sorted source rows.

## The determinant and its cost

Regard the intervals as vertices of a balanced directed multigraph. Write M=Σₑmₑ, let Dᵤ be its outdegrees, and let t be the number of edge-labelled spanning arborescences towards any one root. The row out-Laplacian cofactor counts t and gives zero if the graph is disconnected. For a single vertex its empty cofactor equals one. The number A(m) of linear strings of edge types whose wraparound is a legal circuit, allowing powers, is

    A(m) = M t ∏ᵤ (Dᵤ−1)! / ∏ₑ mₑ! .

Indeed, for a prescribed initial vertex u, distinguish all parallel copies and use the last-exit-tree enumeration of Euler tours. There are Dᵤ t ∏ᵥ(Dᵥ−1)! possibilities. Each fixed rooted string of types admits ∏ₑmₑ! assignments of copy labels, including periodic strings because the positions are fixed. Summing over u gives the formula; the arborescence counts agree across roots for a connected Eulerian graph. By unique primitive roots and divisor inversion the desired number of primitive cyclic type words is

    B(m) = (1/M) Σ_{d | gcd(mₑ)} μ(d) A(m/d).

Thus B(m) is the upper bound and the exact aligned count claimed above. With length N given explicitly, the construction has at most N strips and N vertices. Each divisor requires a polynomial-size integer determinant and factorial arithmetic on O(N log N)-bit operands. Standard exact determinant algorithms give polynomial bit complexity. This cost is per numerical layout. It does not pay for summing all layouts in a colex query. Established connections between BWT-constrained words, Eulerian graphs and spanning-tree counts include [Fici and Gabory, MFCS 2025](https://doi.org/10.4230/LIPIcs.MFCS.2025.48). See also the classical sequence-enumeration treatment by [Jackson and Goulden, 1979](https://uwaterloo.ca/math/sites/default/files/uploads/documents/gjcjm1979.pdf).

## Why the archived symbolic determinant theorem does enter here

The [archived note on cancellation](../../../symbolic-determinants/README.md) concerns matrices in which each nonzero entry is a scalar times one formal variable and each variable occurs in at most two cells. It excludes nonzero constant entries. A Laplacian diagonal generally contains a sum. The following exact bordered representation checks all of the hypotheses.

For a root-deleted directed graph let S denote the tail-indicator matrix (one column per strip type), and T the signed tail-minus-head incidence matrix with the same root row deleted. Put X=diag(xₑ) and Y=diag(yₑ) for independent variables. The weighted out-Laplacian minor is S X Tᵀ. Define the square matrix by its four blocks

    [    0        S Y ]
    [ −X Tᵀ        Y  ] .

In the bottom left each xₑ occurs in at most two cells, with opposite signs if both are present. Each yₑ occurs once on the lower diagonal and at most once above it in the same column. Loops give zero incidence. Consequently this matrix belongs to the two-occurrence class literally. Factor yₑ out of each right-hand column. The lower right block becomes the identity, and taking its Schur complement gives the determinant

    (∏ₑ yₑ) det(S X Tᵀ).

Specializing xₑ to mₑ evaluates t. This is an exact relationship between the investigations. The symbolic archive's specified-coefficient theorem applies to this polynomial before specialization. The tree polynomial already has the positive arborescence expansion, and ordinary numerical cofactor evaluation already gives t in polynomial time. The occurrence theorem supplies no evaluation of the source-row precedence constraints lost when strips split. Its three-occurrence complexity result gives no lower bound for colex ranking. The differential operator in the unrestricted itinerary expression is a different object.

## Checks and failure cases

Two intervals of length 40 with 20 zeros each, at twist zero, are aligned. The single-cycle count is 237520818846111947600 for a family with binomial(40,20)² possible fillings. The single three-cell interval with two zeros and twist one has one genuine completion and two relaxed primitive circuits. Thus even with one interval the cofactor method can strictly overcount. With one zero and no twist, the three-cell example from the earlier mean-matrix counterexample is aligned and this formula returns its correct count of one.

The reference program compared every quota signature and every twist through residual length seven with direct permutation enumeration, including disconnected graphs, loops, powers and forced bits. In a second test it extracted actual positive layouts from all one-cycle binary columns at order nine. At fixed itinerary lengths 2, 4 and 6 the relaxation was tight on 15/26, 48/50 and 56/56 positive layouts respectively. Only 7, 28 and 36 of these were aligned. These finite proportions concern layouts with at least one completion; they are not an error bound for an entire rank query. Recognition of precedence constraints that hold automatically beyond alignment remains unresolved.

Run `python strips.py` in this directory. [Reference implementation](strips.py) · [Complete output](strip-results.txt)
