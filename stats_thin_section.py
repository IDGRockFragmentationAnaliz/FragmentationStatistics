import scipy as sp
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

from pyrockstats.empirical import ecdf
from pyrockstats.distrebutions import lognorm
import json

def main():
    thin_section_folder = Path("D:/PycharmProjects/FragmentationStatistics/ThinSection")

    data = {}
    for i, file_path in enumerate(thin_section_folder.iterdir()):
        name = file_path.name
        print(name)
        file_path = file_path / (name + "_S.mat")
        s, p = get_data(file_path)
        pix2um = 2.5
        pix2um2 = pix2um**2

        areas = s[2]

        x_min = np.log10(np.min(areas))
        x_max = np.log10(np.max(areas))
        s = np.sum(areas)
        bins = np.logspace(x_min, x_max, 20)
        hist, bins = np.histogram(areas, bins)
        bins = bins * pix2um2
        min_num = np.argmin(hist)
        if hist[min_num] == 0:
            hist = hist[0:min_num]
            bins = bins[0:min_num+1]
        hist = hist / (s * (pix2um2))
        data[name] = {
            "bins": list(bins),
            "density": list(hist),
            "units": "um"
        }

    with open("data/thin_section_hists.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)

    #sp.io.savemat("ThinSection_hists.mat", data)


def get_data(file_path: Path):
    mat_dict = sp.io.loadmat(str(file_path), squeeze_me=True)
    s = mat_dict['S']
    p = mat_dict['P']
    return s, p


if __name__ == "__main__":
    main()