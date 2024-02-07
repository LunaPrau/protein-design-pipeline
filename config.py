# select receptor
# select ligand
# dock ligand in receptor (voidDock)
# predict binding sequences (TIMED)
# sequence-based cull
# folding (OMEGA Fold)
# evaluation (DE-STRESS, MD)
# structure-based cull
# top candidates for experiments

import sys
import os
import pathlib
from datetime import datetime
import pathlib

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
### to set imports of packages like voidDock and aposteriori
### add the modules' parent directories to the Python path
voidDock_directory = os.path.join(origin_path, "voidDock")
sys.path.append(voidDock_directory)
aposteriori_directory = os.path.join(origin_path, "aposteriori")
sys.path.append(aposteriori_directory)
timed_design_directory = os.path.join(origin_path, "timed_design")
sys.path.append(timed_design_directory)

### voidDock
voidDock_yaml_config_name = 'voidDock_config.yml'

### aposteriori
# parameters for creating a dataset
# See: https://github.com/wells-wood-research/aposteriori?tab=readme-ov-file#creating-a-dataset for more info

frame_edge_length = 21
voxels_per_side = 21
aposteriori_dataset_name = "data"
extension = ".pdb"
processes = 8
is_pdb_gzipped = False
recursive = True
verbose = 1
encode_cb = True
atom_encoder = "CNOCACB"
voxels_as_gaussian = True
keep_side_chain_portion = 0
compression_gzip = False
voxelise_all_states = True
cfile=""
pieces_filter_file = ""
download_file = ""
blacklist_csv = ""

### timed
# parameters for prediction
timed_model_path = input_path / "TIMED_models" / "default.h5" # alternative: Mert_cnn_timed_cnn_0.5-99-1.82.h5
batch_size = 20
start_batch: int = 0
dataset_map_path = "datasetmap.txt"
blacklist = None
predict_rotamers = False
model_name_suffix = ""
is_consensus = False