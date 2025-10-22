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
    rm -r <sandbox_name>

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
Prepare a list containing the accession numbers of NCBI via **nano download_list**. In this list, every line only contains one accession number without **GB_** or **RS_**. Then run:

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
sMap was installed on Windows. Please follow the author's GitHub for instructions. Then, add the installation path to the PATH environment variable. 
Open the System Properties: Press **Win + X** and select **System**. Click on **Advanced system settings** on the left sidebar.In the System Properties window, click on the **Environment Variables** button. **Edit** the PATH Variable. In the Environment Variables window, scroll down to find the Path variable in the System variables section. Select **Path** and click on **Edit**. Add the sMap path, which is **D:\sMap**. Click **OK** to close each window.

Run:

Press **Win+R** and type **cmd**

    sMap -h 
    
### [ALE](https://github.com/ssolo/ALE/tree/master)
Install ALE on ARC:

    mkdir /work/ebg_lab/software/ale
    singularity build --force --sandbox /work/ebg_lab/software/ale/ docker://boussau/alesuite:latest

Run ale:

    #!/bin/bash
    for file in /work/ebg_lab/eb/Lianchun/temp/*.ufboot

    do
        echo "Processing $file..."
        singularity exec --bind /work/ebg_lab/eb/Lianchun/temp/:/work/ebg_lab/eb/Lianchun/temp/ /work/ebg_lab/software/ale/ ALEobserve "$file"
    done

### [Consel](http://stat.sys.i.kyoto-u.ac.jp/prog/consel/)

    git clone https://github.com/shimo-lab/consel
    cd consel/src
    make
    make install
    make clean
    cd ..
    
    nano ~/.bashrc   #open the configuration file
    export PATH=$PATH:/home/lianchun.yi1/software/consel/bin   #add this to this file and save it
    source ~/.bashrc

### [Sourmash](https://github.com/sourmash-bio/sourmash)

    mamba create -n sourmash_env -c conda-forge sourmash-minimal
    mamba activate sourmash_env
    sourmash --help

### [blast]

    mamba install -c bioconda blast

### [GeneRax](https://github.com/BenoitMorel/GeneRax?tab=readme-ov-file)

    cd ~
    module load bioconda/2024-10
    conda create -n generax_env # This env has been created in /home/lianchun.yi1/.conda/envs/generax_env
    conda activate generax_env
    conda install bioconda::generax
    salloc --mem=20G -c 1 -N 1 -n 2  -t 04:00:00
    module load openmpi/4.0.2-gnu730
    mpirun -np 2 generax -h

When running GenRax:

    salloc --mem=20G -c 1 -N 1 -n 2  -t 04:00:00
    conda activate generax_env
    module load openmpi/4.1.1-gnu
    mpirun -np 2 generax -h
    
### [AleRax](https://github.com/BenoitMorel/AleRax/blob/main/README.md)

    git clone --recursive https://github.com/BenoitMorel/AleRax
    git config --global http.sslVerify "false"
    cd AleRax
    module load cmake/3.30.1
    ./install.sh
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX=/home/lianchun.yi1/software/
    make -j 4
    make install
    nano ~/.bashrc

Adding the following line to the ~/.bashrc file:

    export PATH=/home/lianchun.yi1/software/bin:$PATH
Then

    source ~/.bashrc
    alerax --help

### [Thirdkind] (https://github.com/simonpenel/thirdkind)

    curl https://sh.rustup.rs -sSf | sh
    source ~/.cargo/env
    cargo install thirdkind
    thirdkind --help
    
