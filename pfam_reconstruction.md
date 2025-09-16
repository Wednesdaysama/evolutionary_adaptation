#### Collecting data
     cp *_seq.unique.faa ~/data/pfam_reconstruction
#### bootstrap_gene_tree.slurm
     #!/bin/bash
     #SBATCH --job-name=BootstrapGeneTree
     #SBATCH --output=%x.log
     #SBATCH --nodes=1
     #SBATCH --ntasks=1
     #SBATCH --cpus-per-task=16
     #SBATCH --mem=80GB
     #SBATCH --time=100:00:00
     #SBATCH --mail-user=lianchun.yi1@ucalgary.ca
     #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
     pwd; hostname; date

     cd ~/data/pfam_reconstruction

     find ./*.faa | xargs -n 1 -P 7 -I {} iqtree2 -s {} -m MFP -madd LG+C20,LG+C60 -B 10000 -wbtl -nt 16

     

