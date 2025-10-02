### Launch an interactive session on ARC:
     salloc --mem=20G -c 8 -N 1 -n 1  -t 04:00:00
### Collecting data
#### Species trees
Upload the environment.xlsx file to /home/lianchun.yi1/data/pfam_reconstruction/PF00122/ale. And run:

     cd /home/lianchun.yi1/data/pfam_reconstruction/PF00122/ale
     python collect_rooted_species_tree.py
This script copies the best rooted species tree from /work/...... to the working directory. 
Copied files will be named as {subtree}_BestRoot.newick.
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
     #SBATCH --mem=64G
     #SBATCH --time=24:00:00                       # speed 2 min/file
     #SBATCH --mail-user=lianchun.yi1@ucalgary.ca
     #SBATCH --mail-type=END                       # Send the type: <BEGIN><FAIL><END>
     pwd; hostname; date

     cd /home/lianchun.yi1/data/pfam_reconstruction/PF00122/ale
     find ./*.ufboot | xargs -n 1 -P 2 -I {} ALEobserve {}

Output files will end with *.ale.
### Gene tree and species tree reconciliation
reconcile_tree.slurm

     #!/bin/bash
     #SBATCH --job-name=RT_ATPase
     #SBATCH --output=%x.log
     #SBATCH --nodes=1
     #SBATCH --ntasks=8                             # CPU efficiency： 795.5% / 8 = 99%
     #SBATCH --cpus-per-task=1
     #SBATCH --partition=bigmem                
     #SBATCH --mem=1000G
     #SBATCH --time=24:00:00
     #SBATCH --mail-user=lianchun.yi1@ucalgary.ca
     #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END><ALL>
     pwd; hostname; date
     
     cd /home/lianchun.yi1/data/pfam_reconstruction/PF00122

     mpirun -np 8 ALEml_undated ../bac120_r214.tree.with_missing_leaves.tree.clean ./ATPase.filtered.aln.faa.ufboot.ale separators="."

