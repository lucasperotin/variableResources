USAGE :

genSin.py is the python file used to create Synthetic traces.
vargen.py is the python file used to create Variation traces.
genData.py is the python file used to compute the distribution of job's length based on previous traces.
simu.cc is the file that takes as input a job file, a variation file and a heuristic to simulate the scheduling procedure.
plotter.py is the python file used to draw result plots.

master.py is the global file to run expreriments, that uses all the previous files. In the arguments may be defined all parameters, the current version is the one used for the experiments of this paper, and may be modified.

To run experiments, first compile the simu.cc file with "g++ simu.cc -o SIM -O3"; then execute the master script "python3 master.py"
Once the experiments are done, use the master.py file again to draw graphs, by uncommenting the line "#TODO=["plots"]" and execute "python3 master.py" again.

The first few lines of master.py correspond to the parameters used in the papers. nbSamples (number of traces per set of parameters) and nbVar (number of variations tested for any set of parameters+trace) can be reduced for faster experiments.
