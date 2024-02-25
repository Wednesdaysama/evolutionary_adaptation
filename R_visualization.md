### Read me
This a notebook for the generation of bioinformatics related plots.
Need to click [here](https://posit.cloud/content/yours?sort=name_asc) and upload data files before coding.
Using Ctrl+Enter to run codes.

#### 1. Phylogenetic tree
install.packages("ape")

    library(ape)
    tree <- read.tree("fasttree_file.tree") #read the tree from the file
    set_leaf_color <- function(tree) {
        colors <- sapply(tree$tip.label, function(label) {
            first_letter <- substr(label, 1, 1)
            if (first_letter == "a") {
                "green"
            } else if (first_letter == "m") {
                "blue"
            } else if (first_letter == "o") {
                 "brown"
            } else {
                "black"
            }
        })
        return(colors)
    }
    plot(tree, tip.color = set_leaf_color(tree), cex = 1, no.margin = TRUE, label.offset = 0.005)
    legend("topright", legend = c("alkaline species", "marine species", "other species"),
        col = c("green", "blue", "brown"), pch = 15, bty = "n")
    add.scale.bar(0.42, 1, length = 0.05)