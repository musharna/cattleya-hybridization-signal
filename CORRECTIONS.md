# Corrections

Changes made to [`writeup.md`](writeup.md) after submission. The submitted document itself is
preserved unchanged in [`docs/`](docs/); this file records what differs.

Every replacement below was verified against CrossRef and OpenAlex — first-author surname, year,
title, and venue checked against the DOI — rather than corrected from memory.

## Citations

| # | Reference | Change |
| --- | --- | --- |
| 1 | Abbott et al. (2013) | DOI corrected to `10.1111/j.1420-9101.2012.02599.x`. The printed DOI resolved to Brix & Grosell (2013), a paper on *Cyprinodon* fish. Reference itself was correct. |
| 2 | Lexer & Widmer (2008) | DOI corrected to `10.1098/rstb.2008.0078` (printed one digit off, resolving to Butlin et al. 2008). |
| 3 | Van den Berg (2014) | Title, journal, volume and pages corrected to *Phytotaxa* **186**(2), 75–86, `10.11646/phytotaxa.186.2.2`. No paper of the printed title exists in the printed journal. This is the source of the subgeneric classification, so it is the most consequential of these. |
| 4 | Cribb & Butterfield (2002) | Removed. The book was a conflation of two different titles, neither published by the RHS, and it was cited for a claim about RHS documentation of *Cattleya* hybrids that it does not support. Replaced with the RHS International Orchid Register. |
| 5 | Jangyukala & Hemanta (2021) | Removed. No record of this article, or of the journal, in CrossRef or web search. The claim it supported — intergeneric orchid crosses spanning three to five genera — is now cited to the RHS register, which documents them. |
| 6 | Arnold (1997) | Added. *Natural Hybridization and Evolution* (Oxford University Press) is quoted directly in the Introduction but was missing from the reference list. |

Motes (2021) is retained as printed. It is not in CrossRef, but *Orchids* is a society magazine
that does not issue DOIs and is not indexed there, so absence is not evidence against it; volume
90 does correspond to 2021.

## Reproducibility note

The species-level statistics in Table 2 regenerate close to, but not exactly on, the published
values (K 0.210 vs 0.184; λ 0.337 vs 0.305; Moran's I 0.120 vs 0.13; C<sub>mean</sub> 0.323 vs 0.32).
All four conclusions are unchanged.

The difference is a branch-length effect, not a data difference. Abouheif's C<sub>mean</sub> is
branch-length invariant and reproduces exactly (0.3233 under every scaling tested), which pins the
species set and topology as identical to the original run, while the three branch-length-dependent
statistics drift. Grafen's ρ was deliberately not tuned to close the gap — calibrating a parameter
against the number you are trying to reproduce would make the agreement meaningless.

One deviation from the submitted code was required: a rank holding a single species is attached by
renaming the tip rather than by `bind.tree()` on a zero-edge phylo, which does not terminate under
ape 5.7.1. The two are equivalent here — binding the first singleton left the tip count unchanged,
i.e. it substituted the tip rather than adding one.
