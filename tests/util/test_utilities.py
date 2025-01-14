import glob
import os
import pandas as pd
from simAIRR.util.utilities import count_lines, concatenate_dataframes_with_replacement, get_legal_vj_pairs, \
    filter_legal_pairs
from simAIRR.workflows.Workflows import Workflows


def test_count_lines(tmp_path):
    out_filename = os.path.join(tmp_path, 'background_seqs.tsv')
    command = 'olga-generate_sequences --humanTRB' + ' -o ' + out_filename + ' -n 1000 --seed 1234'
    exit_code = os.system(command)
    assert count_lines(out_filename) == 1000


def test_concatenate_dataframes_with_replacement():
    df_a = pd.DataFrame({
        'junction': ['j1', 'j2', 'j3', 'j4', 'j5', 'j16'],
        'junction_aa': ['aa1', 'aa2', 'aa3', 'aa4', 'aa5', 'aa16'],
        'v_call': ['TRBV20-1', 'TRBV20-2', 'TRBV20-3', 'TRBV20-1', 'TRBV20-2', 'TRBV20-3'],
        'j_call': ['TRBJ2-1', 'TRBJ2-2', 'TRBJ2-3', 'TRBJ2-3', 'TRBJ2-2', 'TRBJ2-1']
    })

    df_b = pd.DataFrame({
        'junction': ['j6', 'j7', 'j8', 'j9', 'j10'],
        'junction_aa': ['aa5', 'aa6', 'aa7', 'aa8', 'aa9'],
        'v_call': ['TRBV20-1', 'TRBV20-2', 'TRBV20-2', 'TRBV20-5', 'TRBV20-5'],
        'j_call': ['TRBJ2-1', 'TRBJ2-2', 'TRBJ2-5', 'TRBJ2-1', 'TRBJ2-5']
    })
    df = concatenate_dataframes_with_replacement([df_a, df_b])
    assert df.shape == (6, 4)

def test_get_legal_vj_pairs(tmp_path):
    user_config_dict = {'mode': 'baseline_repertoire_generation',
                        'olga_model': 'humanTRB',
                        'output_path': None,
                        'n_repertoires': 1,
                        'seed': 1234,
                        'n_sequences': 10000,
                        'n_threads': 1,
                        'store_intermediate_files': True,
                        'depth_variation': True}
    out_path = tmp_path / "workflow_output"
    user_config_dict['output_path'] = out_path
    desired_workflow = Workflows(**user_config_dict)
    desired_workflow.execute()
    background_sequences = glob.glob(os.path.join(out_path, "simulated_repertoires", "*.tsv"))[0]
    legal_pairs = get_legal_vj_pairs(background_sequences)
    df = pd.read_csv(background_sequences, sep="\t", header=0)
    if df.shape[1] == 3:
        df.insert(0, 'nt_seq', "NA")
    df.columns = ['junction', 'junction_aa', 'v_call', 'j_call']
    df['v_j_call'] = list(zip(df['v_call'], df['j_call']))
    unique_combinations = df['v_j_call'].value_counts()
    assert len(legal_pairs) <= unique_combinations.shape[0]

def test_filter_legal_pairs():
    df = pd.DataFrame({
        'junction': ['j1', 'j2', 'j3', 'j4', 'j5'],
        'junction_aa': ['aa1', 'aa2', 'aa3', 'aa4', 'aa5'],
        'v_gene': ['TRBV20-1', 'TRBV20-2', 'TRBV20-3', 'TRBV20-4', 'TRBV20-2'],
        'j_gene': ['TRBJ2-1', 'TRBJ2-2', 'TRBJ2-3', 'TRBJ2-4', 'TRBJ2-2']
    })

    legal_pairs = [('TRBV20-1', 'TRBJ2-1'), ('TRBV20-2', 'TRBJ2-2')]
    df = filter_legal_pairs(df, legal_pairs)
    assert df.shape == (3, 4)
    assert df['junction'].tolist() == ['j1', 'j2', 'j5']