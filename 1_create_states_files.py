'''
NOTE:
This script requires the homologues.tsv file created by Metaerg with the comparative_genomic mode.
Before running this script, make sure to check and change line 15 accordingly.
After running, an Excel file containing all character states of this cluster will be generated.
Additionally, several thousand character state files (.txt) will be created.
---- Lianchun Yi, 2024 July
'''

import pandas as pd
from datetime import datetime
import re
import os

cluster = "test_19" # the name of working folder
file_path = fr'C:\{cluster}\test.tsv' # replace test with homologues
output_dir = fr'C:\{cluster}'

# pre-processing
homologues = pd.read_csv(file_path, sep='\t')
homologues.iloc[:, 2] = homologues.iloc[:, 2].str.replace('MAG: ', '', regex=False)
int_cols = []
for col_idx in range(10, homologues.shape[1]):
    if pd.api.types.is_integer_dtype(homologues.iloc[:, col_idx]):
        col_name = homologues.columns[col_idx]
        col_data = homologues.iloc[:, col_idx]
        int_cols.append((col_name, col_data))

if int_cols:
    int_df = pd.DataFrame({col_name: col_data for col_name, col_data in int_cols})
    idx2_col = homologues.iloc[:, 2]
    int_df.insert(loc=0, column='Annotation', value=idx2_col)
    int_df = int_df[int_df.iloc[:, 0].notna()]
    int_df = int_df[~int_df.iloc[:, 0].astype(str).str.contains('hypothetical protein', na=False, case=False)]
    int_df = int_df[~int_df.iloc[:, 0].astype(str).str.contains('DUF', na=False, case=False)]
    int_df['Annotation'] = int_df['Annotation'].str.replace(r'\s\[.*?\]', '', regex=True)
    int_df['Annotation'] = int_df['Annotation'].str.replace('MAG: ', '', regex=False)
    unique_values = int_df.iloc[:, 0].unique()
    character_states_all = pd.DataFrame()

else:
    print("Columns containing integer data not found")

for val in unique_values:
    subset = int_df[int_df.iloc[:, 0] == val]
    summed_values = subset.iloc[:, 1:].sum(axis=0)
    summed_values['Annotation'] = val
    character_states_all = pd.concat([character_states_all, pd.DataFrame(summed_values).T], ignore_index=True)

cols = list(character_states_all.columns)
cols = ['Annotation'] + [col for col in cols if col != 'Annotation']
character_states_all = character_states_all[cols].transpose()
output_character_states_all = fr'C:\{cluster}\character_states_all.xlsx'
character_states_all.to_excel(output_character_states_all, index=True, header=False)
print(datetime.now(), f"character_states_all.xlsx has been saved.")

'''
This section generates independent character state data for the leaves text files.
Gene families with identical character states will be skipped.
'''

character_states_all_path = fr'C:\{cluster}\character_states_all.xlsx'
character_states_all_excel = pd.read_excel(character_states_all_path)

first_column_name = character_states_all_excel.columns[0]
file_count = 0

for column in character_states_all_excel.columns[1:]:
    if not character_states_all_excel[column].nunique() == 1:
        new_character_states_all = character_states_all_excel[[first_column_name, column]]

        column_length = len(new_character_states_all)
        insert_row = pd.DataFrame({first_column_name: [column_length], column: [1]})
        new_character_states_all = pd.concat([insert_row, new_character_states_all], ignore_index=True)

        character_states = re.sub(r'\s\[.*?\]', '', column)
        character_states = re.sub(r'[^a-zA-Z0-9_]', '_', character_states)

        output_file = os.path.join(output_dir, f"{character_states}.txt")
        new_character_states_all.to_csv(output_file, sep='\t', index=False, header=False)

        file_count += 1
print(datetime.now(), f"Total number of txt files saved: {file_count}")

