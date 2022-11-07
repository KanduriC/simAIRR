.. _simulation approach:

Tool overview
=============

The most common need of simAIRR is for its ability to implant full sequence signals at a publicity rate that is not abnormal (given their generation probability) or beyond what is expected based on experimental studies. However, simAIRR can also be used in different auxiliary modes as shown in the image below.

.. figure:: documentation_modes.png
 :alt: Figure 1. simAIRR workflow.

 **Figure 1: simAIRR workflow.** To mitigate unintended shortcut opportunities for AIRR ML in training datasets, we devised a novel simulation approach to generate AIRR datasets that rely on the empiric relation between generation probability and population incidence of public sequences calibrated from real-world experimental datasets separately for signal and other public sequences. For this, the user could either calibrate and supply the relation either on a real-world dataset of their choice or use the default choice that we supply. **simAIRR approach:** using the empirical relation between generation probability and population incidence of AIRs, simAIRR accepts a user-supplied set of AIRs as a potential pool of immune state-associated signals and (i) determines whether it is feasible to introduce signal into the baseline repertoires at the user-desired witness rate. If deemed feasible, simAIRR continues to (ii) generate baseline repertoires and (iii) adjust the proportion of public sequence component (because in datasets generated with naive sampling there is low sequence sharing between repertoires unlike experimental datasets) and generate repertoires with corrected public sequence component, where the relation between generation probability and population incidence is respected, (iv) introduces signal component into the desired number of repertoires, where the relation between generation probability and population incidence is respected. If the signal introduction was deemed infeasible in (i), simAIRR provides descriptive information to the user to act as guidance in re-configuring the simulation. simAIRR could be used to execute the whole workflow (i, ii, iii, iv) in a sequence or exclusively to perform (i) or (ii) or (iii) as shown in top left panel.

