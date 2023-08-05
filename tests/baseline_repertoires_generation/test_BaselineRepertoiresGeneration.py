from simAIRR.baseline_repertoires_generation.BaselineRepertoiresGeneration import BaselineRepertoiresGeneration
import os


def test_olga_repertoires_generation(tmp_path):
    olga_reps = BaselineRepertoiresGeneration(model='humanTRB', background_sequences_path=None,
                                              output_file_path=tmp_path,
                                              n_seq=9, seed=1234,
                                              n_reps=10, n_threads=2)
    olga_reps.generate_multiple_repertoires()
    files = [fn for fn in os.listdir(tmp_path) if os.path.isfile(os.path.join(tmp_path, fn))]
    print(tmp_path)
    assert len(files) == 10
    num_lines = sum(1 for line in open(os.path.join(tmp_path, 'rep_9.tsv')))
    assert num_lines == 9


def test__generate_repertoire_from_background_sequences(tmp_path):
    out_filename = os.path.join(tmp_path, 'background_seqs.tsv')
    baseline_reps_path = os.path.join(tmp_path, 'baseline_reps')
    command = 'olga-generate_sequences --humanTRB' + ' -o ' + out_filename + ' -n 1000 --seed 1234'
    exit_code = os.system(command)
    baseline_reps = BaselineRepertoiresGeneration(model=None, background_sequences_path=out_filename,
                                                  output_file_path=baseline_reps_path, n_seq=10, seed=1234, n_reps=12,
                                                  n_threads=2)
    baseline_reps.generate_multiple_repertoires()
    files = [fn for fn in os.listdir(baseline_reps_path) if os.path.isfile(os.path.join(baseline_reps_path, fn))]
    print(baseline_reps_path)
    assert len(files) == 12
    num_lines = sum(1 for line in open(os.path.join(baseline_reps_path, 'rep_9.tsv')))
    assert num_lines == 10
