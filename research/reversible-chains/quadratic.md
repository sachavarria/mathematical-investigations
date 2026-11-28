# Predicting exact memory for a parity after one update

**Claim.** For every finite chain in the sixteen-rule family, every specified parity of output sites after one update, and every subset of input sites read before the cut, the exact number of distinguishable prefixes can be computed by polynomially many bit operations in the chain length. The calculation does not enumerate input configurations. It uses elementary linear and quadratic forms over the two-element field. This is a structural control for the experiment. No priority claim is made for the general quadratic calculation.

**Why an algebraic description helps.** After a prefix is supplied, the outstanding question is a Boolean function of the remaining cells. A pair of prefixes may be merged exactly when those functions are identical. A two-input Boolean function has the unique square-free expansion c+Aa+Bb+Cab, where addition is XOR and multiplication is AND. Taking any parity of the updated cells preserves degree at most two. Fixing some inputs can therefore change only a linear term and a constant in the remaining function. It suffices to count the attainable pairs of such changes.

**Proof.** Let u be the values of the p observed coordinates and v the values of the rest. Allocate the constant term to h and write the question as

    f(u,v) = h(v) + q(u) + uᵀ M v,

where q(0)=0. The update rule and requested sites explicitly specify these polynomials and the crossing matrix M. Fixed-zero boundary cells contribute zero wherever their variable appears. Given u, the residual is identified uniquely by (Mᵀu,q(u)): unequal constants differ at v=0, and two different slope vectors can be distinguished on a unit vector once constants agree.

Let r be the rank of M, K the kernel of Mᵀ, and B(u,k)=q(u+k)+q(u)+q(k) the bilinear polar form. There are 2^r slope fibers, each of size 2^{p−r}. In each fiber one or two constants occur. Its constant is unique precisely when

    B(u,k)=q(k) for every k in K.

Indeed this condition says exactly that adding a vector k from K never changes q(u). If the restriction of B to K×K is nonzero, q is nonlinear on K and no u can satisfy these equations, because the left side is linear in k. All fibers then have two possible constants.

Otherwise q restricted to K is linear, and the equations need be checked only on a basis k_j. Solve the affine system B(u,k_j)=q(k_j) by elimination. Inconsistency again gives two constants in every fiber. In the consistent case let h₀ be the rank of its coefficient matrix. There are 2^{p−h₀} solutions. They form whole fibers because B vanishes on K×K. Exactly 2^{r−h₀} of the 2^r fibers therefore have a single constant. The number of distinct residuals is

    2^{r+1} − 2^{r−h₀}   in the consistent case,
    2^{r+1}               when no fiber has a single constant.

This also covers an empty observed set, an empty unread set and a constant question. Computing a kernel, restricting a bilinear form, and solving a system over the binary field are polynomial in n. The answer is at most 2^p and uses at most p+1 bits. Taking its ceiling binary logarithm gives the minimum fixed-length message at this cut with preprocessing allowed. The time spent constructing or evaluating a sequential observer is a separate resource. ▪

**Scope.** A scalar parity at any time in an affine rule remains affine. More generally, for any fixed vector of linear observations, even at several specified times, write the answer vector as Nu+Pv+c. Its number of residuals is exactly 2^{rank N}. This follows since all values in the image of N occur and any two give different answers already at v=0. The presence of higher degree terms after iterating a nonlinear rule prevents applying the one-step quadratic formula unchanged.

**Finite review.** The implementation builds the crossing matrix and q directly from the local rule. A separate literal simulator groups the rows without using the formula. The check includes every mask, every parity (including the empty parity) and every choice of observed sites through n=5. The 96-cell example uses the proved algebraic calculation only. [Reference code](quadratic.py) · [Recorded output](quadratic-results.txt)
