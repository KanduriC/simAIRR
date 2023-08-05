import os
from simAIRR.util.utilities import count_lines


def test_count_lines(tmp_path):
    out_filename = os.path.join(tmp_path, 'background_seqs.tsv')
    command = 'olga-generate_sequences --humanTRB' + ' -o ' + out_filename + ' -n 1000 --seed 1234'
    exit_code = os.system(command)
    assert count_lines(out_filename) == 1000

