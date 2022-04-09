import os
import pandas as pd
from simAIRR.concatenate_public_private_repertoires.PubPvtRepertoireConcatenation import PubPvtRepConcatenation
from simAIRR.expand_repertoire_components.PublicRepertoireGeneration import PublicRepertoireGeneration
from simAIRR.expand_repertoire_components.SignalComponentGeneration import SignalComponentGeneration
from simAIRR.olga_baseline_gen.OlgaRepertoiresGeneration import OlgaRepertoiresGeneration
from simAIRR.olga_compute_pgen.OlgaPgenComputation import OlgaPgenComputation
from simAIRR.olga_compute_pgen.UniqueSequenceFilter import UniqueSequenceFilter
from simAIRR.pgen_count_map.PgenCountMap import PgenCountMap
from simAIRR.util.utilities import makedir_if_not_exists, sort_olga_seq_by_pgen


class Workflows:
    def __init__(self, mode: str, olga_model: str, output_path: str, n_sequences: int, n_repertoires: int, n_threads: int, seed: int,
                 public_seq_proportion: float, public_seq_pgen_count_mapping_file: str, signal_pgen_count_mapping_file: str,
                 signal_sequences_file: str, positive_label_rate: float, phenotype_burden: int, phenotype_pool_size: int):
        self.mode = mode
        self.olga_model = olga_model
        self.output_path = output_path
        self.baseline_reps_path = os.path.join(self.output_path, "baseline_repertoires")
        self.filtered_public_reps_path = os.path.join(self.baseline_reps_path, "filtered_public_repertoires")
        self.n_sequences = n_sequences
        self.n_repertoires = n_repertoires
        self.n_threads = n_threads
        self.seed = seed
        self.public_seq_proportion = public_seq_proportion
        self.public_seq_pgen_count_mapping_file = public_seq_pgen_count_mapping_file
        self.signal_pgen_count_mapping_file = signal_pgen_count_mapping_file
        self.signal_sequences_file = signal_sequences_file
        self.positive_label_rate = positive_label_rate
        self.n_pos_repertoires = int(round(self.n_repertoires * positive_label_rate))
        self.phenotype_burden = phenotype_burden
        self.phenotype_pool_size = phenotype_pool_size
        self.signal_components_path = makedir_if_not_exists(os.path.join(self.output_path, "signal_components"))

    def _baseline_repertoire_generation(self):
        olga_reps = OlgaRepertoiresGeneration(model=self.olga_model, output_file_path=self.baseline_reps_path,
                                              n_seq=self.n_sequences, seed=self.seed,
                                              n_reps=self.n_repertoires, n_threads=self.n_threads)
        olga_reps.olga_generate_multiple_repertoires()

    def _public_component_correction(self):
        seq_filter = UniqueSequenceFilter(baseline_repertoires_path=self.baseline_reps_path,
                                          public_sequence_proportion=self.public_seq_proportion, seed=self.seed)
        seq_filter.write_unique_public_and_private_repertoire_components()
        comp_pgen = OlgaPgenComputation(self.filtered_public_reps_path, n_threads=self.n_threads,
                                        model=self.olga_model)
        comp_pgen.multi_compute_pgen()
        pgen_count_map = PgenCountMap(number_of_repertoires=self.n_repertoires,
                                      pgen_count_map_file=self.public_seq_pgen_count_mapping_file)
        pub_rep_gen = PublicRepertoireGeneration(public_repertoires_path=self.filtered_public_reps_path,
                                                 n_threads=self.n_threads, pgen_count_map_obj=pgen_count_map,
                                                 desired_num_repertoires=self.n_repertoires)
        pub_rep_gen.execute()
        rep_concat = PubPvtRepConcatenation(baseline_repertoires_path=self.baseline_reps_path, n_threads=self.n_threads)
        rep_concat.multi_concatenate_public_private_repertoires()

    def _signal_component_generation(self):
        user_signal = pd.read_csv(self.signal_sequences_file, header=None, sep='\t', index_col=None)
        user_signal_file = os.path.join(self.signal_components_path, "user_supplied_signal.tsv")
        user_signal_pgen_file = os.path.join(self.signal_components_path, "pgen_files", "pgen_user_supplied_signal.tsv")
        user_signal.to_csv(user_signal_file, header=None, sep='\t', index_col=None)
        pgen_compute = OlgaPgenComputation(repertoires_path=self.signal_components_path, n_threads=1,
                                           model=self.olga_model)
        pgen_compute.compute_pgen(user_signal_file)
        sort_olga_seq_by_pgen(user_signal_file, user_signal_pgen_file)
        signal_pgen_count_map = PgenCountMap(number_of_repertoires=self.n_pos_repertoires,
                                             pgen_count_map_file=self.signal_pgen_count_mapping_file)
        signal_gen = SignalComponentGeneration(outdir_path=self.output_path, pgen_count_map_obj=signal_pgen_count_map,
                                               desired_num_repertoires=self.n_pos_repertoires,
                                               desired_phenotype_burden=self.phenotype_burden, seed=self.seed,
                                               phenotype_pool_size=self.phenotype_pool_size)
        signal_generation_status_code = signal_gen.generate_signal_components()
        return signal_generation_status_code

    def _simulated_repertoire_generation(self):
        pass

    def workflow_generate_baseline_repertoires(self):
        self._baseline_repertoire_generation()

    def workflow_generate_public_component_corrected_repertoires(self):
        self._baseline_repertoire_generation()
        self._public_component_correction()

    def workflow_generate_signal_implanted_repertoires(self):
        signal_generation_status = self._signal_component_generation()
        if signal_generation_status == 0:
            self._baseline_repertoire_generation()
            self._public_component_correction()
            self._simulated_repertoire_generation()

    def workflow_assess_signal_feasibility(self):
        self._signal_component_generation()

    def execute(self):
        mode_methods = {"baseline_repertoire_generation": self.workflow_generate_baseline_repertoires(),
                        "public_component_correction": self.workflow_generate_public_component_corrected_repertoires(),
                        "signal_implantation": self.workflow_generate_signal_implanted_repertoires(),
                        "signal_feasibility_assessment": self.workflow_assess_signal_feasibility()}
        mode_methods.get(self.mode)


# if __name__ == '__main__':
#     test_flow = Workflows(mode='signal_feasibility_assessment')
#     test_flow.execute()
