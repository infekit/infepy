# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/1_preprocessing.ipynb.

# %% auto 0
__all__ = ['config', 'read_toml', 'read_nodes', 'read_landmarks', 'write_output']

# %% ../nbs/1_preprocessing.ipynb 3
import os
import numpy as np
import pandas as pd

# %% ../nbs/1_preprocessing.ipynb 4
from .utils import read_k_file, read_csv_file, to_ls_dyna

# %% ../nbs/1_preprocessing.ipynb 6
import toml
from .utils import _merge_path

# %% ../nbs/1_preprocessing.ipynb 7
def read_toml(config_file="Config.toml"):  # Path to the config file
    "Read setting file. The File containes the relative path to source and target."
    config = toml.load(config_file)
    return config


config = read_toml()

# %% ../nbs/1_preprocessing.ipynb 8
def read_nodes(
    path_to_file: str,  # path to file containing source template
) -> pd.DataFrame:  # Numpy array of shape [n_nodes, x,y,z_displacement]
    "Read the nodes from the source template. The source template must be either a .key/.k file or .csv"

    if path_to_file.endswith(".csv") or path_to_file.endswith(".fcsv"):
        mesh_df = read_csv_file(path_to_file)
    elif path_to_file.endswith(".key") or path_to_file.endswith(".k"):
        mesh_df = read_k_file(path_to_file)
    return mesh_df

    # if mesh_df = None, -> no file read.

# %% ../nbs/1_preprocessing.ipynb 9
read_nodes(_merge_path(config["source"]["path"], config["source"]["filename_mesh"]))

# %% ../nbs/1_preprocessing.ipynb 10
def read_landmarks(
    path_to_file: str,  # .csv or .key file containing Landmarks
) -> pd.DataFrame:  # Dataframe of length [n_landmarks] divided in columns [ID - label, x,y,z]
    "Read the landmarks from .csv/.key/.k file."
    file_exist = False
    if path_to_file.endswith(".csv") or path_to_file.endswith(".fcsv"):
        landmarks_df = read_csv_file(path_to_file)
        file_exist = True
    elif path_to_file.endswith(".key") or path_to_file.endswith(".k"):
        landmarks_df = read_k_file(path_to_file)

    assert not landmarks_df.empty
    return landmarks_df

# %% ../nbs/1_preprocessing.ipynb 12
def _check_landmarks(
    source: pd.DataFrame, target: pd.DataFrame  # Source dataframe  # Target dataframe
):
    "This function compares the source and target Dataframe. It performs two test: if the have same amount of landmarks and if Label/IDs are in the same order."
    assert len(source) == len(
        target
    ), "Not same amount of landmarks for source and target"

    bool = target.iloc[:, 0].values == source.iloc[:, 0].values
    assert (
        bool.any() == True
    ), "Order of landmarks is not the same for target and source"

    if bool.any() == False:
        return [i for i, x in enumerate(bool) if x == False]  # => [1, 3]

    # TO DO: return values that are false. Bool gived false and extract index. Print.
    # Sort them
    # if they dont match, return exception -->
    return

# %% ../nbs/1_preprocessing.ipynb 17
def write_output(
    morphed_mesh: np.ndarray,  # Morphed mesh
    morphed_file: np.ndarray,  #  path to directory to save the file
    mesh_file: np.ndarray,  # path to the source mesh from read_setting()
):
    "Write an output file for the morphed mesh in key file format."
    if not os.path.exists(morphed_file):  # write the file if doesn´t exist
        open(morphed_file, "w").close()

    node_indicator = False
    idx_nodes = 0
    # Read the file and read line by line to find *node section.
    with open(mesh_file, "r") as fp:
        file_content = fp.readlines()
    for idx_line, line in enumerate(file_content):
        if line.startswith("*NODE"):
            node_indicator = True
            continue
        if node_indicator and line.startswith("*"):
            break
        if node_indicator:
            line_list = list(line)
            line_list[8:24] = to_ls_dyna(morphed_mesh[idx_nodes, 0])  # x
            line_list[24:40] = to_ls_dyna(morphed_mesh[idx_nodes, 1])  # y
            line_list[40:56] = to_ls_dyna(morphed_mesh[idx_nodes, 2])  # z
            file_content[idx_line] = "".join(line_list)
            idx_nodes += 1
    with open(morphed_file, "w") as fp:
        for line in file_content:
            fp.write(line)
    return
