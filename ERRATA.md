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

### Figure 3 and the species-level row of Table 2 have no surviving code

The committed notebook contains no species-level tree construction and no Moran's I or
Abouheif's C<sub>mean</sub> calls; its two `phylosig` calls run Blomberg's K and Pagel's λ
against the subgeneric tree, which is the null row of Table 2. The species-level results and
Figure 3 were produced outside it and that code was not preserved. The reported numbers stand;
this repository cannot currently regenerate them. See the scope table in the [README](README.md).
