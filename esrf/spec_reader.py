import numpy as np
import json
from .utils import read_spec_file
import os


def read_spec(filename, scans, output_format="txt", output_filename="output"):
    """
    Reads a .spec file and processes the data.

    Parameters:
        filename (str): The path to the .spec file.
        scans (list of int): The scan numbers to read.
        output_format (str): 'txt' or 'json' for the output file format.
        output_filename (str): The base name of the output file (without extension).

    Returns:
        all_scans (np.ndarray): The processed scan data.
        miller (np.ndarray): The miller indices.
    """
    # Read data from the .spec file
    data_all, colname_all, motval_all, motname_all, date = read_spec_file(
        filename, scans
    )

    num_scans = len(data_all)
    num_rows = len(data_all[0])
    all_scans = np.zeros((num_rows, num_scans * 2))
    H, K, L = [], [], []

    for ii in range(num_scans):
        # For each scan
        colnames = colname_all[ii]
        data = data_all[ii]

        # Find indices of required columns
        if "Energy" in colnames:
            ind_energy = colnames.index("Energy")
        elif "Energy (eV)" in colnames:
            ind_energy = colnames.index("Energy (eV)")
        else:
            ind_energy = colnames.index(" Pixel")

        ind_spc = colnames.index("SPC")
        ind_mirror = colnames.index("Mirror current / 1e6")

        # Assuming motor indices are known
        ind_h = 122
        ind_k = 123
        ind_l = 124

        energy = data[:, ind_energy]
        spc = data[:, ind_spc]
        normal = data[:, ind_mirror]

        H.append(motval_all[ii].get("H", np.nan))
        K.append(motval_all[ii].get("K", np.nan))
        L.append(motval_all[ii].get("L", np.nan))

        miller = np.column_stack((H, K, L))

        # Adjust the size of all_scans if necessary
        min_length = min(len(energy), all_scans.shape[0])
        all_scans = all_scans[:min_length, :]
        all_scans[:, ii * 2 : (ii + 1) * 2] = np.column_stack(
            (energy[:min_length], spc[:min_length] / normal[:min_length])
        )

    # Save the output
    if output_format == "txt":
        np.savetxt(f"{output_filename}.txt", all_scans)
    elif output_format == "json":
        with open(f"{output_filename}.json", "w") as f:
            json.dump(all_scans.tolist(), f)
    else:
        raise ValueError("output_format must be 'txt' or 'json'.")

    return all_scans, miller
