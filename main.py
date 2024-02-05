import os
from subprocess import call
from config import *
import yaml
from aposteriori.data_prep.create_frame_data_set import make_frame_dataset
from aposteriori.data_prep.create_frame_data_set import keep_sidechains

# temporary way to deal with input of many receptor+ligand pairs at once:
receptors = ["134189607", "62562582"] # ,"62562582","291312672","432409763","434874344",

### VOIDDOCK
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
with open('voidDock_config.yml', 'w') as outfile:
    yaml.dump(voidDock_config, outfile, default_flow_style=False)
# running voidDock
return_code = call(["python", "voidDock/yaml_voidDock.py", "--config", "voidDock_config.yml"])
if return_code == 0:
    print("Docking call successful.")
else:
    print("Docking call failed with return code", return_code)

#APOSTERIORI and TIMED
for receptor in receptors:
    aposteriori_input = docking_output_path / receptor / "final_docked_pdbs"
    # ("docked_pose_"+ str(pose) + ".pdb")
    # ^ this not needed as make frame dataset just runs on .pdb s in the folder specified
    aposteriori_dataset_name = receptor
    # what happens when one receptor is docked with different ligands? How to name it, how would it be saved?
    timed_receptor_output_path = timed_output_path / receptor
    timed_receptor_output_path.mkdir(parents=True, exist_ok=True)
    timed_dataset_path = timed_receptor_output_path / (aposteriori_dataset_name + ".hdf5")

    # creating dataset with aposteriori
    value = make_frame_dataset(
        structure_files=aposteriori_input,
        output_folder=timed_receptor_output_path,
        name=aposteriori_dataset_name,
        frame_edge_length=frame_edge_length,
        voxels_per_side=voxels_per_side,
        keep_side_chain_portion=keep_side_chain_portion,
        codec=atom_encoder,
        atom_filter_fn=keep_sidechains,
        processes=processes,
        is_pdb_gzipped=is_pdb_gzipped,
        verbosity=verbose,
        encode_cb=encode_cb,
        voxels_as_gaussian=voxels_as_gaussian,
        gzip_compression=compression_gzip,
        voxelise_all_states=voxelise_all_states,
        cfile = cfile
    )
    print(value)

    # predicting residues with timed
    return_code = call(["python3","timed-design/predict.py","--path_to_dataset",str(timed_dataset_path),"--path_to_model",str(timed_model_path),"--path_to_output",str(timed_receptor_output_path)])
    if return_code == 0:
        print("Timed call successful.")
    else:
        print("Timed call failed with return code", return_code)       