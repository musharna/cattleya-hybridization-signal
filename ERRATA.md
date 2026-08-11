# Errata

[`writeup.md`](writeup.md) reproduces the submitted document verbatim, so its text is left
uncorrected. The defects found in a post-hoc audit are recorded here instead.

Every correction below was verified against CrossRef (author, year, venue, volume, pages)
in August 2026.

## Citations

### 1. Abbott et al. (2013) — wrong DOI

The reference is correct; the DOI attached to it is not.

|                               |                                                                                                                                                         |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Printed                       | `https://doi.org/10.1111/jeb.12099`                                                                                                                     |
| That DOI actually resolves to | Brix et al. (2013), _Evaluation of pre- and post-zygotic mating barriers, hybrid fitness and phylogenetic relationship…_, J. Evol. Biol. **26**:854–866 |
| Correct DOI                   | `https://doi.org/10.1111/j.1420-9101.2012.02599.x`                                                                                                      |

The cited article — Abbott et al., _Hybridization and speciation_, J. Evol. Biol.
**26**(2):229–246 — is real and the volume/page numbers given in the reference list are right.

### 2. Lexer & Widmer (2008) — wrong DOI, one digit

|                               |                                                                                                             |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Printed                       | `https://doi.org/10.1098/rstb.2008.0076`                                                                    |
| That DOI actually resolves to | Butlin et al. (2008), _Sympatric, parapatric or allopatric: the most important way to classify speciation?_ |
| Correct DOI                   | `https://doi.org/10.1098/rstb.2008.0078`                                                                    |

Journal, volume and pages as printed (Phil. Trans. R. Soc. B **363**(1506):3023–3036) are correct.

### 3. Van den Berg (2014) — wrong title, journal, volume and pages

This is the load-bearing citation for the subgeneric classification used to build the
species-level tree, so it matters more than the others.

|              |                                                                                                                                                                                                                              |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Printed      | "A revised infrageneric classification for the genus _Cattleya_ (Orchidaceae)", _Botanical Journal of the Linnean Society_, **175**(1), 95–112                                                                               |
| Problem      | No paper with that title exists in that journal                                                                                                                                                                              |
| Actual paper | Van den Berg, C. (2014). _Reaching a compromise between conflicting nuclear and plastid phylogenetic trees: a new classification for the genus Cattleya._ **Phytotaxa 186**(2). `https://doi.org/10.11646/phytotaxa.186.2.2` |

The substance of the write-up is unaffected — the real paper is the one that proposes the
_Cattleya_ classification the analysis relies on.

### 4. Cribb & Butterfield (2002) — book conflated, and the wrong source for the claim

Printed as: _The Genus Paphiopedilum: Orchid Register and Checklist_, Royal Horticultural Society.

Two problems:

- **The book is a conflation.** Cribb wrote _The Genus Paphiopedilum_; Cribb & Butterfield
  together wrote _The Genus Pleione_. Neither carries the subtitle "Orchid Register and
  Checklist", and neither was published by the RHS.
- **It is cited for the wrong claim.** In the Abstract it supports "Hybridization in the genus
  _Cattleya_ has been documented extensively by the Royal Horticultural Society (RHS)". A book
  about _Paphiopedilum_ (or _Pleione_) does not support a statement about RHS documentation of
  _Cattleya_ hybrids.

The appropriate citation is the RHS International Orchid Register itself
(<https://apps.rhs.org.uk/horticulturaldatabase/orchidregister/orchidregister.asp>),
or _Sander's List of Orchid Hybrids_.

### 5. Jangyukala & Hemanta (2021) — no evidence this reference exists

Printed as: "A review of intergeneric hybridization in orchids: Diversity and conservation
perspectives", _Journal of Orchid Research and Development_, **13**(2), 45–54.

No record of this article was found in CrossRef, and no journal by that name was found in
CrossRef or in a web search. Treat this reference as unverified and most likely erroneous.
The sentence it supports — that orchid hybrids include intergeneric crosses spanning three
to five genera — is uncontroversial and easily re-sourced.

### 6. Motes (2021) — unverified, but plausible

Printed as: "The rise and fall of the corsage orchid", _Orchids: The Bulletin of the American
Orchid Society_, **90**(2), 115–123.

Not found in CrossRef, but _Orchids_ is a society magazine that does not issue DOIs and is not
indexed there, so absence is not evidence of a problem. Volume 90 does correspond to 2021. This
one needs checking against the AOS archive directly; it is listed here for completeness, not as
a known defect.

### 7. Missing reference

Michael Arnold's _Natural hybridization and evolution_ is quoted directly in the Introduction
("involving successful matings in nature between individuals from two populations…") but does
not appear in the reference list. The work is Arnold, M. L. (1997), _Natural Hybridization and
Evolution_, Oxford University Press.

## Analysis

### Figure 3 and the species-level row of Table 2 — correction to an earlier claim in this repository

**An earlier version of this repository stated that the code behind Figure 3 and the
species-level row of Table 2 "was not preserved". That was wrong, and it is withdrawn.**

The code exists. It is `analysis/OrchidRootsPlots.Rmd`, which lived in the separate
[`OrchidRootsScraper`](https://github.com/musharna/OrchidRootsScraper) repository and is now
vendored here. It contains the species-level tree construction, Grafen scaling, `phylosig`
for Blomberg's K and Pagel's λ, `phyloSignal` for Moran's I and Abouheif's C<sub>mean</sub>,
and the `contMap` call that produces Figure 3.

The claim was made after grepping the wrong repository for the wrong symbols — `bind.tip`
and `adephylo`, where the actual code uses `bind.tree` and the `phylosignal` package.

`analysis/species_tree_signal.R` now reruns that procedure from the derived tables in `data/`,
so both outputs regenerate without the raw scrape.

### The regenerated statistics are close to, but not identical to, the published ones

| Statistic                  | Published       | Regenerated     |
| -------------------------- | --------------- | --------------- |
| Blomberg's K               | 0.184 (p=0.339) | 0.210 (p=0.286) |
| Pagel's λ                  | 0.305 (p=2.2e−06) | 0.337 (p=1.3e−06) |
| Moran's I                  | 0.13 (p=0.001)  | 0.120 (p=0.001) |
| Abouheif's C<sub>mean</sub> | 0.32 (p=0.001)  | 0.323 (p=0.001) |

Every conclusion is unchanged: K non-significant, λ strongly significant, Moran's I and
Abouheif's C<sub>mean</sub> significant.

The residual differences are branch-length effects, not data differences:

- Abouheif's C<sub>mean</sub> is invariant to branch lengths. Recomputing it under four
  different branch-length schemes (all edges = 1, and Grafen at ρ = 0.5, 1, 2) returns
  0.3233 every time, matching the published 0.32. Since C<sub>mean</sub> depends only on
  topology, **the species set and tree topology are confirmed identical to the original run.**
- K, λ and Moran's I all move with branch lengths, and that is exactly where the
  differences appear.

So the two runs differ only in the branch lengths handed to the tests. The likely cause is a
version difference in `ape::compute.brlen(method = "Grafen")` or in the node structure left by
the original's singleton `bind.tree` calls; the package versions used in April 2025 were not
recorded. The default Grafen scaling that the submitted code specifies is kept as-is —
tuning ρ until the numbers matched would be fitting the reconstruction to its own target.

Independent confirmation that the underlying data match: the published Figure 3 and the
regenerated one carry the same 98 tips, the same per-species counts, and the same colour-scale
range (0.693–10.452).

### One deviation from the submitted code was necessary

The submitted code attached single-species subgeneric ranks with `bind.tree()` on a
zero-edge `phylo` object. Under ape 5.7.1 that call does not terminate. It is replaced by a
direct tip rename, which is what the original resolved to — in the original run, binding the
first singleton left the tip count unchanged, i.e. it substituted the tip rather than adding
one. The published Figure 3 shows those species (e.g. _C. maxima_) as plain tips, consistent
with this.
