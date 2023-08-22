Configuration manual
====================

.. _configuration_table:

.. csv-table:: **simAIRR arguments**
 :header: "Argument", "Description", "Type", "Required", "Default"
 :widths: 10 50 5 5 30

   "mode", "One of the four possible modes to use simAIRR", "str", "True", "
 None; Legal options:

 * 'baseline_repertoire_generation'
 * 'public_component_correction'
 * 'signal_implantation'
 * 'signal_feasibility_assessment'"
   "olga_model", "One of the four possible V(D)J recombination models supplied with Olga tool", "str", "True", "
 None; Legal options:

 * 'humanTRA'
 * 'humanTRB'
 * 'humanIGH'
 * 'mouseTRB'"
   "output_path", "Path to the output directory","str", "False", "./simairr_output"
   "n_repertoires", "Number of desired repertoires", "int", "True", "None"
    "seed", "A seed to be set if simulations need to be reproducible", "int", "False", "No reproducible seed "
    "n_sequences", "Approximate and minimum number of sequences desired in each repertoire", "int", "True", "None"
    "depth_variation", "whether to have poisson variation around desired number of sequences (applicable only in baseline repertoire generation mode)", "bool", "False", "False"
    "background_sequences_path", "path to a file containing background sequences that will be used for the construction of baseline repertoires instead of a OLGA V(D)J model", "str", "False", "None"
    "n_threads", "Number of processes (reduces execution time at the expense of using more of the available CPUs", "int", "True", "None"
    "public_seq_proportion", "The proportion of the total unique sequences in repertoire dataset to be shared across repertoires (a value between 0 and 1)", "float", "False", "0.1"
    "public_seq_pgen_count_mapping_file", "Path to the file in the suggested format with empirical relation between generation probability and population incidence of public sequences", "str", "False", "Empirical relation derived based on public sequence data from Emerson et al., 2017"
    "signal_pgen_count_mapping_file", "Path to the file in the suggested format with empirical relation between generation probability and population incidence of signal sequences", "str", "False", "Empirical relation derived based on reported signal data from Emerson et al., 2017"
    "signal_sequences_file", "Path to the file with signal sequences (in OLGA format)", "str", "True", "None"
    "positive_label_rate", "Proportion of desired repertoires to receive signal implantation", "float", "False", "0.5"
    "phenotype_burden", "Average number of signal sequences each positive class labeled repertoire should carry", "int", "True", "None"
    "phenotype_pool_size", "Desired number of sequences to be used for signal implantation (if a large pool of sequences are supplied initially)", "int", "False", "Minimum number of sequences sufficient to meet desired phenotype burden will be chosen"
    "allow_closer_phenotype_burden", "If signal implantation was found infeasible precisely at the desired phenotype burden, whether to allow signal implantation at a closer phenotype burden", "bool", "False", "True"
    "store_intermediate_files", "whether to store all the intermediate files that were generated and used as the basis for simulated repertoires", "bool", "False", "False"
    "negative_control", "whether baseline repertoires are intended as negative control", "bool", "False", "False"
    "export_nt", "whether to export nucleotide sequences in simulated repertoires", "bool", "False", "
 True; Exception:

 * False when no nucleotide sequences supplied in user-supplied signal sequences"


