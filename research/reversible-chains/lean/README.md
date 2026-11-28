# Exact messages at the even-first cut

Run `lean --wfail Observer.lean` in this directory with the pinned toolchain. The file uses the Lean distribution alone. Read the printed axiom dependencies alongside the exit status. A successful run checks the formal statements for arbitrary finite length.

For a chain of 2q cells with q ≥ 1, let e and o be the even and odd initial cells. The observed bit is the initial right edge XOR the parity of changes at the odd sites after one tick. Each such change is exactly the local Boolean rule applied to eⱼ and oⱼ₋₁, with the exterior cell fixed to zero. The recursive response sums these changes. The odd coordinates are reindexed inside the unread block, which has no effect on equivalence at the cut after all even cells.

The XOR response factors through even parity. Equal responses for every completion are equivalent to equal even parity, and either parity is attainable. For OR, any encoding from which the response can be calculated for every completion must be injective on the even block. Sending the entire even block attains that requirement. Thus the minimum numbers of possible messages are two and 2^q respectively. The Lean statements formalize factorization, attainability and injectivity. The elementary cardinality of a q-bit block and the translation from the original chain update are explained here. The development does not formalize the other chain results.

[Original comparison](../census.md)
