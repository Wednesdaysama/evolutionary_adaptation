
## This is a notebook recording all the steps I have already done. Check here for Dr. Strous' [installation](https://github.com/kinestetika/cloud-computing-for-microbial-ecology/blob/main/cloud_bio_installs.py). For [cheat help](https://github.com/Wednesdaysama/cheat-sheet/blob/main/cheat%20sheet.md).

#### 1.0 Launch an interactive session on ARC:

    salloc --mem=20G -c 1 -N 1 -n 1  -t 04:00:00


<details>
<summary>

## 0 Submit a job to ARC: using blastp as an example.</summary>

    
#### 0.1 basic commands


    arc.nodes  # check the available partition nodes
    nano bicar_blastp.slurm   # write the script (refer the 0.2 for details)  
    sbatch bicar_blastp.slurm # Submit the bicar_blastp.slurm to ARC
    squeue-long -u lianchun.yi1 # check the user's running queue
    arc.job-info <Job ID> # Job Monitoring
    scancel <Job ID> # cancel the job


#### 0.2 Put the content below into the .slurm file:

    #!/bin/bash
    #SBATCH --job-name=bicar      # Job name
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 4 tasks
    #SBATCH --cpus-per-task=1    # Number of CPU cores per task
    #SBATCH --mem=20G            # Job memory request
    #SBATCH --time=4:00:00       # Time limit hrs:min:sec
    #SBATCH --output=blast%j.log  # Standard output and error log
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date
    
    \time blastp -query ~/databases/Soda_lakes_DB_Flag2_no_separator_V5.fasta -db bicar_db -out ~/data/bicar_blastp_run7 -outfmt 6 -evalue 0.001

</details>

<details>
<summary>
    
## 1. Data Acquisition (except Inner Mongolia soda lake)</summary>
There are three alkaline soda lakes: Kulunda Steppe, Inner Mongolia and Cariboo plateau.
References can be found below:

* [Kulunda paper](https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-018-0548-7#Ack1) and 
[data](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA434545/).
* [Inner Mongolia paper](https://www.frontiersin.org/articles/10.3389/fmicb.2020.01740/full#footnote11) and [data](https://figshare.com/s/9c3cb76f0c9646a30e94).
* [Cariboo paper](https://www.nature.com/articles/s41467-019-12195-5) and [data](https://www.ncbi.nlm.nih.gov/bioproject/?term=PRJNA377096).

Download data from Kulunda and Cariboo paper

#### 1.1 Run checkm2 

    cd ~/software/CheckM2
    conda activate ~/software/CheckM2/checkm2

    bin/checkm2 predict -t 30 -x fa --input /home/lianchun.yi1/data/chinese_mags/385-genome --output-directory /home/lianchun.yi1/data/chinese_mags/checkm2_run1
385 genome spend 1 hour

Or run with nohup &

    nohup bin/checkm2 predict -t 30 -x fa --input /home/lianchun.yi1/data/chinese_mags/385-genome --output-directory /home/lianchun.yi1/data/chinese_mags/checkm2_run1 &

#### 1.2 Run gtdb-tk    

    source ~/software/gtdb-tk/bin/activate
should apply more memory and CUP to run gtdbtk, as the pplacer would be killed.

    salloc --mem=20G -c 16 -N 1 -n 1  -t 04:00:00

    gtdbtk classify_wf --genes --genome_dir /home/lianchun.yi1/data/chinese_mags/385-protein -x .faa --out_dir /home/lianchun.yi1/data/chinese_mags/gtdbtk_run1 --cpus 6 --skip_ani_screen

#### 1.3 Run cd-hit to remove duplicate sequence

     cd-hit -i Nodosilinea.faa -o Nodosilinea_cd-hit.faa -c 0.95 -n 5 -T 8

#### 1.4 followed the four jupyter lab notebooks and collected target genomes
32 clusters were built: 399 alkaline species, 646 marine species, and  1168 other species were found.
There were 2213 genomes.

</details>

<details>
<summary>
    
## 2 Annotate genes via Metaerg with --mode usage</summary>
#### 2.1 run metaerg on the cloud
Activate the virtual environment:

    source /bio/bin/profile
    echo $PATH
    source /bio/bin/python-env/bin/activate
Go to the metaerg directory. Run the following command: (23 genomes spend 17.3 hours)

    nohup metaerg --database_dir /bio/databases/metaerg --contig_file ../fna --file_extension .fna --output_dir ./  --force all --mode comparative_genomics &

This command can generate multiply sequence alignment in the directory of /bio/data/Lianchun/evolut_adapt/1/metaerg/comparative_genomics/clusters.faa.align. So the *.faa files in this directory can be used to create ultrafast bootstrap tree distributions.
#### 2.2 run metaerg on ARC
50 G mem：1 genome spent 1 h and 40 min and 95% CPU was used

    #!/bin/bash
    #SBATCH --job-name=metaerg_test      # Job name
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 4 tasks
    #SBATCH --cpus-per-task=6    # Number of CPU cores per task
    #SBATCH --mem=100G            # Job memory request
    #SBATCH --time=04:00:00       # 23 genomes spend 17.3 hours
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    #SBATCH --partition=cpu2021
    pwd; hostname; date

    \time  singularity exec --bind /work/ebg_lab/referenceDatabases/metaerg_db_V214:/databases --bind /home/lianchun.yi1/cluster_data/1/fna:/data --writable /work/ebg_lab/software/metaerg-v2.5.2/sandbox_metaerg_2.5.6/ metaerg --database_dir /databases --contig_file /data --file_extension .fna --mode comparative_genomics 

Compress and decompress

    tar -zcvf archive.tar.gz ./
    tar -xzf archive.tar.gz 

</details>


## 3 Make species tree for one clade
Submitting the **species_tree.slurm** file below to ARC: (CPU efficiency: 100%, Memory efficiency: 0.1%). 

Remember to change the **-nt** value accordingly.

Check the log file of tree_of_mags. Compare it to the real genome count. 


    #!/bin/bash
    #SBATCH --job-name=1_SpeciesTree      # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=16    # Number of CPU cores per task
    #SBATCH --mem=50G            # Job memory request
    #SBATCH --time=48:00:00       # tree_of_mags: 17 genomes spend 8 min. Iqtree spends 40 min
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    cd /work/ebg_lab/eb/Lianchun/1   # need to change this clade number correspondingly

    source ~/bio/bin/3.10_python-env/bin/activate        
    tree_of_mags --mag_faa_dir ./fna/faa --mag_file_extension .faa
    iqtree2 -s ./alignments/concatenated_alignment -nt 16 -bb 100000 -wbtl
    sed -E 's/\)([0-9]+(\.[0-9]+)?)\:/\):/g' ./alignments/concatenated_alignment.treefile > concatenated_alignment_NoSupport.treefile

After completing this run, several things need to be done manually:

1. Uploading the ./concatenated_alignment.treefile to [ITOL](https://itol.embl.de/upload.cgi) to make rerooted phylogenetic trees.

   GTDB phylogenetic tree should be taken into account. 

3. Exporting the rerooted trees in Newick format. Exclude the internal node IDs. 

4. Naming the rerooted trees as **reroot1**, **reroot2**, etc.

5. Saving the reroot1.txt, reroot2.txt... files to .\Exp_EvolutionaryAdaptation\cluster_results\<order>.
   
6. Running [LY_species_tree_name_modify.py](https://github.com/Wednesdaysama/evolutionary_adaptation/blob/main/LY_species_tree_name_modify.py) on local computer.

7. Uploading all generated files, including *.newick, roots_to_test.txt and species_list_demo.txt files to ./<clade order>/fna/comparative_genomics/clusters.cds.faa.align.

8. Downloading the  ./concatenated_alignment.treefile to .\Exp_EvolutionaryAdaptation\cluster_results\<order>. And generating unrooted tree figure by running [LY_generate_trees.py](https://github.com/Wednesdaysama/evolutionary_adaptation/blob/main/LY_generate_trees.py) on local computer.


## 4 Create ultrafast bootstrap gene tree distributions
Submitting the **xargs_bootstrap_gene_tree.slurm** file to arc: (CPU efficiency: 97%, Mem efficiency: 52%)

    #!/bin/bash
    #SBATCH --job-name=1_GeneTree      # Job name
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=16    # Number of CPU cores per task
    #SBATCH --mem=150GB           # Job memory request
    #SBATCH --time=150:00:00      # speed: 360 files/h 
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    cd /work/ebg_lab/eb/Lianchun/1

    find ./fna/comparative_genomics/clusters.cds.faa.align/*.faa | xargs -n 1 -P 500 -I {} iqtree2 -s {} -m MFP -madd LG+C20,LG+C60 -B 10000 -wbtl



## 5 Create ale objects
Submitting the following **xargs_create_ale_objects.slurm** file to arc: (CPU efficiency: x%, Memory efficiency: x%)

Make sure to change the actual clade orders!

    #!/bin/bash
    #SBATCH --job-name=test_Ale_Objects      # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=16    # Number of CPU cores per task
    #SBATCH --mem=64G            # Job memory request
    #SBATCH --time=10:00:00       # 1.3 files/s
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date


    for file in /work/ebg_lab/eb/Lianchun/1    

    find ./fna/comparative_genomics/clusters.cds.faa.align/*.ufboot | xargs -n 1 -P 1500 -I {} sh -c 'echo "Processing {}..." && singularity exec --bind /work/ebg_lab/eb/Lianchun/1/fna/comparative_genomics/clusters.cds.faa.align/temp/:/work/ebg_lab/eb/Lianchun/1/fna/comparative_genomics/clusters.cds.faa.align/temp/ /work/ebg_lab/software/ale/ ALEobserve {}'                                                                                          



Open the *.ale files and check the name of the species! There are double names!




## 6 Computing gene trees for each candidate rooted species tree
Go to /work/.../<clade order>/fna/comparative_genomics/clusters.cds.faa.align/

    mkdir reroot1
    cp *.ale reroot1 
    cp -r reroot1 reroot2
    cp -r reroot1 reroot3
    cp -r reroot1 reroot4
    cp -r reroot1 reroot5


Submitting the following **xargs_reconcile_tree_*.slurm** file to arc: (CPU efficiency: 33%, Memory efficiency: 0.2%)

Make sure to change the actual clade orders!

    #!/bin/bash
    #SBATCH --job-name=19_reconciliation_reroot1      # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=4    # Number of CPU cores per task
    #SBATCH --mem=20G            # Job memory request
    #SBATCH --time=04:00:00       # 35 files/min
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    # should change 1 place on the following command lines

    cd /work/ebg_lab/eb/Lianchun/19

    bash -c 'for file in ./fna/comparative_genomics/clusters.cds.faa.align/reroot1/*.ale; do ALEml_undated ./fna/comparative_genomics/clusters.cds.faa.align/reroot1.newick "$file" separators="."; done'



## 7 Interpretation of ALE results
### 7.1 choose rerooted species tree. 
Go to /work/.../<clade order>/fna/comparative_genomics/clusters.cds.faa.align/ directory, run:

    cd reroot1
    rename reroot1 root *
    cd ../reroot2
    rename reroot2 root *
    cd ../reroot3
    rename reroot3 root *    
    cd ../reroot4
    rename reroot4 root *

This will replace root1 with root in all filenames containing root1/2/3/4 in the reroot1/2/3/4 subdirectories.

Then, run:

    cd ..
    cp ~/write_consel_file_p3.py ./
    python write_consel_file_p3.py reroot1 reroot2 reroot3 reroot4 > likelihoods_table
    mv likelihoods_table likelihoods_table.mt
    makermt likelihoods_table.mt
    consel likelihoods_table
    catpv likelihoods_table > au_test_out 

The root1 and root2 are directory names, which containing the .uml_rec files. Open the au_test_out file and accept the rerooted tree with au(*P*) > 0.05.
    
### 7.2 Robustness check 
Download the above script in the same directory as write_consel_file_p3.py (directory A). Create 3 subdirectories in directory A named: root1, root2 and root3. The number of subdirectories is the same as the number of candidate roots. Copy *uml_rec files to their respective subdirectories. In the directory A, manually create text files named [roots_to_test.txt](https://github.com/ak-andromeda/ALE_methods/blob/main/Demo_data/roots_to_test.txt) and [species_list_demo.txt](https://github.com/ak-andromeda/ALE_methods/blob/main/Demo_data/species_list_demo.txt). In the first file, write the name of the directory of the root to be tested. In this example, write reroot1, reroot2. In the second file, write the species names. Note: In these 2 txt files, each directory name or species name must be on a separate line. In the directory A, run the following code:

    source ~/bio/bin/python-env/bin/activate
    cp ~/DTL_ratio_analysis_ML_diff_Fan.py ./
    python DTL_ratio_analysis_ML_diff_Fan.py reroot2 S
    python DTL_ratio_analysis_ML_diff_Fan.py reroot2 D
    python DTL_ratio_analysis_ML_diff_Fan.py reroot2 T
    python DTL_ratio_analysis_ML_diff_Fan.py reroot2 L
    python DTL_ratio_analysis_ML_diff_Fan.py reroot2 LS
    python DTL_ratio_analysis_ML_diff_Fan.py reroot2 TS
    python DTL_ratio_analysis_ML_diff_Fan.py reroot2 DS
    
### 7.3 Gene content evolution on the most likely rooted species tree
Go to the **best reroot directory** and run [branchwise_numbers_of_events.py](https://github.com/ak-andromeda/ALE_methods/blob/main/branchwise_number_of_events.py) below. Check the internal node orders. Remember the first and last internal node orders. If the number of internal nodes (branch nodes) are from 16-30, 16 and 30 should be the first and last internal node orders. In the same reroot directory, run [Ancestral_reconstruction_VK.py](https://github.com/vmkhot/Comparative-Genomics-Verruco/blob/master/ancestral_trial/ancestral_modified_VK.py).


    source ~/bio/bin/python-env/bin/activate
    cp ~/ancestral_modified_VK.py ./
    cp ~/branchwise_number_of_events.py ./
    python branchwise_number_of_events.py > dtloc.tsv
    less dtloc.tsv

Remember the internal node numbers.    

    python ancestral_modified_VK.py 0.5 16 30
    
In this case, 0.5 is that 50% of the family's copies exist on the corresponding node. 16 and 30 refer to the number of the first and last internal node. The internal nodes are shown in .uml_rec files.

