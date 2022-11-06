User guide
===========

Running simAIRR
----------------
simAIRR can be run through a command-line interface with a single user-supplied parameter - the path to the configuration specification file. Example below:

.. code-block:: console

    $ sim_airr -i <path_to_specification_file>


Configuration format
-------------------------

The configuration for simAIRR's simulations are to be supplied through a flat config file in `YAML format <https://en.wikipedia.org/wiki/YAML>`_. The snippets below show examples of the configuration for different usage modes of simAIRR. See :ref:`configuration_table` for description and default settings of parameters.

Signal implantation mode (without much customisation)
-----------------------------------------------

In the example specification below, since no values were supplied for the non-required arguments, default settings will be used for some parameters (that are not shown in the snippet below). See :ref:`configuration_table` for default settings of other parameters.

.. code-block:: YAML

    mode: signal_feasibility_assessment
    olga_model: humanTRB
    n_repertoires: 10
    n_sequences: 10
    n_threads: 2
    signal_sequences_file: /path/to/ground_truth_signal_sequences.tsv #TODO: write about signal sequences file format
    phenotype_burden: 3

Signal implantation mode (more customisation)
-------------------------------------------------

.. code-block:: YAML

    mode: signal_implantation
    olga_model: humanTRB
    output_path: /path/to/output/directory
    n_repertoires: 10
    seed: 1234
    store_intermediate_files: True
    n_sequences: 10
    n_threads: 2
    public_seq_proportion: 0.08 # 8% of the total unique sequences will be shared across repertoires
    public_seq_pgen_count_mapping_file: /path/to/public_seq_pgen_count_mapping.tsv
    signal_pgen_count_mapping_file: /path/to/signal_pgen_count_mapping.tsv
    signal_sequences_file: /path/to/ground_truth_signal_sequences.tsv
    positive_label_rate: 0.3 # 30% of the total repertoires will receive signal implantation
    phenotype_burden: 3
    phenotype_pool_size: 100 # use only any 100 of the total supplied sequences as a signal superset
    allow_closer_phenotype_burden: False

Signal feasibility assessment mode
-----------------------------------

- It is possible that user-supplied signal sequences cannot be sufficient to meet the user-desired specifications of implantation statistics including desired phenotype burden, number of positive class-labeled repertoires and so on based on realistic levels of population incidence given the generation probability.
- In such a case, `signal_implantation` mode will not succeed in generating simulated repertoires. Rather, guidance will be provided on the signal implantation statistics (what is realistically possible) that will help the user to either tune the simulation parameters or supply a different set of signal sequences or both.
- To help with this process of fine-tuning a set of signal sequences file and parameters of simulation, `signal_feasibility_assessment` mode coule be used. All the parameters of `signal_implantation` mode and `signal_feasibility_assessment` mode are identical. The only difference is that in `signal_implantation` mode, if implantation was deemed feasible, it will proceed with expensive computation steps of baseline repertoire generation and public component correction, whereas the `signal_feasibility_assessment` mode will stop even if the implantation was deemed feasible.

Baseline repertoires generation
--------------------------------

Since the `signal_implantation` mode involves a sequence of steps that also involves baseline repertoires generation, this functionality is also made available to be run in a separate mode. Although generation of baseline repertoires can be accomplished with a few lines of code around existing tools, the parallelised version of this functionality implemented in `baseline_repertoire_generation` mode may turn out to be useful.

.. code-block:: YAML

    mode: baseline_repertoire_generation
    olga_model: humanTRB
    output_path: /path/to/output/directory
    n_repertoires: 20
    n_sequences: 10
    n_threads: 2

Public component correction
---------------------------

When synthetic AIRR datasets are generated using sampling from know V(D)J recombination models using existing tools, the resulting repertoires represent naive repertoires that have not experienced any antigen events. Thus, the proportion of public (shared) sequences in such AIRR datasets will be lower than what is observed in experimental AIRR datasets of antigen-experienced repertoires. To match real-world experimental datasets in terms of public sequences, simAIRR's workflows include a public component correction step, where a fraction of the total unique sequences in the synthetic AIRR dataset (`public_seq_proportion`) will be forced to be shared across repertoires. The sharing pattern will be determined based on empirically learnt relation between generation probability and population incidence of sequences. With sampling from known V(D)J recombination models, one cannot exclude the possibility of observing same sequence twice; `public_component_correction` mode filters out duplicate sequences before making the sequences public.

.. code-block:: YAML

    mode: baseline_repertoire_generation
    olga_model: humanTRB
    output_path: /path/to/output/directory
    n_repertoires: 20
    n_sequences: 10
    n_threads: 2
    public_seq_proportion: 0.12 # 12% of the total unique sequences will be shared across repertoires. Default is 10% if this argument is not supplied.
    public_seq_pgen_count_mapping_file: /path/to/public_seq_pgen_count_mapping.tsv # default is a real-world experimental dataset calibrated mapping that is included with simAIRR


pgen_count_mapping file format
-------------------------------

- For both the signal sequences and remaining public sequences, user could supply custom empirical relation between generation probability and population incidence. The file format for both of those files is shown below. The file should be tab-delimited with required fields: `"pgen_left", "pgen_right",	"sample_size_prop_left", "sample_size_prop_right", "prob"`.
- To prepare such files based on a dataset of interest, one should compute empirical probabilities (`prob`) of observing sequences within a range of population incidence levels (`sample_size_prop_left` and `sample_size_prop_right`) for a given range of generation probability (`pgen_left` and `pgen_right`).
- An example of such file is shown below:

.. csv-table:: pgen_count_mapping file format and example
    :file: public_seq_pgen_count_map.tsv
    :header-rows: 1
    :delim: 0x00000009