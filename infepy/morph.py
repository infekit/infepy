# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/1_morphing.ipynb.

# %% auto 0
__all__ = ['morphing', 'write_output']

# %% ../nbs/1_morphing.ipynb 3
import os
import numpy as np
# https://gideonbrimleaf.github.io/2021/01/26/relative-imports-python.html

# %% ../nbs/1_morphing.ipynb 4
from .rbf import RBF

# %% ../nbs/1_morphing.ipynb 6
def morphing(source_template: np.ndarray, # coordinates of the template mesh 
             source_landmarks: np.ndarray,  # Landmarks of the source template
             target_landmarks: np.ndarray,  # Target Landmarks
             ):
    "Morph the target mesh with RBF function - Thin Plate Spine. Plot the mesh and morphed mesh."
#     rbf = RBF(original_control_points=source_landmarks, deformed_control_points=target_landmarks,
#             func='thin_plate_spline', radius=1.0)
#     return rbf#rbf(source_template)

# %% ../nbs/1_morphing.ipynb 7
def write_output(mesh: np.ndarray, # Morphed mesh
    ):
    "Write an output file for the morphed mesh in key file format."
    pass
    return

# %% ../nbs/1_morphing.ipynb 10
# @click.command()
# def hello():
#     click.echo("hello")
