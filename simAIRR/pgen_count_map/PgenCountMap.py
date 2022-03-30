import pandas as pd
import os
import numpy as np
import random


class PgenCountMap:
    
    def __init__(self, number_of_repertoires,
                 pgen_count_map_file=os.path.join(os.path.dirname(__file__), "pgen_count_map.tsv")):
        self.number_of_repertoires = number_of_repertoires
        self.pgen_count_map_file = pgen_count_map_file
        self.pgen_count_map = pd.read_csv(self.pgen_count_map_file, index_col=None, header=0, sep='\t')
        self.pgen_count_map[self.pgen_count_map < 0] = 1e-100
        self.pgen_count_map[['pgen_left', 'pgen_right']] = np.log10(self.pgen_count_map[['pgen_left', 'pgen_right']]).astype(int)

    def get_pgen_breaks(self):
        pgen_breaks = sorted(list(set(self.pgen_count_map['pgen_left']).union(set(self.pgen_count_map['pgen_right']))))
        return pgen_breaks

    def _get_pgen_bin_sample_size_weights(self):
        self.pgen_count_map['pgen_bin'] = self.pgen_count_map[['pgen_left', 'pgen_right']].apply(tuple, axis=1)
        self.pgen_count_map['sample_size_prop_bin'] = self.pgen_count_map[
            ['sample_size_prop_left', 'sample_size_prop_right']].apply(tuple, axis=1)
        new_pgen_count_map = self.pgen_count_map[['pgen_bin', 'sample_size_prop_bin', 'prob']]
        new_pgen_count_map = new_pgen_count_map.groupby('pgen_bin')[['sample_size_prop_bin', 'prob']].apply(
            lambda x: x.set_index('sample_size_prop_bin').to_dict(orient='dict')).to_dict()
        new_pgen_count_map = {key: value['prob'] for key, value in new_pgen_count_map.items()}
        return new_pgen_count_map

    def _get_implantation_rate(self, seq_pgen_bin: tuple):
        pgen_count_map_dict = self._get_pgen_bin_sample_size_weights()
        sample_size_intervals_list = list(pgen_count_map_dict[seq_pgen_bin].keys())
        keys_len = len(sample_size_intervals_list)
        weights_list = list(pgen_count_map_dict[seq_pgen_bin].values())
        sample_size_lower, sample_size_upper = [sample_size_intervals_list[i] for i in np.random.choice(keys_len, 1, p=weights_list)][0]
        return random.uniform(sample_size_lower, sample_size_upper)

    def get_absolute_number_of_repertoires(self, seq_pgen_bin: tuple):
        implant_rate = self._get_implantation_rate(seq_pgen_bin)
        absolute_number_of_repertoires = round(implant_rate * self.number_of_repertoires)
        if absolute_number_of_repertoires < 2:
            absolute_number_of_repertoires = 2
        return absolute_number_of_repertoires


if __name__ == '__main__':
    # test_map = PgenCountMap(number_of_repertoires=200, pgen_count_map_file=
    # '/Users/kanduric/Documents/Projects/bm_competition/pilot_bm_data/emerson_pgen_to_counts_mapping_with_vj.tsv')
    # print(test_map._get_pgen_bin_sample_size_weights())
    # num_reps = test_map.get_absolute_number_of_repertoires((-11.0, -10.0))
    # print(num_reps)

    test_map = PgenCountMap(number_of_repertoires=200, pgen_count_map_file=
    '/Users/kanduric/Documents/Projects/bm_competition/pilot_bm_data/emerson_ground_truth_pgen_to_counts_mapping_with_vj.tsv')
    # print(test_map._get_pgen_bin_sample_size_weights())
    for i in range(10):
        num_reps = test_map.get_absolute_number_of_repertoires((-11.0, -10.0))
        print(num_reps)