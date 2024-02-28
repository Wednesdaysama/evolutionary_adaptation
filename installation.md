
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
Create a metaerg_pull_docker.slurm file.

    #!/bin/bash
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca
    #SBATCH --mail-type=ALL
    #SBATCH --nodes=1
    #SBATCH --ntasks=1
    #SBATCH --cpus-per-task=2
    #SBATCH --mem=50GB
    #SBATCH --time=24:00:00
    #SBATCH --partition=cpu2021
    pwd; hostname; date

    source /home/lianchun.yi1/bio/bin/python-env/bin/activate
    cd /work/ebg_lab/software/metaerg-v2.5.1
    
    \time apptainer build metaerg.sif docker://kinestetika/metaerg:latest
    
