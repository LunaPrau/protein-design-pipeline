# select receptor
# select ligand
# dock ligand in receptor (voidDock)
# predict binding sequences (TIMED)
# sequence-based cull
# folding (OMEGA Fold)
# evaluation (DE-STRESS, MD)
# structure-based cull
# top candidates for experiments

import pathlib
from datetime import datetime
from pathlib import Path

# TODO before strating:
# place ligands and receptors in .pdb format in "input" folder (see FOLDER STRUCTURE below)
# edit docking_commands.csv, defining which ligand to dock with which receptor in a form of [(recpetor) ID, Liagnd]
# edit fields below: mglTools_path, util24_path

# FOLDER STRUCTURE
# in the origin_path there must be:
# this script.py,
# ./input/ligands/ with ligands in .pdb format,
# ./input/receptors/ with receptors in .pdb format,
# ./input/docking_commands.csv
# ./timed-design/ with TIMED model in .h5 format

### experiment set up:
# n_docking_poses = 10

### paths:
origin_path = pathlib.Path(__file__).parent
# inputs:
input_path = origin_path / ("input")
dock_command_csv = input_path / ("docking_commands.csv")
receptors_path = input_path / ("receptors")
ligands_path = input_path / ("ligands")
# outputs:
current_date = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
output_path = origin_path / ("output") / ("experiment_" + current_date)
docking_output_path = output_path / ("docking")
timed_output_path = output_path / ("timed")
[path.mkdir(parents=True, exist_ok=True) for path in [docking_output_path, timed_output_path]]
# tools:
mglTools_path = "/home/mchrnwsk/bin/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs"
util24_path = "/home/mchrnwsk/bin/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24"
timed_model_path = origin_path / "timed-design" / "TIMED.h5"
aposteriori_data_prep_path = "/home/mchrnwsk/aposteriori/aposteriori/src/aposteriori/data_prep/cli.py"

### aposteriori
# parameters for creating a dataset
# See: https://github.com/wells-wood-research/aposteriori?tab=readme-ov-file#creating-a-dataset for more info

frame_edge_length = 21
voxels_per_side = 21
aposteriori_dataset_name = "data"
processes = 8
is_pdb_gzipped = False
recursive = True
verbose = True
encode_cb = True
atom_encoder = "CNOCACB"
# download_file = PATH
voxels_as_gaussian = True

### timed
# parameters for prediction
