# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/1_morphing.ipynb.

# %% auto 0
__all__ = ['morphing', 'write_output', 'main']

# %% ../nbs/1_morphing.ipynb 3
import os
import numpy as np
import click
import sys
sys.path.append("..")
from pygem.rbf import RBF
# https://gideonbrimleaf.github.io/2021/01/26/relative-imports-python.html

# %% ../nbs/1_morphing.ipynb 5
def morphing(source_template: np.ndarray, # coordinates of the template mesh 
             source_landmarks: np.ndarray,  # Landmarks of the source template
             target_landmarks: np.ndarray,  # Target Landmarks
             ):
    "Morph the target geometry with RBF function - Thin Plate Spine. Plot the mesh and morphed mesh."
    rbf = RBF(original_control_points=source_landmarks, deformed_control_points=target_landmarks,
            func='thin_plate_spline', radius=1.0)
    return rbf#rbf(source_template)

# %% ../nbs/1_morphing.ipynb 6
def write_output(mesh: np.ndarray, # Morphed geometry
    ):
    "Write an output file for the morphed geometry in key file format."
    pass
    return

# %% ../nbs/1_morphing.ipynb 7
def main():
    print(os.getcwd())
    config = read_toml()
    source_landmarks = read_landmarks(config['source']['filename_landmarks'])
    template_geometry = read_nodes(config['source']['filename_geometry'])

    if multiple_targets() == bool: # single target
        target_landmarks = read_landmarks(config['target']['filename_landmarks'])
    # _check_landmarks(source_landmarks, target_landmarks)
        morphed_geometry = morphing(source_landmarks, target_landmarks, template_geometry)
        write_output(morphed_geometry)
    else:
        targets_folder = multiple_targets()
        for folder in targets_folder:
            new_path = os.path.join(config['target']['path'],folder, config['target']['filename_landmarks'])
            target_landmarks = read_landmarks(new_path)
        # _check_landmarks(source_landmarks, target_landmarks)
            morphed_geometry = morphing(source_landmarks, target_landmarks, template_geometry)
            write_output(morphed_geometry)
            print("Yes!!")
    return

# %% ../nbs/1_morphing.ipynb 9
# @click.command()
# def hello():
#     click.echo("hello")

# %% ../nbs/1_morphing.ipynb 10
if __name__ == "__main__":
    main()
    
