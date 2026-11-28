# Forms of a future

How much of a partial observation must survive until the remaining cells arrive? A reversible chain makes it possible to change the rule, the reading order or the question separately, and measure the effect of each change. [Open the browser study](https://where-the-count-lives.cosmicmami.chatgpt.site/chains/index.html) · [Earlier pilot and reassessment](https://github.com/sachavarria/mathematical-investigations/tree/9c492d5fa2c5c5ee5f8c6ae3275c80c9f82ad81a)

Take a finite binary chain with two fixed zero cells to its left. At each tick, each site flips precisely when a specified Boolean function of its two left neighbors returns one. All sites update simultaneously. Each of the sixteen possible functions yields a bijection because the initial bits can be recovered in order from the updated bits. The observer reads each initial bit once in a prescribed order and must answer a specified question exactly. Two partial readings may share memory precisely when every completion gives them the same answer. Counting distinct response functions gives the minimum number of states at that cut. Storage for transitions and the cost of discovering equivalences are separate resources.

## The address inside the chain

For rule 4, the two neighbors trigger a flip when the nearer one is occupied and the farther one is empty. On an odd chain of length 2r+1 at time 2ᵏ−1 ≥ r, successive parities of the even cells form a table of r+1 independent bits. The uninterrupted run of occupied odd cells leading backward from the last site selects the table entry. This describes the future endpoint for every initial state. In ordinary spatial order a running bit suffices at every cut. Seeing all even cells first requires r+1 bits at the group boundary. Seeing all odd cells first requires only enough bits to name one of r+1 entries there. An unknown address makes every table entry potentially relevant. Once the address is known they can be discarded as they arrive. [Derivation and arbitrary-cut algorithm](structure.md)

The eight affine rules have affine scalar predictions at every time and need at most one bit of data memory for any order. For two nonlinear rules, masks 2 and 4, an arbitrary-cut state count is computable in polynomial time for any specified future cell, even for a time given in binary. The other six nonlinear rules remain outside this all-time classification. A second comparison holds wiring, essential support, output balance and reading order fixed: XOR and OR require respectively one and q memory bits at the half-chain cut of a matched two-time question on 2q cells. [Proof and all sixteen rules](census.md)

## Evidence and reproduction

- [Quadratic calculation](quadratic.md) gives a polynomial algorithm for the exact memory at any cut for a parity of updated sites after one tick, for all sixteen rules. [Delayed questions](guards.md) ask how much information must survive if the choice of observation time comes later.
- [Scope and proof review](review.md) separates correctness from exposition and finite checks. [Source register](sources.md) gives the published communication-complexity framework, related elementary automata and antecedents for evolution on linear domains. The observation-specific formulas are candidate mathematical contributions pending independent verification and confirmation of publication priority.
- Run the following commands in this directory with Python 3 and Node.js. The four CSV files give midpoint and peak counts from complete profiles. Committed result files record each check. The browser study uses self-contained HTML and embedded Space Grotesk. [Visual construction and viewport checks](visual.md)

```sh
python3 census.py
python3 quadratic.py
python3 check_ladder.py
python3 arbitrary_cut.py
python3 check_guards.py
node check_visual.cjs
```

## Where the comparison should go

The chain supplies a controlled instance of a general distinction between receiving an address before or after its possible answers. A next test would use a branching network with marked terminals. The same path question could be asked with route decisions or terminal marks arriving first. Charge explicitly for any buffering that changes that order. Compare the prediction from address order with the prediction from the width of the network cut. If both merely recover standard lookup complexity, a new chain census would add little. Exact Grandmama decoding remains a benchmark for a different resource, the cost of computing a rank from a complete local observation.

The visual study compares one evolving configuration with the full family of possible answers at a cut. Whether a viewer can recognize a change of computational requirement before seeing its count is an open perceptual question. Mathematical equality of response functions gives an exact basis for the comparison. It does not establish a human or synthetic observer's experience.

27 November 2026. Conceptual and aesthetic research direction, S.A. Chavarría. Current derivations, implementation, design realization and internal computational and proof review, Codex. Reproducible finite calculations used CPU execution with Python and Node.js and browser viewport emulation. No external proof review of this installment has been recorded.
