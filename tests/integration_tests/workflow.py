import os.path
import glob
import dask.dataframe as dd

from simAIRR.olga_baseline_gen.OlgaRepertoiresGeneration import OlgaRepertoiresGeneration
from simAIRR.olga_compute_pgen.UniqueSequenceFilter import UniqueSequenceFilter
from simAIRR.olga_compute_pgen.OlgaPgenComputation import OlgaPgenComputation
from simAIRR.pgen_count_map.PgenCountMap import PgenCountMap


def test_workflow():
    out_path = "/Users/kanduric/Desktop/simairr_tests/baseline_reps/"
    olga_reps = OlgaRepertoiresGeneration(model='humanTRB', output_file_path=out_path,
                                          n_seq=100, seed=1234,
                                          n_reps=10, n_threads=2)
    olga_reps.olga_generate_multiple_repertoires()
    seq_filter = UniqueSequenceFilter(baseline_repertoires_path=out_path, public_sequence_proportion=0.1, seed=1234)
    seq_filter.write_unique_public_and_private_repertoire_components()
    comp_pgen = OlgaPgenComputation(os.path.join(out_path, "filtered_public_repertoires"), n_threads=3, model='humanTRB')
    comp_pgen.multi_compute_pgen()
    # # to be modified later
    pgen_files_path = os.path.join(out_path, "filtered_public_repertoires", "pgen_files")
    pgen_files = glob.glob(pgen_files_path + "/pgen_*.tsv", recursive=False)
    test_map = PgenCountMap(number_of_repertoires=10, pgen_count_map_file=
    '/Users/kanduric/Documents/Projects/bm_competition/pilot_bm_data/emerson_pgen_to_counts_mapping_with_vj.tsv')
    breaks_list = test_map.get_pgen_breaks()


    # iterate the list of repertoire_sequence_presence_indices and write_repertoire_files (use maybe separate methods) to write each repertoire file to disk
