# A nonlinear rule with an exact prediction for every observation cut

Candidate derivation and internal checks by Codex. Sites run from 0 to m−1. The rule uses a first left neighbor a and a second left neighbor b. The mask is read at position 2a+b with bit zero least significant. Boundaries are zero. Time, observation site and order are fixed before the initial cells are read. A state below means an equivalence class of partial observations with identical future answers for every legal completion. This finite-layer measure allows arbitrary preprocessing and fixed position-dependent transitions. A bit count for such a state excludes the specification of the rule, schedule and clock.

## Why the two-state pilot persists

Consider mask 4. Its local update is xᵢ′ = xᵢ + xᵢ₋₁(1+xᵢ₋₂), with addition modulo two. A cell can flip precisely when its two predecessors read 01 from left to right. For all chain lengths, all times, and every specified output cell, a left-to-right observer can accumulate the exact answer using one bit of data memory. Reading from the right uses at most two bits. At a general cut there is a polynomial-time algorithm to compute the exact number of necessary states, even when this number is exponential. Mask 2 has the same conclusions. Flipping every input and output bit conjugates its dynamics to mask 4 **with left boundary one**.

**Prior mathematics.** On the full line mask 4 is centered elementary CA 166 followed by a one-site shift. The two operations commute. Inokuchi, Honda, Lee, Sato, Mizoguchi and Kawahara give the alternating product for powers of two in Lemma 9.1. The same dyadic identity appears in *Propositional Logic and Cellular Automata*, Lemma 6.6. Dürr, Rapaport and Theyssier already study cellular automata by communication complexity; their representative 154, related by color conjugacy, appears in their bounded experimental class. The precise boundary, arbitrary bipartitions of input sites, and exact response counts matter to the claims below. Priority of the arbitrary-time rewriting or observer results remains unconfirmed. [Inokuchi et al.](https://arxiv.org/pdf/nlin/0504058) · [Lemma 6.6](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1894-03.pdf) · [Communication complexity of CA](https://arxiv.org/abs/cs/0210008)

### The calculation

The choice of features comes from the dyadic formula: an alternating string of occupied sites carries a bit from its left end. Fix output site i, let F₀=xᵢ and for j≥1 put

    aⱼ = xᵢ₋₂ⱼ₊₁,    eⱼ = xᵢ₋₂ⱼ,    Aⱼ = a₁⋯aⱼ,    Fⱼ = Aⱼ(1+eⱼ).

Use the constant boundary for all negative indices. Either all-zero or all-one negative sites stay unchanged under mask 4, so this extension obeys the same local equations. Denote by T* the operation that evaluates a feature one time step later as a function of the current state. Then

    T*Fⱼ = Fⱼ + Fⱼ₊₁    for every j≥0.

**Proof.** The j=0 equation is the rule. For j≥1 the gate updates are aₛ′=aₛ+eₛ(1+aₛ₊₁), and eⱼ′=eⱼ+aⱼ₊₁(1+eⱼ₊₁). If aⱼ₊₁=1, the last gate aⱼ remains fixed. Working back through the gates, the last zero among a₁,...,aⱼ remains zero because its successor is one. If every gate is one, all remain one. Thus Aⱼ′=Aⱼ, and substituting eⱼ′ gives the displayed recurrence. If aⱼ₊₁=0, then eⱼ′=eⱼ and Fⱼ₊₁=0. For eⱼ=1 both Fⱼ and its update vanish. For eⱼ=0 the last gate aⱼ remains fixed. If that gate is zero both products vanish; otherwise the same last-zero argument proves equality of products. This exhausts the cases. ▪

Iteration and the binomial theorem now give the answer at time t:

    yᵢ(t) = F₀ + Σ_{j≥1, j a binary submask of t} Fⱼ.

Here “submask” means that every set bit of j is set in t. The coefficient follows by factoring (1+z)^t over the two-element field into the factors (1+z^(2^k)) selected by the bits of t. With boundary zero every Fⱼ vanishes for j>floor((i+1)/2); with boundary one it vanishes for j>floor(i/2). The sum can be evaluated for a time given in binary. The full zero-boundary mask-4 chain has order the least power of two exceeding floor(m/2): at that power only F₀ remains at every site. When the power is larger than one, at half the power the last site's surviving Fⱼ can be set to one by setting its gates to one and its left-end bit to zero, including when that bit is the zero boundary. Hence the half-power is not identity and the asserted order follows.

In a scan from left to right, take the indices j in decreasing order. Maintain one initially zero bit. At eⱼ, add 1+eⱼ if j is selected; at aⱼ, multiply the running bit by aⱼ. Add xᵢ at the end. Expansion gives exactly the formula above, including the possible fixed left-end contribution. In a right-to-left scan, maintain a running product of the gates and the parity accumulated so far. This proves the data-memory bounds, allowing bit tests on the fixed time and the known site index. The output bit itself forces two final states for an unconstrained input.

## Reordering the same observation

Take i=2r, with 2r+1 input cells. Write J for the positive submasks of t that are at most r. The even-indexed cells carry xᵢ and the freely chosen coefficients dⱼ=1+eⱼ. The odd cells are gates a₁,...,aᵣ. They select an initial segment of J through Aⱼ: once a gate is zero, no terms to its left survive.

If every even cell is presented first, the residual functions on the odd cells number **2^(|J|+1)**. Each choice of the constant and active coefficients is visible. Indeed, setting exactly the first h gates to one tests the parity of coefficients up through h together with the constant. Successive parities recover each coefficient. If all odd cells are presented first, there are **|J|+1** residual functions on the even cells: the surviving initial segment of J determines the answer function, and distinct segments differ on some freely chosen coefficient. At t=2^k−1≥r these counts are 2^(r+1) and r+1. In the natural scan a single bit still suffices. This supplies an asymptotic separation within one nonlinear rule for the same site, time, output balance and underlying population. It measures resources in a deterministic single pass. A physical acquisition process could incur costs to rearrange the cells.

A change of data coordinates makes the effect recognizable. Replace the constant and the active data coefficients by their successive prefix parities. This is invertible on those coordinates. The gates select one of these table entries by the position of their first zero. Retaining a table before the address arrives is the established one-way Index problem. The rule supplies this lookup structure internally. A change of coordinates mixing data from opposite sides of a cut has its own access cost. [One-way communication complexity](https://jeffe.cs.illinois.edu/teaching/497/09-communication.pdf)

At m=9, i=8 and t=7, natural order peaks at two states. The even-first order peaks at 32 and the odd-first order at five. With an even-site target and all coefficients active, every gate and every data bit influences the output: a single coefficient can test the relevant gate product. The distinction therefore survives a check on effective input support, not only formal dependencies.

## Predicting the exact state count at an arbitrary cut

The procedure below works for every site, including the odd-site boundary case. Fix which initial coordinates have already arrived. Coordinates to the right of the output may be discarded. Start with mask 4; for mask 2 use complemented inputs, the fixed-one ghost, and a final complement. Relabeling bits leaves equivalence-class counts unchanged.

Separate the known gates from the unread gates. Let ℓ be the index of the first zero **among known gates**, and h the index of the first zero **among unread gates**, with a common sentinel r+1 when all gates of the relevant group are one. Every index in its respective group, as well as its sentinel, is realizable. For a fixed known-gate assignment the answer is

    xᵢ + Σ_{j in J, j<min(ℓ,h)} dⱼ.

This formula identifies the entire function on the unread sites by listing, for each possible h, an affine function of the unread data bits. The coefficient of an unread active dⱼ equals the step vector 1[h>j] if j<ℓ, and otherwise vanishes. Distinct sets of such visible unread data give distinct linear parts: at h=r+1 each surviving unread variable has coefficient one. The coefficient on an unread xᵢ never changes. These fixed linear parts separate the residual functions into disjoint groups.

For a fixed ℓ, a **known** active free data bit with j<ℓ can add its own step vector to the constants; a known xᵢ adds the all-ones vector. Step vectors with the same first nonzero position coincide. The distinct vectors are independent, as taking consecutive differences in h recovers their coefficients. They thus span a binary subspace whose dimension is just the number of distinct first positions represented. As ℓ increases these spaces nest. At even i there are no fixed data bits; within each group of equal linear parts, all smaller spaces lie in the largest one. Sum 2^dimension for the largest space of each group. This counts future answer functions exactly, including states differing by a constant.

**Boundary case.** With zero ghosts and odd i the last possible dᵣ can be the fixed value one. If r∈J it adds a single forced step at ℓ=r+1. Within that linear-part group the largest space is then translated by this vector. An earlier space is contained in it if the translating vector belongs to the largest free space, and is disjoint otherwise. Counting that last coset, plus the largest earlier space only in the disjoint case, gives the exact union. If r is inactive or the ghost is one, no adjustment is needed. These statements also cover J empty and one-cell inputs.

There are at most r+1 candidates for ℓ and at most r+1 choices of h; signatures and vectors can be stored as small sets of integers. The resulting work is polynomial in m and the binary length of t at each cut. It computes the exact number of distinguishable states without iterating through the initial configurations or materializing the observer. At m=129, t=63 the prediction for either mask at the rightmost cell is two classes at the natural midpoint, 2^64 classes after the even cells, and 64 classes after the odd cells. The middle figure describes 64 necessary retained bits at that cut in the stated model. It does not require an exponentially long numerical computation to derive the number.

## What changes when the time is chosen later?

For target 2r and an allowed family of times U, suppose the initial state must be discarded before a single time in U is requested. Form the binary matrix B with rows indexed by U and columns 0 through r, with B[t,j] the parity of the binomial coefficient. The vector of possible answers equals B·(F₀,...,Fᵣ). Setting all gates to one makes these r+1 features freely assignable via distinct even cells. Thus there are exactly 2^rank(B) different answer vectors, and precisely rank(B) retained bits are necessary and sufficient in a fixed-length summary with unrestricted preprocessing. The set U={0,...,r} requires r+1 bits because the corresponding square matrix is triangular with diagonal one. This is an application of linear algebra after a nonlinear change of features.

## Audit and scope

The scalar audit compares the direct time evolution of every state and every site at lengths 1 through 11, for two complete periods, with the proposed left-to-right evaluator. It also tests exact periods, three order profiles, delayed-query ranks, and seeded long-time examples. The separate arbitrary-cut audit compares the symbolic class count with literal enumerations over every observed subset at widths 1 through 8 for both masks. These finite checks test the implementation and boundary cases. The feature recurrence and residual-space argument establish the unbounded statements. [Binary time evaluator and audit](check_ladder.py) · [Results](ladder-results.txt) · [Arbitrary-cut algorithm and oracle](arbitrary_cut.py) · [Results](arbitrary-results.txt)

The argument uses one special feature of the truth table: an intact chain of gates suppresses their own updates. It establishes no comparable all-time compact summary for the product rule g=ab. A small observer for one output does not imply a small summary for every question an investigation may later formulate.
