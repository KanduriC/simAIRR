import os
import glob
import secrets
from multiprocessing import Pool
import pandas as pd
import numpy as np
from simAIRR.util.utilities import makedir_if_not_exists, concatenate_dataframes_with_replacement


class RepComponentConcatenation:
    def __init__(self, components_type, super_path, n_threads, export_nt=None, n_sequences=None, annotate_signal=None,
                 export_cdr3_aa=None, n_pos_repertoires=None):
        self.components_type = components_type
        self.super_path = str(super_path).rstrip('/')
        self.n_threads = n_threads
        self.export_nt = export_nt
        self.proxy_primary_fns = None
        self.n_sequences = n_sequences
        self.annotate_signal = annotate_signal
        self.export_cdr3_aa = export_cdr3_aa
        self.n_pos_repertoires = n_pos_repertoires

    def _set_component_specific_paths(self):
        # super_path in case of "public_private" concatenation is baseline_repertoires_path and
        # in case of signal+baseline is output_path (to be related with attributes of workflows class)
        if self.components_type == "public_private":
            self.primary_reps_path = os.path.join(self.super_path, "corrected_public_repertoires")
            self.secondary_reps_path = os.path.join(self.super_path, "filtered_private_repertoires")
            self.concatenated_reps_path = os.path.join(os.path.dirname(self.super_path),
                                                       "corrected_baseline_repertoires")
        else:
            self.primary_reps_path = os.path.join(self.super_path, "corrected_baseline_repertoires")
            self.secondary_reps_path = os.path.join(self.super_path, "signal_components", "signal_rep_chunks",
                                                    "filtered_implantable_signal_pool")
            self.concatenated_reps_path = os.path.join(self.super_path, "simulated_repertoires")

    def concatenate_repertoire_components(self, file_number):
        rep_file_name = f"rep_{file_number}.tsv"
        if self.components_type == "baseline_and_signal":
            concat_fn = os.path.join(self.concatenated_reps_path, self.proxy_primary_fns[rep_file_name])
            is_head = True
        else:
            concat_fn = os.path.join(self.concatenated_reps_path, rep_file_name)
            is_head = None
        primary_rep = os.path.join(self.primary_reps_path, rep_file_name)
        secondary_rep = os.path.join(self.secondary_reps_path, rep_file_name)
        dfs_list = []
        for i, rep_file in enumerate([primary_rep, secondary_rep]):
            try:
                rep_df = pd.read_csv(rep_file, header=None, index_col=None, sep='\t')
                rep_df.columns = ['junction', 'junction_aa', 'v_call', 'j_call']
                if self.annotate_signal is True:
                    rep_df['is_signal'] = i
                dfs_list.append(rep_df)
            except (pd.errors.EmptyDataError, FileNotFoundError) as e:
                continue
        try:
            if self.components_type == "public_private":
                concatenated_df = pd.concat(dfs_list)
            else:
                concatenated_df = concatenate_dataframes_with_replacement(dfs_list)
            if self.export_cdr3_aa is True:
                concatenated_df['cdr3_aa'] = concatenated_df['junction_aa'].str[1:-1]
                concatenated_df = concatenated_df.drop('junction_aa', axis=1)
                if self.annotate_signal is True:
                    concatenated_df = concatenated_df[['junction', 'cdr3_aa', 'v_call', 'j_call', 'is_signal']]
                else:
                    concatenated_df = concatenated_df[['junction', 'cdr3_aa', 'v_call', 'j_call']]
            if self.export_nt is False:
                concatenated_df = concatenated_df.drop('junction', axis=1)
        except ValueError:
            concatenated_df = pd.DataFrame()
            # concatenated_df.columns = ['junction', 'junction_aa', 'v_call', 'j_call']
        if self.components_type == "public_private":
            n_seq = np.random.poisson(self.n_sequences)
            concatenated_df = concatenated_df.head(n_seq)
        concatenated_df = concatenated_df.sample(frac=1).reset_index(drop=True)
        concatenated_df.to_csv(concat_fn, header=is_head, index=None, sep='\t')

    def multi_concatenate_repertoire_components(self):
        self._set_component_specific_paths()
        makedir_if_not_exists(self.concatenated_reps_path, fail_if_exists=True)
        found_primary_reps = glob.glob(self.primary_reps_path + "/rep_*.tsv", recursive=False)
        found_secondary_reps = glob.glob(self.secondary_reps_path + "/rep_*.tsv", recursive=False)
        if self.components_type == "baseline_and_signal":
            primary_rep_fns = [os.path.basename(rep) for rep in found_primary_reps]
            proxy_subject_ids = [secrets.token_hex(16) for i in range(len(found_primary_reps))]
            proxy_primary_fns = [subject_id + ".tsv" for subject_id in proxy_subject_ids]
            self.proxy_primary_fns = dict(zip(primary_rep_fns, proxy_primary_fns))
            rep_indices = [int(rep.split("_")[1].split(".")[0]) for rep in primary_rep_fns]
            lab_pos = [True if i < self.n_pos_repertoires else False for i in rep_indices]
            labels_mapping = dict(zip(primary_rep_fns, lab_pos))
            file_names = [self.proxy_primary_fns[rep] for rep in primary_rep_fns]
            labels = [labels_mapping[rep] for rep in primary_rep_fns]
            subject_ids = [fn.split(".")[0] for fn in file_names]
            metadata_dict = {'subject_id': subject_ids, 'filename': file_names, 'label_positive': labels}
            metadata_df = pd.DataFrame.from_dict(metadata_dict)
            metadata_df.to_csv(os.path.join(self.super_path, "metadata.csv"))
            metadata_df.to_csv(os.path.join(self.concatenated_reps_path, "metadata.csv"))
        else:
            assert len(found_primary_reps) == len(found_secondary_reps)
        pool = Pool(self.n_threads)
        pool.map(self.concatenate_repertoire_components, list(range(len(found_primary_reps))))
