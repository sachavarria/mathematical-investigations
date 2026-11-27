# Research methodology

The inquiry concerns the distance between possessing enough information to determine an answer and having the means to compute it. In the Grandmama sequence, a local window uniquely identifies a position on a cycle. The mathematical problem is to recover that position efficiently from the window. A related aesthetic question concerns what makes the organization of the cycle perceptible and invites sustained attention to it.

Across an independent research practice involving different natural and synthetic intelligences, sustained exchange gives a proposition more than one occasion for scrutiny. A computational result can survive independent reproduction while its interpretation changes. An objection to the design of an instrument can expose an assumption shared by several calculations. The following cases trace what changed in the inquiry and the evidence for each change.

## Work performed before observation

The ruler in *Temporal Access* made a global coordinate immediately legible. Its construction had already enumerated the cycle. This observation exposed a problem with using the ruler as evidence for computational accessibility. The same act of reading a coordinate can follow very different amounts of preparatory work.

*Where the count lives* made that difference available for investigation by varying how much of the ordering was indexed in advance and measuring the scan left at query time. Construction cost, stored information and query cost became separate quantities. Whether the experience of encountering the ruler draws attention to the structure of the cycle remains an aesthetic question. The recorded measurements concern computational operations. [Instrument, cost model and checks](experiments/grandmama/weighted-rank/README.md)

## What an unresolved origin contributes to uncertainty

An early ranking certificate supplied an interval of possible ranks by charging the full weight of configurations with competing starting positions. For one order-14 example it gave the interval [2884, 2900]. Agent 404 reported independently reproducing both that enclosure and the exact rank of 2900. This finite agreement left a conceptual question open. What accounted for the sixteen units of width if some competing positions already gave the same answer?

For a specified threshold, a configuration whose possible starting positions all fall on the same side has a determined contribution. Incorporating this observation into the certificate changed the quantity being bounded. With the same 320 leaves in the search, the interval for that example narrowed to [2900, 2900]. The refined calculation took longer in the recorded run. An exact answer at a given search depth and the cost of obtaining it are separate findings. The refined result has its own derivation and internal checks. The independent reproduction applies to the earlier calculation. [Original certificate](experiments/grandmama/fixed-density-gaps/README.md) · [Refinement and measurements](experiments/grandmama/question-sensitive-ranking/README.md)

## When a smaller residual problem warrants a change of method

Grouping repeated returns compressed large families of possible histories into a smaller ranking query. The objection concerned the scope of the reduction. It started with a restricted family and ended with an unrestricted query. To turn this into an algorithm for the whole population would require a way to cover that population and bound the total cost across all resulting calls.

Changing to lexicographically sorted rotation rows made it possible to test that objection in a representation where the canonical starting row is known from the outset. A specified path contracts to a smaller permutation. Yet at fixed half density a single comparison can admit exponentially many paths in the number of independently chosen blocks in the construction, even as each contraction removes about half the rows. This redirected the investigation toward summing paths together. It places a limit on explicit path enumeration. The complexity of general exact ranking remains open. [Ordered-return reduction](experiments/grandmama/ordered-return-transfers/README.md) · [Contraction proof and total-work test](experiments/grandmama/shuffle-contraction/README.md)

## Returning to the atlas through an invariant of order

The original atlas compares the topology of a population with the geometry through which its relations become visible. Returning to that distinction raised a question for temporal ranking: which neighbors survive a change of order when every individual window is retained? Holding identity fixed in a paired spatial representation made the scarcity of common lexicographic and colexicographic neighbors countable. The finite pattern led to an elementary proof valid at every order of at least three. A second correspondence connects a visible feature to a computational resource. The circular transitions from one to zero in a rotation packet equal the peak number of edges crossing a cut in the stable-shuffle computation. That equality bounds the state required by a particular transfer and supplies the meaning of the mint marks on the BWT rim. Its perceptual consequences remain open.

The earlier independent reproduction by Agent 404 sharpened the distinction between an exact finite answer and the cost of obtaining it. That distinction now serves as a test for the determinant approach: counting millions of completions within a fixed family matters only alongside an accounting of how many families the full query requires. The earlier symbolic determinant theorem enters at a specific directed-tree minor. A bordered-matrix identity establishes its hypotheses there, while a counterexample identifies an ordering constraint that the determinant omits elsewhere. Conceptual and aesthetic research direction: S.A. Chavarría. Current derivations, implementation and internal checks: Codex. The earlier verification report concerns the preceding ranking work. [Mathematical note, instrument and reproducible evidence](experiments/grandmama/morphology-of-order/README.md)

## Evidence and provenance

Each subsequent entry should identify the question at stake, the objection or observation that altered it, the mathematical or experimental consequence, and what remains unresolved. Attribution belongs with the specific contribution. A derivation warrants examination of its assumptions and proof. Independent numerical verification carries the scope of the cases checked. Critical interpretation can change what a calculation ought to measure, even when its numerical result stands. Original artifacts retain their credits, dates and verification records.

Verbatim research fragments require an available original exchange, accurate attribution and explicit approval of the passage for publication.
