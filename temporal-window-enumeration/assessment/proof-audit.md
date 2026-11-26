# Proof audit for independent review

Status: candidate original mathematical contribution pending independent verification and confirmation of publication priority. This is an internal audit of the stated proof. The original research note contains the complete argument.

| Hinge in the argument | Check and outstanding review target |
|---|---|
| Prefix balance survives complementation | Subtract floor and ceiling from the integer full count at each scale up to n. At the distinguishing scale r the omitted prefixes are distinct, also when the deficit is exactly q^r. |
| The overlap permutation determines actual n-words | Check k≥r, suffix-prefix consistency around a whole orbit, and recovery starting at every labelled prefix. At r=1 the overlap constraint is empty. |
| Euler tours count rotations once | A specified surviving edge occurs once. The graph is balanced and every vertex still has positive degree. A disconnected residual graph must contribute zero. Binary n=d=2 supplies a test. |
| Orientation and normalization | Verify the row transition convention, the out-Laplacian, trees oriented toward the chosen root, and the ratio of the local BEST factorials. The inverse's constant component vanishes after compression and multiplication by I−S. |
| Limit and degree | Only overlaps shorter than r escape the permutation transition rule. Check the finite geometric tail, periodicity of the short-overlap corrections, and the rank bound d minus the number of cycles. |
| Closed limit for d≤q | Check the permutation cycle index, the q falling factorial from labelled choices, and the coefficient recurrence in the proof. |

The 26 exact cases exercise finite counts. The word enumeration is independent of the graph interpretation. The full-cofactor verifier shares the tree-count theorem with the proposed derivation. Finite counts do not certify the limiting or polynomial assertions. No independent proof review, proof-assistant certificate or exhaustive historical priority search has been completed.
