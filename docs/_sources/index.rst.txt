.. simAIRR documentation master file, created by
   sphinx-quickstart on Tue Apr 26 21:33:02 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to simAIRR's documentation!
===================================

simAIRR provides a simulation approach to generate synthetic AIRR datasets that are suitable for benchmarking machine learning (ML) methods, where undesirable access to ground truth signals in training datasets for ML methods is mitigated. Unlike state-of-the-art approaches, simAIRR constructs antigen-experienced-like baseline repertoires and introduces signals by following the empirical relationship between generation probability and sharing pattern of public sequences calibrated from real-world experimental datasets.

Getting started
---------------

To get started:

- Read a brief overview of simAIRR's simulation approach under :ref:`simulation approach`
- Consult the descriptions of :ref:`configuration_table`
- For installation, see :ref:`Install simAIRR`
- Consult the :ref:`user guide` for tutorials and examples of different workflows


Contents
--------

.. toctree::
   :maxdepth: 1

   installation
   overview
   configuration
   tutorials


..
   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
