import os
import pandas as pd
import numpy as np
from multiprocessing import Pool
from simAIRR.util.utilities import makedir_if_not_exists, count_lines


class BaselineRepertoiresGeneration:

    def __init__(self, model: str, background_sequences_path: str, output_file_path: str, n_seq: int, seed: int,
                 n_reps: int, n_threads: int):
        self.model = model
        self.background_sequences_path = background_sequences_path
        self.total_seqs = None
        self.background_sequences = None
        self.output_file_path = output_file_path
        self.n_seq = n_seq
        self.seed = seed
        self.n_reps = n_reps
        self.n_threads = n_threads

    def generate_multiple_repertoires(self):
        makedir_if_not_exists(self.output_file_path, fail_if_exists=True)
        pool = Pool(self.n_threads)
        number_reps = list(range(1, self.n_reps + 1))
        if self.background_sequences_path is not None:
            self.background_sequences = pd.read_csv(self.background_sequences_path, header=None, sep='\t', index_col=False)
            self.total_seqs = self.background_sequences.shape[0]
            pool.map(self._generate_repertoire_from_background_sequences, number_reps)
        else:
            pool.map(self._olga_generate_repertoire, number_reps)

    def _olga_generate_repertoire(self, rep):
        out_filename = os.path.join(self.output_file_path, 'rep_' + str(rep) + '.tsv')
        rep_seed = rep + self.seed
        command = 'olga-generate_sequences --' + self.model + ' -o ' + out_filename + ' -n ' + str(
            self.n_seq) + ' --seed ' + str(rep_seed)
        exit_code = os.system(command)
        if exit_code != 0:
            raise RuntimeError(f"Running olga tool failed:{command}.")

    def _generate_repertoire_from_background_sequences(self, rep):
        out_filename = os.path.join(self.output_file_path, 'rep_' + str(rep) + '.tsv')
        rep_seed = rep + self.seed
        np.random.seed(rep_seed)
        selected_indices = np.random.choice(self.total_seqs, self.n_seq, replace=False)
        background_seqs = self.background_sequences.copy(deep=True)
        selected_seqs = background_seqs.iloc[selected_indices, :]
        selected_seqs.to_csv(out_filename, header=None, index=None, sep='\t')