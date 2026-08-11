# _Cattleya_ Hybridization: Trends Over Time and Phylogenetic Signal

Does the tendency to hybridize cluster on the _Cattleya_ phylogeny, or is it just where breeders happened to look?

Course project write-up (bioinformatics), May 2025 — Jaret Arnold.

📄 **[Read the full write-up →](writeup.md)** · original submitted `.docx` in [`docs/`](docs/) · corrections in [`ERRATA.md`](ERRATA.md)

> The write-up is reproduced as submitted. A later audit found citation defects in it — two wrong DOIs, a miscited classification paper, and one reference that appears not to exist. Rather than quietly editing the record, they are documented in [`ERRATA.md`](ERRATA.md).

---

## What this is

The Royal Horticultural Society has registered orchid hybrids since the 1850s, which makes _Cattleya_ an unusually complete record of ~170 years of deliberate, human-driven hybridization. This project scrapes that record (19,577 hybrid records, 141 species records — 132 after removing infraspecific taxa), asks how hybridization and hybrid _complexity_ have changed over time, and then tests whether hybrid counts are phylogenetically clustered.

## Headline results

**Hybridization and complexity both rose, then partly reversed.** Early crosses were overwhelmingly primary (species × species). By the mid-20th century "highly complex" (hybrid × hybrid) crosses dominated, peaking during the _Cattleya_ Corsage Era and collapsing as corsages fell out of fashion. Today the three classes are roughly balanced again. Mean ancestors per hybrid climbed from ~2 in the 1850s to ~25 by the 1980s and has plateaued since.

<p align="center"><img src="figures/fig1_hybridization_trends_by_type.png" width="85%" alt="Hybridization trends over time by hybrid type"></p>

**Hybridization is phylogenetically clustered — but only the species-level tree can see it.** Tested on a subgeneric-rank tree, every statistic was non-significant. Rebuilt as a species-level tree (species attached as polytomies within their Van den Berg subgeneric ranks, Grafen branch lengths), three of four tests became significant:

| Tree                   | Blomberg's K    | Pagel's λ             | Moran's I          | Abouheif's C<sub>mean</sub> |
| ---------------------- | --------------- | --------------------- | ------------------ | --------------------------- |
| Subgeneric rank tree   | 0.768 (p=0.405) | ~0.00004 (p=1)        | −0.105 (p=0.478)   | −0.095 (p=0.338)            |
| **Species level tree** | 0.184 (p=0.339) | **0.305 (p=2.2e−06)** | **0.13 (p=0.001)** | **0.32 (p=0.001)**          |

That contrast is itself the methodological result: collapsing species into subgeneric ranks destroyed the signal. Blomberg's K stayed non-significant on both trees, which is expected given the tree is largely polytomous and K is sensitive to branch-length structure that Grafen scaling only approximates.

<p align="center"><img src="figures/fig3_hybrid_counts_on_species_tree.png" width="90%" alt="Hybrid counts painted on the Cattleya species tree"></p>

## Reproducing

Figures 1, 2, S1 and S2 regenerate from the derived tables in `data/`, with no access to the raw scrape:

```r
# from analysis/
Rscript figures_from_derived.R
```

Requires `ggplot2` and `dplyr`. Output is written to `figures_regenerated/`.

### Scope — what is and is not reproducible here

| Output                         | Reproducible | From                                             |
| ------------------------------ | ------------ | ------------------------------------------------ |
| Figure 1, 2, S1, S2            | yes          | `figures_from_derived.R` + `data/`               |
| Table 2, subgeneric-rank row   | yes          | `orchidrootsplotting.Rmd` (needs the raw scrape) |
| **Figure 3**                   | **no**       | code not preserved                               |
| **Table 2, species-level row** | **no**       | code not preserved                               |

The species-level tree — the one that produced the significant Pagel's λ, Moran's I and Abouheif's C<sub>mean</sub>, and Figure 3 — was built outside the committed notebook, and that code did not survive. `orchidrootsplotting.Rmd` contains no species-tree construction and no Moran's I or Abouheif calls; its two `phylosig` calls run Blomberg's K and Pagel's λ against the _subgeneric_ tree, which is the null row of Table 2. The species-level numbers in the write-up stand as reported, but this repository cannot currently regenerate them.

`data/species_hybrid_counts.csv` holds the trait vector those tests were run on, and `data/cattleya_subgeneric.nwk` holds the subgeneric topology they were built from, so the analysis is reconstructable by someone willing to rebuild the tree.

> **Note on the code:** `orchidrootsplotting.Rmd` is the submitted analysis, unchanged except that its hardcoded Windows input paths were rewritten to relative paths. It reads the raw scrape, which is not distributed here, so it will not run from a clone as-is — it is kept as the record of what was actually submitted. The rendered notebook from the original run is committed as [`analysis/orchidrootsplotting.nb.html`](analysis/orchidrootsplotting.nb.html).

## Repository layout

```
writeup.md   full write-up, figures and tables inline
ERRATA.md    defects found in a post-hoc audit of the submitted text
docs/        original submitted .docx + the earlier research proposal
figures/     figure panels as PNG (Fig 1-3, Fig S1-S2)
analysis/    derive_tables.R, figures_from_derived.R, the submitted Rmd,
             and the rendered notebook
data/        derived tables + the two Newick tree inputs (see data/README.md)
```

## Data provenance

Derived from a scrape of [orchidroots.com](https://www.orchidroots.com/) taken on **12 March 2025**, which republishes the RHS International Orchid Register.

**The raw scrape is not distributed here** — `data/` contains only derived aggregates, carrying no grex names, parentage strings, registrants or source links. The reasoning is in [`data/README.md`](data/README.md); the short version is that copying the register for non-commercial research is well covered, but republishing a substantial part of a UK-maintained database is a different act and an unnecessary one.

The scraper itself lives in a separate repository: [`musharna/OrchidRootsScraper`](https://github.com/musharna/OrchidRootsScraper).

## License

Text and figures © 2025 Jaret Arnold. Analysis code is available under the MIT License ([`LICENSE`](LICENSE)). The scraped data is third-party content — see `data/README.md`.
