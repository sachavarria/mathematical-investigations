# The order between

A draft for The Morphology of Information, 27 November 2026. One population, the binary windows of length n, passes between four arrangements. Selecting a window holds its identity fixed as the two rims change. The linking line records where the same window has gone. The design draws on the atlas’s comparison of topology with geometry, carrying its dark ground, Space Grotesk and violet and mint marks into an experiment with circular order. The colored crossings are consequences of measured positions. Their appearance has no assigned measure of perceptual effort. [Established atlas](https://sachavarria.github.io/The-Morphology-of-Information-/) · [Open the private browser draft](https://where-the-count-lives.cosmicmami.chatgpt.site/order/index.html) · [Standalone HTML](index.html)

| Arrangement | What can be read locally |
|---|---|
| Lexicographic | Shared leading bits delimit contiguous intervals of windows. |
| Colexicographic | Shared trailing bits delimit contiguous intervals. |
| Grandmama time | A step advances one place in the de Bruijn cycle. Consecutive windows overlap in n−1 bits. |
| BWT packets | The primitive last column identifies a rotation packet. Within it, each row has an LF successor determined by stable sorting. The display orders packets by last column and rows by lexicographic rank within each packet. This ordering across packets is a design choice. |

The full population, individual windows and membership in rotation packets survive all four arrangements. Circular adjacency usually changes. At order eight, counting unordered neighboring pairs and including the seam, Grandmama time shares 3 of its 256 adjacencies with lex order and 62 with the displayed BWT packet order. These numbers describe adjacency in this instrument. Assigning a temporal coordinate without preprocessing is a separate computational problem.

## A pattern with an explanation

Across all six displayed orders, lex and colex share precisely one adjacency. This holds for every n≥3. The seam joins the all-zero and all-one windows in both circles. For any other lex step x to x+1, let t be the number of trailing ones in x. Bit reversal changes the integer key by 3·2^(n−1−t)−2^n. For the two reversed keys to be circular neighbors this must be ±1 modulo 2^n. The power of two must therefore be 1, leaving 3, which is neither residue for n≥3. Thus the seam is the unique shared edge. What looks like almost complete dispersal of neighbors is forced by the coordinate transformation.

The three shared temporal and lex adjacencies also invite a check independent of the Grandmama construction. In any binary de Bruijn cycle with N=2^n, n≥3, a time step from integer x produces (2x+b) mod N for b∈{0,1}. Requiring the result to equal x±1 leaves only four directed possibilities: 0→1, N−1→N−2, 1→2 and N−2→N−3. The first two are forced since a complete cycle cannot loop at the homogeneous states. The count is therefore between two and four for every such cycle. The displayed count of three at orders four through nine is a finite observation about Grandmama. The packet/time overlap, including 62 at order eight, depends on the chosen inter-packet arrangement. [JavaScript audit](check_order.cjs) · [All adjacency counts](order-results.txt)

## A visible quantity in the exact computation

Mint ticks on the BWT rim mark rows that start in zero and end in one. Inside a packet they count the 1→0 boundaries of its primitive circle. That same integer is the maximum number of stable-shuffle edges crossing a row cut in one direction. It bounds the size of the partial-path matching required by an exact transfer. The count links a feature visible in the object to work in one specified algorithm. [Invariant, complexity bound and verification](frontier.md)

## Connectivity and the observed past

A prescribed backward history and a single permutation cycle must hold in the same column. Three calculations investigate that joint requirement.

* Fix the number of zeros in each consecutive pair of rows. A prescribed bit history forces one trail. A directed-tree determinant then counts all compatible single-cycle completions in polynomial time for the cell. The explicit cover by such cells remains exponentially large. [Proof, total-work bound and finite checks](joint.md)
* After fixing a numerical itinerary, compress its residual target ranges into strips. Aligned strips admit an exact count by a tree determinant and divisor inversion. In general the same calculation gives an upper bound, and a three-row example exhibits a strict overcount. A bordered matrix proves exactly where the earlier symbolic determinant theorem applies. [The determinant connection](bridge.md)
* Instead of fixing pairs or a path, the partial-path transfer sums all allowed columns with bounded crossing count at once. Its work depends on crossing width and the length of the requested history. [Transfer proof](frontier.md)

The outstanding question is whether the tree determinants can be summed across quotas while preserving the precedence of targets carrying the same bit. The pair construction improves on scanning all BWT columns, but its exponential bound is weaker than the prior candidate square-root-exponent method. General exact polynomial-time ranking remains unresolved. The numerical checks and candidate derivations in this directory are by Codex. External proof review and priority assessment remain open.

Run `node check_order.cjs`, `python frontier.py`, `python check_joint.py` and `python strips.py` from this directory. The browser draft supports orders four through nine. Browser layout and interaction were checked at 390 × 844 and 844 × 390 CSS pixels. Physical-device usability and perceptual responses have yet to be measured.
