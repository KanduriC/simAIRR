.. _user guide:

Tutorials
===========

Running simAIRR
----------------
simAIRR can be run through a command-line interface with a single user-supplied parameter - the path to the configuration specification file. Example below:

.. code-block:: console

    $ sim_airr -i <path_to_specification_file>


Configuration file format
--------------------------

The configuration for simAIRR's simulations are to be supplied through a flat config file in `YAML format <https://en.wikipedia.org/wiki/YAML>`_. The snippets below show examples of the configuration for different usage modes of simAIRR. See :ref:`configuration_table` for description and default settings of parameters.

Signal implantation mode (without much customisation)
------------------------------------------------------

In the example specification below, since no values were supplied for the non-required arguments, default settings will be used for some parameters (that are not shown in the snippet below). See :ref:`configuration_table` for default settings of other parameters.

.. code-block:: YAML

    mode: signal_feasibility_assessment
    olga_model: humanTRB
    n_repertoires: 10
    n_sequences: 10
    n_threads: 2
    signal_sequences_file: /path/to/ground_truth_signal_sequences.tsv
    phenotype_burden: 3

Signal implantation mode (more customisation)
----------------------------------------------

- See acceptable file formats of signal sequences file :ref:`signal_seq_file_format`


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
    allow_closer_phenotype_burden: False # whether to allow signal implantation if the feasible phenotype burden is closer to the user-desired phenotype burden (although it is not exact match)
    export_nt: False # whether to export nucleotide sequences in the simulated repertoire files

Signal feasibility assessment mode
-----------------------------------

- It is possible that user-supplied signal sequences cannot be sufficient to meet the user-desired specifications of implantation statistics including desired phenotype burden, number of positive class-labeled repertoires and so on based on realistic levels of population incidence given the generation probability.
- In such a case, `signal_implantation` mode will not succeed in generating simulated repertoires. Rather, guidance will be provided on the signal implantation statistics (what is realistically possible) that will help the user to either tune the simulation parameters or supply a different set of signal sequences or both.
- To help with this process of fine-tuning a set of signal sequences file and parameters of simulation, `signal_feasibility_assessment` mode coule be used. All the parameters of `signal_implantation` mode and `signal_feasibility_assessment` mode are identical. The only difference is that in `signal_implantation` mode, if implantation was deemed feasible, it will proceed with expensive computation steps of baseline repertoire generation and public component correction, whereas the `signal_feasibility_assessment` mode will stop even if the implantation was deemed feasible.

.. _baseline repertoires generation:

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
----------------------------

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


Querying sequences enriched for k-mer like patterns
---------------------------------------------------

Using simAIRR and the new `bionumpy <https://github.com/bionumpy/bionumpy>`_ library, one could query and retrieve sequences enriched for k-mer like patterns very easily with just a few lines of Python code. Below, we provide a simple Python recipe.

Generation of reference sequences to query against
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- First, use the simAIRR's :ref:`baseline repertoires generation` mode to generate a large number of reference sequences to query against. For instance, in the code chunk below, we generate a single file with ten million sequences.

.. code-block:: YAML

    mode: baseline_repertoire_generation
    olga_model: humanTRB
    output_path: /path/to/output/directory
    n_repertoires: 1
    n_sequences: 10000000
    n_threads: 1

Note that instead of generating 10 million sequences in a single file, if multiple processes are used using `n_threads` argument (if more CPUs are available), and the n_sequences are split across multiple repertoires using `n_threads` argument, the reference sequence generation will be much quicker. For instance, the following configuration will generate 10 million sequences across 40 files in less than 2 minutes wall time.

.. code-block:: YAML

    mode: baseline_repertoire_generation
    olga_model: humanTRB
    output_path: /path/to/output/directory
    n_repertoires: 40
    n_sequences: 250000
    n_threads: 40

To combine them into a single file:

.. code-block:: console

    $ cat /path/to/output/directory/* > reference_sequences.txt

- Alternatively, one could use the reference sequences of their choice to query the sequences for k-mer like patterns. The code chunks above is just one example to get a large number of sequences to make queries.
- Let us assume that the ten million sequences that were generated in previous step are stored in a file named ``reference_sequences.txt``.

Pattern matching recipe using bionumpy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Next, we import relevant functionalities from the bionumpy library to read in the ``reference_sequences.txt``, create a lookup index and querying the sequences.
- bionumpy works with popular file formats of biological sequence data. Since bionumpy does not know the file format of our ``reference_sequences.txt``, we first need to tell bionumpy that the first two fields of this custom file format are a dna sequence and an amino acid sequence. The code chunk below shows how to do this. This is routine code and can just be copied as shown below.

    >>> from bionumpy.io.delimited_buffers import DelimitedBuffer, get_bufferclass_for_datatype
    >>> from bionumpy.bnpdataclass import bnpdataclass
    >>> import bionumpy as bnp
    >>> from bionumpy.sequence.indexing.wildcard_index import WildCardLookup

    >>> @bnpdataclass
    ... class Olga:
    ...   dna: bnp.DNAEncoding
    ...   amino_acid: bnp.AminoAcidEncoding


    >>> class OlgaBuffer(DelimitedBuffer):
    ...    dataclass = Olga

- Using the newly created buffer type, we read-in the files with that file format.

    >>> olga_sequence_data = bnp.open(filename="reference_sequences.txt", buffer_type=OlgaBuffer).read()
    >>> olga_sequence_data
    Olga with 10000000 entries
                          dna               amino_acid
      TGCGCCACCTGGGGGGACGA...               CATWGDEQYF
      TGTGCCAGCTCACCTACGAA...         CASSPTNSGSNYGYTF
      TGCGGGCCCGTAATGAACAC...              CGPVMNTEAFF
      TGTGCCAGCAGTGAAGCGCG...         CASSEARPARMYGYTF
      TGTGCCAGCAGTAGTGGGAC...          CASSSGTGPDQPQHF
      TGTGCCAGCAACCTAGCGGG...          CASNLAGKNTGELFF
      TGTGCCAGCAGCCAACCGGG...         CASSQPGGSGNYGYTF
      TGCGCCAGCAGCCGCGGCCT...           CASSRGLREETQYF
      TGTGCCAGCAGCCAAGTCTC...        CASSQVSRQDSSYEQYF
      TGTGCCAGCAGGCCGGGACA...     CASRPGQGAPGWEDNYGYTF

- We create a wildcard lookup table on the amino acid sequences of the file that we read-in.

    >>> aminoacid_wildcard_lookup = WildCardLookup.create_lookup(olga_sequence_data.amino_acid)
    >>> aminoacid_wildcard_lookup
    Lookup on WildcardIndex of 10000000 sequences

- We then retrieve all the sequences that contain a pattern like "RG.", where the "." indicates a wildcard character.

    >>> rg_wildcard_sequences = aminoacid_wildcard_lookup.get_sequences("RG.")
    >>> rg_wildcard_sequences
    encoded_ragged_array(['CASSRGLREETQYF',
                          'CASGCRGTSGGASLDEQFF',
                          'CATSDLGVRRGALIATNEKL...',
                          'CATRRGYGYTF',
                          'CATRGAKRIDEQYF',
                          'CASSLRGQGLLRGNQPQHF',
                          'CASSFSCLRGESSYNEQFF',
                          'CASRGLFPQPQHF',
                          'CASSGCRGGNTEAFF',
                          'CASSEADRGRKAFF',
                          'CASRVASRGRDKQPQHF'], AlphabetEncoding('ACDEFGHIKLMNPQRSTVWY'))


Presence of multiple motifs in sequences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- One may be interested in multiple patterns in sequences. For instance, let us assume that one is interested in sequences that contain either of the following pattern: ``GG**GG`` or ``GG**YG``. One can consider this as two cases:
1. One, where the user is interested in mining those sequences that contain patterns ``GG`` and either of another ``GG`` or ``YG`` that are always two residues apart, where the two residues can be any residues.
2. Alternatively, mining for the above patterns will also result in sequences that always contain a ``GG`` in addition to another ``GG`` or ``YG``.

In either case, the following code block will mine the sequences of interest:

    >>> gg_gg_wildcard_sequences = aminoacid_wildcard_lookup.get_sequences("GG..GG")
    >>> gg_gg_wildcard_sequences
    encoded_ragged_array(['CASSVKPSGGVAGGETQYF',
                          'CSARPGGGEGGENQPQHF',
                          'CASGGRAGGVWAYEQYF',
                          'CASSTEGGLAGGLTYNEQFF',
                            ...
                          'CASSGGPEGGFSSTDTQYF'], AlphabetEncoding('ACDEFGHIKLMNPQRSTVWY'))
    >>> len(gg_gg_wildcard_sequences)
    14968

    >>> gg_yg_wildcard_sequences = aminoacid_wildcard_lookup.get_sequences("GG..YG")
    >>> len(gg_yg_wildcard_sequences)
    28070

If the user is interested in filtering the search results above based on further criteria like gene usage or for containing additional motifs, the resulting sequence set can be considered a proxy for complex signal based on multiple criteria.


Recipe using grep
^^^^^^^^^^^^^^^^^^

Alternatively, one could use the unix ``grep`` function instead. If the user wants to query multiple patterns from the reference sequences, all the patterns could be listed in one file as shown below. In the example below, three patterns are listed in the file named ``query_patterns.txt``.

.. code-block:: console

    $ cat query_patterns.txt
    WKDY
    ERFY
    YREV

- We then query the reference sequences using the patterns from the file ``query_patterns.txt`` and write the output to ``search_results.txt``.

.. code-block:: console

    $ grep -f query_patterns.txt reference_sequences_file.txt > search_results.txt

- We retrieved a total of 705 sequences from the 10 million sequences that contained any of the three patterns listed in ``query_patterns.txt``.

.. code-block:: console

    $ wc -l search_results.txt
    705

Conditioning on gene usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If one is interested in using/testing sequences that match only a particular V or J gene, the ``search_results.txt`` could further be filtered to match the specific genes of interest. As an example, if the user is interested only in those sequences where TRBV5 or TRBV27 genes are used, one could further filter the ``search_results.txt`` as shown below:

.. code-block:: console

    $ grep "TRBV27\|TRBV5" search_results.txt > search_results_trbv5_trbv27.txt
    $ wc -l search_results_trbv5_trbv27.txt
    114



Wall time estimate for pattern matching
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- In the examples that we have shown above, generation of 10 million sequences on 40 CPUs took less than 1 minute wall time and the query of the reference sequences using either bionumpy or unix grep took less than 1 minute wall time when we queried three patterns. The query time can increase with increase in the number of patterns, but for AIRR benchmarking datasets-relevant number of patterns, the query time could still be reasonably efficient.

.. _signal_seq_file_format:

File format of ground truth signal sequences
---------------------------------------------

The ground truth signal sequences file is expected to be a tab-delimited file with at least 3 columns and without a header line. See below for file formats that are accepted.

Supplying nucleotide sequences is optional. If nucleotide sequences are not supplied,
nucleotide sequences are not exported in the simulated repertoires by default. This behavior can be changed with `export_nt` parameter.

.. csv-table:: When including nucleotide sequences
    :file: with_nt.tsv
    :header-rows: 0
    :delim: 0x00000009

.. csv-table:: When not including nucleotide sequences
    :file: with_empty_nt.tsv
    :header-rows: 0
    :delim: 0x00000009

.. csv-table:: When not including nucleotide sequences
    :file: with_empty_nt_2.tsv
    :header-rows: 0
    :delim: 0x00000009

.. csv-table:: When not supplying nucleotide sequences field
    :file: no_nt.tsv
    :header-rows: 0
    :delim: 0x00000009

pgen_count_mapping file format
-------------------------------

The user is not required to supply this file unless the user desires to generate simulated datasets based on a custom model derived from a specific experimental dataset.

- For both the signal sequences and remaining public sequences, user could supply custom empirical relation between generation probability and population incidence. The file format for both of those files is shown below. The file should be tab-delimited with required fields: `"pgen_left", "pgen_right",	"sample_size_prop_left", "sample_size_prop_right", "prob"`.
- To prepare such files based on a dataset of interest, one should compute empirical probabilities (`prob`) of observing sequences within a range of population incidence levels (`sample_size_prop_left` and `sample_size_prop_right`) for a given range of generation probability (`pgen_left` and `pgen_right`).
- An example of such file is shown below:

.. csv-table:: pgen_count_mapping file format and example
    :file: public_seq_pgen_count_map.tsv
    :header-rows: 1
    :delim: 0x00000009

