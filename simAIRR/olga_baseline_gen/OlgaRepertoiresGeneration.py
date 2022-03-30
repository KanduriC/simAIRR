import os
from multiprocessing import Pool
from simAIRR.util.utilities import makedir_if_not_exists


class OlgaRepertoiresGeneration:

    def __init__(self, model: str, output_file_path: str, n_seq: int, seed: int, n_reps: int, n_threads: int):
        self.model = model
        self.output_file_path = output_file_path
        self.n_seq = n_seq
        self.seed = seed
        self.n_reps = n_reps
        self.n_threads = n_threads

    def olga_generate_multiple_repertoires(self):
        pool = Pool(self.n_threads)
        number_reps = list(range(1, self.n_reps + 1))
        makedir_if_not_exists(self.output_file_path)
        pool.map(self._olga_generate_repertoire, number_reps)

    def _olga_generate_repertoire(self, rep):
        out_filename = os.path.join(self.output_file_path, 'rep_' + str(rep) + '.tsv')
        rep_seed = rep + self.seed
        command = 'olga-generate_sequences --' + self.model + ' -o ' + out_filename + ' -n ' + str(
            self.n_seq) + ' --seed ' + str(rep_seed)
        exit_code = os.system(command)
        if exit_code != 0:
            raise RuntimeError(f"Running olga tool failed:{command}.")

# if __name__ == '__main__': olga_reps = OlgaRepertoiresGeneration(model='humanTRB',
# output_file_path="/Users/kanduric/Desktop/simairr_tests/baseline_reps/", n_seq=10, seed=1234, n_reps=10,
# n_threads=2) olga_reps.olga_generate_multiple_repertoires()