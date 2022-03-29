from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='simAIRR',
    version='0.1',
    packages=find_packages(exclude=["tests", "test.*"]),
    url='',
    license='MIT',
    author='Chakravarthi Kanduri',
    author_email='chakra.kanduri@gmail.com',
    description='',
    include_package_data=True,
    zip_safe=False
    # entry_points={'console_scripts': ['gen_kmer_specs=utilities_immuneml.generate_random_kmer_specification:execute',
    #                                   'gen_kmer_lists=utilities_immuneml.generate_varying_number_kmers_lists:execute',
    #                                   'gen_random_rep=utilities_immuneml.generate_random_repertoire:execute',
    #                                   'gen_metadata_file=utilities_immuneml.generate_metadata_file:execute',
    #                                   't_test=utilities_immuneml.t_test_between_labeled_groups:execute',
    #                                   'gen_rare_fullseq_specs=utilities_immuneml'
    #                                   '.generate_rare_full_seq_implantation_specs:execute',
    #                                   'generate_n_rare_seqs=utilities_immuneml.return_n_rare_sequences:execute',
    #                                   'perform_fisher=utilities_immuneml.fisher_test_between_labeled_groups:execute',
    #                                   'cat_multipgens=utilities_immuneml.concatenate_multiple_pgen_files:execute',
    #                                   'compute_pgen=utilities_immuneml.run_snakemake_compute_pgen:execute',
    #                                   'concat_airr=utilities_immuneml.concatenate_airr_files:execute',
    #                                   'plot_pgen=utilities_immuneml.plot_pgen_density:execute',
    #                                   'get_pgen_percentiles=utilities_immuneml.get_pgen_distribution_percentiles'
    #                                   ':execute',
    #                                   'pheno_classifier=utilities_immuneml.phenotype_burden_classifier:execute',
    #                                   'gen_coefs_csv=utilities_immuneml.generate_coefs_csv:execute',
    #                                   'anonym_dirs=utilities_bm.anonymise_directories:execute',
    #                                   'generate_baseline_datasets=utilities_bm.generate_baseline_datasets:execute',
    #                                   'gather_datasets=utilities_bm.gather_datasets:execute',
    #                                   'generate_simulation_yamls=utilities_bm.simulation_workflow:execute',
    #                                   'run_immuneml_simulations=utilities_bm.simulation_runner:execute',
    #                                   'reorder_correct_mapping=utilities_bm.reorder_correct_mapping:execute',
    #                                   'run_compairr_seqcounts=utilities_bm.run_compairr_seq_count:execute',
    #                                   'compute_pgen_public=utilities_bm.compute_pgen_public_sequences:execute',
    #                                   'concat_pdata=one_time_scripts.concatenate_pdata_files:execute',
    #                                   'get_signal=one_time_scripts.get_seqs_from_yaml:execute']}
)
