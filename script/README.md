# chain_submit.py
will help you to submit all the shell scripts in a second in HPC.
not written by myself.
The directory with this file should be added to $PATH

# prepare-ein.py
will help to prepare directories with files using the templates in this directory.
You can name directory, training data size, QUIP parameters, and everything.
Once you run it, directories are ready to go.

# submit-ein.py
it will automatically submit all the shell scripts in orders using 'chain_submit.py'

# plot.py
Once we have the QUIP data after running all the scripts,
it will automatically run all the 'plot_gap.py' in newly created directories for making figure.
