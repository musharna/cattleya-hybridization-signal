# _Cattleya_ Hybridization: Trends Over Time and Phylogenetic Signal

Does the tendency to hybridize cluster on the _Cattleya_ phylogeny, or does it mostly reflect where
breeders happened to look?

Course project write-up (bioinformatics), May 2025, by Jaret Arnold.
The full write-up is in [writeup.md](writeup.md), the submitted `.docx` is in [`docs/`](docs/),
and post-submission corrections are listed in [CORRECTIONS.md](CORRECTIONS.md).

## What this is

The Royal Horticultural Society has registered orchid hybrids since the 1850s, which makes
_Cattleya_ an unusually complete record of roughly 170 years of deliberate hybridization. This
project scrapes that record, covering 19,577 hybrid records and 141 species records (132 after
removing infraspecific taxa). It asks how hybridization and hybrid complexity have changed over
time, then tests whether hybrid counts are phylogenetically clustered.

## Results

Hybridization and complexity both rose and then partly reversed. Early crosses were overwhelmingly
primary, meaning species crossed with species. By the mid-20th century "highly complex" crosses of
hybrid with hybrid dominated, peaking during the _Cattleya_ corsage era and collapsing as corsages
went out of fashion. The three classes are roughly balanced again today. Mean ancestors per hybrid
climbed from about 2 in the 1850s to about 25 by the 1980s and has plateaued since.

<p align="center"><img src="figures/fig1_hybridization_trends_by_type.png" width="85%" alt="Hybridization trends over time by hybrid type"></p>

Hybrid counts are phylogenetically clustered, but only the species-level tree detects it. On a
subgeneric-rank tree every statistic was non-significant. Rebuilt as a species-level tree, with
species attached as polytomies within their Van den Berg subgeneric ranks and Grafen branch lengths
applied, three of the four tests became significant:

| Tree                   | Blomberg's K    | Pagel's λ         | Moran's I        | Abouheif's C<sub>mean</sub> |
| ---------------------- | --------------- | ----------------- | ---------------- | --------------------------- |
| Subgeneric rank tree   | 0.768 (p=0.405) | ~0.00004 (p=1)    | −0.105 (p=0.478) | −0.095 (p=0.338)            |
| Species level tree     | 0.184 (p=0.339) | 0.305 (p=2.2e−06) | 0.13 (p=0.001)   | 0.32 (p=0.001)              |

That contrast is itself a methodological result, since collapsing species into subgeneric ranks
destroyed the signal. Blomberg's K remained non-significant on both trees, which is expected given
that the tree is largely polytomous and K is sensitive to branch-length structure that Grafen
scaling only approximates.

<p align="center"><img src="figures/fig3_hybrid_counts_on_species_tree.png" width="90%" alt="Hybrid counts painted on the Cattleya species tree"></p>

## Reproducing

Everything below runs from the derived tables in `data/` and needs no access to the raw scrape:

```r
# from analysis/
Rscript figures_from_derived.R    # Figures 1, 2, S1, S2      (ggplot2, dplyr)
Rscript species_tree_signal.R     # Figure 3 + Table 2 row 2  (ape, phytools, phylosignal, phylobase, viridis)
```

Output is written to `figures_regenerated/`.

### Scope

| Output                       | Reproducible    | From                                             |
| ---------------------------- | --------------- | ------------------------------------------------ |
| Figure 1, 2, S1, S2          | yes             | `figures_from_derived.R` and `data/`             |
| Figure 3                     | yes             | `species_tree_signal.R` and `data/`              |
| Table 2, species-level row   | yes, to ~2 s.f. | `species_tree_signal.R` and `data/`              |
| Table 2, subgeneric-rank row | yes             | `orchidrootsplotting.Rmd` (needs the raw scrape) |

The species-level statistics regenerate to within rounding of the published values and all four
conclusions are unchanged (K 0.210 vs 0.184, λ 0.337 vs 0.305, Moran's I 0.120 vs 0.13,
C<sub>mean</sub> 0.323 vs 0.32). The small differences come from branch lengths rather than from the
data. Abouheif's C<sub>mean</sub> is branch-length invariant and reproduces exactly, which fixes the
species set and topology as identical to the original run.

`orchidrootsplotting.Rmd` and `OrchidRootsPlots.Rmd` are the two submitted analysis files, unchanged
apart from having their hardcoded Windows input paths rewritten as relative paths. Both read the raw
scrape, which is not distributed here, so neither runs from a clone. They are kept as the record of
what was submitted, and `species_tree_signal.R` is the runnable equivalent of the second one. The
rendered notebook from the original run is committed as
[`analysis/orchidrootsplotting.nb.html`](analysis/orchidrootsplotting.nb.html).

## Repository layout

```
writeup.md      full write-up, figures and tables inline
CORRECTIONS.md  post-submission corrections to the write-up
docs/           original submitted .docx and the earlier research proposal
figures/        figure panels as PNG (Fig 1-3, Fig S1-S2)
analysis/       derive_tables.R, figures_from_derived.R, species_tree_signal.R,
                the two submitted Rmds, and the rendered notebook
scraper/        the Selenium scraper used to collect the source data
data/           derived tables and the two Newick tree inputs (see data/README.md)
```

## Data provenance

Derived from a scrape of [orchidroots.com](https://www.orchidroots.com/) taken on 12 March 2025,
which republishes the RHS International Orchid Register.

The raw scrape is not distributed here. `data/` contains only derived aggregates and carries no grex
names, parentage strings, registrants or source links. The reasoning is set out in
[`data/README.md`](data/README.md). In short, copying the register for non-commercial research is
well covered, but republishing a substantial part of a UK-maintained database is a different act and
an unnecessary one.

The scraper used to collect it is vendored here as [`scraper/scraper_v1.0.py`](scraper/) and also
lives in its own repository, [`musharna/OrchidRootsScraper`](https://github.com/musharna/OrchidRootsScraper).

## License

Text and figures © 2025 Jaret Arnold. Analysis code is available under the MIT License
([`LICENSE`](LICENSE)). The scraped data is third-party content, discussed in `data/README.md`.
