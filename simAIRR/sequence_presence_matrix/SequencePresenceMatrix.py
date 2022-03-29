import numpy as np
import pandas as pd


class SequencePresenceMatrix:
    def __init__(self, number_of_repertoires, presence_counts_list):
        self.number_of_repertoires = number_of_repertoires
        self.null_matrix = np.zeros((len(presence_counts_list), self.number_of_repertoires), dtype=int)
        self.presence_counts_list = presence_counts_list

    def _get_random_presence_indices(self, presence_count):
        return np.random.choice(self.number_of_repertoires, presence_count, replace=False)

    def _update_seq_presence_matrix(self, presence_count, row_index):
        col_indices = self._get_random_presence_indices(presence_count)
        self.null_matrix[row_index, col_indices] = 1

    def _map_update_seq_presence_matrix(self):
        for i, presence_count in enumerate(self.presence_counts_list):
            self._update_seq_presence_matrix(presence_count=presence_count, row_index=i)

    def get_repertoire_sequence_presence_indices(self):
        self._map_update_seq_presence_matrix()
        nonzero_seq_indices = [np.where(self.null_matrix[:, i] > 0) for i in range(self.number_of_repertoires)]
        return [item for sublist in nonzero_seq_indices for item in sublist]


if __name__ == '__main__':
    test_mat = SequencePresenceMatrix(number_of_repertoires=10, presence_counts_list=[2,1,1,4,2,6,1,3,9])
    print(test_mat.get_repertoire_sequence_presence_indices())
    # nonzero_seq_indices = [np.where(test_mat.null_matrix[:,i]>0) for i in range(10)]
    # print(nonzero_seq_indices)
    # test_df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list('ABCD'))
    # print("indices are:", nonzero_seq_indices[0][0])
    # print(test_df.loc[nonzero_seq_indices[i][0]])