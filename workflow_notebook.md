
### This is a notebook recording all the steps I have already done.


#### 1. Data Acquisition
There are three alkaline soda lakes: Kulunda Steppe, Inner Mongolia and Cariboo plateau.
References can be found below:

* [Kulunda paper](https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-018-0548-7#Ack1) and 
[data](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA434545/).
* [Inner Mongolia paper](https://www.frontiersin.org/articles/10.3389/fmicb.2020.01740/full#footnote11) and [data](https://figshare.com/s/9c3cb76f0c9646a30e94).
* [Cariboo paper](https://www.nature.com/articles/s41467-019-12195-5) and [data](https://www.ncbi.nlm.nih.gov/bioproject/?term=PRJNA377096).

##### 1.0 Launch an interactive session on ARC:

    salloc --mem=20G -c 1 -N 1 -n 1  -t 04:00:00


##### 1.1 Run checkm2 

    cd software/CheckM2
    conda activate checkm2
    bin/checkm2 predict

    bin/checkm2 predict -t 30 -x fa --input /home/lianchun.yi1/data/chinese_mags/385-genome --output-directory /home/lianchun.yi1/data/chinese_mags/checkm2_run1 &
385 genome spend 1 hour

Or run with nohup &

    nohup bin/checkm2 predict -t 30 -x fa --input /home/lianchun.yi1/data/chinese_mags/385-genome --output-directory /home/lianchun.yi1/data/chinese_mags/checkm2_run1 &

##### 1.2 Run gtdb-tk    

    source software/gtdb-tk/bin/activate
    GTDBTK_DATA_PATH=/home/lianchun.yi1/software/gtdb-tk/bin/release214
    gtdbtk classify_wf --genes --genome_dir /home/lianchun.yi1/data/chinese_mags/385-protein -x .faa --out_dir /home/lianchun.yi1/data/chinese_mags/gtdbtk_run1 --cpus 6 --skip_ani_screen


 Download genome data from the given list by fetch_genome.py.