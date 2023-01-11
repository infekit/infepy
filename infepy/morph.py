# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/3_morphing.ipynb.

# %% auto 0
__all__ = ['parser', 'morphing', 'do_morphing']

# %% ../nbs/3_morphing.ipynb 4
import os
import numpy as np
import click
from argparse import ArgumentParser

# %% ../nbs/3_morphing.ipynb 5
import infepy.rbf as rbf
import infepy.preprocessing as pre
import infepy.utils as utils

# %% ../nbs/3_morphing.ipynb 6
def morphing(
    source_landmarks: np.ndarray,  # Landmarks of the source mesh
    target_landmarks: np.ndarray,  # Target Landmarks
    source_mesh: np.ndarray,  # Coordinates of the mesh/ mesh
    func,
    smoothing,
):
    "Morph the target mesh with RBF function - Thin Plate Spine."
    basis_function = func

    rad_bas_fun = rbf.RBF(
        original_control_points=utils.from_df_to_np(source_landmarks),
        deformed_control_points=utils.from_df_to_np(target_landmarks),
        func=basis_function,
        smoothing=smoothing,
    )

    return rad_bas_fun(utils.from_df_to_np(source_mesh))

# %% ../nbs/3_morphing.ipynb 8
parser = ArgumentParser(description="Morphing function")
parser.add_argument(
    "--function",
    type=str,
    default="thin_plate_spline",
    help="Basis Function for morphing",
)
parser.add_argument("--smoothing", type=float, default=0.0, help="Smoothing Factor")


def do_morphing(func, smoothing):
    config = utils.read_toml()
    source_landmarks = pre.read_landmarks(
        utils._merge_path(
            config["source"]["path"], config["source"]["filename_landmarks"]
        )
    )
    template_mesh = pre.read_nodes(
        utils._merge_path(config["source"]["path"], config["source"]["filename_mesh"])
    )

    if utils.multiple_targets() == False:  # single target
        target_landmarks = pre.read_landmarks(
            utils._merge_path(
                config["target"]["path"], config["target"]["filename_landmarks"]
            )
        )
        pre._check_landmarks(source_landmarks, target_landmarks)
        morphed_mesh = morphing(
            source_landmarks, target_landmarks, template_mesh, func, smoothing
        )
        pre.write_output(
            morphed_mesh,
            utils._merge_path(config["target"]["path"], "morphed.key"),
            utils._merge_path(
                config["source"]["path"], config["source"]["filename_mesh"]
            ),
        )
    else:
        targets_folder = utils.multiple_targets()
        for folder in targets_folder:
            folder_path = os.path.join(config["target"]["path"], folder)
            target_landmarks = pre.read_landmarks(
                utils._merge_path(folder_path, config["target"]["filename_landmarks"])
            )
            pre._check_landmarks(source_landmarks, target_landmarks)
            morphed_mesh = morphing(
                source_landmarks, target_landmarks, template_mesh, func, smoothing
            )
            pre.write_output(
                morphed_mesh,
                utils._merge_path(folder_path, "morphed.key"),
                utils._merge_path(
                    config["source"]["path"], config["source"]["filename_mesh"]
                ),
            )
    return

# %% ../nbs/3_morphing.ipynb 10
# |eval: false
if __name__ == "__main__":
    args = parser.parse_args()
    print("Radial Basis Function: ", args.function)
    print("Smoothing factor: ", args.smoothing)
    do_morphing(args.function, args.smoothing)
