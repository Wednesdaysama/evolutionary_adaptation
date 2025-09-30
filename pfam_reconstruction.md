### Launch an interactive session on ARC:
     salloc --mem=20G -c 8 -N 1 -n 1  -t 04:00:00
### Collecting data
#### Species trees
Upload the environment.xlsx file to /home/lianchun.yi1/data/pfam_reconstruction/PF00122/ale. And run:

     python collect_rooted_species_tree.py
This script copies the best rooted species trees from /work/...... to the working directory.


     cp /work/ebg_lab/eb/ancestral_reconstruction/pf_seq/*_seq.aln.faa ~/data/pfam_reconstruction
     python extract_alkaline_sequences.py ATPase # It only extracts protein sequences that are in the alkaline subclade of its Pfam tree. Output file will be named as ATPase.filtered.aln.faa.
### Create ultrafast bootstrap gene tree distributions
bootstrap_gene_tree.slurm

     #!/bin/bash
     #SBATCH --job-name=BootstrapGeneTree
     #SBATCH --output=%x.log
     #SBATCH --nodes=1
     #SBATCH --ntasks=1
     #SBATCH --cpus-per-task=32
     #SBATCH --mem=100GB
     #SBATCH --time=24:00:00                      # speed: 12~24 hours/file
     #SBATCH --mail-user=lianchun.yi1@ucalgary.ca
     #SBATCH --mail-type=END                       # Send the type: <BEGIN><FAIL><END>
     pwd; hostname; date

     cd ~/data/pfam_reconstruction

     find ./*filtered.aln.faa | xargs -n 1 -P 2 -I {} iqtree2 -s {} -m MFP -madd LG+C20,LG+C60 -B 1000 -wbtl -nt 32 -redo

Output files will end with *.faa.ufboot.
### Create ale objects
create_ale_objects.slurm

     #!/bin/bash
     #SBATCH --job-name=PF04066_CreateObjects
     #SBATCH --output=%x.log
     #SBATCH --nodes=1
     #SBATCH --ntasks=1
     #SBATCH --cpus-per-task=16
     #SBATCH --mem=64G
     #SBATCH --time=01:00:00                       # speed 2 min/file
     #SBATCH --mail-user=lianchun.yi1@ucalgary.ca
     #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
     pwd; hostname; date

     cd /home/lianchun.yi1/data/pfam_reconstruction/PF04066
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

