import os
from subprocess import run
from config import *
import yaml

from aposteriori.data_prep import cli, create_frame_data_set

# temporary way to deal with input of many receptor+ligand pairs at once:
receptors = ["134189607"] # ,"62562582","291312672","432409763","434874344",

#APOSTERIORI and TIMED
for receptor in receptors:
    aposteriori_input = "/home/mchrnwsk/january-pipeline/pipeline/output/experiment_2024-01-19_10:10:35/docking/134189607/final_docked_pdbs"
    aposteriori_dataset_name = receptor
    timed_receptor_output_path = timed_output_path / receptor
    timed_receptor_output_path.mkdir(parents=True, exist_ok=True)
    timed_dataset_path = timed_receptor_output_path / (aposteriori_dataset_name + ".hdf5")
    
    create_frame_data_set.make_frame_dataset(
        structure_files = aposteriori_input,
        output_folder = str(timed_receptor_output_path),
        name = aposteriori_dataset_name,
        frame_edge_length = frame_edge_length,
        voxels_per_side = voxels_per_side,
        keep_side_chain_portion = 0.2,
        processes = processes,
        is_pdb_gzipped = False,
        encode_cb = encode_cb,
        codec = atom_encoder,
        voxels_as_gaussian = voxels_as_gaussian,
        cfile=""
    )
    # creating dataset with aposteriori
# subprocess.run('source activate environment-name && "enter command here" && source deactivate', shell=True)

"""
    os.chdir("/home/mchrnwsk/aposteriori/aposteriori/src/aposteriori/data_prep")
    "-vr"
    cmd = " ".join(["python",str(aposteriori_data_prep_path),str(aposteriori_input),"-o",str(timed_receptor_output_path),"-e",".pdb","--name",aposteriori_dataset_name,"--frame-edge-length",str(frame_edge_length),"--voxels-per-side",str(voxels_per_side),"-p",str(processes),"-vr","-cb",str(encode_cb),"-ae",atom_encoder,"-g",str(voxels_as_gaussian)])
    cmd = 'conda run -n aposteriori '+cmd
    run(cmd, shell=True)
    print("success")
    return_code = run(["python",str(aposteriori_data_prep_path),str(aposteriori_input),"-o",str(timed_receptor_output_path),"-e",".pdb","--name",aposteriori_dataset_name,"--frame-edge-length",str(frame_edge_length),"--voxels-per-side",str(voxels_per_side),"-p",str(processes),"-vr","-cb",str(encode_cb),"-ae",atom_encoder,"-g",str(voxels_as_gaussian)])
    if return_code == 0:
        print("Aposteriori call successful.")
    else:
        print("Aposteriori call failed with return code", return_code)"""