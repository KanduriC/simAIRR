import logging
import os.path
import subprocess

import pandas as pd
import numpy as np
from pathlib import Path
import yaml


def concatenate_files(files_path, file_pattern):
    found_files = Path(files_path).glob(file_pattern)
    li = []
    for i, filename in enumerate(found_files):
        fn = pd.read_csv(filename, header=None, sep='\t')
        li.append(fn)
    concatenated_df = pd.concat(li, axis=0, ignore_index=True)
    return concatenated_df, len(li)


def makedir_if_not_exists(some_path, fail_if_exists=False):
    if os.path.exists(some_path):
        files = [fn for fn in os.listdir(some_path) if
                 os.path.isfile(os.path.join(some_path, fn))]
        files_exists = f"Output folder may already contain relevant files: {some_path}"
        if fail_if_exists:
            assert len(files) == 0, files_exists
    else:
        os.makedirs(some_path)


def split_dataframe(data_frame, number_of_splits, split_files_path):
    for idx, chunk in enumerate(np.array_split(data_frame, number_of_splits)):
        chunk.to_csv(os.path.join(split_files_path, f'rep_{idx}.tsv'), index=None, header=None, sep='\t')


def sort_olga_seq_by_pgen(olga_sequence_file, olga_pgen_file):
    pgen_file = pd.read_csv(olga_pgen_file, header=None, sep='\t', index_col=None)
    seq_file = pd.read_csv(olga_sequence_file, header=None, sep='\t', index_col=None)
    pgen_file.columns = ['aa_seq_pgen', 'pgen']
    seq_file.columns = ['nt_seq', 'aa_seq', 'v_gene', 'j_gene']
    pgen_file['row_index_pgen'] = np.arange(len(pgen_file))
    seq_file['row_index_seq'] = np.arange(len(seq_file))
    merged_df = pd.merge(seq_file, pgen_file, how="left", left_on=['aa_seq', 'row_index_seq'],
                         right_on=['aa_seq_pgen', 'row_index_pgen'])
    sorted_df = merged_df.sort_values(by='pgen')
    seq_df = sorted_df[['nt_seq', 'aa_seq', 'v_gene', 'j_gene']]
    pgen_df = sorted_df[['aa_seq_pgen', 'pgen']]
    seq_df.to_csv(olga_sequence_file, header=None, sep='\t', index=None)
    pgen_df.to_csv(olga_pgen_file, header=None, sep='\t', index=None)


def write_yaml_file(yaml_dict, out_file_path):
    with open(out_file_path, "w+") as yaml_file:
        yaml.dump(yaml_dict, yaml_file)


def merge_dicts(dicts_list):
    merged_dict = {k: v for d in dicts_list for k, v in d.items()}
    return merged_dict


def count_lines(file_path):
    try:
        result = subprocess.run(["wc", "-l", file_path], capture_output=True, text=True, check=True)
        line_count = int(result.stdout.strip().split()[0])
        return line_count
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0


def concatenate_dataframes_with_replacement(dfs_list):
    df_a, df_b = dfs_list
    for idx, row in df_b.iterrows():
        match_idx = df_a[(df_a['v_call'] == row['v_call']) & (df_a['j_call'] == row['j_call'])].index
        if not match_idx.empty:
            df_a = df_a.drop(match_idx[0])
    df = pd.concat([df_a, df_b], ignore_index=True)
    return df


def filter_legal_pairs(df, legal_pairs):
    df['pairs'] = list(zip(df['v_gene'], df['j_gene']))
    initial_n_rows = df.shape[0]
    df = df[df['pairs'].isin(legal_pairs)]
    df = df.drop(columns=['pairs'])
    final_n_rows = df.shape[0]
    logging.info('Number of sequences removed from the user-supplied signal because of lack of legal gene '
                 'combinations: ' + str(initial_n_rows - final_n_rows))
    return df

def get_legal_vj_pairs(background_sequences_path):
    df = pd.read_csv(background_sequences_path, sep="\t", header=0)
    if df.shape[1] == 3:
        df.insert(0, 'nt_seq', "NA")
    df.columns = ['junction', 'junction_aa', 'v_call', 'j_call']
    df['v_j_call'] = list(zip(df['v_call'], df['j_call']))
    unique_combinations = df['v_j_call'].value_counts()
    unique_combinations = unique_combinations.reset_index()
    unique_combinations.columns = ['v_j_call', 'count']
    unique_combinations['count'] = unique_combinations['count'].astype(int)
    unique_combinations['percentage'] = unique_combinations['count'] / unique_combinations['count'].sum() * 100
    filtered_combinations = unique_combinations[unique_combinations['percentage'] > 0.015]
    legal_combinations = filtered_combinations['v_j_call'].to_list()
    return legal_combinations
