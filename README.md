# simAIRR

![unit_tests](https://github.com/KanduriC/simAIRR/actions/workflows/run_unit_tests.yml/badge.svg)
![docker](https://github.com/KanduriC/simAIRR/actions/workflows/push_docker.yml/badge.svg)

simAIRR provides a simulation approach to generate synthetic AIRR datasets that are suitable for benchmarking machine learning (ML) methods, where undesirable access to ground truth signals in training datasets for ML methods is mitigated. Unlike state-of-the-art approaches, simAIRR constructs antigen-experienced-like baseline repertoires and introduces signals by following the empirical relationship between generation probability and sharing pattern of public sequences calibrated from real-world experimental datasets.

Getting started
---------------

To get started:

- For installation instructions and tutorials, see [documentation](https://kanduric.github.io/simAIRR/): https://kanduric.github.io/simAIRR/
- Consult the [tutorials](https://kanduric.github.io/simAIRR/tutorials.html) for detailed examples of different workflows
- Read a brief overview of simAIRR's simulation approach under [simulation approach](https://kanduric.github.io/simAIRR/overview.html)
- Consult the descriptions of valid [parameter configurations](https://kanduric.github.io/simAIRR/configuration.html)

Installation
============

Install using pip
------------------

``` 
$ pip install simAIRR 
```

Manual installation using git
------------------------------

``` 
$ pip install git+https://github.com/KanduriC/simAIRR.git
```

Use simAIRR through Docker
--------------------------

```
$ docker run -it -v $(pwd):/wd --name my_container kanduric/simairr:latest sim_airr --help
```