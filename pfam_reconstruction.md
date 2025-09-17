#### Collecting data
     cp /work/ebg_lab/eb/ancestral_reconstruction/pf_seq/*_seq.aln.faa ~/data/pfam_reconstruction
#### Create ultrafast bootstrap gene tree distributions
bootstrap_gene_tree.slurm

     #!/bin/bash
     #SBATCH --job-name=BootstrapGeneTree
     #SBATCH --output=%x.log
     #SBATCH --nodes=1
     #SBATCH --ntasks=1
     #SBATCH --cpus-per-task=16
     #SBATCH --mem=100GB
     #SBATCH --time=100:00:00
     #SBATCH --mail-user=lianchun.yi1@ucalgary.ca
     #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
     pwd; hostname; date

     cd ~/data/pfam_reconstruction

     find ./*seq.aln.faa | xargs -n 1 -P 2 -I {} iqtree2 -s {} -m MFP -madd LG+C20,LG+C60 -B 1000 -wbtl -nt 16

Output files will end with *.faa.ufboot

