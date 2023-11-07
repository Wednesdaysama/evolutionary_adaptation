#### how to use CheckM2 
##### 1. on the terminal

    cd OngoingProjects/CheckM2
    conda activate checkm2
    bin/checkm2 -h
##### 2. on the arc

    cd software/CheckM2
    conda activate checkm2
    bin/checkm2 predict

    bin/checkm2 predict -t 30 -x fa --input /home/lianchun.yi1/data/chinese_mags/385-genome --output-directory /home/lianchun.yi1/data/chinese_mags/checkm2_run1 &
385 genome spend 1 hour

or run with nohup &

    nohup bin/checkm2 predict -t 30 -x fa --input /home/lianchun.yi1/data/chinese_mags/385-genome --output-directory /home/lianchun.yi1/data/chinese_mags/checkm2_run1 &


#### Anaconda
start the anaconda nevigator:

    anaconda-nevigator

start the jupyterlab or notebook:

    jupyter lab

start the jupyternotebook:

     jupyter-notebook