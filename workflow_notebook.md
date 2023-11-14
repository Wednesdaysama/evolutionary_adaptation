
### This is a notebook recording all the steps I have already done.


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

    cd software/CheckM2
    conda activate checkm2

    bin/checkm2 predict -t 30 -x fa --input /home/lianchun.yi1/data/chinese_mags/385-genome --output-directory /home/lianchun.yi1/data/chinese_mags/checkm2_run1
385 genome spend 1 hour

Or run with nohup &

    nohup bin/checkm2 predict -t 30 -x fa --input /home/lianchun.yi1/data/chinese_mags/385-genome --output-directory /home/lianchun.yi1/data/chinese_mags/checkm2_run1 &

##### 1.2 Run gtdb-tk    

    source software/gtdb-tk/bin/activate
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

