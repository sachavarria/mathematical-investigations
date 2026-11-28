# An address disclosed after compression

## Question

Retain an exact deterministic summary of an initial string. Afterward, an index selects which future time of the rightmost cell to report. This is a delay in the specification of the question. Time during preprocessing and during response is unrestricted. The resource counted here is fixed-length storage at the interface.

## Proposition

Use sites \(0,\ldots,2L\), two frozen zero ghosts and \(L\ge1\). Let the nonlinear mask be 2 or 4. For any \(S\subseteq\{0,\ldots,L-1\}\), the whole family of future endpoint bits at times in \(S\) realizes every bit vector of length \(|S|\). The minimum storage after reading the full string and before learning the selected time is exactly \(|S|\) bits. At the cut just before reading the endpoint, the minimum message to an observer who will be given the endpoint and the selected time is exactly \(|S\setminus\{0\}|\) bits.

## Proof

Fix site zero to zero. For mask 2, set all odd sites to zero. They stay zero because the second predecessor of each odd site is zero. The free even sites \(y_j=x_{2j}\), \(1\le j\le L\), obey \(y'_j=y_j\oplus y_{j-1}\), with \(y_0=0\). For mask 4, set all odd sites to one. Each odd site of index at least three has a one as its second predecessor, which makes its increment zero. Site one has a zero immediate predecessor, so its increment also vanishes. Now \(y'_j=y_j\oplus y_{j-1}\oplus1\). Site zero remains zero under both masks.

In either restriction the linear part is \(I+D\), where \((Dy)_j=y_{j-1}\). Thus at time \(t<L\) the endpoint is an affine form whose earliest variable is \(y_{L-t}\) with coefficient one. This follows by the unique product of \(t\) shifts in \((I+D)^t\). All earlier times have coefficient zero on that variable. The forms have linearly independent rows, including for an arbitrary subset of the times. Their joint affine map is onto. A deterministic retained message must distinguish any two answer vectors that differ in a coordinate, and storing all answers meets the resulting bound.

For the cut before the endpoint, fix \(y_L=0\) in the lower-bound argument. Each positive time still has its distinct earliest pivot. Hence all vectors of answers for the positive times occur with a common final input bit. For an upper bound, the triangular rule gives endpoint at time \(t\) equal to the initial endpoint XOR a function of its strict prefix. Store these prefix-dependent offsets for the positive times. The offset for time zero is identically zero. This proves equality.

## Interpretation and audit

A fixed positive time uses exactly one bit at this cut. The delayed choice of any of the \(L-1\) positive times requires exactly \(L-1\) bits. These are interface or one-way message lengths. Intermediate workspace required to construct the message can be larger. A restriction gives the full-population lower bound because a procedure correct on every input must also work on the restriction. It gives no distributional lower bound for typical unrestricted inputs. No claim is made for arbitrary masks, arbitrary time sets beyond the stated horizon or intrinsic human cognitive effort.

The proof uses two established ingredients, a linear factor in the dynamics on an invariant subset and the elementary deterministic indexing lower bound. The mask-2 guard subsystem itself has an exact antecedent in Ohi, Proposition 1.1(2), as documented in `sources.md`. Its colour conjugate supplies the bulk mask-4 construction. The finite boundary check and indexing consequence are derived above. Publication priority for the composite statement has not been established. A separate direct enumeration in `check_guards.py` tests the guard invariance, predicted affine evolution, surjectivity and the cut formula.
