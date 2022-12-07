# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/1_morphing.ipynb.

# %% auto 0
__all__ = ['morphing', 'do_morphing']

# %% ../nbs/1_morphing.ipynb 3
import os
import numpy as np
import click

# %% ../nbs/1_morphing.ipynb 4
from .rbf import RBF

# %% ../nbs/1_morphing.ipynb 5
from infepy.preprocessing import (
    read_landmarks,
    read_nodes,
    _check_landmarks,
    write_output,
)
from infepy.utils import (
    read_toml,
    multiple_targets,
    _merge_path,
    to_ls_dyna,
    read_csv_file,
    from_df_to_np,
)

# %% ../nbs/1_morphing.ipynb 6
def morphing(
    source_landmarks: np.ndarray,  # Landmarks of the source mesh
    target_landmarks: np.ndarray,  # Target Landmarks
    source_mesh: np.ndarray,  # Coordinates of the mesh/ mesh
):
    "Morph the target mesh with RBF function - Thin Plate Spine."

    rbf = RBF(
        original_control_points=from_df_to_np(source_landmarks),
        deformed_control_points=from_df_to_np(target_landmarks),
        func="thin_plate_spline",
        radius=1.0,
    )

    return rbf(from_df_to_np(source_mesh))

# %% ../nbs/1_morphing.ipynb 8
@click.command()
@click.option(
    "--name_source",
    type=str,
    prompt="Filename of the source mesh",
    help=" Source mesh name. Indicate complete name and extension.  Example: file.key",
)
@click.option(
    "--landmarks_source",
    type=str,
    prompt="Filename landmark source",
    help=" Source landmarks filename. Indicate complete name and extension.  Example: landmarks.key or landmarks.csv",
)
@click.option(
    "--landmarks_target",
    type=str,
    prompt="Filename landmark target",
    help=" Target landmarks filename. Indicate complete name and extension.  Example: landmarks.key or landmarks.csv",
)
@click.option(
    "--n_target",
    default=1,
    type=int,
    prompt="Number of targets (default is set to 1)",
    help=" Number of targets. INT format. State the number of targets. If no argument is passed, 1 is default value.",
)
def do_morphing(n_target, name_source, landmarks_source, landmarks_target):
    "Perform morphing."
    config = read_toml()
    source_landmarks = read_landmarks(
        _merge_path(config["source"]["path"], landmarks_source)
    )
    template_mesh = read_nodes(_merge_path(config["source"]["path"], name_source))

    if n_target == 1:  # single target
        target_landmarks = read_landmarks(
            _merge_path(config["target"]["path"], landmarks_target)
        )
        _check_landmarks(source_landmarks, target_landmarks)
        morphed_mesh = morphing(source_landmarks, target_landmarks, template_mesh)
        write_output(
            morphed_mesh,
            _merge_path(config["target"]["path"], "morphed_{}".format(name_source)),
            _merge_path(config["source"]["path"], name_source),
        )
    else:
        targets_folder = multiple_targets()
        for folder in targets_folder:
            folder_path = os.path.join(config["target"]["path"], folder)
            target_landmarks = read_landmarks(
                _merge_path(folder_path, landmarks_target)
            )
            _check_landmarks(source_landmarks, target_landmarks)
            morphed_mesh = morphing(source_landmarks, target_landmarks, template_mesh)
            write_output(
                morphed_mesh,
                _merge_path(folder_path, "morphed.key"),
                _merge_path(config["source"]["path"], name_source),
            )
    return

# %% ../nbs/1_morphing.ipynb 9
if __name__ == "__main__":
    do_morphing()
