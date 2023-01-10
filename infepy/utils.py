# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/2_utils.ipynb.

# %% auto 0
__all__ = ['multiple_targets', 'read_k_file', 'read_csv_file', 'from_df_to_np', 'to_ls_dyna']

# %% ../nbs/2_utils.ipynb 3
import os
import numpy as np
import pandas as pd
import toml

# %% ../nbs/2_utils.ipynb 4
def read_toml(config_file="../test_data/config.toml"):  # Path to the config file
    "Read setting file. The File containes the relative path to source and target."
    config = toml.load(config_file)
    return config

# %% ../nbs/2_utils.ipynb 6
def _merge_path(path1: str, path2: str) -> str:
    "Join one or more path components. Return the join path in str type."
    return os.path.join(path1, path2)

# %% ../nbs/2_utils.ipynb 8
def multiple_targets():
    "This function checks if the there are multiple target subject."
    config = read_toml()
    path = config["target"]["path"]
    filename = config["target"]["filename_landmarks"]
    list_target = [
        name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))
    ]
    if not list_target:
        assert os.path.isfile(_merge_path(path, filename)), "No file with Landmarks"
        return False
    else:
        return list_target

# %% ../nbs/2_utils.ipynb 10
def read_k_file(
    path_to_file: str,  # File to read
) -> pd.DataFrame:  # Dataframe of shape [n_nodes, [ID,x,y,z]]
    "This function read *NODES section from .k/.key file."
    id_list = []
    node_coords = []
    find_nodes = False

    # assert os.path.exists(path_to_file), "Wrong path. Path not existent. Check the name/extension of the file."

    with open(path_to_file, "r") as fp:
        for _, line in enumerate(fp):
            if line.startswith("*NODE"):
                find_nodes = True
                continue
            if find_nodes and line.startswith("*"):
                break
            if find_nodes:
                node_id = int(line[:8])
                node_x = float(line[8:24])
                node_y = float(line[24:40])
                node_z = float(line[40:56])
                id_list.append(node_id)
                node_coords.append([node_x, node_y, node_z])

    assert node_coords, "Nodes have NOT been read."

    df = pd.concat([pd.DataFrame(id_list), pd.DataFrame(node_coords)], axis=1)
    df.columns = ["Label - node id", "x", "y", "z"]
    return df

# %% ../nbs/2_utils.ipynb 12
def read_csv_file(
    path_to_file: str,  # File to read.
) -> pd.DataFrame:  # Dataframe of columns are id, x, y,z
    "This function read .csv files in format [id, x, y,z] to Pandas DataFrame"
    with open(path_to_file) as fp:
        df = pd.read_csv(fp, header=None, comment="#")
        df = df.iloc[:, :4]
        df.columns = ["Label - node id", "x", "y", "z"]
    return df

# %% ../nbs/2_utils.ipynb 14
def from_df_to_np(df: pd.DataFrame) -> np.ndarray:
    "This function transform a pd.Dataframe of shape [ID, x,y,z] to numpy array of coordinates [x,y,z]"
    if len(df.columns) == 4:
        return df.iloc[:, 1:4].values

    elif len(df.columns) == 3:
        return df.values
    else:
        raise Exception(
            "Invalid number of column in the Dataframe. Expected either 3 or 4 columns. "
        )

# %% ../nbs/2_utils.ipynb 16
def to_ls_dyna(number):
    "This function write coordinates according to LS-DYNA formatting. Coordinates of nodes requires 16 digit."
    return "{:16f}".format(number)

# %% ../nbs/2_utils.ipynb 17
to_ls_dyna(6.8)
