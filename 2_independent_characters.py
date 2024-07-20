'''
This script requires at least three files:
    1. Tree file of the target cluster: <cluster name>.tre
        The cluster name should be as the same as the working directory's name.
    2. One file contains 1000 bootstrap trees: <cluster name>.treedist
    3. At least one text file contains the character states information: <character name>.txt
        This file can be created by the first script: 1_create_states_files.
All files should be prepared before running this script and should be placed in the same directory.
The lines 17-18 should be changed accordingly.
---- Lianchun Yi, 2024 July
'''

import os
from datetime import datetime
import math

cluster = "test_19"
file_path = fr'C:\{cluster}'

txt_files = [f for f in os.listdir(file_path) if f.endswith('.txt')]
character = [os.path.splitext(f)[0] for f in txt_files]
total_character = len(character)

# 1/6 {character}_ML_ARD
for idx, char in enumerate(character, start=1):
    new_dir = os.path.join(file_path, f"{char}_ML_ARD")
    if not os.path.exists(new_dir):
        os.system(f'mkdir "{new_dir}"')

    sMap_command = f'sMap -t {file_path}\\{cluster}.tre -d {file_path}\\{char}.txt -o {new_dir}\\round1 -n 1000'
    os.system(sMap_command)
    print(datetime.now(), f'{character}_ML_ARD was done.')

# 2/6 {character}_Bayes_ARD
    R1_params_file_path = os.path.join(new_dir, 'round1.mean.params.txt')
    Bayes_ARD_Rates = {}
    if os.path.exists(R1_params_file_path):
        with open(R1_params_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and line.startswith('r'):
                    parts = line.split(':')
                    if len(parts) == 2:
                        key = parts[0].strip()[2:-1]
                        value_raw = float(parts[1].strip())  # This raw value is ML estimate
                        if value_raw < 0.01:
                            value = "Exponential(100)"
                        else:
                            value_log = 1.0000498827 * math.log(value_raw) + 0.0000988121  # Convert ML estimate to parameter for log-normal priors for Bayesian analyses
                            value = f"LogNormal({value_log}, 1)"
                        Bayes_ARD_Rates[key] = value

    Bayes_ARD_nex_file_path = os.path.join(file_path, f"{char}.model.Bayes.ARD.nex")
    with open(Bayes_ARD_nex_file_path, 'w') as Bayes_ARD_nex_file:
        Bayes_ARD_nex_file.write("#NEXUS\n\n")
        Bayes_ARD_nex_file.write("Begin Pi;\n\n")
        Bayes_ARD_nex_file.write("    Character: 0;\n\n")
        Bayes_ARD_nex_file.write("    Default: Dirichlet(1);\n\n")
        Bayes_ARD_nex_file.write("End;\n\n")
        Bayes_ARD_nex_file.write("Begin Rates;\n\n")
        Bayes_ARD_nex_file.write("    Character: 0;\n\n")
        Bayes_ARD_nex_file.write("    Rates:\n")


        for key, value in Bayes_ARD_Rates.items():
            Bayes_ARD_nex_file.write(f"        {key}: {value}\n")

        Bayes_ARD_nex_file.write("        ;\n\n")
        Bayes_ARD_nex_file.write("End;\n")
    print(datetime.now(), '.Bayes.ARD.nex was created')

    Bayes_ARD_dir = os.path.join(file_path, f"{char}_Bayes_ARD")
    if not os.path.exists(Bayes_ARD_dir):
        os.system(f'mkdir "{Bayes_ARD_dir}"')

    sMap_command = f'sMap -t {file_path}\\{cluster}.treedist -T {file_path}\\{cluster}.tre -d {file_path}\\{char}.txt -o {Bayes_ARD_dir}\\round2 -n 1000 -i {file_path}\\{char}.model.Bayes.ARD.nex --ss --max-samples=10000'#-ss --max-cov=1
    os.system(sMap_command)

    print(datetime.now(), f'{character}_Bayes_ARD was done.')

# 3/6 {character}_ML_ER
    R2_params_file_path = os.path.join(Bayes_ARD_dir, 'round2.mean.params.txt')
    ML_ER_Rates = {}
    first_key = None
    if os.path.exists(R2_params_file_path):
        with open(R2_params_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and line.startswith('r'):
                    parts = line.split(':')
                    if len(parts) == 2:
                        key = parts[0].strip()[2:-1]
                        if first_key is None:
                            ML_ER_Rates[key] = 'ML'
                            first_key = key
                        else:
                            ML_ER_Rates[key] = f'Equal({first_key})'

    ML_ER_nex_file_path = os.path.join(file_path, f"{char}.model.ML.ER.nex")
    with open(ML_ER_nex_file_path, 'w') as ML_ER_nex_file:
        ML_ER_nex_file.write("#NEXUS\n\n")
        ML_ER_nex_file.write("Begin Rates;\n\n")
        ML_ER_nex_file.write("    Character: 0;\n\n")
        ML_ER_nex_file.write("    Rates:\n")

        for key, value in ML_ER_Rates.items():
            ML_ER_nex_file.write(f"        {key}: {value}\n")

        ML_ER_nex_file.write("        ;\n\n")
        ML_ER_nex_file.write("End;\n")

    print(datetime.now(), f'{char}.ML.ER.nex was created.')

    new_dir = os.path.join(file_path, f"{char}_ML_ER")
    if not os.path.exists(new_dir):
        os.system(f'mkdir "{new_dir}"')

    sMap_command = f'sMap -t {file_path}\\{cluster}.tre -d {file_path}\\{char}.txt -o {new_dir}\\round3 -n 1000 -i {file_path}\\{char}.model.ML.ER.nex'
    os.system(sMap_command)

    print(datetime.now(), f'{char}_ML_ER was done.')

# 4/6 {character}_Bayes_ER
    R3_params_file_path = os.path.join(new_dir, 'round3.mean.params.txt')
    Bayes_ER_Rates = {}
    first_key = None
    if os.path.exists(R3_params_file_path):
        with open(R3_params_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and line.startswith('r'):
                    parts = line.split(':')
                    if len(parts) == 2:
                        key = parts[0].strip()[2:-1]

                        if first_key is None:
                            value_raw = float(parts[1].strip())
                            value_log = 1.0000498827 * math.log(value_raw) + 0.0000988121
                            value = f"LogNormal({value_log}, 1)"
                            first_key = key
                        else:
                            value = f"Equal({first_key})"

                        Bayes_ER_Rates[key] = value

    Bayes_ER_nex_file_path = os.path.join(file_path, f"{char}.model.Bayes.ER.nex")
    with open(Bayes_ER_nex_file_path, 'w') as Bayes_ER_nex_file:
        Bayes_ER_nex_file.write("#NEXUS\n\n")
        Bayes_ER_nex_file.write("Begin Pi;\n\n")
        Bayes_ER_nex_file.write("    Character: 0;\n\n")
        Bayes_ER_nex_file.write("    Default: Dirichlet(1);\n\n")
        Bayes_ER_nex_file.write("End;\n\n")
        Bayes_ER_nex_file.write("Begin Rates;\n\n")
        Bayes_ER_nex_file.write("    Character: 0;\n\n")
        Bayes_ER_nex_file.write("    Rates:\n")

        for key, value in Bayes_ER_Rates.items():
            Bayes_ER_nex_file.write(f"        {key}: {value}\n")

        Bayes_ER_nex_file.write("        ;\n\n")
        Bayes_ER_nex_file.write("End;\n")

    print(datetime.now(), '.Bayes.ER.nex was created')

    Bayes_ER_dir = os.path.join(file_path, f"{char}_Bayes_ER")
    if not os.path.exists(Bayes_ER_dir):
        os.system(f'mkdir "{Bayes_ER_dir}"')

    sMap_command = f'sMap -t {file_path}\\{cluster}.treedist -T {file_path}\\{cluster}.tre -d {file_path}\\{char}.txt -o {Bayes_ER_dir}\\round4 -n 1000 -i {file_path}\\{char}.model.Bayes.ER.nex --ss --max-samples=10000'  # -ss --max-cov=1
    os.system(sMap_command)

    print(datetime.now(), f'{character}_Bayes_ER was done.')

# 5/6 {character}_Bayes_blended
    # extract Bayes_ARD_ln-marginal_likelihood and Bayes_ER_ln-marginal_likelihood
    Bayes_ARD_file_path = os.path.join(Bayes_ARD_dir, 'round2.marginal.likelihood.txt')
    if os.path.exists(Bayes_ARD_file_path):
        with open(Bayes_ARD_file_path, 'r') as file:
            for line in file:
                if line.startswith("Overall ln-marginal likelihood:"):
                    Bayes_ARD_ln_marginal_likelihood = float(line.split(":")[1].strip())
                    break

    Bayes_ER_file_path = os.path.join(Bayes_ER_dir, 'round4.marginal.likelihood.txt')
    if os.path.exists(Bayes_ER_file_path):
        with open(Bayes_ER_file_path, 'r') as file:
            for line in file:
                if line.startswith("Overall ln-marginal likelihood:"):
                    Bayes_ER_ln_marginal_likelihood = float(line.split(":")[1].strip())
                    break

    exp_ARD = math.exp(Bayes_ARD_ln_marginal_likelihood)
    exp_ER = math.exp(Bayes_ER_ln_marginal_likelihood)

    PosteriorProbability_ARD = exp_ARD / (exp_ARD + exp_ER) * 100  # Unit: %
    PosteriorProbability_ER = exp_ER / (exp_ARD + exp_ER) * 100

    Bayes_blended_dir = os.path.join(file_path, f"{char}_Bayes_blended")
    if not os.path.exists(Bayes_blended_dir):
        os.system(f'mkdir "{Bayes_blended_dir}"')

    sMap_command = f'Blend-sMap -o {Bayes_blended_dir}/round5.blended.smap.bin -n 5000 -s {Bayes_ARD_dir}/round2.smap.bin,{PosteriorProbability_ARD} -s {Bayes_ER_dir}/round4.smap.bin,{PosteriorProbability_ER}'
    os.system(sMap_command)

    print(datetime.now(), f'{character}_Bayes_blended was done.')

# 6/6 create plot
    sMap_command = f'Plot-sMap -s {Bayes_blended_dir}/round5.blended.smap.bin --batch'
    os.system(sMap_command)

    remaining_files = total_character - idx
    print(datetime.now(), f'Plot of {char} was saved in {Bayes_blended_dir}.')
    print(f'                           {remaining_files} characters remaining.')


