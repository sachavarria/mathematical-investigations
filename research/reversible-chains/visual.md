# Forms of a future

[Open the study](index.html) · [Order of reading](index.html?study=gates) · [Odd-site change check](index.html?study=changes)

Two populations of initial chains share the same chain length, observation, observation time and reading order. The two panels can use different local rules. Each site updates simultaneously by XOR with the value of its rule on its two left neighbors, with zeros outside the left boundary. Site zero is leftmost. Rule numbers use least significant bit for neighbor pair 00 and most significant for 11, with the nearer neighbor first.

## A finite answer drawn in space

After a specified number of cells have been read, a single reading has an answer for each possible assignment of the remaining cells. A section of the drawing collects every reading with the same entire sequence of answers. Its radial coordinate samples that sequence on a circle. All sections share the same angular convention, the reflected binary Gray order of endings in the selected reading order. Consecutive samples differ in one unread bit when at least one bit remains. Its depth, as a fraction of the total occupied depth, equals the proportion of readings in the section. The interface counts distinct sections by exact equality before constructing the drawing.

The separation of sections makes distinctions between future answers inspectable. The interpolation, tilt, spacing and camera angle are aesthetic decisions. In particular, the length of a contour cannot be interpreted as a memory bound. Reordering the endings would alter the contours while preserving all residual equivalence classes. That freedom suggests a question about representation: among admissible coordinate orders, which minimizes the number of radial changes, and how does that compare with the order minimizing the number of distinct sections? No observation of human perceptual effort has been made.

## Evolution in time

The second view follows a single initial state. A curve follows one site down the sequence of time steps. Bright and dim points encode one and zero. Short marks at the top identify cells read in the selected order. Changing only the reading order leaves the trajectory and its answer intact even as the classification of possible readings changes. The evolution view thereby gives a control for a distinction made visible in the response view.

For the nine-cell last-site observation at time seven, rule 4 gives 32 sections after reading the five even sites and five sections after reading the four odd sites. The cuts in this comparison have different lengths. A second preset controls the length of the reading as well. With eight cells and four even sites read first, the odd-site change check after one step gives two sections for rule 6 and sixteen for rule 14. Each panel reports a count of possible persistent memory states at the selected cut in the specified exact reading model. Enumeration in the study constructs these states explicitly. Its rendering time does not estimate optimal observer work.

## Visual provenance and checks

The atlas sets its paired studies against near-black fields with pale text, restrained violet and mint, and Space Grotesk typography. The paired view adopts that language and uses generated contours and trajectories derived from the reversible chain. The font and Open Font License are embedded. [Atlas source](https://github.com/sachavarria/The-Morphology-of-Information-/blob/main/index.html) · [Established atlas](https://sachavarria.github.io/The-Morphology-of-Information-/)

Browser viewport emulation at 390 × 844 and 844 × 390 CSS pixels gave vertically stacked and side-by-side panels respectively, with no horizontal overflow. Canvas sizes were 336 × 187 and 351 × 200 CSS pixels. Both rendered nonempty, loaded Space Grotesk, and updated the state counts after changes of order, chain length and cut. Evolution displayed the selected trajectory's answer in both viewports. This is an emulated layout check. Testing on physical iOS devices and perceptual studies remain open.

Run `node check_visual.cjs` from this directory for a finite cross-check of the actual model inside the HTML. The independent cell-array evolution and grouping by ordinary suffix order test both state dynamics and the multiset of class sizes. Results appear in [visual-results.txt](visual-results.txt).
