from config import *
from aposteriori.data_prep.create_frame_data_set import make_frame_dataset
from aposteriori.data_prep.create_frame_data_set import keep_sidechains

# temporary way to deal with input of many receptor+ligand pairs at once:
receptors = ["134189607"] # ,"62562582","291312672","432409763","434874344",

#APOSTERIORI and TIMED
for receptor in receptors:
    aposteriori_input = "/home/mchrnwsk/protein-design-pipeline/max-with-git/protein-design-pipeline/output/example/docking/62562582/final_docked_pdbs"
    aposteriori_dataset_name = receptor
    timed_receptor_output_path = timed_output_path / receptor
    timed_receptor_output_path.mkdir(parents=True, exist_ok=True)
    timed_dataset_path = timed_receptor_output_path / (aposteriori_dataset_name + ".hdf5")

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
        cfile = ""
    )

    print(value)