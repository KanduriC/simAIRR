import os.path
import pandas as pd
import numpy as np
from pathlib import Path


def concatenate_files(files_path, file_pattern):
    found_files = Path(files_path).glob(file_pattern)
    li = []
    for i, filename in enumerate(found_files):
        print("processing file number:", i)
        fn = pd.read_csv(filename, header=None, sep='\t')
        li.append(fn)
    concatenated_df = pd.concat(li, axis=0, ignore_index=True)
    return concatenated_df, len(li)


def makedir_if_not_exists(some_path):
    if os.path.exists(some_path):
        files = [fn for fn in os.listdir(some_path) if
                 os.path.isfile(os.path.join(some_path, fn))]
        files_exists = f"Output folder may already contain relevant files: {some_path}"
        assert len(files) == 0, files_exists
    else:
        os.makedirs(some_path)


def split_dataframe(data_frame, number_of_splits, split_files_path):
    for idx, chunk in enumerate(np.array_split(data_frame, number_of_splits)):
        chunk.to_csv(os.path.join(split_files_path, f'rep_{idx}.tsv'), index=None, header=None, sep='\t')
