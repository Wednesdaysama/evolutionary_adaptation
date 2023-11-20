
### This is a notebook recording all the steps I have already done. Check here for Dr. Strous' [installation](https://github.com/kinestetika/cloud-computing-for-microbial-ecology/blob/main/cloud_bio_installs.py).

#### 0 Submit a job to ARC: using blastp as an example.
##### 0.1 Create a .slurm file:

    nano bicar_blastp.slurm

##### 0.2 Put the content below into the .slurm file:

    #!/bin/bash
    #SBATCH --job-name=bicar      # Job name
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=4            # Run 4 tasks
    #SBATCH --cpus-per-task=50    # Number of CPU cores per task
    #SBATCH --mem=100G            # Job memory request
    #SBATCH --time=48:00:00       # Time limit hrs:min:sec
    #SBATCH --output=blast%j.log  # Standard output and error log
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
#SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date
    
    blastp -query ~/databases/Soda_lakes_DB_Flag2_no_separator_V5.fasta -db bicar_db -out ~/data/bicar_blastp_run7 -outfmt 6

##### 0.3 Submit the bicar_blastp.slurm to ARC
 
    sbatch bicar_blastp.slurm
A job ID will be generated.
##### 0.4 Job Monitoring

    squeue # check the running queue
    arc.job-info <Job ID>
##### 0.5 Cancel the Job

    scancel <Job ID> 

#### 1. Data Acquisition (except Inner Mongolia soda lake)
There are three alkaline soda lakes: Kulunda Steppe, Inner Mongolia and Cariboo plateau.
References can be found below:

* [Kulunda paper](https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-018-0548-7#Ack1) and 
[data](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA434545/).
* [Inner Mongolia paper](https://www.frontiersin.org/articles/10.3389/fmicb.2020.01740/full#footnote11) and [data](https://figshare.com/s/9c3cb76f0c9646a30e94).
* [Cariboo paper](https://www.nature.com/articles/s41467-019-12195-5) and [data](https://www.ncbi.nlm.nih.gov/bioproject/?term=PRJNA377096).

##### 1.1 download data from Kulunda and Cariboo paper


##### 1.0 Launch an interactive session on ARC:

    salloc --mem=20G -c 1 -N 1 -n 1  -t 04:00:00


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

    salloc --mem=100G -c 16 -N 6 -n 16  -t 04:00:00

    gtdbtk classify_wf --genes --genome_dir /home/lianchun.yi1/data/chinese_mags/385-protein -x .faa --out_dir /home/lianchun.yi1/data/chinese_mags/gtdbtk_run1 --cpus 6 --skip_ani_screen


##### 1.3 CheckM2 and GTDB-Tk results process
1.3.1 Make a dictionary called new_genomes:

new_genomes = {}
with open('/home/wednesdaysama/Downloads/Evolutionary_adaptation/checkm2_run1/quality_report.tsv') as handle:
    for line in handle:
        try:
            words = line.split()
            new_genomes[words[0]] = {'accession': words[0],
                                 'completeness': float(words[1]),
                                 'contamination': float(words[2])}
        except ValueError:
            print('Skipping', words[0])
print(len(new_genomes), 'checkm results read.')

1.3.2 Update the new_genomes dictionary to add the 'taxonomy' information for each genome to the dictionary.

with open('/home/wednesdaysama/Downloads/Evolutionary_adaptation/gtdbtk_run1/gtdbtk.bac120.summary.tsv') as handle:
    for line in handle:
        try:
            words = line.split()
            genome = new_genomes[words[0]]
            genome['taxonomy'] = words[1]
        except KeyError:
            print('Skipping', words[0])

1.3.3 Check out quality 

count = 0
for ng in new_genomes.values():
    if ng['completeness'] > 90 and ng['contamination'] < 5 and ng.get('taxonomy',0):
        #print(ng['taxonomy'])
       count += 1

print('high quality genomes', count)

