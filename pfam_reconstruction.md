### Launch an interactive session on ARC:
     salloc --mem=20G -c 8 -N 1 -n 1  -t 04:00:00
### Collecting data
#### Species trees
Upload the environment.xlsx file to /home/lianchun.yi1/data/pfam_reconstruction/PF00122/ale. And run:

     cd /home/lianchun.yi1/data/pfam_reconstruction/PF00122/ale
     python collect_rooted_species_tree.py
This script copies the best rooted species tree from /work/...... to the working directory. Then modifies the name of the leaves. For example: from GCF_003014715_GCF_003014715 to GCF_003014715. New files will be named as {subtree}_BestRoot.newick.
#### multiple sequences aligned genes
Upload a txt file that contains the leaf IDs of the alkaline subcalde. Then run:

     cp ../*_seq.aln.faa ./ # or run: cp /work/ebg_lab/eb/ancestral_reconstruction/pf_seq/PF00122_seq.aln.faa ./ 
     python extract_subtree_sequences.py ATPase 
It only extracts protein sequences for each subtree that are in the alkaline subclade of its Pfam tree. Output files will be named as {subtree}.filtered.aln.faa.

### Create ultrafast bootstrap gene tree distributions
bootstrap_gene_tree.slurm

     #!/bin/bash
     #SBATCH --job-name=ATPase_BS
     #SBATCH --output=%x.log
     #SBATCH --nodes=1
     #SBATCH --ntasks=1
     #SBATCH --cpus-per-task=32
     #SBATCH --mem=50GB
     #SBATCH --time=100:00:00                      # speed: 23 files per day
     #SBATCH --mail-user=lianchun.yi1@ucalgary.ca
     #SBATCH --mail-type=END                       # Send the type: <BEGIN><FAIL><END>
     pwd; hostname; date

     cd ~/data/pfam_reconstruction/PF00122/ale

     find ./*filtered.aln.faa | xargs -n 1 -P 5 -I {} iqtree2 -s {} -m MFP -madd LG+C20,LG+C60 -B 5000 -wbtl -nt 32

Output files will end with *.faa.ufboot. 
NOTE: PF00122 is not present in subtrees 22 and 23_24. There are only 3 sequences in 16_filtered.aln.faa. It makes no sense to perform bootstrap with less than 4 sequences.
### Create ale objects
create_ale_objects.slurm

     #!/bin/bash
     #SBATCH --job-name=ATPase_AO
     #SBATCH --output=%x.log
     #SBATCH --nodes=1
     #SBATCH --ntasks=1
     #SBATCH --cpus-per-task=1
     #SBATCH --mem=30G
     #SBATCH --time=30:00:00                       # speed 2 min/file
     #SBATCH --mail-user=lianchun.yi1@ucalgary.ca
     #SBATCH --mail-type=END                       # Send the type: <BEGIN><FAIL><END>
     pwd; hostname; date

     cd /home/lianchun.yi1/data/pfam_reconstruction/PF00122/ale
     find ./*.ufboot | xargs -n 1 -P 2 -I {} ALEobserve {}

Output files will end with *.ale.
### Gene tree and species tree reconciliation
#### 1. Reconciling against 30 alkaline lineages
Run the following script under /home/lianchun.yi1/data/pfam_reconstruction/PF00122/ale

reconcile_tree.slurm

     #!/bin/bash
     #SBATCH --job-name=RT_ATPase
     #SBATCH --output=%x.log
     #SBATCH --nodes=1
     #SBATCH --ntasks=16                             # CPU efficiency: 99%
     #SBATCH --cpus-per-task=1
     #SBATCH --mem=500G
     #SBATCH --time=04:00:00                         # running time: 30 min
     #SBATCH --mail-user=lianchun.yi1@ucalgary.ca
     #SBATCH --mail-type=END                       # Send the type: <BEGIN><FAIL><END><ALL>
     pwd; hostname; date

     for tree in *_BestRoot.newick; do
         obj=${tree%_BestRoot.newick}
         ale_file="${obj}_filtered.aln.faa.ufboot.ale"

         if [[ -f "$ale_file" ]]; then
             echo "Running ALEml_undated for $obj ..."
             mpirun -np 16 ALEml_undated "./${tree}" "./${ale_file}" separators="."
         else
             echo "Warning: ALE file not found for $obj"
         fi
     done
     
#### 2. Reconciling against the big tree
Constructing a species tree that contains 2644 species.

treeOfMags_iqtree.slurm

    #!/bin/bash
    #SBATCH --job-name=iqtree_2644
    #SBATCH --ntasks=1          
    #SBATCH --cpus-per-task=64
    #SBATCH --mem=500G           
    #SBATCH --time=100:00:00       # tree_of_mags: 15 hours. Iqtree spends ... min
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    cd /home/lianchun.yi1/data/faa_all

    #tree_of_mags --mag_faa_dir ./ --mag_file_extension .faa
    iqtree2 -s ./alignments/concatenated_alignment -nt 64 -bb 1000 -wbtl

Or using FasttreeMP. It only takes 1.5 hours when applying 32 threads:

    cd /home/lianchun.yi1/data/faa_all
    export OMP_NUM_THREADS=32
    FastTreeMP ./alignments/concatenated_alignment > fasttree.treefile

This tree is an **unrooted** species tree. Running AleRax to infer a rooted one.

reconcile_tree.slurm

    #!/bin/bash
    #SBATCH --job-name=RT_ATPase_2644
    #SBATCH --output=%x.log
    #SBATCH --nodes=1
    #SBATCH --ntasks=16
    #SBATCH --cpus-per-task=1             
    #SBATCH --mem=500G
    #SBATCH --time=24:00:00                       # running time: 3 hours
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca
    #SBATCH --mail-type=END                       # Send the type: <BEGIN><FAIL><END><ALL>
    pwd; hostname; date
     
    cd /home/lianchun.yi1/data/pfam_reconstruction/PF00122

    mpirun -np 16 ALEml_undated ../bac120_r214.tree.with_missing_leaves.tree.clean ./ATPase.filtered.aln.faa.ufboot.ale separators="."

### Result interpretation
As the trees above are already rooted and have passed the robustness check. Here, we can just interpret the results.
#### 1. Reconciling against 30 alkaline lineages

     cd /home/lianchun.yi1/data/pfam_reconstruction/PF00122/ale
     ./interpretation.sh ATPase
For every lineage, this script plots a tree file that shows the evolutionary events within this lineage. It also produces a .treefile.

##### Some useful commands
Checking origination events across all lineages:

     for dir in */; do
         csv_file="$dir/Total_copies_at_node/Sum_of_DTLSC_at_each_node.csv"
         if [ -f "$csv_file" ]; then
             echo "Processing $csv_file"
             awk -F',' 'NR>1 && $6 > 0.5' "$csv_file"
         fi
     done


#### 2. Reconciling against the big tree
    source ~/bio/bin/3.10_python-env/bin/activate
    cp ~/ancestral_modified_VK.py ./
    cp ~/branchwise_number_of_events.py ./
    python branchwise_number_of_events.py > dtloc.tsv
    awk -F'\t' '$1 !~ /^[A-Za-z]/ {print $1}' dtloc.tsv | sort -n | awk 'NR==1{min=$1} {max=$1} END{print "python ancestral_modified_VK.py 0.5 " min " " max}' | bash
    cp ~/history_ale.py ./
    python history_ale.py ATPase

print the originatation event that happened at which node

    awk -F',' 'NR>1 && $6 > 0.5' Total_copies_at_node/Sum_of_DTLSC_at_each_node.csv


### Reconciling with [GeneRax](https://github.com/BenoitMorel/GeneRax)
#### Prepare mapping file

    grep "^>" ATPase.filtered.aln.faa \
    | sed -E 's/^>([^ ]*).*/\1/' \
    | awk -F'.' '{species=$1; print species":"$0}' \
    > mapping.link
    
#### Prepare family file

    [FAMILIES]
    - ATPase
    alignment = /home/lianchun.yi1/data/pfam_reconstruction/PF00122/ATPase.filtered.aln.faa
    starting_gene_tree = /home/lianchun.yi1/data/pfam_reconstruction/PF00122/ATPase.filtered.aln.faa.treefile
    mapping = /home/lianchun.yi1/data/pfam_reconstruction/PF00122/mapping.link
    subst_model = GTR+G



Remove internal node ID:
     perl -0777 -pe 's/\)\s*\d+(\.\d+)?\s*:/):/g' bac120_r214.tree.with_missing_leaves.tree.clean > removed_internal_nodeID.newick


