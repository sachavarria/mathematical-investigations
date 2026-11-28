# Antecedents and conventions

## A direct comparison from 2004

Christoph Dürr, Ivan Rapaport and Guillaume Theyssier studied the cost of predicting the central cell of a cellular automaton when its initial data are divided between observers. For elementary cellular automata their matrix records the output bit for a left input and a right input, conditioning on the central symbol. Identical rows can share one message. Distinct rows need distinct messages in the deterministic one-way model. They measure row and column multiplicities, tabulate elementary rules empirically in Section 3, and consider other cut locations in Section 8. Even the juxtaposition of a space-time picture and a communication matrix has an explicit antecedent here. Table 1 lists ECA 154 in the empirically bounded group and ECA 106 in “Other.” Finite observations in their table do not establish asymptotics for either rule. [Dürr, Rapaport and Theyssier, *Cellular automata and communication complexity*](https://theyssier.perso.math.cnrs.fr/data/tcs04.pdf)

The present comparison uses a fixed finite chain with two zero ghosts, a specified order of observations, an arbitrary cut in that order, and in some questions a choice of observation time disclosed after the initial state has been read. An interior light cone with a geometric left/right split gives the same row-count mechanism as the earlier work. A different split or a different question can change that matrix. The mature literature on ordered binary decision diagrams also identifies equivalent partial assignments by equality of their residual Boolean functions. For a fixed cut the exact deterministic message length is the ceiling of the binary logarithm of the number of distinct rows. The maximum row count over cuts is a layered width. Reduced decision diagrams can skip variables, so a literal graph-level size need not equal this width. [Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*](https://doi.org/10.1109/TC.1986.1676819)

Closely related work studies the communication cost of testing whether a distinguished cell follows a prescribed temporal trace. Testing a specific trace, returning the whole trace and answering an index supplied after compression have different output contracts. [Goles, Guillon and Rapaport, *Traced communication complexity of cellular automata*](https://www.sciencedirect.com/science/article/pii/S0304397511001459)

## Exact rule identification

Write the two input bits as \(a=x_{i-1}, b=x_{i-2}\), with \(g(a,b)\) stored at bit \(2a+b\) of a four-bit mask. The centered elementary rule is \(f(l,c,r)=r\mathbin{\oplus}g(c,l)\). Its Wolfram number is \(\sum_{l,c,r}2^{4l+2c+r} f(l,c,r)\). For masks 0 through 15 in numeric order this gives

`170, 169, 154, 153, 166, 165, 150, 149, 106, 105, 90, 89, 102, 101, 86, 85`.

On the full line the triangular update equals one centered update followed by a one-cell shift toward increasing indices. At time \(t\) its cell \(i\) therefore equals centered cell \(i-t\). This identity compares local evolutions directly in interior cones. For a rule with \(g(0,0)=1\) a frozen zero reservoir does not follow the bulk evolution. Colour conjugation transforms a zero reservoir into a one reservoir, and spatial reflection interchanges geometric reading directions. Predictions near a boundary require a separate calculation. On a finite chain the triangular map is a permutation for every mask, since each previous bit is recovered after its lower-indexed predecessors. The elementary-rule identification concerns the local law and moving coordinates, and carries no automatic assertion of reversibility of the centered infinite or periodic system. [Wolfram, *Statistical Mechanics of Cellular Automata*](https://files.wolframcdn.com/pub/www.stephenwolfram.com/pdf/statistical-mechanics-cellular-automata.pdf)

The bit dependence is an instance of the triangular or T-function framework, in which output bit \(i\) may depend only on input bits through \(i\). That framework predates the experiment. [Klimov and Shamir, *New Applications of T-functions in Block Ciphers and Hash Functions*](https://citeseerx.ist.psu.edu/document?doi=d7a9b066953183f8a7dc73e72d56578e90dc1ee7&repid=rep1&type=pdf)

## A prior exact prediction formula

Lemma 9.1 of Inokuchi, Honda, Lee, Sato, Mizoguchi and Kawahara gives the dyadic iterate of ECA 166, mask 4 in these coordinates. For \(t=2^k\), its formula simplifies to

\[
 T^t(x)_i=x_i\mathbin{\oplus}
  (1\mathbin{\oplus}x_{i-2t})
  \prod_{j=1}^{t}x_{i-2t+2j-1}.
\]

The paper states the lemma using periodic indices. Any finite dependency cone can be embedded in a periodic configuration of sufficiently large period. For mask 4 the frozen zero left extension is invariant, so the same formula holds at the finite boundary if negative indices are set to zero. In increasing index order, before reading the endpoint a prefix need only record whether every inspected literal in the product is true, giving at most two residual rows for single-time prediction. In an interior cone both rows occur at the cut just before the endpoint. The dyadic closed form is a published result. It supplies a control for this experiment, particularly when a numerical profile changes sharply with time. [Inokuchi et al., *On Reversible Cellular Automata with Triplet Local Rules*, Lemma 9.1](https://arxiv.org/pdf/nlin/0504058)

## A prior exact invariant domain

Fumio Ohi's Proposition 1.1(2) gives the mask-2 guard construction explicitly for the moving-frame evolution of rule 154, as a member of a larger class. In the subspace where every odd bit vanishes, each even bit evolves as its XOR with the even bit two sites earlier. On the full line, bit complementation takes this to the corresponding mask-4 domain. Theorem 3.3 in the same paper goes further, describing the time evolution of configurations decomposed into specified blocks by piecing together additive evolutions. This is a close all-time antecedent for a description by linear pieces. Identifying a new coordinate formula requires a term-by-term comparison with that decomposition. The finite zero boundary for mask 4 is checked separately in the delayed-address calculation. Rupe's Chapter 5, Table 5.2 independently describes the rule-154 invariant domain in centered coordinates. The present use concerns its consequence for the exact number of reachable answer vectors. [Ohi, *基本セルオートマトンが生成する時空間パターン: Sierpinski Gasket*, Proposition 1.1](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1306-18.pdf) · [Rupe, *Cellular Automata: Domain Subdynamics*, Chapter 5](https://csc.ucdavis.edu/~atr486/static/dissertation.pdf)

## Scope of attribution

The deterministic row-count criterion, additive evolution over the binary field, triangular invertibility, the connection to elementary cellular automata, and the dyadic ECA 166 formula all have established mathematical antecedents. Finite experiments identify examples and suggest classifications. An unlocated exact antecedent for a particular restricted rule or measurement is insufficient evidence of publication priority. This source register sets the scope of the comparison and makes no priority claim.
