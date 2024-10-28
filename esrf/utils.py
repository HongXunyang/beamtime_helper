import numpy as np


def read_spec_file(filename, scans):
    """
    Reads a .spec file and extracts data for the given scans.

    Parameters:
        filename (str): The path to the .spec file.
        scans (list of int): The scan numbers to read.

    Returns:
        data_all (list of np.ndarray): Data arrays for each scan.
        colname_all (list of list): Column names for each scan.
        motval_all (list of dict): Motor values for each scan.
        motname_all (list of list): Motor names for each scan.
        date (list): Dates for each scan.
    """
    data_all = []
    colname_all = []
    motval_all = []
    motname_all = []
    date = []

    with open(filename, "r") as file:
        content = file.readlines()

    for scan_num in scans:
        scan_header = f"#S {scan_num}"
        scan_data = []
        colnames = []
        motvals = {}
        motnames = []
        scan_date = ""

        in_scan = False
        for line in content:
            if line.startswith(scan_header):
                in_scan = True
            elif in_scan and line.startswith("#L"):
                colnames = line[3:].strip().split()
            elif in_scan and line.startswith("#P"):
                mot_values = line[3:].strip().split()
                motvals = {
                    f"Motor_{i+1}": float(val) for i, val in enumerate(mot_values)
                }
            elif in_scan and line.startswith("#D"):
                scan_date = line[3:].strip()
            elif in_scan and not line.startswith("#"):
                data_line = [float(val) for val in line.strip().split()]
                scan_data.append(data_line)
            elif in_scan and line.strip() == "":
                # End of scan data
                break

        if scan_data:
            data_all.append(np.array(scan_data))
            colname_all.append(colnames)
            motval_all.append(motvals)
            motname_all.append(list(motvals.keys()))
            date.append(scan_date)

    return data_all, colname_all, motval_all, motname_all, date
