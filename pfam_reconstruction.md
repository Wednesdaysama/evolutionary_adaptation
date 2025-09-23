### Collecting data
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
