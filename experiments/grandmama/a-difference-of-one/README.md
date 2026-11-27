# A difference of one

A silent procedural HTML motion study, November 26, 2026. S.A. Chavarría directed the investigation into beauty, intellectual desire and temporal access. Agent 404 independently reproduced earlier finite-order findings as reported by Chavarría, and proposed the distinction that prompted this study. Mathematical development, composition and implementation of this draft by Codex (GPT-6.2 Astra). Agent 404's earlier checks do not cover the new argument below.

[Download the standalone HTML](A-difference-of-one.html) and open it in a browser. Space Grotesk Regular is embedded, with its SIL Open Font License. The page has no external assets.

## The score

Two contours each carry twelve evenly indexed marks. Their radial folds interpolate the bits in two actual windows. The opening starts three ticks after each chosen boundary and walks backward to it. A boundary here is a primitive word that is lexicographically first among its rotations. The windows at arrival are 000000000001 and 000000000011. During the turn the two contours acquire depth. Each interior cross-section uses the canonical necklace at a block start and each emitted bit in the half-open interval contributes one point. Some points overlap in projection. The tilt, palette, interpolation, rate and photographic perspective are compositional choices. A transverse section is an image of a block, not a geometric invariant of the clock. The piece enumerates its small clock at load time. The duration of the turn has no interpretation as an algorithmic lower bound.

Tap to hold the interval open, tap again to release it. Pause freezes the automatic movement. Reduced-motion preferences start it paused. About contains the reading key. The silent screen edition renders the same canvas score at 24 frames per second.

In developing the piece we consulted sampled film frames from NULL OBJECT, the SPECTRA interface source, the HYPERSTITION source and project notes, and the Morphology atlas documentation and Temporal Access motion source. One formal observation was how a close approach to the panels in NULL OBJECT changes what portion of an utterance can be read. Another was SPECTRA's uneven arrival of communications and its quiet beats. The score borrows a question about viewpoint, selection and duration; all its contours and bit records are drawn procedurally. There is no imported installation imagery or simulated testimony. Whether this movement induces a desire to investigate is an open question for viewers.

## One changed bit, a macroscopic phase displacement

Candidate original mathematical observation, pending independent verification and priority review. This note concerns the binary Grandmama construction and its zero-based clock convention from [the earlier study](../weighted-rank/README.md).

For n ≥ 16 let A = 0^(n−1)1 and B = 0^(n−2)11. Both are primitive least rotations (each has a unique longest circular zero run). Their Hamming distance is one. **Their shorter circular phase distance exceeds 2^n/128.** In particular normalized Hamming distance tends to zero while normalized circular distance stays bounded away from zero. The bound is conservative.

Proof. Write N = 2^n, k = ceil(log2(2n)), and m = n−k−4 ≥ 0. Form the two families of n-bit strings

    0^k 1 v 1 01      and      0^k 1 v 1 11,

where v has length m and contains no run of k zeros. At most m·2^(m−k) fillings are excluded by the union bound (zero exclusions if m<k). Hence at least half of all fillings survive. In both families the initial run is uniquely longest on the circle, because ones separate the variable portion from the ends. Every resulting word is a primitive least rotation and emits n clock bits. Every first-family word lies strictly between A and B in colex order: its final 01 precedes B's 11, and A has the smallest reverse key of any nonconstant representative. Every second-family word strictly follows B: they end in 111 whereas B ends in 011. Thus each of the two circular arcs between the starts of A and B contains entire interior blocks with mass at least n·2^(m−1) = N·n/(32·2^k) > N/128, since 2^k < 4n. This proves the claim.

This is a statement about the geometry of two representations. It establishes neither a lower bound on decoding time nor that arbitrary one-bit errors have this effect. In the ordinary binary counter a single high bit can likewise change the phase enormously, and ranking remains easy. Grandmama's additional constraint here is that both addresses pass the same full-block recognition test.

## Verification and next question

Run python3 verify.py to reproduce ranks.csv. The verifier groups every word by its least rotation, checks that both positions emit the stated window and sums orbit sizes before each threshold. The HTML independently lists canonical words by reversed binary key. At order 12 the separation is 1,635 of 4,096 ticks; at order 16 it is 27,694 of 65,536. As a research question, does the normalized forward distance for this explicit pair approach a limit, and which statistics of the final run of a canonical necklace control it? A viewer can encounter the near coincidence before deciding whether to examine that question. No human response measurements were taken.
