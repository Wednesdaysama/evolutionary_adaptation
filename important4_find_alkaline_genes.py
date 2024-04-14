# Author: Lianchun Yi, lianchun.yi1@ucalgary.ca
# Attention: change lines 8-11. This script will take a while

import pandas as pd
import re
import os

cluster_number = 1
alkaline_nodes = [21, 22, 23, 24, 25, 28, 30, 31, 32, 34, 35]
alkaline_nodes_count = 12
non_alkaline_nodes_count = 9

directory = rf'D:\OneDrive - University of Calgary\Exp_EvolutionaryAdaptation\cluster_results\{cluster_number}\Gene_families_at_each_node'
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]


print('Processing gene families annotation...')
for csv_file in csv_files:
    Node_gene_present_path = os.path.join(directory, csv_file)

    df = pd.read_csv(Node_gene_present_path)
    pattern = re.compile(r'\d+')
    matching_rows = df['Gene_family'].apply(lambda x: pattern.search(x))
    filtered_rows = matching_rows[matching_rows.notnull()]
    extracted_cluster_ids = []
    for match in filtered_rows:
        extracted_cluster_id = match.group(0)
        extracted_cluster_ids.append(extracted_cluster_id)

    annotation_path = r'D:\OneDrive - University of Calgary\Exp_EvolutionaryAdaptation\cluster_results\1\homologues.xlsx'
    df1 = pd.read_excel(annotation_path)
    cluster_id_annotation = dict(zip(df1.iloc[:, 0], df1.iloc[:, 2]))

    for extracted_cluster_id in extracted_cluster_ids:
        if extracted_cluster_id in cluster_id_annotation:
            print(f"Cluster ID: {extracted_cluster_id}, Annotation: {cluster_id_annotation[extracted_cluster_id]}")

    extracted_cluster_ids = list(map(int, extracted_cluster_ids))
    values = [cluster_id_annotation.get(cluster_id) for cluster_id in extracted_cluster_ids]

    results_df = pd.DataFrame({'cluster_id_annotation_values': values})
    merged_df = pd.concat([df, results_df], axis=1)

    output_filename = os.path.splitext(csv_file)[0] + '_merged.txt'
    output_path = os.path.join(directory, output_filename)
    merged_df.to_csv(output_path, index=False, sep='\t')

print("Merging text files...")

txt_files = [f for f in os.listdir(directory) if f.endswith('_merged.txt')]
total_df = pd.DataFrame()
for txt_file in txt_files:
    file_path = os.path.join(directory, txt_file)
    df = pd.read_csv(file_path, sep='\t')
    total_df = pd.concat([total_df, df], ignore_index=True)

alkaline_genes_set = set()
other_genes_set = set()

for index, row in total_df.iterrows():
    cluster_id = int(row.iloc[1])
    if cluster_id in alkaline_nodes:
        gene_info = row['Gene_family']
        alkaline_genes_set.add(gene_info)
    else:
        gene_info = row['Gene_family']
        other_genes_set.add(gene_info)
alkaline_unique_genes = alkaline_genes_set - other_genes_set
alkaline_non_unique_genes = alkaline_genes_set - alkaline_unique_genes
other_genes_unique = other_genes_set - alkaline_non_unique_genes

print("Creating alkaline unique and non-unique gene families...")

gene_position_check = []
for index, row in total_df.iterrows():
    gene_info = row['Gene_family']
    if gene_info in alkaline_unique_genes:
        gene_position_check.append(1)
    elif gene_info in alkaline_non_unique_genes:
        gene_position_check.append(2)
    elif gene_info in other_genes_unique:
        gene_position_check.append(3)

total_df['gene_position_check'] = gene_position_check

for node in alkaline_nodes:
    node_list = []
    for index, row in total_df.iterrows():
        cluster_id = int(row.iloc[1])
        if cluster_id == node:
            gene_info = row['Gene_family']
            if gene_info in alkaline_unique_genes:
                node_list.append("unique")
            elif gene_info in alkaline_non_unique_genes:
                node_list.append("non_unique")
            else:
                node_list.append(0)
        if cluster_id != node:
            node_list.append(0)
    total_df[f'Node_{node}_Check'] = node_list

output_path = os.path.join(directory, 'Total_GeneFamilies_alkaline_genes.xlsx')
with pd.ExcelWriter(output_path) as writer:
    total_df.to_excel(writer, sheet_name='Total', index=False)

unique_alkaline_df = total_df[['Node', 'Gene_family', 'cluster_id_annotation_values', "Duplications", "Transfers",	"Losses",	'Originations',	'Copies',
'gene_position_check'] + list(total_df.columns[10:])].copy()
unique_alkaline_df = unique_alkaline_df[unique_alkaline_df['gene_position_check'] == 1]


other_genes_unique_df = total_df[['Node', 'Gene_family', 'cluster_id_annotation_values', "Duplications", "Transfers",	"Losses",	'Originations',	'Copies',
'gene_position_check'] + list(total_df.columns[10:])].copy()
other_genes_unique_df = total_df[total_df['gene_position_check'] == 3]


output_path_unique_alkaline = os.path.join(directory, 'GeneFamilies_analysis.xlsx')
non_unique_alkaline_df = total_df[['Node', 'Gene_family', 'cluster_id_annotation_values', "Duplications", "Transfers",	"Losses",	'Originations',	'Copies',
'gene_position_check'] + list(total_df.columns[10:])].copy()


non_unique_alkaline_df = non_unique_alkaline_df[non_unique_alkaline_df['gene_position_check'] == 2]
non_unique_in_alkaline_cluster_df = non_unique_alkaline_df[non_unique_alkaline_df['Node'].isin(alkaline_nodes)]
non_unique_in_other_cluster_df = non_unique_alkaline_df[~non_unique_alkaline_df['Node'].isin(alkaline_nodes)]

gene_familiy_number_in_unique_alkaline = len(set(alkaline_unique_genes))
gene_familiy_number_sharing = len(set(alkaline_non_unique_genes))
gene_familiy_number_in_unique_non_alkaline = len(set(other_genes_unique))

normalization_value_df = pd.DataFrame(columns=['group', 'Duplications', 'Transfers', 'Losses', 'Originations', 'Copies'])

unique_alkaline_sum = unique_alkaline_df[['Duplications', 'Transfers', 'Losses', 'Originations', 'Copies']].sum() / gene_familiy_number_in_unique_alkaline / alkaline_nodes_count
normalization_value_df.loc[0] = ['unique_alkaline_df'] + unique_alkaline_sum.tolist()
non_unique_in_alkaline_cluster_sum = non_unique_in_alkaline_cluster_df[['Duplications', 'Transfers', 'Losses', 'Originations', 'Copies']].sum() / gene_familiy_number_sharing / alkaline_nodes_count
normalization_value_df.loc[1] = ['non_unique_in_alkaline_cluster_df'] + non_unique_in_alkaline_cluster_sum.tolist()
non_unique_in_other_cluster_sum = non_unique_in_other_cluster_df[['Duplications', 'Transfers', 'Losses', 'Originations', 'Copies']].sum() / gene_familiy_number_sharing / non_alkaline_nodes_count
normalization_value_df.loc[2] = ['non_unique_in_other_cluster_df'] + non_unique_in_other_cluster_sum.tolist()
other_genes_unique_sum = other_genes_unique_df[['Duplications', 'Transfers', 'Losses', 'Originations', 'Copies']].sum() / gene_familiy_number_in_unique_non_alkaline / non_alkaline_nodes_count
normalization_value_df.loc[3] = ['other_genes_unique_df'] + other_genes_unique_sum.tolist()

with pd.ExcelWriter(output_path_unique_alkaline) as writer:
    unique_alkaline_df.to_excel(writer, sheet_name='unique_alkaline', index=False)
    non_unique_in_alkaline_cluster_df.to_excel(writer, sheet_name='sharing_in_alkaline', index=False)
    non_unique_in_other_cluster_df.to_excel(writer, sheet_name='sharing_in_non_alkaline', index=False)
    other_genes_unique_df.to_excel(writer, sheet_name='unique_in_non_alkaline', index=False)
    normalization_value_df.to_excel(writer, sheet_name='Normalization', index = False)

merged_files = os.listdir(directory)

for file in merged_files:
    if file.endswith("_merged.txt"):
        file_path = os.path.join(directory, file)
        os.remove(file_path)

print('Done!')
