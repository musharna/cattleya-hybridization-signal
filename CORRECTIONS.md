# Corrections

Changes made to [writeup.md](writeup.md) after submission. The submitted document itself is
preserved unchanged in [`docs/`](docs/), so this file records only what differs.

Each replacement below was checked against CrossRef and OpenAlex, comparing first-author surname,
year, title and venue against the DOI, rather than corrected from memory.

## Citations

Abbott et al. (2013). The reference was right but the DOI attached to it was not. The printed
`10.1111/jeb.12099` resolves to Brix and Grosell (2013), a paper on *Cyprinodon* fish. Corrected to
`10.1111/j.1420-9101.2012.02599.x`.

Lexer and Widmer (2008). The printed DOI was one digit off and resolved to Butlin et al. (2008).
Corrected to `10.1098/rstb.2008.0078`. Journal, volume and pages were already correct.

Van den Berg (2014). Printed with the wrong title, journal, volume and pages. No paper of that
title exists in the *Botanical Journal of the Linnean Society*. The actual paper is "Reaching a
compromise between conflicting nuclear and plastid phylogenetic trees: a new classification for the
genus *Cattleya*", *Phytotaxa* 186(2), 75-86, `10.11646/phytotaxa.186.2.2`. This is the source of the
subgeneric classification the species-level tree is built from, so it is the most consequential of
these corrections.

Cribb and Butterfield (2002). Removed. The book as printed conflates two different titles: Cribb
wrote *The Genus Paphiopedilum* and Cribb and Butterfield together wrote *The Genus Pleione*. Neither
carries the subtitle given, and neither was published by the RHS. It was also cited in the Abstract
for a claim about RHS documentation of *Cattleya* hybrids, which a book about *Paphiopedilum* cannot
support. The claim is now cited to the RHS International Orchid Register.

Jangyukala and Hemanta (2021). Removed. No record of this article was found in CrossRef, and no
journal by that name was found either. The claim it supported, that orchid hybrids include
intergeneric crosses spanning three to five genera, is now cited to the RHS register, which
documents them.

Arnold (1997). Added. *Natural Hybridization and Evolution* (Oxford University Press) is quoted
directly in the Introduction but was missing from the reference list.

Motes (2021) is kept as printed. It does not appear in CrossRef, but *Orchids* is a society magazine
that does not issue DOIs and is not indexed there, so its absence is not evidence against it. Volume
90 does correspond to 2021.

## Reproducibility note

The species-level statistics in Table 2 regenerate close to the published values without landing
exactly on them: K 0.210 against 0.184, lambda 0.337 against 0.305, Moran's I 0.120 against 0.13,
and C<sub>mean</sub> 0.323 against 0.32. All four conclusions are unchanged.

The difference comes from branch lengths rather than from the underlying data. Abouheif's
C<sub>mean</sub> is branch-length invariant and reproduces exactly at 0.3233 under every scaling
tested, which fixes the species set and topology as identical to the original run, while the three
branch-length-dependent statistics drift. Grafen's rho was deliberately left alone, since tuning a
parameter against the number you are trying to reproduce would make any agreement meaningless.

One deviation from the submitted code was necessary. A rank holding a single species is attached by
renaming the tip rather than by calling `bind.tree()` on a zero-edge phylo, which does not terminate
under ape 5.7.1. The two are equivalent here, since binding the first singleton left the tip count
unchanged and so substituted the tip rather than adding one.
