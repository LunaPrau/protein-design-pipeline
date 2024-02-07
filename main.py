# general tools
import yaml
import sys
import os
import typing
import pathlib
import warnings
# configuration / input file
from config import *

# tools for the pipeline steps
voidDock_directory = os.path.join(origin_path, "voidDock")
sys.path.append(voidDock_directory)
aposteriori_directory = os.path.join(origin_path, "aposteriori")
sys.path.append(aposteriori_directory)
timed_design_directory = os.path.join(origin_path, "timed_design")
sys.path.append(timed_design_directory)

import voidDock
import aposteriori
from aposteriori.data_prep.create_frame_data_set import (
    Codec,
    make_frame_dataset,
    StrOrPath,
    keep_sidechains,
    download_pdb_from_csv_file,
)
from timed_design.predict import load_dataset_and_predict

# temporary way to deal with input of many receptor+ligand pairs at once:
receptors = ["134189607", "62562582"] # ,"62562582","291312672","432409763","434874344",

### VOIDDOCK


# running voidDock
voidDock_yaml_config = dock_structures
voidDock.main(voidDock_yaml_config)

#APOSTERIORI and TIMED
for receptor in receptors:
    aposteriori_input = docking_output_path / receptor / "final_docked_pdbs"
    aposteriori_dataset_name = receptor # what happens when one receptor is docked with different ligands? How to name it, how would it be saved?
    timed_receptor_output_path = timed_output_path / receptor
    timed_receptor_output_path.mkdir(parents=True, exist_ok=True)
    timed_dataset_path = timed_receptor_output_path / (aposteriori_dataset_name + ".hdf5")

    # creating dataset with aposteriori
    ### COPIED FROM CLI to avoid click decorator
    extension = "pdb1.gz"
    if download_file and pathlib.Path(download_file).exists():
        structure_files: typing.List[StrOrPath] = download_pdb_from_csv_file(
            pdb_csv_file=pathlib.Path(download_file),
            pdb_outpath=pathlib.Path(timed_receptor_output_path),
            verbosity=verbose,
            workers=processes,
            voxelise_all_states=voxelise_all_states,
        )
    else:
        # Extract all the PDBs in folder:
        if pathlib.Path("/home/mchrnwsk/dataset/TIMED_datasets/structures").exists():
            structure_folder_path = pathlib.Path("/home/mchrnwsk/dataset/TIMED_datasets/structures")
            structure_files: typing.List[StrOrPath] = list(
                structure_folder_path.glob(f"**/*{extension}")
                if recursive
                else structure_folder_path.glob(f"*{extension}")
            )
            if not structure_files:
                print(
                    f"No structure_files found in `{structure_folder_path}`. Did you mean to "
                    f"use the recursive flag?"
                )
                sys.exit()
        else:
            warnings.warn(
                f"{aposteriori_input} file not found. Did you specify the -d argument for the download file? If so, check your spelling."
            )
            sys.exit()
    # Create Codec:
    if atom_encoder == "CNO":
        codec = Codec.CNO()
    elif atom_encoder == "CNOCB":
        codec = Codec.CNOCB()
    elif atom_encoder == "CNOCACB":
        codec = Codec.CNOCACB()
    elif atom_encoder == "BackSideOrg":
        codec = Codec.BackSideOrg()
    elif atom_encoder == "BackCBSideOrg":
        codec = Codec.BackCBSideOrg()

    else:
        assert atom_encoder in [
            "CNO",
            "CNOCB",
            "CNOCACB",
            "BackSideOrg",
            "BackCBSideOrg",
        ], f"Expected encoder to be CNO, CNOCB, CNOCACB, BackSideOrg or BackCBSideOrg but got {atom_encoder}"

    make_frame_dataset(
        structure_files=structure_files,
        output_folder=timed_receptor_output_path,
        name=aposteriori_dataset_name,
        frame_edge_length=frame_edge_length,
        voxels_per_side=voxels_per_side,
        keep_side_chain_portion=keep_side_chain_portion,
        cfile=cfile,
        codec=codec,
        atom_filter_fn=keep_sidechains,
        pieces_filter_file=pieces_filter_file,
        processes=processes,
        is_pdb_gzipped=True,
        verbosity=verbose,
        encode_cb=encode_cb,
        voxels_as_gaussian=voxels_as_gaussian,
        blacklist_csv=blacklist_csv,
        gzip_compression=compression_gzip,
        voxelise_all_states=voxelise_all_states,
    )

    print("Here I am!")

    # predicting residues with timed
    load_dataset_and_predict(
         models = [timed_model_path],
         dataset_path = timed_dataset_path,
         path_to_output = timed_receptor_output_path,
         batch_size = batch_size,
         start_batch = start_batch,
         dataset_map_path = dataset_map_path,
         blacklist = blacklist,
         predict_rotamers = predict_rotamers,
         model_name_suffix = model_name_suffix,
         is_consensus = is_consensus
    )

####################################################################################################################################################################################################################################################################################

def dock_structures():
    # arguments in voidDock format
    voidDock_config = dict(
        dockingTargetsInfo = dict(
            protDir = str(receptors_path),
            ligandDir = str(ligands_path),
            outDir = str(docking_output_path),
            ligandOrdersCsv = str(dock_command_csv)
        ),
        toolInfo = dict(
            mglToolsDir = str(mglTools_path),
            util24Dir = str(util24_path)
        )
    )
    # save yaml config file
    voidDock_yaml_config = voidDock_yaml_config_name
    with open(voidDock_yaml_config, 'w') as outfile:
        yaml.dump(voidDock_config, outfile, default_flow_style=False)

    return voidDock_yaml_config