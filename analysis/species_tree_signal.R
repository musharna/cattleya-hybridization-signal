#!/usr/bin/env Rscript
# Species-level tree construction and phylogenetic signal tests.
#
# This reproduces Figure 3 and the species-level row of Table 2 from the
# derived tables in data/ alone -- no access to the raw scrape is needed.
#
# The procedure is taken verbatim from the submitted analysis
# (analysis/OrchidRootsPlots.Rmd, recovered from the scraper repository).
# The only change is the input: that file read the raw species CSV and
# computed `LowestRank` from the multi-line "Subgeneric Ranks" field, whereas
# this script reads the already-reduced `LastSubgenus` column, which
# derive_tables.R computes the same way (last non-empty line of that field).
#
# Usage, from analysis/:   Rscript species_tree_signal.R

suppressPackageStartupMessages({
  library(ape); library(phytools); library(phylosignal)
  library(phylobase); library(viridis)
})

set.seed(1)                       # permutation tests below use 999 replicates
out_dir <- "../figures_regenerated"
dir.create(out_dir, showWarnings = FALSE)

# ---- inputs ---------------------------------------------------------------
tree_lowestrank <- read.tree("../data/cattleya_subgeneric.nwk")
sp <- read.csv("../data/species_hybrid_counts.csv", stringsAsFactors = FALSE)
sp$SpeciesName <- gsub(" ", "_", sp$Binomial)

cat(sprintf("subgeneric tree: %d tips\n", length(tree_lowestrank$tip.label)))
cat(sprintf("species records: %d\n", nrow(sp)))

# ---- build the species-level tree -----------------------------------------
# Each subgeneric rank tip is replaced by a star polytomy of its species.
rank_to_species <- split(sp$SpeciesName, sp$LastSubgenus)

# A rank holding a single species becomes that species' tip: the submitted
# code expressed this as bind.tree() of a zero-edge phylo, which under
# ape 5.7.1 does not terminate. Renaming the tip is what that bind resolved
# to -- binding the first singleton left the tip count unchanged at 10,
# i.e. it substituted the tip rather than adding one.
tree_species <- tree_lowestrank
for (rank in names(rank_to_species)) {
  s <- rank_to_species[[rank]]
  idx <- which(tree_species$tip.label == rank)
  if (length(idx) == 0) next          # rank absent from the subgeneric tree
  if (length(s) == 1) {
    tree_species$tip.label[idx] <- s
  } else {
    tree_species <- bind.tree(
      tree_species, stree(length(s), tip.label = s, type = "star"),
      where = idx)
  }
}
tree_species <- drop.tip(
  tree_species,
  intersect(tree_species$tip.label, tree_lowestrank$tip.label))

# Ranks absent from the subgeneric tree (Crispae, Stellata) never get bound,
# so their species drop out here -- matching the submitted analysis, which
# excluded Stellata explicitly and restricted to tips present in the tree.
dropped <- setdiff(sp$SpeciesName, tree_species$tip.label)
cat(sprintf("species-level tree: %d tips (%d dropped: ranks not in tree)\n",
            length(tree_species$tip.label), length(dropped)))

# ---- trait vector ---------------------------------------------------------
hybrid_counts <- setNames(sp$Descendants, sp$SpeciesName)
common <- intersect(tree_species$tip.label, names(hybrid_counts))
tree_phylo <- drop.tip(tree_species, setdiff(tree_species$tip.label, common))
hybrid_counts <- hybrid_counts[common]

# ---- branch lengths -------------------------------------------------------
tree_phylo$edge.length <- rep(1, nrow(tree_phylo$edge))
tree_grafen <- compute.brlen(tree_phylo, method = "Grafen")

# ---- Table 2, species-level row -------------------------------------------
K_result      <- phylosig(tree_grafen, hybrid_counts, method = "K",      test = TRUE)
lambda_result <- phylosig(tree_grafen, hybrid_counts, method = "lambda", test = TRUE)

trait_df <- data.frame(hybrids = hybrid_counts[tree_grafen$tip.label])
rownames(trait_df) <- tree_grafen$tip.label
tree4d <- phylo4d(tree_grafen, trait_df)
ps <- phyloSignal(tree4d, methods = c("K", "I", "Cmean"), reps = 999)

cat("\n--- Table 2, species-level row ---\n")
cat(sprintf("Blomberg's K       %.3f  (p = %.3f)\n", K_result$K, K_result$P))
cat(sprintf("Pagel's lambda     %.3f  (p = %.3g)\n",
            lambda_result$lambda, lambda_result$P))
cat(sprintf("Moran's I          %.3f  (p = %.3f)\n", ps$stat$I,     ps$pvalue$I))
cat(sprintf("Abouheif's Cmean   %.3f  (p = %.3f)\n", ps$stat$Cmean, ps$pvalue$Cmean))

write.csv(
  data.frame(statistic = c("Blomberg K", "Pagel lambda", "Moran I", "Abouheif Cmean"),
             value = c(K_result$K, lambda_result$lambda, ps$stat$I, ps$stat$Cmean),
             p     = c(K_result$P,  lambda_result$P,     ps$pvalue$I, ps$pvalue$Cmean)),
  file.path(out_dir, "table2_species_level.csv"), row.names = FALSE)

# ---- Figure 3 -------------------------------------------------------------
tree_clean <- tree_phylo
tree_clean$edge.length <- rep(1, nrow(tree_clean$edge))
tree_clean <- compute.brlen(tree_clean, method = "Grafen")

abbrev <- setNames(
  gsub(" ", "_", sub("^([A-Za-z])[a-z]+\\s+", "\\1. ", sp$Binomial)),
  sp$SpeciesName)
tree_clean$tip.label <- abbrev[tree_clean$tip.label]
counts_clean <- setNames(hybrid_counts, abbrev[names(hybrid_counts)])
counts_clean <- counts_clean[tree_clean$tip.label]

stopifnot(all(tree_clean$tip.label == names(counts_clean)))
stopifnot(!any(is.na(counts_clean)))

png(file.path(out_dir, "fig3_hybrid_counts_on_species_tree.png"),
    width = 2200, height = 2600, res = 220)
log_counts <- setNames(log1p(counts_clean), names(counts_clean))
cm <- setMap(contMap(tree_clean, log_counts, plot = FALSE), viridis(100, option = "D"))
# plot.contMap resets par(), so mar must be passed to it and xpd set AFTER --
# setting either beforehand is silently discarded and the count column then
# falls outside the clip region and is dropped entirely.
plot(cm, fsize = 0.6, legend = 0.7, outline = FALSE, mar = c(5, 2, 5, 13))
par(xpd = NA)
coords <- get("last_plot.phylo", envir = .PlotPhyloEnv)
n <- length(tree_clean$tip.label)
# The count column must clear the WIDEST tip label, not a fixed fraction of
# tree depth -- tip labels vary in width, so a fixed offset overlaps the long
# ones (C. alvarenguensis, C. amethystoglossa) while leaving the short ones far away.
label_w <- max(strwidth(tree_clean$tip.label, cex = 0.6, font = 3))
text(x = max(coords$xx[1:n]) + label_w + strwidth("00", cex = 0.6),
     y = coords$yy[1:n],
     labels = counts_clean[tree_clean$tip.label], cex = 0.6, font = 2, adj = 0)
title("Hybridization Counts Across Cattleya Species Tree (log scale)", line = 2)
invisible(dev.off())

cat(sprintf("\nwrote %s/fig3_hybrid_counts_on_species_tree.png\n", out_dir))
cat(sprintf("wrote %s/table2_species_level.csv\n", out_dir))
