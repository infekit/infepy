# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/000_test.ipynb.

# %% auto 0
__all__ = []

# %% ../nbs/000_test.ipynb 2
import numpy as np
import pandas as pd

# %% ../nbs/000_test.ipynb 3
from .preprocessing import _check_landmarks

# %% ../nbs/000_test.ipynb 4
def _test_landmarks():
    s = {"a": ["Head", "Shaft", "Epiphysis"], "A": [0, 1, 0]}
    t = {"a": ["Head", "Shaft", "Epiphysis"], "A": [0, 1, 1]}
    source = pd.DataFrame(s)
    target = pd.DataFrame(t)
    _check_landmarks(source, target)
    return


_test_landmarks()
