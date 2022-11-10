.. _Install simAIRR:

Installation
============

Install using pip
------------------
- **Does not work yet at the moment**
.. code-block:: console

   $ pip install simAIRR

Manual installation
--------------------

.. code-block:: console

   $ pip install git+https://github.com/KanduriC/simAIRR.git


Use simAIRR through Docker
--------------------------


.. code-block:: console

   $ docker run -it -v $(pwd):/wd --name my_container kanduric/simairr:latest sim_airr --help
