# Six questions on one reversible family

Candidate comparisons and finite computations by Codex, 27 November 2026. These controls use binary open chains of even length n. Coordinate zero is at the left and is stored as the low integer bit. The two exterior bits are fixed at zero at each step. The update

    xᵢ' = xᵢ XOR g(xᵢ₋₁, xᵢ₋₂)

uses the old state at every site. Mask k gives g(a,b) by reading bit 2a+b of k. Thus mask 8 is AND, mask 4 is a AND (NOT b), mask 6 is XOR, and mask 14 is OR. Every update is bijective because successive old bits can be recovered from the left.

## Same wiring, same support, different scaling

Consider a chain of length 2q with q≥1. Read all even cells before the odd cells. The question observes the parity of the sites of odd index that changed in one update, together with the initial bit at the right edge. Its one-bit answer is the XOR of those quantities. The edge term includes the final unpaired input in the question and makes the answer balanced. This is a two-time observable and does not measure the pilot’s endpoint alone.

**Claim.** For local rule XOR the minimum number of deterministic midpoint states is two. For OR it is 2^q. Both observations depend essentially on all 2q inputs, use the same local dependency graph and take each answer on exactly half the initial states. Both admit at most four states at every cut if the coordinates are read in spatial order.

**Proof.** Write eⱼ=x₂ⱼ, oⱼ=x₂ⱼ₊₁ and o₋₁=0. All sums below are modulo two. The odd-site change at j is g(eⱼ,oⱼ₋₁). For XOR the answer is the parity of the entire input. At the midpoint the parity of the even sites is both necessary and sufficient. For OR the identity a OR b = a+b+ab gives

    Q = o_{q−1} + Σⱼ eⱼ + Σ_{j=0}^{q−2} (1+e_{j+1}) oⱼ.

The slopes on the unseen bits determine e₁,…,e_{q−1}. Evaluation at the all-zero suffix then determines e₀. Thus distinct even-site assignments yield distinct response functions, and there are precisely 2^q possible assignments. The row criterion gives necessity; storing the even assignment gives sufficiency. The last odd bit always flips either answer. In the OR rule, setting all odd bits to zero makes flipping any eⱼ change Q, while setting all even bits to zero makes flipping any odd bit change Q. For ordinary spatial order keep the accumulated parity and the most recent odd bit until the next even bit arrives; then both inputs for the next g are available. Include the last odd bit when finishing. Four states suffice, with the read position known. ▪

This separation specializes the standard deterministic one-way inner-product mechanism to a controlled comparison of local dynamics. The result does not establish an asymptotic endpoint-prediction separation, nor does it claim novelty for inner product or its communication bound. The distinction between states and bits matters: 2^q states require q bits, and two states require one.

**All sixteen rules.** Write g=c+Aa+Bb+Cab. Each even assignment selects a constant term cq+AΣeⱼ in the preceding response and selects the coefficients B+Ce_{j+1} on o₀,…,o_{q−2}. The coefficient on o_{q−1} is one. For the alternative question giving just parity of the updated odd sites, a fixed linear function of the odd inputs is added. Both questions therefore have exactly

    2^{A+(q−1)C}

distinct midpoint states. When C=0 only the constant can vary. When C=1 the q−1 variable slopes are independent, and e₀ realizes both constants for any fixed slopes exactly when A=1. This includes q=1. The forward four-state upper bound for updated odd parity accumulates each odd cell’s own bit as it arrives in addition to the g contributions. Computational checks for both observables and every mask are included in the census.

## Design of the finite scan

For n=6,8,10,12, every initial state was evolved for t=0,…,2n under each mask. The six questions are endpoint at t; XOR of rightmost two cells at t; their ordered two-bit response (penultimate then last); the ordered pair of endpoint bits at times zero and t; parity of the odd sites at t; and the edge bit at time zero XOR the parity of all odd-site changes between zero and t. The three orders are increasing index, decreasing index and evens then odds, increasing within each parity. Every read position was tested. The 1,216 mask/time/size rows supply 21,888 complete cut profiles.

Let f(p,s) be the answer on a chosen prefix p and suffix s. A reader can share a state between two prefixes exactly when every suffix gives the same output in both cases. At the last cut, identify the answer values directly; one step earlier a prefix’s signature is the ordered pair of signatures obtained by appending zero and one. Inductively these signatures identify exactly the distinct suffix-response functions. This computation includes the terminal output states. It permits nonuniform preprocessing and does not account for its cost. These are minimal deterministic states in a specified read order, not general runtime lower bounds. For comparison see [Erickson’s one-way communication notes](https://jeffe.cs.illinois.edu/teaching/497/09-communication.pdf).

Run `python census.py` in this directory. The four CSV files each contain the binary endpoint support mask and, for each named question and read order, the entry midpoint/maximum. Maximum ranges over all cuts at this rule, time, size, question and order. Bit zero of the support mask denotes the leftmost cell and is printed at the right end of the string. Full profiles are returned by the widths function if finer inspection is wanted. Every next-state map was checked against a scalar site-by-site implementation and verified bijective. For n≤8, independent direct string grouping checked every cut of every reported profile. The n=8 endpoint pilot’s counts of two and nine were recovered. The proof-derived midpoint predictions above are checked against the distinct-row enumeration at t=1 for all sizes. The two evaluations sharing generated output tables do not constitute independent external proof review.

## What varies in the measured range

Peak states for the single final cell at n=12, taking the maximum across all cuts and t=0,…,24:

| Mask | Forward | Reverse | Evens first |
|---:|---:|---:|---:|
| 0 | 2 | 2 | 2 |
| 1 | 95 | 254 | 155 |
| 2 | 2 | 4 | 6 |
| 3 | 2 | 2 | 2 |
| 4 | 2 | 4 | 7 |
| 5 | 2 | 2 | 2 |
| 6 | 2 | 2 | 2 |
| 7 | 125 | 256 | 171 |
| 8 | 55 | 184 | 98 |
| 9 | 2 | 2 | 2 |
| 10 | 2 | 2 | 2 |
| 11 | 123 | 256 | 176 |
| 12 | 2 | 2 | 2 |
| 13 | 127 | 256 | 168 |
| 14 | 66 | 220 | 116 |
| 15 | 2 | 2 | 2 |

For the pilot rules 4 and 8, at t=7 and n=6,8,10,12, every initial bit affects the endpoint for both rules. The forward midpoint states for mask 4 are 2,2,2,2; for mask 8 they are 3,9,16,26. This fixed-time sequence cannot continue to grow indefinitely: once the incoming prefix lies entirely outside the endpoint’s finite backward cone, it has just one response. A scaling conjecture must specify how time and observation site change with length.

At n=12 and t=11, mask 8's endpoint peak is 51 in spatial order and 170 in reverse order; jointly observing the last two cells gives 85 and 326. Thus the choice of read order and the question both matter within one fixed dynamics. The exact one-step parity separation explains one family of experiments; longer-time endpoint results require a separate argument.
