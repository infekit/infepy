# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/10_write_key_file.ipynb.

# %% auto 0
__all__ = ['parser', 'df_to_ls_dyna_format', 'write_kfile']

# %% ../nbs/10_write_key_file.ipynb 3
import os
import numpy as np
from nbdev.showdoc import *
import pandas as pd
from argparse import ArgumentParser

# %% ../nbs/10_write_key_file.ipynb 5
def df_to_ls_dyna_format(
    dataframe: pd.DataFrame,  # Dataframe containing node position [Label,x,y,z]
):
    # Trasfrom from a df to LS-DYNA node format *NODE x y z (8,16,16,16)
    list = []
    for i in range(dataframe.shape[0]):
        x = round(float(dataframe.iloc[i, 1]), 6)
        y = round(float(dataframe.iloc[i, 2]), 6)
        z = round(float(dataframe.iloc[i, 3]), 6)
        a = str(dataframe.iloc[i, 0]).ljust(8)
        b = str(x).ljust(16)
        c = str(y).ljust(16)
        d = str(z).ljust(16)
        tmp = "{}{}{}{}\n".format(a, b, c, d)
        list.append(tmp)
    return list

# %% ../nbs/10_write_key_file.ipynb 7
parser = ArgumentParser(description="Write .k file in LS-DYNA from a .csv file. ")
parser.add_argument("--file", type=str, help="Type the path to a csv file")


def write_kfile(path_to_file):
    file = pd.read_csv(path_to_file, comment="#", header=None)  # read the csv
    file_extension = os.path.basename(path_to_file)
    file_name = os.path.splitext(file_extension)[0]  # get the file name

    with open("{}/{}.k".format("../test_data/", file_name), "w") as f:
        list = df_to_ls_dyna_format(file)
        f.write("*NODE \n")  # first line is *NODE
        f.write("# ID\t \t x,\t \ty,\t \tz\n")  # first line is *NODE
        for j in range(len(list)):
            f.writelines("{}".format(list[j]))

# %% ../nbs/10_write_key_file.ipynb 8
# |eval: false
write_kfile("../test_data/source/landmarks_source.fcsv")

# %% ../nbs/10_write_key_file.ipynb 9
# |eval: false
if __name__ == "__main__":
    args = parser.parse_args()
    print("csv file to transform: ", args.file)
    write_kfile(args.file)
