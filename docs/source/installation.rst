.. _Install simAIRR:

Installation
============

Install using pip
------------------

.. code-block:: console

   $ pip install simAIRR

Manual installation using git
------------------------------

.. code-block:: console

   $ pip install git+https://github.com/KanduriC/simAIRR.git


Use simAIRR through Docker
--------------------------

.. code-block:: console

   $ docker run -it -v $(pwd):/wd --name my_container kanduric/simairr:latest sim_airr --help
