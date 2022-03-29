from simAIRR.olga_compute_pgen.UniqueSequenceFilter import UniqueSequenceFilter
import os
import pandas as pd
import numpy as np


def test_filter_unique_sequences(tmp_path):
    baseline_reps_path = tmp_path / "baseline_reps"
    baseline_reps_path.mkdir()
    df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list('ABCD'))
    for idx, chunk in enumerate(np.array_split(df, 10)):
        chunk.to_csv(baseline_reps_path / f'rep_{idx}.tsv', index=None, header=None, sep='\t')
    filtered_path = baseline_reps_path / "filtered_repertoires"
    print(filtered_path)
    original_files = [fn for fn in os.listdir(baseline_reps_path) if os.path.isfile(os.path.join(baseline_reps_path, fn))]
    seq_filter = UniqueSequenceFilter(baseline_reps_path)
    seq_filter.filter_unique_sequences()
    filtered_files = [fn for fn in os.listdir(filtered_path) if os.path.isfile(os.path.join(filtered_path, fn))]
    assert len(original_files) == len(filtered_files)