
### This is a notebook recording all the steps I have already done. Check here for Dr. Strous' [installation](https://github.com/kinestetika/cloud-computing-for-microbial-ecology/blob/main/cloud_bio_installs.py). For [cheat help](https://github.com/Wednesdaysama/cheat-sheet/blob/main/cheat%20sheet.md).

#### 0 Submit a job to ARC: using blastp as an example.
##### 0.1 basic commands

    arc.nodes  # check the available partition nodes
    nano bicar_blastp.slurm   # write the script (refer the 0.2 for details)  
    sbatch bicar_blastp.slurm # Submit the bicar_blastp.slurm to ARC
    squeue-long -u username # check the user's running queue
    arc.job-info <Job ID> # Job Monitoring
    scancel <Job ID> # cancel the job
##### 0.2 Put the content below into the .slurm file:

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


#### 1. Data Acquisition (except Inner Mongolia soda lake)
There are three alkaline soda lakes: Kulunda Steppe, Inner Mongolia and Cariboo plateau.
References can be found below:

* [Kulunda paper](https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-018-0548-7#Ack1) and 
[data](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA434545/).
* [Inner Mongolia paper](https://www.frontiersin.org/articles/10.3389/fmicb.2020.01740/full#footnote11) and [data](https://figshare.com/s/9c3cb76f0c9646a30e94).
* [Cariboo paper](https://www.nature.com/articles/s41467-019-12195-5) and [data](https://www.ncbi.nlm.nih.gov/bioproject/?term=PRJNA377096).

##### 1.1 download data from Kulunda and Cariboo paper


##### 1.0 Launch an interactive session on ARC:

    salloc --mem=10G -c 1 -N 1 -n 1  -t 02:00:00


##### 1.1 Run checkm2 

    cd ~/software/CheckM2
    conda activate ~/software/CheckM2/checkm2

    bin/checkm2 predict -t 30 -x fa --input /home/lianchun.yi1/data/chinese_mags/385-genome --output-directory /home/lianchun.yi1/data/chinese_mags/checkm2_run1
385 genome spend 1 hour

Or run with nohup &

    nohup bin/checkm2 predict -t 30 -x fa --input /home/lianchun.yi1/data/chinese_mags/385-genome --output-directory /home/lianchun.yi1/data/chinese_mags/checkm2_run1 &

##### 1.2 Run gtdb-tk    

    source ~/software/gtdb-tk/bin/activate
should apply more memory and CUP to run gtdbtk, as the pplacer would be killed.

    salloc --mem=20G -c 16 -N 1 -n 1  -t 04:00:00

    gtdbtk classify_wf --genes --genome_dir /home/lianchun.yi1/data/chinese_mags/385-protein -x .faa --out_dir /home/lianchun.yi1/data/chinese_mags/gtdbtk_run1 --cpus 6 --skip_ani_screen

##### 0 Run cd-hit to remove duplicate sequence

     cd-hit -i Nodosilinea.faa -o Nodosilinea_cd-hit.faa -c 0.95 -n 5 -T 8

##### 1.4 followed the four jupyter lab notebooks and collected target genomes
32 clusters were built: 399 alkaline species, 646 marine species, and  1168 other species were found.
There were 2213 genomes.

#### 2 make species tree 
build concatenated_alignment via tree_of_mags

     tree_of_mags --mag_fna_dir ../fna --mag_faa_dir ../fna --mag_file_extension .fna
go to the alignments directory, and make the tree via fasttree or raxml or iqtree 

     fasttree ./concatenated_alignment >fasttree_file
raxml 23 genomes spend ~50 mins

     nohup raxmlHPC-PTHREADS -s ./concatenated_alignment -n raxml-tree -m PROTGAMMALG -f a -p 13 -x 123 -# 100 -T 16 &
iqtree: 23 genomes spend 53.5 mins

     nohup iqtree2 –s ./concatenated_alignment &
upload the fasttree_file, RAxML_bestTree.result and concatenated_alignment.treefile to [ITOL](https://itol.embl.de/upload.cgi) to make visualized phylogenetic trees. Or using [R](https://posit.cloud/spaces/485061/content/all?sort=name_asc).

#### 3 annotate genes via Metaerg with --mode usage
##### 3.1 run metaerg on the cloud
Activate the virtual environment:

    source /bio/bin/profile
    echo $PATH
    source /bio/bin/python-env/bin/activate
Go to the metaerg directory. Run the following command: (23 genomes spend 17.3 hours)

    nohup metaerg --database_dir /bio/databases/metaerg --contig_file ../fna --file_extension .fna --output_dir ./  --force all --mode comparative_genomics &
##### 3.2 run metaerg on ARC
    
    singularity run /work/ebg_lab/software/metaerg-v2.5.1/metaerg.sif metaerg -h
    
