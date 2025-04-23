'''
requirement:
    1. alkaline_node_list;
    2. Events_at_all_nodes.csv;
    3. homologues.tsv.
Notice:
    1. For the Fisher test, when infinity is detected, the odds ratio returns 100;
    2. For Poisson regression, when perfect separation happens, the odds ratio returns 0.5 or 20,
                                                                P-value retruns 0.00001.
'''
import os
import re
import pandas as pd
import numpy as np
from scipy.stats import fisher_exact
import statsmodels.api as sm
from statsmodels.tools.sm_exceptions import PerfectSeparationError
import plotly.express as px
from collections import defaultdict
import sys

seq_id = float(sys.argv[1])

work_dir = os.path.dirname(os.path.abspath(__file__))

#work_dir = r'D:\OneDrive - University of Calgary\Exp_EvolutionaryAdaptation\statistical_analysis\copies'
os.chdir(work_dir)

print('Processing category_dict dictionary.')
environment = pd.read_excel('environment.xlsx', usecols=['accession_number', 'category'])
category_dict = dict(zip(environment['accession_number'],
                         environment['category'].apply(lambda x: 'alkaline' if x == 'alkaline' else 'not_alkaline')))

protein_distribution = pd.read_csv(os.path.join(work_dir, f'protein_distribution_{seq_id}.csv'))
set_dict = {}
print('Processing protein_distribution dictionary.')
processed_count = 0
total_dicts = len(protein_distribution)

for _, row in protein_distribution.iterrows():
    set_id = row['Set_ID']
    concatenated_files = row['Concatenated_Files']
    if pd.isna(concatenated_files):
        set_dict[set_id] = set()
    else:
        files_list = {file.strip().replace('.faa', '') for file in concatenated_files.split('|')}
        set_dict[set_id] = files_list

    processed_count += 1
    if processed_count % 20000 == 0:
        print(f'Processed {processed_count}/{total_dicts} dictionaries.')
print('protein_distribution dictionary done.')

print('Reading Events_at_all_nodes_above_0.5.csv files...')
copies = []
file_count = 0
total_files = sum(1 for root, _, _ in os.walk(work_dir)
                  if os.path.exists(os.path.join(root, 'fna', 'comparative_genomics',
                                                 'clusters.cds.faa.align', 'Events_at_all_nodes_above_0.5.csv')))
subfolder_to_nodes = defaultdict(list)
for root, _, _ in os.walk(work_dir):
    target_file = os.path.join(root, 'fna', 'comparative_genomics', 'clusters.cds.faa.align',
                               'Events_at_all_nodes_above_0.5.csv')
    if os.path.exists(target_file):
        data = pd.read_csv(target_file)

        filtered = data.loc[
            (data['Node'].str.contains(r'\(', na=False)) & (data['Copies'] > 0.5),
            ['Node', 'Gene Family', 'Copies']
        ]

        subfolder_name = os.path.basename(root)
        nodes = data['Node'].unique()
        subfolder_to_nodes[subfolder_name].extend(nodes)


        def extract_faa_value(gene_family):
            match = re.search(r'_(\d+)\.faa', gene_family)
            return match.group(1) if match else None


        filtered['CladeID_FamilyID'] = filtered['Gene Family'].apply(
            lambda x: f"{subfolder_name}:{extract_faa_value(x)}" if extract_faa_value(x) else None)

        copies.append(filtered)
        file_count += 1

        if file_count % 5 == 0:
            print(f'Reading "Events_at_all_nodes_above_0.csv" files, read {file_count}/{total_files} files.')

copies = pd.concat(copies, ignore_index=True)
copies['Copies'] = copies['Copies'].astype(float)
copies.to_csv(os.path.join(work_dir, 'copies.csv'), index=True)

def modify_index(index):
    parts = index.split('_')
    if len(parts) == 2:
        return parts[0]
    elif len(parts) >= 3:
        return '_'.join(parts[:2])
    return index

print('Processing gene_matrix...')


unique_nodes = copies['Node'].drop_duplicates().tolist()
gene_matrix = pd.DataFrame(index=unique_nodes)
gene_matrix.index.name = 'Node'  

set_ids = [k for k,v in set_dict.items() if v]
chunk_size = 1000  
all_gene_chunks = []
all_binary_chunk = []
for i in range(0, len(set_ids), chunk_size):
    print(f"Processing chunk {i // chunk_size + 1}/{(len(set_ids) - 1) // chunk_size + 1}")

    chunk_set_ids = set_ids[i:i + chunk_size]
    chunk_matrix = pd.DataFrame(
        index=unique_nodes,
        columns=chunk_set_ids,
        dtype=np.float32
    )


    for set_id in chunk_set_ids:
        target_ids = set_dict[set_id]
        matched = pd.merge(
            copies[['Node', 'Copies']],
            copies[copies['CladeID_FamilyID'].isin(target_ids)][['Node']].drop_duplicates(),
            on='Node',
            how='inner'
        )
        if not matched.empty:
            chunk_matrix[set_id].update(
                matched.groupby('Node')['Copies'].first()
            )


    chunk_matrix_np = chunk_matrix.to_numpy()
    row_indices = {node: i for i, node in enumerate(chunk_matrix.index)}

    for set_idx, set_id in enumerate(chunk_matrix.columns):
        filled_mask = ~pd.isna(chunk_matrix_np[:, set_idx])

        for subfolder, nodes in subfolder_to_nodes.items():
            valid_nodes = [row_indices[n] for n in nodes if n in row_indices]
            if not valid_nodes:
                continue

            subfolder_mask = np.zeros(len(chunk_matrix), dtype=bool)
            subfolder_mask[valid_nodes] = True

            if filled_mask[subfolder_mask].any():
                rule1_mask = subfolder_mask & (~filled_mask)
                chunk_matrix_np[rule1_mask, set_idx] = 0
            else:
                chunk_matrix_np[subfolder_mask, set_idx] = -1

    chunk_matrix = pd.DataFrame(chunk_matrix_np,
                                index=chunk_matrix.index,
                                columns=chunk_matrix.columns)
    chunk_matrix = chunk_matrix.replace(-1, 'E')
    chunk_matrix.index = chunk_matrix.index.map(modify_index)
    binary_chunk_matrix = chunk_matrix
    for col in binary_chunk_matrix.columns:
        binary_chunk_matrix[col] = binary_chunk_matrix[col].apply(
            lambda x: 1 if isinstance(x, (int, float)) and x > 0
            else (0 if isinstance(x, (int, float)) and x == 0
                  else x
                  ))

    #chunk_matrix.to_csv(f'gene_matrix_chunk_{i}.csv')
    #binary_chunk_matrix.to_csv(f'binary_chunk_matrix_{i}.csv')
    all_gene_chunks.append(chunk_matrix)
    all_binary_chunk.append(binary_chunk_matrix)


try:
    gene_matrix = pd.concat(all_gene_chunks, axis=1)
    gene_matrix.to_csv(os.path.join(work_dir, f'gene_matrix_{seq_id}.csv'), index=True)
    binary_matrix = pd.concat(all_binary_chunk, axis=1)
    binary_matrix.to_csv(os.path.join(work_dir, f'binary_matrix_{seq_id}.csv'), index=True)
except MemoryError:
    print("MemoryError")
print('gene_matrix.csv and binary_matrix.csv have been saved!')

results = []

for gene_family in binary_matrix.columns:
    alkaline_present = 0
    non_alkaline_present = 0
    alkaline_absent = 0
    non_alkaline_absent = 0

    for idx, value in binary_matrix[gene_family].items():
        if value == "E":
            continue

        category = category_dict.get(idx)
        if value == 0:
            if category == 'alkaline':
                alkaline_absent += 1
            elif category == 'not_alkaline':
                non_alkaline_absent += 1

        elif value == 1:
            if category == 'alkaline':
                alkaline_present += 1
            elif category == 'not_alkaline':
                non_alkaline_present += 1

    contingency_table = [
        [alkaline_present, non_alkaline_present],
        [alkaline_absent, non_alkaline_absent]
    ]
    # Perform Fisher's Exact Test
    odds_ratio, p_value = fisher_exact(contingency_table, alternative='two-sided')

    if np.isinf(odds_ratio):
        odds_ratio = 100

    # Store results
    results.append({
        'GeneFamily': gene_family,
        'OddsRatio': odds_ratio,
        'PValue': p_value
    })

# Convert results into a DataFrame for easy inspection
results_df = pd.DataFrame(results)
# Step 1: Sort p-values in ascending order and assign ranks
# LY: When identical P-values exist, method='min' assigns these identical values the same lowest ranking
results_df['Rank'] = results_df['PValue'].rank(method='min')
# Step 2: Calculate the adjusted p-values using the BH procedure formula
m = len(results_df)  # Total number of tests (gene families)
results_df['BH_Adjusted_PValue'] = results_df['PValue'] * m / results_df['Rank']
# Step 3: Ensure adjusted p-values do not exceed 1
results_df['BH_Adjusted_PValue'] = np.minimum(results_df['BH_Adjusted_PValue'], 1)
# Step 4: Determine which tests are significant after BH correction
results_df['Significant'] = results_df['BH_Adjusted_PValue'] < 0.05
results_df_filtered = results_df.loc[results_df['PValue'] < 0.05]

results_df.to_csv(f'Fisher_results_{seq_id}.csv',index = False)
print('Fisher_results_{seq_id}.csv has been saved!')
# Fisher plot
plot_data = results_df.copy()
plot_data['-log10(padj)'] = -np.log10(plot_data['BH_Adjusted_PValue'])
plot_data['GeneFamily'] = plot_data['GeneFamily'].astype(str)
plot_data['Significance'] = np.where(plot_data['Significant'], 'Significant', 'Not Significant')
fig = px.scatter(plot_data, x='OddsRatio', y='-log10(padj)', color='Significance',
                 color_discrete_map={'Significant': 'red', 'Not Significant': 'blue'},
                 hover_data={'GeneFamily': True, 'OddsRatio': ':.2f', 'PValue': ':.3f', 'BH_Adjusted_PValue': ':.3f',
                             'Significant': False, '-log10(padj)': False},
                 title='Volcano Plot: Gene Family Enrichment/Depletion')
fig.update_traces(marker=dict(opacity=0.2, line=dict(color='rgba(128, 128, 128, 0.8)', width=0.8)))
fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="red", opacity=0.7)
fig.update_layout(xaxis_title='Odds Ratio', yaxis_title='-Log10 Adjusted P-value',
                  hovermode='closest', showlegend=False, margin=dict(l=40, r=40, t=60, b=40),
                  font=dict(family="Arial", size=12, color="black"))
fig.write_html(f"Fisher_test_{seq_id}.html")
print('Fisher test done!')

results = []
for gene_family in gene_matrix.columns:
    temp = gene_matrix[[gene_family]].loc[
        ~gene_matrix[gene_family].isin(['E'])].astype(float)

    if temp.empty:
        continue

    temp['y'] = temp.index.map(lambda idx: 1 if category_dict.get(idx) == 'alkaline' else 0)

    X = sm.add_constant(temp[[gene_family]])
    y = temp['y']

    try:
        poisson_family = sm.families.Poisson(link=sm.families.links.log())
        poisson_model = sm.GLM(y, X, family=poisson_family).fit()

        results.append({
            'GeneFamily': gene_family,
            'OddsRatio': np.exp(poisson_model.params[gene_family]),
            'PValue': poisson_model.pvalues[gene_family],
            'PerfectSeparation': False
        })

    except PerfectSeparationError:
        print(f"Perfect separation detected for {gene_family}.")

        if X[y == 1][gene_family].mean() > X[y == 0][gene_family].mean():
            odds_ratio = 20.0
            p_value = 0.00001
        else:
            odds_ratio = 0.5
            p_value = 1.0

        results.append({
            'GeneFamily': gene_family,
            'OddsRatio': odds_ratio,
            'PValue': p_value,
            'PerfectSeparation': True
        })

    except ValueError as e:
        print(f"Skipping {gene_family} due to error: {e}")


# Display the results
results_df_pois = pd.DataFrame(results)
# Step 1: Sort p-values in ascending order and assign ranks
results_df_pois['Rank'] = results_df_pois['PValue'].rank(method='min')
# Step 2: Calculate the adjusted p-values using the BH procedure formula
m = len(results_df_pois)  # Total number of tests (gene families)
results_df_pois['BH_Adjusted_PValue'] = results_df_pois['PValue'] * m / results_df_pois['Rank']
# Step 3: Ensure adjusted p-values do not exceed 1
results_df_pois['BH_Adjusted_PValue'] = np.minimum(results_df_pois['BH_Adjusted_PValue'], 1)
# Step 4: Determine which tests are significant after BH correction
results_df_pois['Significant'] = results_df_pois['BH_Adjusted_PValue'] < 0.05
results_df_pois['-log10(padj)'] = -np.log10(results_df_pois['BH_Adjusted_PValue'])
results_df_pois['Significance'] = np.where(results_df_pois['BH_Adjusted_PValue'] < 0.05, 'Significant',
                                           'Not Significant')
# filtered cos it gave me some really weird odds ratios
results_df_pois_filt = results_df_pois.loc[(results_df_pois['OddsRatio'] < 50) & (
            results_df_pois['OddsRatio'] > 0.01)]  # & ] (results_df['BH_Adjusted_PValue'] < 0.05)

results_df_pois.to_csv(f'poisson_results_{seq_id}.csv',index = False)
print('poisson_results_{seq_id}.csv has been saved!')


results_df_pois = results_df_pois[results_df_pois['OddsRatio'] < 21].copy()

fig = px.scatter(results_df_pois, x='OddsRatio', y='-log10(padj)', color='Significance',
    color_discrete_map={'Significant': 'red', 'Not Significant': 'blue'},
    hover_data={'GeneFamily': True, 'OddsRatio': ':.2f', 'PValue': ':.3f', 'BH_Adjusted_PValue': ':.3f',
        'Significance': False, '-log10(padj)': False},
    title='Volcano Plot: Gene Family Enrichment/Depletion')
fig.update_traces(marker=dict(opacity=0.4, line=dict(color='rgba(128, 128, 128, 0.8)', width=0.8)))
fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="red", opacity=0.7)
fig.update_layout(xaxis_title='Odds Ratio', yaxis_title='-Log10 Adjusted P-value',
    hovermode='closest', showlegend=False, margin=dict(l=40, r=40, t=60, b=40),
    font=dict(family="Arial", size=12, color="black"))
fig.write_html(f"Poisson_Regression_{seq_id}.html")

print('Poisson regression done! Now generating final results...')
results_df_filt = results_df.loc[results_df['BH_Adjusted_PValue'] < 0.05]
results_df_pois_filt_2 = results_df_pois_filt.loc[results_df_pois_filt['BH_Adjusted_PValue'] < 0.05]
df_test_merged = pd.merge(results_df,results_df_pois_filt, how='outer', on='GeneFamily', suffixes=['_Fisher', '_Poisson'])
df_test_merged = df_test_merged.loc[(df_test_merged['BH_Adjusted_PValue_Fisher'] < 0.05) | (df_test_merged['BH_Adjusted_PValue_Poisson'] < 0.05)]
df_test_merged = df_test_merged.merge(
    protein_distribution[['Set_ID', 'Lookup_Mapping']],
    left_on='GeneFamily', right_on='Set_ID', how='left')

df_test_merged.rename(columns={'Lookup_Mapping': 'Annotations'}, inplace=True)
df_test_merged.drop(columns=['Set_ID'], inplace=True)
df_test_merged.to_csv(f'statistical_analysis_{seq_id}.csv', index = False)
print('All done!')

