#!/bin/bash

# Initializing conda
CONDA_BASE=$( conda info --base ) # a variable to store the path to conda
source ${CONDA_BASE}/etc/profile.d/conda.sh # executing the conda.sh file that activates conda

# Activating prokka env
conda activate prokka

echo '\n>> Executing script to run Prokka...\n'

# Creating prokka output directory
mkdir prokka_output

# Looping through mags and executing prokka on each one
for f in mags/*; do
	# Editing the mag name/id
	mag=$( basename $f .fna )
	echo '\n##############################'
	echo '>> Working with:' ${mag}
	echo '##############################\n'

	# Creating the output directory for the mag
	mkdir prokka_output/${mag}

	# Executing prokka on the mag
	prokka mags/${mag}.fna \
		--outdir prokka_output/${mag} \
		--prefix ${mag} \
		--compliant \
		--force
done

# Deactivating prokka env
conda deactivate

