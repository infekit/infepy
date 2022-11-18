# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/1_morphing.ipynb.

# %% auto 0
__all__ = ['morphing']

# %% ../nbs/1_morphing.ipynb 3
import os
import numpy as np

# %% ../nbs/1_morphing.ipynb 4
from .preprocessing import read_landmarks, read_nodes
from .utils import read_toml

# %% ../nbs/1_morphing.ipynb 5
def morphing(source_template: np.ndarray, # coordinates of the template mesh 
             source_landmarks: np.ndarray,  # Landmarks of the source template
             target_landmarks: np.ndarray,  # Target Landmarks
             ):
    "Morph the target geometry with RBF function - Thin Plate Spine. Plot the mesh and morphed mesh."
        
        #rbf = RBF(original_control_points=source_landmarks, deformed_control_points=target_landmarks,
        #       func='thin_plate_spline', radius=1.0)
        #return rbf(source_template)
    
    pass
    return
