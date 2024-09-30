import pandas as pd
from Bio import Phylo
import matplotlib.pyplot as plt
import os
import matplotlib.patches as mpatches

file_path = r"D:\OneDrive - University of Calgary\Exp_EvolutionaryAdaptation\alkaline_clusters_1500_N50.xlsx"
sheet_name = 'alkaline_clusters_1500_6'
df = pd.read_excel(file_path, sheet_name=sheet_name)

selected_columns = df.iloc[:, [6, 8, 9]]

tree_file = r"D:\OneDrive - University of Calgary\Exp_EvolutionaryAdaptation\cluster_results\1\iqtree_1000.txt"
output_file = os.path.join(os.path.dirname(tree_file), "UnrootedTree_1000_backup.png")
new_tree_file = os.path.join(os.path.dirname(tree_file), "updated_UnrootedTree_1000.txt")

if os.path.exists(tree_file):
    tree = Phylo.read(tree_file, "newick")

    replacements = dict(zip(selected_columns.iloc[:, 1], selected_columns.iloc[:, 2]))

    for clade in tree.get_terminals():
        if clade.name in replacements:

            clade.name = replacements[clade.name].replace(" ", "_")

    fig = plt.figure(figsize=(13, 30)) #fig = plt.figure(figsize=(13, 7))
    axes = fig.add_subplot(1, 1, 1)

    label_colors = {}
    for _, row in selected_columns.iterrows():
        clade_name = row[2].replace(" ", "_")
        category = row[0]

        if category == "alkaline":
            label_colors[clade_name] = "green"
        elif category == "marine":
            label_colors[clade_name] = "blue"
        else:
            label_colors[clade_name] = "black"

    Phylo.draw(tree, axes=axes, label_colors=label_colors)

    # Create legend
    legend_labels = {
        "Alkaline": "green",
        "Marine": "blue",
        "Others": "black"
    }

    patches = [mpatches.Patch(color=color, label=label) for label, color in legend_labels.items()]
    axes.legend(handles=patches, loc='lower right')

    # Save the figure
    fig.savefig(output_file)
    print(f"Updated tree with colors and legend saved to: {output_file}")

    # Save the updated tree to a new file
    Phylo.write(tree, new_tree_file, format="newick")
    print(f"Updated tree saved to: {new_tree_file}")

    plt.close(fig)
else:
    print(f"File {tree_file} does not exist.")
