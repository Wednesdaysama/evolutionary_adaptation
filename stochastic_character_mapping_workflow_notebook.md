## This is a notebook recoding how to use stochastic character mapping.

### 1 Data collection
Prepare species [tree](https://github.com/arklumpus/sMap/blob/master/TestAnalysis/Cerataphidini.tre) **Cerataphidini.tre**.
This tree must be rooted and should be clock-like.
Prepare character status data **Cerataphidini.txt**. 
The format should be like [this](https://github.com/arklumpus/sMap/blob/master/TestAnalysis/Cerataphidini.txt)


***
### 2 Running one character [sMap](https://github.com/arklumpus/sMap/blob/master/sMap.pdf)
Press **win+R** and type **cmd**. Navigate to the fold (C:\test_LY) that contains the files above.

#### 2.1 ML analysis with default
Create an output directory:

    mkdir Aphids_ML_ARD_bi

Run sMap by default:

    sMap -t Cerataphidini.tre -d Cerataphidini.txt -o Aphids_ML_ARD_bi/tutorial1 -n 1000

Keep the AIC(c) and BIC values in mind.
Go to the Aphids_ML_ARD_bi directory and check the tutorial1.smap.pdf file.

    cd Aphids_ML_ARD_bi

Get the posterior probabilities for each state for the root node:

    NodeInfo -s tutorial1.smap.bin -m Neothoracaphis_yanonis Ceratovacuna_lanigera --batch

#### 2.2 ML analysis with an equal-rates (ER) model
ER model assumes the rates of change are all equal. 
Should prepare a [.ER.nex](https://github.com/arklumpus/sMap/blob/master/Tutorials/Tutorial2/Cerataphidini.model.ML.ER.nex) file in advance.
Check the user manual for detailed info.
First, create a new directory:

    mkdir Aphids_ML_ER_bi
Run:

    sMap -t Cerataphidini.tre -d Cerataphidini.txt -o Aphids_ML_ER_bi/tutorial2 -n 1000 -i Cerataphidini.model.ML.ER.nex
    cd Aphids_ML_ER_bi
    NodeInfo -s tutorial2.smap.bin -n 0,2,3,4,9,10 --batch
Keep the AIC(c) and BIC values in mind.

#### 2.3 Bayesian analysis with an ARD model
Prepare two files like [here](https://github.com/arklumpus/sMap/tree/master/Tutorials/Tutorial3).

Run:

    mkdir Aphids_Bayes_ARD_bi
    sMap -t Cerataphidini.tre -d Cerataphidini.txt -o Aphids_Bayes_ARD_bi/tutorial3 -n 1000 -i Cerataphidini.model.Bayes.ARD.nex

Also, can provide sMap multiple trees, which have different topologies and branch length.
In this case, the Cerataphidini.treedist file contains a list of 1000 clock-like trees. We can use it and run:

    sMap -t Cerataphidini.treedist -T Cerataphidini.tre -d Cerataphidini.txt -o Aphids_Bayes_ARD_bi/tutorial3 -n 1000 -i Cerataphidini.model.Bayes.ARD.nex
In the tutorial3.ssize.pdf file, thicker branches mean higher sample sizes.

Get the posterior probability values for the nodes we are interested in:

    cd Aphids_Bayes_ARD_bi
    NodeInfo -s tutorial3.smap.bin -n 0,2,3,4,9,10 --batch

#### 2.4 Bayesian analysis with an ER model
Prepare a file like [this](https://github.com/arklumpus/sMap/blob/master/Tutorials/Tutorial4/Cerataphidini.model.Bayes.ER.nex).

Run:

    mkdir Aphids_Bayes_ER_bi
    sMap -t Cerataphidini.treedist -T Cerataphidini.tre -d Cerataphidini.txt -o Aphids_Bayes_ER_bi/tutorial4 -n 1000 -i Cerataphidini.model.Bayes.ER.nex
    cd Aphids_Bayes_ER_bi
    NodeInfo -s tutorial4.smap.bin -n 0,2,3,4,9,10 --batch

#### 2.5 Bayesian model selection with marginal likelihoods
ARD:
    
    mkdir Aphids_Bayes_ARD_ss_bi
    sMap -t Cerataphidini.treedist -T Cerataphidini.tre -d Cerataphidini.txt -o Aphids_Bayes_ARD_ss_bi/tutorial5 -n 1000 -i Cerataphidini.model.Bayes.ARD.nex -ss
Check the Ln-marginal likelihood for the ARD model.

ER run:
    
    mkdir Aphids_Bayes_ER_ss_bi
    sMap -t Cerataphidini.treedist -T Cerataphidini.tre -d Cerataphidini.txt -o Aphids_Bayes_ER_ss_bi/tutorial5 -n 1000 -i Cerataphidini.model.Bayes.ER.nex -ss
Check the Ln-marginal likelihood for the ER model and the tutorial5.marginal.likelihoods.txt in the Aphids_Bayes_ER_ss_bi directory.

Blend the stochastic maps:

    mkdir Aphids_Bayes_blended_bi
    Blend-sMap -o Aphids_Bayes_blended_bi/tutorial5.blended.smap.bin -n 5000 -s Aphids_Bayes_ARD_ss_bi/tutorial5.smap.bin,79.74 -s Aphids_Bayes_ER_ss_bi/tutorial5.smap.bin,20.26
    Plot-sMap -s Aphids_Bayes_blended_bi/tutorial5.blended.smap.bin --batch
Check the tutorial5.blended.smap.pdf file in the Aphids_Bayes_blended_bi directory.

Calculate the posterior probabilities for the nodes above:

    cd Aphids_Bayes_blended_bi
    NodeInfo -s tutorial5.blended.smap.bin -n 0,2,3,4,9,10 --batch
Now, these are the **FINAL** results we need.  
The posterior probabilities for each node would change with different priors!

### 3 Multifurcating summary tree

#### 3.1 ML analysis with an ARD model
    mkdir Aphids_ML_ARD_multi
    sMap -t Cerataphidini.halfcompat.tre -d Cerataphidini.txt -o Aphids_ML_ARD_multi/tutorial6 -n 1000
    cd Aphids_ML_ARD_multi 

Have a look the tutorial6.smap.pdf file in this directory and take a note of ML estimate rates.

#### 3.2 ML analysis with an ER model
    mkdir Aphids_ML_ER_multi
    sMap -t Cerataphidini.halfcompat.tre -d Cerataphidini.txt -o Aphids_ML_ER_multi/tutorial6 -n 1000 -i Cerataphidini.model.ML.ER.nex

Take note of this ML estimate value.

#### 3.3 Bayesian analysis with an ARD model
    mkdir Aphids_Bayes_ARD_ss_multi
Edit the Cerataphidini.model.Bayes.ARD.nex file. Change the prior for the A to P and the P to A.

    sMap -t Cerataphidini.treedist -T Cerataphidini.halfcompat.tre -d Cerataphidini.txt -o Aphids_Bayes_ARD_ss_multi/tutorial6 -n 1000 -i Cerataphidini.model.Bayes.ARD.nex -ss --max-cov=1
Take a look of the tutorial6.smap.pdf file and have a look of the ML estimate.

#### 3.4 Bayesian analysis with an ER model, also estimating the marginal likelihood
    mkdir Aphids_Bayes_ER_ss_multi
Edit the Cerataphidini.model.Bayes.ER.nex file. Change the prior for the A to P and the P to A.

    sMap -t Cerataphidini.treedist -T Cerataphidini.halfcompat.tre -d Cerataphidini.txt -o Aphids_Bayes_ER_ss_multi/tutorial6 -n 1000 -i Cerataphidini.model.Bayes.ER.nex -ss --max-cov=1
Look at the tutorial6.smap.pdf file in the output folder. Take note of the log-marginal likelihood estimate.

#### 3.5 Blend the previous analyses according to the model posterior probabilities
Should compute the model posterior probabilities for the ER and ARD models. Can refer to [5.7.5](https://github.com/arklumpus/sMap/blob/master/sMap.pdf) for details.

    mkdir Aphids_Bayes_blended_multi
    Blend-sMap -o Aphids_Bayes_blended_multi/tutorial6.blended.smap.bin -n 5000 -s Aphids_Bayes_ARD_ss_multi/tutorial6.smap.bin,79.74 -s Aphids_Bayes_ER_ss_multi/tutorial6.smap.bin,20.26

Plot the analysis:
    
    Plot-sMap -s Aphids_Bayes_blended_multi/tutorial6.blended.smap.bin --batch

Look at the tutorial6.blended.smap.pdf file.

### 4 Plotting a stochastic mapping analysis
Navigating to the directory that contains **.blended.smap.bin** file.

    cd Aphids_Bayes_blended_bi
    Plot-sMap -s tutorial5.blended.smap.bin
Using the arrow and enter keys to modify the user interface.

***

### 5 Multiple characters
Prepare consensus (clocklike) tree file **Pontederiaceae.tre**.
Prepare 1’000 tree samples from the posterior distribution called **Pontederiaceae.treedist**.
Prepare character stater data file for two characters, called **Pontederiaceae.txt**.
#### 5.1 Treat the two characters as independent: self-incompatibility

    mkdir Plants_self_ML_ARD
    sMap -t Pontederiaceae.tre -d Pontederiaceae_self.txt -o Plants_self_ML_ARD/tutorial8 -n 1000
Take note of the ML estimates for the rates (which you can also find in the tutorial8.mean.params.txt file in the output folder)
,that should be around 2.822 for the 𝐼 → 𝐶 rate (which translates to a LogNormal(1.03744585343062, 1) prior) and 0.288 for the 𝐶 → 𝐼 rate.

    mkdir Plants_self_Bayes_ARD
    sMap -t Pontederiaceae.treedist -T Pontederiaceae.tre -d Pontederiaceae_self.txt -o Plants_self_Bayes_ARD/tutorial8 -n 1000 -i Pontederiaceae_self.model.Bayes.ARD.nex -ss --max-cov=1
Take note of the ln-marginal likelihood value, which should be around -9.85.

    mkdir Plants_self_ML_ER
    sMap -t Pontederiaceae.tre -d Pontederiaceae_self.txt -o Plants_self_ML_ER/tutorial8 -n 1000 -i Pontederiaceae_self.model.ML.ER.nex
Take note of the ML estimates for the rate, which should be around 0.248.

    mkdir Plants_self_Bayes_ER
    sMap -t Pontederiaceae.treedist -T Pontederiaceae.tre -d Pontederiaceae_self.txt -o Plants_self_Bayes_ER/tutorial8 -n 1000 -i Pontederiaceae_self.model.Bayes.ER.nex -ss --max-cov=1
Take note of the ln-marginal likelihood value, which should be around -10.79.

    mkdir Plants_flower_ML_ARD
    sMap -t Pontederiaceae.tre -d Pontederiaceae_flower.txt -o Plants_flower_ML_ARD/tutorial8 -n 1000
Take note of the ML estimates for the rates.These priors are specified in the 
Pontederiaceae_flower.model.Bayes.ARD.nex file which is located in the 
flower_models folder.

    mkdir Plants_flower_Bayes_ARD
    sMap -t Pontederiaceae.treedist -T Pontederiaceae.tre -d Pontederiaceae_flower.txt -o Plants_flower_Bayes_ARD/tutorial8 -n 1000 -i flower_models/Pontederiaceae_flower.model.Bayes.ARD.nex -ss --max-cov=1
Take note of the ln-marginal likelihood value, which should be around -21.69.

Using a script to run the rest of 11 models for maximum-likelihood analyses. 
For windows, run:
    
    Pontederiaceae_flower_ML_WIN.bat

Using a script to run the Bayesian analyses.
For window, run:

    Pontederiaceae_flower_Bayes_WIN.bat

Check values in **tutorial8.marginal.likelihood.txt** files.
Using these values with the ones we computed for 
the self-incompatibility character to compute the marginal likelihoods for all combinations of character models.

#### 5.2 Treat the two characters as dependent characters

    mkdir Plants_dep_ML_ARD
    sMap -t Pontederiaceae.tre -d Pontederiaceae.txt -o Plants_dep_ML_ARD/tutorial8 -n 1000 -i Pontederiaceae_dep.model.ML.ARD.nex --pm 5 --mr 5
Take note of the ML estimates for the rates.
These priors are specified in the Pontederiaceae_dep.model.Bayes.ARD.nex file.

    mkdir Plants_dep_Bayes_ARD
    sMap -t Pontederiaceae.treedist -T Pontederiaceae.tre -d Pontederiaceae.txt -o Plants_dep_Bayes_ARD/tutorial8 -n 1000 -i Pontederiaceae_dep.model.Bayes.ARD.nex -ss --max-samples=10000 --ss-estimate-steps
Take note of the ln-marginal likelihood, which should be around -24.75.

    $mkdir Plants_dep_ML_ER
    sMap -t Pontederiaceae.tre -d Pontederiaceae.txt -o Plants_dep_ML_ER/tutorial8 -n 1000 -i Pontederiaceae_dep.model.ML.ER.nex
Take note of the ML estimate for the rates, which should be around 0.252.

    mkdir Plants_dep_Bayes_ER
    sMap -t Pontederiaceae.treedist -T Pontederiaceae.tre -d Pontederiaceae.txt -o Plants_dep_Bayes_ER/tutorial8 -n 1000 -i Pontederiaceae_dep.model.Bayes.ER.nex -ss --max-cov=1
Once the analysis finishes, take note of the ln-marginal likelihood, which should be around -
32.36.

    mkdir Plants_dep_ML_SYM
    sMap -t Pontederiaceae.tre -d Pontederiaceae.txt -o Plants_dep_ML_SYM/tutorial8 -n 1000 -i Pontederiaceae_dep.model.ML.SYM.nex
Take note of the ML estimates for the rates.

    mkdir Plants_dep_Bayes_SYM
    sMap -t Pontederiaceae.treedist -T Pontederiaceae.tre -d Pontederiaceae.txt -o Plants_dep_Bayes_SYM/tutorial8 -n 1000 -i Pontederiaceae_dep.model.Bayes.SYM.nex -ss --max-cov=1 --min-ess=1 --min-samples=10000 --ss-estimate-steps
Once the analysis finishes, take note of the ln-marginal likelihood, which should be around -
25.11.

*Blend* the ARD and SYM analyses using the Blend-sMap utility:
    
    mkdir Plants_blended
    Blend-sMap -o Plants_blended/tutorial8.blended.smap.bin -n 2000 -s Plants_dep_Bayes_ARD/tutorial8.smap.bin,57.55 -s Plants_dep_Bayes_SYM/tutorial8.smap.bin,41.37
    
Create plots of the blended analysis with the Plot-sMap utility:

To create a plot for both characters at once:

    Plot-sMap -s Plants_blended/tutorial8.blended.smap.bin –batch
To create a plot for the flower morphology:
    
    Plot-sMap -s Plants_blended/tutorial8.blended.smap.bin –batch -c 0 -o Plants_blended/tutorial8.blended.smap.flower.pdf
To create a plot for the self-incompatibility:

    Plot-sMap -s Plants_blended/tutorial8.blended.smap.bin –batch -c 1 -o Plants_blended/tutorial8.blended.smap.self.pdf

#### 5.3 Multiple characters (conditioned)
Use a script to run the Bayesian analyses:

    Pontederiaceae_cond_Bayes_WIN.bat
The marginal likelihoods will be reported in the tutorial9.marginal.likelihood.txt files in 
each output folder.

Blend the analyses using Blend-sMap:

    mkdir Plants_cond_blended
    Blend-sMap -o Plants_cond_blended/tutorial9.blended.smap.bin -n 10000 -s Plants_cond_Bayes_ARD/tutorial9.smap.bin,11.08 -s Plants_cond_Bayes_ER/tutorial9.smap.bin,3.45 -s Plants_cond_Bayes_SYM/tutorial9.smap.bin,25.36 -s Plants_cond_Bayes_ORD1_ARD/tutorial9.smap.bin,10.51 -s Plants_cond_Bayes_ORD1_ER/tutorial9.smap.bin,20.53 -s Plants_cond_Bayes_ORD1_SYM/tutorial9.smap.bin,25.32 -s Plants_cond_Bayes_ORD2_ARD/tutorial9.smap.bin,0.64 -s Plants_cond_Bayes_ORD2_ER/tutorial9.smap.bin,0.81 -s Plants_cond_Bayes_ORD2_SYM/tutorial9.smap.bin,1.46 -s Plants_cond_Bayes_ORD3_ARD/tutorial9.smap.bin,0.12 -s Plants_cond_Bayes_ORD3_ER/tutorial9.smap.bin,0.11 -s Plants_cond_Bayes_ORD3_SYM/tutorial9.smap.bin,0.62
Ignore the ones with the lowest probabilities (e.g. < 5%).

Create plots of the blended analysis with the Plot-sMap utility:
    
    Plot-sMap -s Plants_cond_blended/tutorial9.blended.smap.bin --batch
    Plot-sMap -s Plants_cond_blended/tutorial9.blended.smap.bin --batch -c 0 -o Plants_cond_blended/tutorial9.blended.smap.flower.pdf
    Plot-sMap -s Plants_cond_blended/tutorial9.blended.smap.bin --batch -c 1 -o Plants_cond_blended/tutorial9.blended.smap.self.pdf

#### 5.4 Test for correlation between characters
Perform a D-test to  determine whether the self-incompatibility and flower morphology evolve 
in a correlated fashion.

To run the ARD analysis (Self-incompatibility):

    mkdir Plants_self_PP_ARD
    sMap -t Pontederiaceae.treedist -T Pontederiaceae.tre -d Pontederiaceae_self.txt -o Plants_self_PP_ARD/tutorial10 -n 1000 -i Pontederiaceae_self.model.Bayes.ARD.nex --pp 100
Wait until the analysis finished. Remember that the log-marginal likelihood value for this 
model was around -9.85.

To run the ER analysis (Self-incompatibility):

    mkdir Plants_self_PP_ER
    sMap -t Pontederiaceae.treedist -T Pontederiaceae.tre -d Pontederiaceae_self.txt -o Plants_self_PP_ER/tutorial10 -n 1000 -i Pontederiaceae_self.model.Bayes.ER.nex --pp 100
Wait until the analysis finished. Remember that the log-marginal likelihood value for this 
model was around -10.79.

To blend the two analyses(Self-incompatibility):

Compute the model posterior probabilities, which should be around 71.9% for the ARD model 
and 28.1% for the ER model.

    Blend-sMap -o tutorial10_self.blended.smap.bin -n 2000 -s Plants_self_PP_ARD/tutorial10.smap.bin,71.9 -s Plants_self_PP_ER/tutorial10.smap.bin,28.1

To run the ARD, ER and blend analysis (Flower morphology):

    mkdir Plants_flower_PP_ARD
    sMap -t Pontederiaceae.treedist -T Pontederiaceae.tre -d Pontederiaceae_flower.txt -o Plants_flower_PP_ARD/tutorial10 -n 1000 -i flower_models/Pontederiaceae_flower.model.Bayes.ARD.nex --pp 100
    mkdir Plants_flower_PP_ER
    sMap -t Pontederiaceae.treedist -T Pontederiaceae.tre -d Pontederiaceae_flower.txt -o Plants_flower_PP_ER/tutorial10 -n 1000 -i flower_models/Pontederiaceae_flower.model.Bayes.ER.nex --pp 100
    Blend-sMap -o tutorial10_flower.blended.smap.bin -n 2000 -s Plants_flower_PP_ARD/tutorial10.smap.bin,71.9 -s Plants_flower_PP_ER/tutorial10.smap.bin,28.1

Merging the characters and performing the D-test:

    Merge-sMap -o tutorial10.merged.smap.bin -n 2000 -s "tutorial10_self.blended.smap.bin;0" -s "tutorial10_flower.blended.smap.bin;0" 
-s "tutorial10_self.blended.smap.bin;0": this argument provides an input file
and identifies which characters from that file should be included (in this case, character 0, 
which is the only character). The value of the argument should be enclosed within double 
quotes, because otherwise the semicolon (;) may be interpreted by some shells as the end 
of the command.

    Stat-sMap -s tutorial10.merged.smap.bin -t 0 1 tutorial10.dtest
-t 0 1 tutorial10.dtest: this argument specifies that we want to perform a D-test 
between characters 0 and 1.
Check the **tutorial10.dtest.pdf** file.

### 6 Assessing the reliability of a maximum-likelihood estimate
    mkdir Plants_ML_assessment
    sMap -t Pontederiaceae.tre -d Pontederiaceae_flower.txt -o Plants_ML_assessment/tutorial11 -n 1000 --sl --pl

Check the **tutorial11.computed.likelihoods.pdf** file. 
Plot explanation can be found in [5.12.1](https://github.com/arklumpus/sMap/blob/master/sMap.pdf).
















