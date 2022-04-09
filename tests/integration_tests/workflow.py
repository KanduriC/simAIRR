import os.path
from simAIRR.concatenate_public_private_repertoires.PubPvtRepertoireConcatenation import PubPvtRepConcatenation
from simAIRR.expand_repertoire_components.PublicRepertoireGeneration import PublicRepertoireGeneration
from simAIRR.expand_repertoire_components.SignalComponentGeneration import SignalComponentGeneration
from simAIRR.olga_baseline_gen.OlgaRepertoiresGeneration import OlgaRepertoiresGeneration
from simAIRR.olga_compute_pgen.UniqueSequenceFilter import UniqueSequenceFilter
from simAIRR.olga_compute_pgen.OlgaPgenComputation import OlgaPgenComputation
from simAIRR.pgen_count_map.PgenCountMap import PgenCountMap
import pandas as pd

from simAIRR.util.utilities import sort_olga_seq_by_pgen


def test_workflow():
    """
    Given a signal sequences file (in strictly olga format) and optionally a signal_pgen_count mapping file,
    first compute pgen of signal sequences using OlgaPgenComputation.compute_pgen and instantiate a pgen_count_map based
    on signal_pgen_count_mapping and user-defined dataset_implantation_rate, generate multiple signal files using PublicRepertoireGeneration class.

    :param public_seq_pgen_count_mapping:
    :param signal_pgen_count_mapping:
    :param olga_model:
    :param outdir_path:
    :param n_sequences:
    :param n_repertoires:
    :param public_seq_proportion:
    :param seed:
    :param n_threads:
    :param signal_sequences_file:
    :param positive_label_rate:
    :param phenotype_burden:
    :param phenotype_pool_size:
    """
    out_path = "/Users/kanduric/Desktop/simairr_tests/baseline_reps/"
    olga_reps = OlgaRepertoiresGeneration(model='humanTRB', output_file_path=out_path,
                                          n_seq=100, seed=1234,
                                          n_reps=10, n_threads=2)
    olga_reps.olga_generate_multiple_repertoires()
    seq_filter = UniqueSequenceFilter(baseline_repertoires_path=out_path, public_sequence_proportion=0.1, seed=1234)
    seq_filter.write_unique_public_and_private_repertoire_components()
    comp_pgen = OlgaPgenComputation(os.path.join(out_path, "filtered_public_repertoires"), n_threads=3, model='humanTRB')
    comp_pgen.multi_compute_pgen()
    pgen_count_map = PgenCountMap(number_of_repertoires=10, pgen_count_map_file=
    '/Users/kanduric/Documents/Projects/bm_competition/pilot_bm_data/emerson_pgen_to_counts_mapping_with_vj.tsv')
    pub_rep_gen = PublicRepertoireGeneration(
        public_repertoires_path=os.path.join(out_path, "filtered_public_repertoires"),
        n_threads=2, pgen_count_map_obj=pgen_count_map, desired_num_repertoires=10)
    pub_rep_gen.execute()
    rep_concat = PubPvtRepConcatenation(baseline_repertoires_path=out_path, n_threads=2)
    rep_concat.multi_concatenate_public_private_repertoires()

