import glob
import os
import secrets
import shutil
import random
import pandas as pd
import numpy as np
from multiprocessing import Pool

from simAIRR.baseline_repertoires_generation.GeneValidator import GeneValidator
from simAIRR.util.utilities import makedir_if_not_exists, split_dataframe


class BaselineRepertoiresGeneration:

    def __init__(self, model: str, background_sequences_path: str, output_file_path: str, n_seq: int, seed: int,
                 n_reps: int, n_threads: int, depth_variation: bool = False):
        self.model = model
        self.background_sequences_path = background_sequences_path
        self.output_file_path = output_file_path
        self.n_seq = n_seq
        self.seed = seed
        self.n_reps = n_reps
        self.n_threads = n_threads
        self.depth_variation = depth_variation

    def generate_multiple_repertoires(self):
        makedir_if_not_exists(self.output_file_path, fail_if_exists=True)
        if self.background_sequences_path is not None:
            self._generate_repertoires_from_background_sequences()
        else:
            pool = Pool(self.n_threads)
            number_reps = list(range(1, self.n_reps + 1))
            pool.map(self._olga_generate_repertoire, number_reps)

    def _generate_repertoires_from_background_sequences(self):
        background_sequences = pd.read_csv(self.background_sequences_path, header=None, sep='\t', index_col=False)
        validator = GeneValidator()
        background_sequences = validator.validate_background_sequences(background_sequences, self.model)
        np.random.seed(self.seed)
        shuffled_indices = np.random.permutation(background_sequences.index)
        background_sequences = background_sequences.iloc[shuffled_indices]
        required_lines = self.n_seq * self.n_reps
        if required_lines > len(background_sequences):
            raise ValueError(f"Number of required sequences ({required_lines}) is greater than the number of "
                             f"sequences in the background file ({len(background_sequences)}).")
        required_seqs = background_sequences.iloc[:required_lines, :]
        split_dataframe(data_frame=required_seqs, number_of_splits=self.n_reps, split_files_path=self.output_file_path)

    def _olga_generate_repertoire(self, rep):
        out_filename = os.path.join(self.output_file_path, 'rep_' + str(rep) + '.tsv')
        rep_seed = rep + self.seed
        if self.depth_variation:
            n_seq = np.random.poisson(self.n_seq)
            command = ('olga-generate_sequences --' + self.model + ' -o ' + out_filename + ' -n ' + str(n_seq)
                       + ' --seed ' + str(rep_seed))
        else:
            command = ('olga-generate_sequences --' + self.model + ' -o ' + out_filename + ' -n ' + str(self.n_seq)
                       + ' --seed ' + str(rep_seed))
        exit_code = os.system(command)
        if exit_code != 0:
            raise RuntimeError(f"Running olga tool failed:{command}.")

    @staticmethod
    def postprocess_baseline_repertoires(output_path, export_nt_sequences=True, negative_control=False):
        sim_reps_path = os.path.join(os.path.dirname(output_path), "simulated_repertoires")
        makedir_if_not_exists(sim_reps_path, fail_if_exists=True)
        found_reps = glob.glob(str(output_path) + "/rep_*.tsv", recursive=False)
        proxy_subject_ids = [secrets.token_hex(16) for i in range(len(found_reps))]
        proxy_fns = [subject_id + ".tsv" for subject_id in proxy_subject_ids]
        if negative_control:
            num_reps = len(found_reps)
            num_true = num_reps // 2
            num_false = num_reps - num_true
            labels = [True] * num_true + [False] * num_false
            random.shuffle(labels)
        else:
            labels = [False for rep in proxy_fns]
        metadata_dict = {'subject_id': proxy_subject_ids, 'filename': proxy_fns,
                         'label_positive': labels}
        metadata_df = pd.DataFrame.from_dict(metadata_dict)
        metadata_df.to_csv(os.path.join(sim_reps_path, "metadata.csv"))
        if not export_nt_sequences:
            for i, rep in enumerate(found_reps):
                rep_df = pd.read_csv(rep, sep='\t', header=None, index_col=False)
                rep_df = rep_df.iloc[:, 1:]
                rep_df.to_csv(os.path.join(sim_reps_path, proxy_fns[i]), sep='\t', index=False, header=False)
        else:
            for i, rep in enumerate(found_reps):
                shutil.copy(rep, os.path.join(sim_reps_path, proxy_fns[i]))
        shutil.rmtree(output_path)


