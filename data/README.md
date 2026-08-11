# Data

This directory holds **derived tables only**. The raw orchidroots scrape is not
distributed here — see "Why derived only" below.

## Files

| File                                | Rows   | What it is                                                                                                                 |
| ----------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------- |
| `hybrids_by_year_type.csv`          | 474    | Registered hybrids counted by year × hybrid type. Reproduces Figure 1.                                                     |
| `ancestors_by_year.csv`             | 18,718 | `(Year, Ancestors)` pairs, one per registered hybrid. No names, parentage, registrants or links. Reproduces Figure 2.      |
| `hybrids_per_year.csv`              | 158    | Hybrids registered per year, plus the running cumulative total. Reproduces Figures S1 and S2.                              |
| `species_hybrid_counts.csv`         | 100    | Per-species hybrid descendant counts and terminal subgeneric rank. This is the trait the phylogenetic signal tests run on. |
| `cattleya_subgeneric.nwk`           | —      | Subgeneric-rank topology, hand-built from Van den Berg (2014).                                                             |
| `subtree-ottol-819061-Cattleya.tre` | —      | Open Tree of Life subtree ott819061, retrieved 2025-03-14.                                                                 |

All four derived tables are produced by [`../analysis/derive_tables.R`](../analysis/derive_tables.R),
which is the only script that reads the raw scrape.

## Why derived only

The underlying records come from [orchidroots.com](https://www.orchidroots.com/),
which republishes the Royal Horticultural Society's International Orchid Register.
The RHS is a UK body, and the UK retained the sui generis database right after
Brexit under the Database Regulations 1997 — a right that protects investment in
compiling a database rather than originality, and which a complete genus-level
dump would engage even though the individual facts are not themselves
copyrightable.

Copying the register for non-commercial research analysis is well covered
(s.29A CDPA text-and-data-mining in the UK, fair use in the US). Republishing a
substantial part of it is a different act, and not one this repository needs to
perform: the tables above reproduce every figure in the write-up that has
accompanying code, while containing no grex names, parentage strings,
registrants, originators or source links.

If you want the underlying records, please get them from
[orchidroots.com](https://www.orchidroots.com/) directly rather than from a
2025 snapshot — the register is updated continuously.

`subtree-ottol-819061-Cattleya.tre` comes from the
[Open Tree of Life](https://tree.opentreeoflife.org/), which publishes its
synthetic tree under CC0.

## Cleaning applied before derivation

Reproduced verbatim from the submitted analysis, in `derive_tables.R`:

- hybrids flagged "Synonym of" in `Parentage` are dropped;
- species whose `Binomial` contains `subsp.` or ` var.` are dropped;
- the year 2025 is excluded (a partial year at scrape time);
- species with no subgeneric rank recorded are dropped from the trait table.

Hybrids are classified by capitalisation of each parent's second word: both
parents species → **Primary** (species × species), both parents hybrids →
**Highly Complex** (hybrid × hybrid), otherwise **Complex** (hybrid × species).
After cleaning this gives 18,739 hybrids — 1,468 primary, 5,005 complex and
12,266 highly complex.
