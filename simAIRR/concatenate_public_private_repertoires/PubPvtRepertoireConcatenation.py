import os
import glob
from multiprocessing import Pool
import pandas as pd


class PubPvtRepConcatenation:
    def __init__(self, baseline_repertoires_path, n_threads):
        self.baseline_repertoires_path = baseline_repertoires_path.rstrip('/')
        self.pub_reps_path = os.path.join(self.baseline_repertoires_path, "corrected_public_repertoires")
        self.pvt_reps_path = os.path.join(self.baseline_repertoires_path, "filtered_private_repertoires")
        self.corrected_reps_path = os.path.join(os.path.dirname(self.baseline_repertoires_path), "corrected_baseline_repertoires")
        self.n_threads = n_threads
        if not os.path.exists(self.corrected_reps_path):
            os.makedirs(self.corrected_reps_path)

    def concatenate_public_private_repertoires(self, file_number):
        rep_file_name = f"rep_{file_number}.tsv"
        concat_fn = os.path.join(self.corrected_reps_path, rep_file_name)
        pub_rep = os.path.join(self.pub_reps_path, rep_file_name)
        pvt_rep = os.path.join(self.pvt_reps_path, rep_file_name)
        dfs_list = [pd.read_csv(rep_file, header=None, index_col=None, sep='\t') for rep_file in [pub_rep, pvt_rep]]
        concatenated_df = pd.concat(dfs_list)
        concatenated_df.to_csv(concat_fn, header=None, index=None, sep='\t')

    def multi_concatenate_public_private_repertoires(self):
        found_pub_reps = glob.glob(self.pub_reps_path + "/rep_*.tsv", recursive=False)
        found_pvt_reps = glob.glob(self.pvt_reps_path + "/rep_*.tsv", recursive=False)
        assert len(found_pub_reps) == len(found_pvt_reps)
        pool = Pool(self.n_threads)
        pool.map(self.concatenate_public_private_repertoires, list(range(len(found_pub_reps))))


if __name__ == '__main__':
    test_rep_concat = PubPvtRepConcatenation(baseline_repertoires_path='/Users/kanduric/Desktop/simairr_tests'
                                                                       '/baseline_reps/', n_threads=2)
    test_rep_concat.multi_concatenate_public_private_repertoires()
