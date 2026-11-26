# How much of the four-word bound was already known?
**Private literature audit for S.A. Chavarría • 18 November 2026**

**Disposition.** Potentially new mathematical result for the entire family, with priority unresolved. I located published inputs that give four or eight, published small-length evidence sufficient for the first two primes, and close precedents for all four proof steps. I did not locate a published theorem eliminating eight for the entire family. The narrowest candidate contribution is recognizing that the *necessary* small factor forces a specific interleaving, so the published exact class theorem applies. This is a source audit by the same mathematical collaborator who developed the draft. Its source checks are independent of the draft's claims; it is not an independent referee opinion.

## 1. Identify the object before comparing claims
For a labeled binary word s, count every contiguous nonempty interval by its pair (#0,#1), retaining multiplicity. Two words agree if these multisets agree. E_n is the largest number of distinct oriented words producing one record. Labels are fixed. The full word is measured. H_n in the 2010 ISIT paper is the same quantity. Equivalent views include the histogram of Hamming weights at every window length; the multiset of Parikh vectors of all factors; positive displacements between vertices of a monotone unit lattice path; and the connected-subpath composition deck of a binary path. In graph language verify whether reversal is quotiented out. An eight-word fiber consists of four reversal pairs: a palindrome has only a singleton class by the published reciprocal-factor characterization and squarefree diagonal. Mere existence of a factor of a given composition, ordered substring spectra, arbitrary subsequences, prefix–suffix compositions, graph counts modulo all automorphisms, and sizes of reconstruction codes define different quantities.

The path representation is an exact change of language. A prefix of length i ends at (a_i,b_i), and the displacement from prefix i to prefix j gives the composition of positions i+1 through j. Mirroring adds the negative displacements and the n+1 zero differences. Thus homometry is genuinely relevant. An arbitrary homometric point set need not form the prefix vertices of a monotone unit-step path. A theorem about a broader class could settle our question if its upper bound were strong enough; a construction or pair characterization in that broader class is insufficient.

## 2. Historical mathematical gap
Use the 2015 journal numbering unless a source below is explicitly marked ISIT or arXiv.

|Source and hypotheses|Exact consequence here|
|---|---|
|2010 ISIT, Thms 7–8: a binary word with r nonreciprocal prime factors has class size 2^r. For arbitrary length, H_n ≤ min(2^(d(n+1)−1), (n+1)^1.23), where d counts positive divisors.|The four divisors of 3p give eight. Cor. 9 concerns odd prime powers, Cor. 10 primes, Cor. 11 twice an odd prime. None gives four for 3p. Cor. 11 already uses three-factor saturation and a forced linear lift.|
|2015 Thm 12, Cor. 18, Lemmas 19–20: for a word polynomial, independently reciprocate integer irreducible factors; exactly 2^r distinct words result. Nonconstant factors retain positive degree on the diagonal.|Eight requires three nonreciprocal factors. At the target length the entire diagonal contains only three distinct irreducibles.|
|2015 Thm 27: if n+1=2^e times the product of distinct odd primes q_i with positive exponents a_i, E_n ≥ 2^(floor(e/2)+sum a_i). Thm 32: the general divisor and power upper bounds of ISIT Thm 8.|Four ≤ E_(3p−1) ≤ eight. The power bound is weaker here. All possible maxima are powers of two.|
|2015 Thms 21,22,24: unique up to reversal at n=7, n=q−1 or n=2q−1 with q prime. Thm 33 displays E_(2^k−1)=2^floor(k/2), E_(q^k−1)=2^k for odd prime q and positive k. The surrounding text discusses tightness also for twice prime powers.|3p with p≥5 is neither a prime power nor twice a prime power. Theorem 22 applies at the **separator** length p−1, after a reduction. The excluded p=3 gives n=8 and is already settled by Thm 33.|
|2015 Thm 26: for binary component words s_i, the entire class of their interleaving consists of interleavings of words equivalent to each component. Section 11 after Thm 27 reports all confusable words through length 22 are interleaved.|The finite report and Thms 22,26,27 together settle p=5 and 7. For a nontrivial interleaving at those lengths the component prefix counts multiply to 15 or 21. They must be 3 and p, in either order, so each component admits at most two orientations. Both maxima are four. For p≥11 the finite report does not apply.|
|2015 conclusion asks whether the Thm 27 lower bound is always attained as the maximum.|This establishes a documented broader gap in 2015. It does not say every length was open then or that this special case remains open today.|

[ISIT paper](https://doi.org/10.1109/ISIT.2010.5513668) · [SIAM journal](https://doi.org/10.1137/140962486) · [Journal full text, §§7–12, conclusion and Appendices A/B](https://people.csail.mit.edu/jayadev/papers/sidma-strings.pdf)

**Post-2015 result.** I located no subsequently published bound improving this uniform four/eight bracket for the same object. A 2024 exact formula for a differently defined E_n and a 2026 construction of exponentially many graph labelings are the strongest apparent conflicts inspected below. The two special prime cases and the known four-word construction should not be presented as discoveries by this project.

## 3. Attribute each proposed contribution
|Claim|Classification|Reason and remaining issue|
|---|---|---|
|Eight forces a nonreciprocal factor specializing to Phi_3(t)=1+t+t².|Direct consequence of published work.|Apply Cor. 18, Lemma 20 and Thm 32’s proof to the squarefree product Phi_3 Phi_p Phi_(3p). Every factor consumes at least one distinct diagonal irreducible. ISIT 2010 Cor. 11 executes the analogous saturation argument for Phi_2.|
|The nonreciprocal quadratic lift must be P_01 or P_10.|Direct consequence of published work with a short additional coefficient argument.|The two polynomials are explicitly displayed after 2015 Thm 22; that example alone does not classify arbitrary factors. Degree additivity and the endpoint property reduce the mixed lift to 1+a x+(1−a)y+xy. Thm 12 supplies flipped paths. Their first x coefficients differ by 2a−1, forcing a=0 or 1. We located analogous linear and quadratic case analyses in Thm 24 and Appendix A, not this exact assertion.|
|A word already interleaved with 01 has P_01 as a factor; every word in a given interleaved class arises from equivalent components.|Already published.|Lemma 28 and Thm 26. Appendix B, Lemma 47, assumes a substituted autocorrelation identity; divisibility of an arbitrary word polynomial by P_01 is a different hypothesis.|
|Conversely, divisibility by P_01 at length 3m+2 forces the word 01 b_1 01 ... b_m 01, for every m≥0 (and the reflected version for 10).|Potentially new mathematical result as an explicitly isolated lemma; priority unresolved.|The strongest close precedent is 2015 Thm 24 case 2, which passes from a diagonal factor constraint to repeated blocks at a different length by a diagonal derivative. Appendix A case 3 applies the idea to a length-seven word t u t. Section 5 already uses the 01 construction. A reverse characterization of all words divisible by P_01 was not located. The degree-by-degree stripping induction is a candidate proof of that characterization.|
|Equivalent interleaved words have equivalent separator words (with the block aligned).|Already published / direct consequence.|Thm 26 and the fixed locations of the separators. Lemma 28 supplies the polynomial substitution.|
|The length-k separator histogram is one third the length-3k full-word histogram shifted by k ones.|Direct consequence of the known interleaving construction by elementary window counting. Exact prior publication of the measurement formula unresolved.|The Thm 25 proof tracks substrings by separator interval and end pieces. I found no statement there that singles out the decimated histogram. The rule recovers it using fewer measurements than Thm 26 assumes. It is an optional proof/decoder, and its simplicity argues against an independent originality claim.|
|Derivative at the diagonal exposes prefix counts; eight-word interleaving example at length 26.|Already published.|See Thm 24 case 2 and the proof of Thm 33 for the derivative. ISIT 2010 explicitly displays the three-block length-26 example after Cor. 9. The length-124 construction likewise specializes the prime-power construction. Counting them afresh is verification.|
|E_(3p−1)=4 for every prime p≥5.|Potentially new mathematical result; priority unresolved.|If an earlier source proves the converse above, the target follows by a short combination with published results. If an earlier upper bound for all odd semiprimes or any covering family exists, the target is a direct consequence even if its proof omits interleavings. No inspected source established either antecedent.|
|An alternative proof of an already known all-primes equality.|Unresolved.|No verified source for the all-primes equality has been identified. “Potentially new proof of a known result” fits the finite special cases only, not the whole family on present evidence.|

## 4. Source register and adversarial checks
The following entries specify what was checked. Section or proposition numbers are supplied where they support an inference; a source inspected only through metadata or an abstract cannot supply theorem-level negative evidence.

1. **Jayadev Acharya, Hirakendu Das, Olgica Milenkovic, Alon Orlitsky, Shengjun Pan, On reconstructing a string from its substring compositions**, IEEE ISIT, June 2010. Author PDF §§IV–V. Thm 2 gives collisions by reversing the individual components of a maximal interleaving factorization, already supplying four for a two-component construction with both components nonpalindromic. For example use 01 and any nonpalindromic length-(p−1) block, whose prefix count p is prime and thus has no nontrivial interleaving factorization. Thms 7–8, Cors 9–11; see §2 above. The earlier H_n notation and explicit prime-power example are important priority corrections. The target's factor is nonreciprocal whereas the linear lift in their Cor. 11 is reciprocal. [DOI](https://doi.org/10.1109/ISIT.2010.5513668) · [Author PDF](https://people.ece.cornell.edu/acharya/papers/rcn_str_sbs.pdf)
2. **Same five authors, Quadratic-backtracking algorithm for string reconstruction from substring compositions**, IEEE ISIT, 2014. Abstract and algorithmic analysis address random words over alphabets of size at least four with high-probability running-time guarantees; an algorithm listing a fiber is compatible with either worst-case binary maximum. [DOI](https://doi.org/10.1109/ISIT.2014.6875042)
3. **Same five authors, String Reconstruction from Substring Compositions**, arXiv March 2014; SIAM Journal on Discrete Mathematics 29, 1340–1371, online 4 August 2015. Principal source for §§2–3. Also Thm 29 constructs collisions when word polynomials share a factor; it assumes that factor and gives a pair construction. The length-23 noninterleaved example in §11 explicitly distinguishes ribbon equivalence. The authors’ broader question appears in §16, Conclusions (locate “always tight”). [Preprint](https://arxiv.org/abs/1403.2439) · [Journal](https://doi.org/10.1137/140962486)
4. **Dénes Bartha, Péter Burcsi, Zsuzsanna Lipták, Reconstruction of Trees from Jumbled and Weighted Subtrees**, CPM 2016. An edge-labeled path recovers precisely the contiguous-word measurement. Thm 5 computes the subtree Parikh polynomial recursively for a rooted tree, using the rooted and child-subtree polynomials. Computing this invariant is a forward map. No mixed-prime upper bound follows from that recurrence. [DOI and open paper](https://doi.org/10.4230/LIPIcs.CPM.2016.10)
5. **Dénes Bartha, Reconstructibility of tree graphs**, ELTE doctoral dissertation, submitted 2021, defended 2022. Ch. 3, Props 3.2.4–3.2.5 and Table 3.2. The first starts with equivalent binary paths; the second exhibits equal weight decks but unequal Parikh decks. Its length-14 example is specifically a warning against conflating weights with compositions. Table 3.2 enumerates signed trees across shapes and up to isomorphism. It is not E_14. The repository and indexed dissertation text were checked. [DOI](https://doi.org/10.15476/ELTE.2021.095)
6. **Pedro Ascensão Ferreira Matias, Exact Learning of Sequences from Queries and Trackers**, UC Irvine doctoral dissertation, 2021. Ch. 2 §2.4, Lemma 2.9: yes/no jumbled-index queries cannot distinguish a nonpalindromic word from its reverse. Queries with an end marker give additional information. Neither oracle is the complete multiset in our question. [Repository](https://escholarship.org/uc/item/5784n4zq)
7. **Utkarsh Gupta and Hessam Mahdavifar, A New Algebraic Approach for String Reconstruction From Substring Compositions**, arXiv and ISIT 2022; IEEE Transactions on Information Theory, January 2025. Same complete binary input. Checked preprint formulation and code construction including Thm 9 (bijection between the paper's reconstruction code S(n) and its defined positive walks). Guarantees for selected words and runtime are not worst-case fiber bounds. Final issue metadata checked; preprint theorem numbering is used here. Residual check: compare final text for additions to the preprint. [Journal](https://doi.org/10.1109/TIT.2024.3493762) · [Preprint](https://arxiv.org/abs/2201.09955)
8. **Zuo Ye and Ohad Elishco, Reconstruction of a Single String From a Part of Its Composition Multiset**, arXiv 2022; IEEE Transactions on Information Theory, June 2024. Section V, Cor. V.8 and Thm V.10 in the preprint calculate class sizes and the exact extremum for all-prefix/all-suffix compositions of a binary word. On the entire range relevant here their maximum is 2^(floor((n−2)/4)+1). At n=14 that gives 16; our complete-record maximum is four. Their Example V.9 at n=6 gives four words where the complete-record class has size ≤2 by the prime-minus-one theorem. This concrete comparison excludes an identification of the two invariants. [Full preprint](https://arxiv.org/abs/2208.14963)
9. **Anisha Banerjee, Antonia Wachter-Zeh, Eitan Yaakobi, Insertion and Deletion Correction in Polymer-Based Data Storage**, ISIT 2022; IEEE Transactions on Information Theory, July 2023. The conference Thm 1 concerns correction of t asymmetric multiset deletions by a specified code. This is a statement on a selected codebook and an error channel; it does not upper-bound arbitrary full-record fibers. [Conference paper](https://yaakobi.net.technion.ac.il/files/2022/08/133_Indel_Polymer_ISIT22.pdf)
10. **Srilakshmi Pattabiraman, Ryan Gabrys, Olgica Milenkovic, Coding for Polymer-Based Data Storage**, preprint 2020; IEEE Transactions on Information Theory, August 2023. Binary mass-error correcting codes use restricted prefix/suffix weights and interleaved Catalan–Bertrand paths. A uniquely decodable subset yields no uniform upper bound on fibers in the whole ambient space. Abstract/construction scope screened; incidental observations outside the construction remain unresolved. [Preprint](https://arxiv.org/abs/2003.02121)
11. **Antoine Dailly and Tuomo Lehtilä, Reconstructing graphs with subgraph compositions**, preprint March 2025; Discrete Applied Mathematics 390, September 2026. Thm 6 counts labelings up to path symmetry. Preprint Thm 26 preserves equivalence when a graph is joined at the middle separator of an interleaving of a path of ≥2 vertices with an odd-order path and the latter is reversed. Thm 27 gives families of subdivided stars with many mutually equivalent labelings. Both are existential constructions on specified graphs. The path case is a genuine translation; graph construction does not eliminate eight on every binary 3p−1 path. [Journal](https://doi.org/10.1016/j.dam.2026.04.023) · [Preprint](https://arxiv.org/abs/2504.00169)
12. **Joseph Rosenblatt and Paul D. Seymour, The Structure of Homometric Sets**, 1982. The publisher's main characterization concerns finite integer point measures with equal autocorrelations; they factor as C*D and C*D-reflected. The factors may be signed. This is prior art for factor flips. The characterization by itself imposes neither unit monotone steps nor four solutions at a point count of 3p. **Unresolved full-text source**: original theorem numbering, examples, and potential special corollaries were not verified against the entire article. [DOI](https://doi.org/10.1137/0603035)
13. **Paul Lemke, Steven S. Skiena, Warren D. Smith, Reconstructing Sets From Interpoint Distances**, DIMACS TR 2002-37; book chapter 2003. The general turnpike solution-count bound is used in 2015 Thm 32 through a univariate embedding. A bound of order (3p)^1.23 exceeds eight throughout this family. Further special arithmetic restrictions on *two permissible consecutive gaps* would matter; a guarantee for arbitrary distances or an algorithm for recovering all solutions supplies no such restriction. [Report](https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2002/2002-37.html)
14. **Tamara Dakić, On the Turnpike Problem**, Simon Fraser University PhD dissertation, August 2000. Positive pairwise-distance multiset of a finite point set on a line, quadratic programming formulations and semidefinite relaxations. Title page, repository summary and subject checked. No path-specialized count verified; any incidental counting statement remains unresolved. [Dissertation](https://sandbox.dodona.be/en/activities/1441444585/description/extUwCk3NzejXgat/media/Dakic2000.pdf)
15. **Louis J. Billera, Hugh Thomas, Stephanie van Willigenburg, Decomposable compositions, symmetric quasisymmetric functions and equality of ribbon Schur functions**, preprint 2004; Advances in Mathematics, August 2006. Preprint Thm 4.1 characterizes equivalent integer compositions under equality of coarsening data/ribbon Schur function by reversal of irreducible components. This is a particularly plausible false match because it also counts choices of orientations. Acharya et al. explicitly separate the equivalence relations in §11. A restricted coincidence at our lengths would require its own proof. [Journal](https://doi.org/10.1016/j.aim.2005.05.014) · [Preprint](https://arxiv.org/abs/math/0405434)
16. **Gennadiy Averkov and Barbara Langfeld, Homometry and direct-sum decompositions of lattice-convex sets**, preprint 2014. Lattice-convex sets and direct sums with lattice tiling constraints. A monotone path need not contain all lattice points in its convex hull: prefixes of 0011 omit (1,1), although it lies in their convex hull. This blocks blanket application. Full case-by-case comparison of specialized direct-sum families unresolved. [Preprint](https://arxiv.org/abs/1412.7676)
17. **Yaoyu Yang, Survey of Sequence Reconstruction Problems and Their Applications in DNA-Based Storage**, IEEE JSAIT, 4 August 2025. **Unresolved full-text lead**: publisher abstract and bibliographic record inspected; a complete text and its treatment of ambiguity bounds were not verified. A survey is a lead to further sources, not evidence that an unmentioned theorem does not exist. [DOI](https://doi.org/10.1109/JSAIT.2025.3595457)
18. **Nikhil Bansal, Mark Cieliebak, Zsuzsanna Lipták, Finding submasses in weighted strings with Fast Fourier Transform**, online 2006; Discrete Applied Mathematics, 2007. Given a weighted string, find occurrences of requested masses. Forward evaluation differs from bounding the inverse fiber of a histogram. An injective mass encoding for words of bounded length, e.g. weights 1 and n+1, does make a complete multiplicity-preserving mass histogram equivalent to our record. This is why weighted-string work was searched rather than discarded by title. [DOI](https://doi.org/10.1016/j.dam.2005.09.019)

## 5. Search protocol and residual uncertainty
I followed the SIAM publisher's displayed forward-citation list from its first through its last entry (48 title records, including conference/journal duplicates), its backward references on turnpike, homometry and ribbons, references in Dailly–Lehtilä to the tree thesis and CPM proceedings, author-hosted manuscripts, indexed thesis repositories and full-text arXiv retrieval. The appendix lists the displayed titles to distinguish a title screen from theorem-level inspection. In addition to exact-notation searches I tried extremal confusability, prime products, reciprocal quadratic lifts, forced interleavings, composition/weight histograms, jumbled and weighted paths, Parikh-vector multisets, homometry and ribbon-equivalence hypotheses. Attempts to obtain an OpenAlex DOI citation export through the available search interface did not yield a usable record. Publisher citation lists omit uncited parallels and can omit indexed citations. No comprehensive subscription database export, exhaustive multilingual dissertation coverage, or independent specialist priority check is claimed.

**What would change the verdict.** A reference proving the all-primes maximum, an upper bound four on a class containing these lengths, a universal tightness theorem for this lower bound, or a prior factor-to-interleaving converse with applicable hypotheses would materially change attribution. An eight-word example at any target length would invalidate correctness. A novel proof of a false statement, or a correct proof of a known statement, would not establish a new theorem. Numerical tests at additional primes cannot resolve priority.

**Review recommendation.** Ask a specialist about the converse under its own name-free formulation: if a monotone prefix polynomial has 1+x+xy as an integer divisor, must the path be a succession of identical two-step blocks separated by one free step? Search for known divisibility-to-word-morphism or tiling criteria that apply even when the cofactor may have signed coefficients. The separate proof note states the assumptions needed for this deduction. No external correspondence or submission was undertaken.

## Appendix A. Reproducible query strings

- "equicomposable" maximum size substring compositions prime powers lower bound tight E_n conjecture subsequently solved 3p
- citing Acharya String Reconstruction from Substring Compositions maximum ambiguity polynomial factorization equicomposable Gupta Ye Wang polynomial time factorization maximal cardinality
- dissertation thesis equicomposable strings largest set interleaving substring compositions algebraic characterization binary strings Acharya Kannan
- homometric monotone lattice paths equicomposable binary strings factorization direct sum interleaving Radcliffe Scott substring composition 3p semiprime
- "substring compositions" "lower bound" equicomposable prime maximum confusable strings p q 3p theorem
- Srilakshmi Pattabiraman doctoral dissertation Illinois polymer storage thesis coding author
- Utkarsh Gupta Michigan dissertation polymer storage algebraic string reconstruction deepblue
- Hirakendu Das PhD dissertation string reconstruction substring compositions UCSD Jayadev Acharya thesis nonparametric
- homometric ribbon Schur equal coarsenings Billera Thomas van Willigenburg factorization ambiguity compositions 2006 DOI Rosenblatt Seymour homometric sets theorem
- "Survey of Sequence Reconstruction Problems" composition substring survey authors theorem substring composition Acharya
- site:arxiv.org "Reconstructing graphs with subgraph compositions" Theorem paths graphs equicomposable common factor authors
- "equicomposable" ("3p" OR "pq" OR "semiprime") strings binary maximal ambiguity polynomial 01 interleaving forced
- "Pattabiraman" thesis storage site:ideals.illinois.edu molecular
- "Shengjun Pan" dissertation site:escholarship.org string reconstruction
- Thesis equicomposable strings "string reconstruction" polymer storage dissertation codes substring composition doctoral thesis
- Rosenblatt Seymour structure homometric sets theorem 2.1 polynomial factorization DOI full text direct sum
- "Quadratic-backtracking algorithm" authors 2014 DOI and "On reconstructing a string from its substring compositions" 2010 DOI
- "Reconstructing graphs with subgraph compositions" theorem subdivided stars theorem 26 path corollary equicomposable
- "Reconstructibility of tree graphs" Bartha értekezés pdf reconstructibility ELTE 2021 thesis
- Bansal Cieliebak Liptak reconstructing strings from substring weights CPM 2004 maximum number solutions weighted alphabet two letters interleaving bounds
- Bartha Reconstruction of trees jumbled weighted subtrees lemma theorem indistinguishable paths string factorization equicomposable theorem confusability
- Acharya 2010 "On reconstructing a string" Theorem largest number E_n pdf ISIT 2010 factorization theorem 3 primes
- binary equicomposable strings substring composition maximum cardinality semiprime factor interleaving 3p−1 same substring composition multiset
- "equicomposable" polynomial interleaving factor "01" substring composition "divisible" preprint proof reconstruction interleaved
- 2025 2026 maximal equicomposable sets binary strings composition multiset E_n H_n homometric monotone lattice paths semiprimes preprint extremal equicomposable sets November 2026
- Bartha Burcsi Liptak reconstruction trees jumbled weighted subtrees theorem path strings multiplicities CPM 2016 10.4230
- Dénes Bartha Reconstructibility of tree graphs dissertation PDF reconstructibility of tree graphs 2021 multiset string composition equicomposable 3p tree graphs thesis
- equicomposable strings undergraduate master's thesis equicomposability substring composition ambiguity polynomial binary strings dissertation reconstruction Illinois Michigan
- "substring compositions" PhD dissertation Acharya Das information theory sequence reconstruction doctoral dissertation polymer-based storage Pattabiraman Gupta dissertation title
- "The turnpike problem" Tamir Dakić PhD thesis 2000 Simon Fraser URL homometric maximum solutions
- abelian factor equivalence all lengths multisets Parikh vectors binary words substring composition equicomposable abelian k-binomial k-abelian jumbled indexing multiset reconstructibility
- homometric sets maximum number of solutions interpoint distances composite cardinality 3p turnpike Lemke Skiena Smith bounds homometric subsets diffractive homometry direct sums Averkov Langfeld polynomial
- homometric lattice convex sets direct sum theorem Averkov Langfeld covariogram planar lattice-convex sets three points width one homometric
- Coven Meyerowitz tiling integers cardinality two prime factors conditions T1 T2 positive 0 1 polynomial tile 3p DOI cyclotomic homometry direct sum

## Appendix B. SIAM forward citation title screen

Publisher link order on the audit date. Titles here document screening only. Consult the source register for depth of review and mathematical scope. [Publisher citation list](https://epubs.siam.org/doi/10.1137/140962486#citedby)

1. Repeat-Free Codes With Local Constraints
2. Reconstructing graphs with subgraph compositions
3. Improvements on permutation reconstruction from minors
4. On the Intersections of q-ary Hamming Balls
5. Levenshtein's sequence reconstruction problem and results for larger alphabet sizes
6. Coded String Reconstruction from Erroneous Prefix-Suffix Compositions
7. Reconstructing Graphs from Subgraph Compositions
8. The beltway problem over orthogonal groups
9. A New Algebraic Approach for String Reconstruction From Substring Compositions
10. Reconstruction of Multiple Strings of Constant Weight from Prefix–Suffix Compositions
11. Coding Methods for String Reconstruction From Erroneous Prefix-Suffix Compositions
12. Survey of Sequence Reconstruction Problems and Their Applications in DNA-Based Storage
13. Reconstruction From Noisy Substrings
14. Reconstruction of multiple strings of constant weight from prefix-suffix compositions
15. DNA-Based Data Storage Systems: A Review of Implementations and Code Constructions
16. Reconstruction of a Single String From a Part of Its Composition Multiset
17. On Codes for the Noisy Substring Channel
18. DNA sequences and DNA codes
19. Adversarial Torn-Paper Codes
20. Generalized Unique Reconstruction From Substrings
21. Coding for Polymer-Based Data Storage
22. Insertion and Deletion Correction in Polymer-Based Data Storage
23. The Learning and Communication Complexity of Subsequence Containment
24. On Constant-Weight Binary B 2 -Sequences
25. Insertion and Deletion Correction in Polymer-based Data Storage
26. A New Algebraic Approach for String Reconstruction from Substring Compositions
27. Adversarial Torn-paper Codes
28. The Gapped k-Deck Problem
29. Improved Rank-Modulation Codes for DNA Storage With Shotgun Sequencing
30. Information-Theoretic Foundations of DNA Data Storage
31. Adaptive learning of compressible strings
32. Spectral concepts in genome informational analysis
33. Multi-strand Reconstruction from Substrings
34. Repeat-Free Codes
35. On Codes for the Noisy Substring Channel
36. Reconstruction of Strings From Their Substrings Spectrum
37. Realization problems on reachability sequences
38. Reconstructing Point Sets From Distance Distributions
39. Reconstruction of Strings from their Substrings Spectrum
40. Mass Error-Correction Codes for Polymer-Based Data Storage
41. Reconstruction Codes for DNA Sequences With Uniform Tandem-Duplication Errors
42. Adaptive Exact Learning in a Mixed-Up World: Dealing with Periodicity, Errors and Jumbled-Index Queries in String Reconstruction
43. Unique Reconstruction of Coded Strings From Multiset Substring Spectra
44. Reconstruction of Rooted Directed Trees
45. On the Number of Distinct k-Decks: Enumeration and Bounds
46. Reconstruction Codes for DNA Sequences with Uniform Tandem-Duplication Errors
47. Unique Reconstruction of Coded Sequences from Multiset Substring Spectra
48. The hybrid k-deck problem: Reconstructing sequences from short and long traces
