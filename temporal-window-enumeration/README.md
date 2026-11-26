# Temporal Window Enumeration

**Candidate original mathematical contribution pending independent verification and confirmation of publication priority.** Investigation led by the research prompt of S.A. Chavarría, 25 November 2026.

How many cyclic signals reveal their phase as evenly as arithmetic permits at every observation length? For fixed alphabet size and a fixed number of missing identifying windows, the candidate theorem expresses the count relative to the full de Bruijn count as a sum of determinants indexed by short-context permutations. It gives a rational limit and a residue-class polynomial correction. The result concerns information recoverability under partial observation. It establishes no cryptographic hardness assumption.

| Item | Archive file |
|---|---|
| Original research note, unchanged | [Original](original/Temporal-window-enumeration.md) |
| Typeset manuscript and editable source | [PDF](manuscript/manuscript.pdf) · [LaTeX](manuscript/manuscript.tex) |
| Verification and recorded output | [Python](verification/verify.py) · [Results](verification/results.txt) |
| Internal proof audit | [Audit](assessment/proof-audit.md) |
| Candidate selection, literature and priority | [Assessment](assessment/literature-and-novelty.md) |
| Original commission and documented discovery | [Prompt](provenance/original-prompt.txt) · [Process and resources](provenance/discovery.md) |
| Presentation-ready explanation | [Three-minute talk](presentation/talk.md) |
| File integrity | [SHA-256 manifest](SHA256SUMS) |

From this directory run:

```sh
python3 verification/verify.py > /tmp/temporal-window-results.txt
diff -u verification/results.txt /tmp/temporal-window-results.txt
sha256sum -c SHA256SUMS
```

Use Python 3.9 or later with assertions enabled. A matching run has 26 output rows and an empty diff. Full graph determinants were checked in 21 cases. Nine of those and five additional cases were checked by direct word enumeration. All-scale claims for arbitrary order, polynomial corrections and publication priority remain subjects for independent review. The original study contains no Lean certificate. Subsequent corrections should appear as separate dated files or commits that retain the original note.
