import glob
import os
import pandas as pd
import numpy as np
from operator import attrgetter
from multiprocessing import Pool
from simAIRR.pgen_count_map.PgenCountMap import PgenCountMap
from simAIRR.sequence_presence_matrix.SequencePresenceMatrix import SequencePresenceMatrix


class PublicRepertoireGeneration:
    def __init__(self, public_repertoires_path, n_threads, pgen_count_map_obj, desired_num_repertoires):
        self.public_repertoires_path = public_repertoires_path
        self.pgen_files_path = os.path.join(self.public_repertoires_path, "pgen_files")
        self.tmp_chunks_path = os.path.join(self.public_repertoires_path, "tmp_chunks")
        self.corrected_public_repertoires_path = os.path.join(os.path.dirname(self.public_repertoires_path),
                                                              "corrected_public_repertoires")
        self.n_threads = n_threads
        self.pgen_count_map_obj = pgen_count_map_obj
        self.desired_num_repertoires = desired_num_repertoires
        if not os.path.exists(self.corrected_public_repertoires_path):
            os.makedirs(self.corrected_public_repertoires_path)

    def generate_public_repertoires(self, pgen_file):
        original_rep_file = os.path.join(self.public_repertoires_path, os.path.basename(pgen_file).replace('pgen_', ''))
        pgen_dat = pd.read_csv(pgen_file, header=None, index_col=None, sep='\t', names=['aa_seq', 'pgen'])
        pgen_intervals_array = self._get_pgen_intervals(pgen_dat=pgen_dat)
        abs_rep_num = self._get_absolute_number_of_repertoires(pgen_intervals_array)
        seq_presence_indices = self._get_repertoire_sequence_presence_indices(abs_rep_num)
        self._write_public_repertoire_chunks(original_repertoire_file=original_rep_file,
                                             repertoire_sequence_presence_indices=seq_presence_indices)

    def multi_generate_public_repertoires(self):
        found_pgen_files = glob.glob(self.pgen_files_path + "/pgen_*.tsv", recursive=False)
        pool = Pool(self.n_threads)
        pool.map(self.generate_public_repertoires, found_pgen_files)

    def _get_pgen_intervals(self, pgen_dat):
        pgen_dat['pgen_bins'] = pd.cut(np.log10(pgen_dat['pgen']), bins=self.pgen_count_map_obj.get_pgen_breaks(),
                                       include_lowest=True)
        pgen_dat['pgen_left'] = pgen_dat['pgen_bins'].map(attrgetter('left'))
        pgen_dat['pgen_right'] = pgen_dat['pgen_bins'].map(attrgetter('right'))
        pgen_dat['pgen_interval'] = pgen_dat[['pgen_left', 'pgen_right']].apply(tuple, axis=1)
        pgen_intervals_list = pgen_dat['pgen_interval'].to_list()
        return [(int(x), int(y)) for x, y in pgen_intervals_list]

    def _get_absolute_number_of_repertoires(self, pgen_intervals_list):
        return [self.pgen_count_map_obj.get_absolute_number_of_repertoires(interval_bin) for interval_bin in
                pgen_intervals_list]

    def _get_repertoire_sequence_presence_indices(self, abs_num_of_reps_list):
        return SequencePresenceMatrix(number_of_repertoires=self.desired_num_repertoires,
                                      presence_counts_list=abs_num_of_reps_list).get_repertoire_sequence_presence_indices()

    def _write_public_repertoire_chunks(self, original_repertoire_file, repertoire_sequence_presence_indices):
        original_file = pd.read_csv(original_repertoire_file, header=None, index_col=None, sep='\t')
        original_file_chunk_name = os.path.basename(original_repertoire_file).replace(".tsv", "").replace("rep",
                                                                                                          "chunk")
        chunk_path = os.path.join(self.tmp_chunks_path, original_file_chunk_name)
        if not os.path.exists(chunk_path):
            os.makedirs(chunk_path)
        for i, indices in enumerate(repertoire_sequence_presence_indices):
            original_file.loc[indices].to_pickle(os.path.join(chunk_path, f"rep_{i}.pkl"))

    def concatenate_public_repertoire_chunks(self, pgen_file_chunks_list):
        concat_fn = os.path.join(self.corrected_public_repertoires_path, os.path.basename(pgen_file_chunks_list[0]).replace(".pkl", ".tsv"))
        chunk_dfs_list = []
        for file_chunk in pgen_file_chunks_list:
            chunk_df = pd.read_pickle(file_chunk)
            chunk_dfs_list.append(chunk_df)
        concatenated_df = pd.concat(chunk_dfs_list)
        concatenated_df.to_csv(concat_fn, header=None, index=None, sep='\t')

    def multi_concatenate_public_repertoire_chunks(self):
        found_pgen_file_chunks = []
        for i in range(self.desired_num_repertoires):
            found_pgen_files = glob.glob(self.tmp_chunks_path + f"/*/rep_{i}.pkl", recursive=True)
            found_pgen_file_chunks.append(found_pgen_files)
        pool = Pool(self.n_threads)
        pool.map(self.concatenate_public_repertoire_chunks, found_pgen_file_chunks)


if __name__ == '__main__':
    test_gen = PublicRepertoireGeneration(
        public_repertoires_path='/Users/kanduric/Desktop/simairr_tests/baseline_reps/filtered_public_repertoires',
        n_threads=2, pgen_count_map_obj=PgenCountMap(number_of_repertoires=10, pgen_count_map_file=
        '/Users/kanduric/Documents/Projects/bm_competition/pilot_bm_data/emerson_pgen_to_counts_mapping_with_vj.tsv'),
        desired_num_repertoires=10)
    test_gen.multi_generate_public_repertoires()
    test_gen.multi_concatenate_public_repertoire_chunks()
