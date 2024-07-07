### Remember to update the configuration file 
If you want to run blastp, the export command line should be included in the .bashrc file. Then, save this file and source it.

    export PATH=$PATH:~/software/ncbi-blast-2.15.0+/bin
    source .bashrc
    
### [checkm2](https://github.com/chklovski/CheckM2)


    git clone https://github.com/chklovski/checkm2.git && cd checkm2
    vim checkm2.yml
Check the version requirement, especially the python version!! 
Delete the tensorflow line, then save the checkm2.yml file.

    conda env create -n checkm2 -f checkm2.yml
    conda activate checkm2
    conda install tensorflow=2.2.0    
    bin/checkm2 -h   # check the installation
    bin/checkm2 --download # download the diamond database.  

Checkm2 relies on diamond for annotation.
The database will be installed in /home/lianchun.yi1/databases/checkm2.

### [gtdb-tk](https://ecogenomics.github.io/GTDBTk/installing/bioconda.html#step-1-install-conda-if-not-already-done)

**/home/lianchun.yi1/software/gtdb-tk/bin/activate** is a python virtual environment.

    cd software
    python -m venv gtdb-tk   # create a gtdb-tk virtual environment
    source gtdb-tk/bin/activate # activate the virtual environment
    python -m pip install gtdbtk  # install gtdbtk by pip
Download and alias the GTDB-Tk reference data. 
GTDB-Tk requires an environment variable named GTDBTK_DATA_PATH to be set to the directory
containing the unarchived GTDB-Tk reference data.

    export GTDBTK_DATA_PATH=/path/to/release/package/
    cd /home/lianchun.yi1/databases
    wget https://data.gtdb.ecogenomic.org/releases/latest/auxillary_files/gtdbtk_data.tar.gz
    tar xvzf gtdbtk_data.tar.gz   # path: /home/lianchun.yi1/databases/release214
    GTDBTK_DATA_PATH=/home/lianchun.yi1/databases/release214
    gtdbtk check_install # check GTDB-Tk reference data

### [Metaerg](https://github.com/kinestetika/MetaErg/tree/master)
Make an empty directory called sandbox. Use singularity build to make a sandbox and run metaerg in the sandbox.

    singularity build --force --sandbox /work/ebg_lab/software/metaerg-v2.5.2/sandbox1/ docker://kinestetika/metaerg:latest

Download or move the metaerg databases. For me, I save all the helper databases under /work/ebg_lab/referenceDatabases/metaerg_db_V214 directory. Then, using the following command to execute a test running.

    singularity exec --bind /work/ebg_lab/referenceDatabases/metaerg_db_V214:/databases --bind /home/lianchun.yi1/test_data_fna:/data --writable /work/ebg_lab/software/metaerg-v2.5.2/sandbox_metaerg_2.5.4/ metaerg --database_dir /databases --contig_file /data --file_extension .fna --force all

Delete the sandbox

    chmod -R u+rwX <sandbox_name>
    rm <sandbox_name>

Update metaerg on the Cloud:

    pip install metaerg --upgrade

### [Qiime2](https://educe-ubc.github.io/qiime2.html#:~:text=Installing%20QIIME%202%201%20Create%20a%20new%20Conda,Test%20that%20QIIME%202%20is%20installed%3A%20qiime%20info)
install:

    source /home/lianchun.yi1/software/gtdb-tk/bin/activate
    curl -sL   "https://data.qiime2.org/distro/core/qiime2-2020.8-py36-linux-conda.yml" >   "qiime2.yml"
    conda env create -n qiime2 --file qiime2.yml
    rm qiime2.yml
run Qiime2

    conda activate qiime2
    qiime info # check the installation

### [PUPpy](https://github.com/Tropini-lab/PUPpy?tab=readme-ov-file#install-with-conda-x86-64--linux-64)
Installation: make sure update the conda to the latest version.

    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ./miniconda3/miniconda.sh
    bash ./miniconda3/miniconda.sh -b -u -p ./miniconda3
    conda config --add channels defaults
    conda config --add channels conda-forge
    conda config --add channels bioconda
    /home/lianchun.yi1/software/miniconda3/bin/conda create -n puppy -c hghezzi -y puppy
    nano ~/.bashrc

add **export PATH=$PATH:/home/lianchun.yi1/software/miniconda3/bin** to the .bashrc file:

    source .bashrc
    
Running puppy to design primers for a group:

    conda deactivate
    conda activate puppy
    puppy-align -pr target_genomes -nt non_target_genomes -o output
    puppy-primers -pr target_genomes/ -i ./output/ResultDB.tsv -o primer/ -p group

### [ncbi-genome-download](https://github.com/kblin/ncbi-genome-download)
Install:

    pip install ncbi-genome-download
Prepare a list containing the accession numbers of NCBI via **nano download_list**. In this list, every line only contains one accession number. Then run:

    ncbi-genome-download --section genbank --formats fasta --assembly-accessions GCA_list bacteria --flat-output # download GCA
    ncbi-genome-download --formats fasta --assembly-accessions GCF_list bacteria --flat-output                   # download GCF
    gunzip *.fna.gz

### [iqtree2](https://github.com/iqtree/iqtree2/releases)
Install:
download the latest release in /home/lianchun.yi1/software/iqtree2: iqtree-2.3.4-Linux-intel.tar.gz

    tar -zxvf iqtree-2.3.4-Linux-intel.tar.gz
    mv iqtree-2.3.4-Linux-intel/bin/iqtree2 ./
    rm -r iqtree-2.3.4-Linux-intel
    rm iqtree-2.3.4-Linux-intel.tar.gz

    nano ~/.bashrc   #open the configuration file
    export PATH=$PATH:/home/lianchun.yi1/software/iqtree2 #add this to this file and save it
    source ~/.bashrc
    
### [sMap](https://github.com/arklumpus/sMap/tree/master)
sMap was installed on Windows. Please follow the author's GitHub for detailed instructions.

Run:

Press *Win+R*, type *cmd*, and then type *sMap -h*.
    
    
    

    



    
    

    
    
    
