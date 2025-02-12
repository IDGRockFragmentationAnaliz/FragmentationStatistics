import scipy as sp
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

from pyrockstats.empirical import ecdf
from pyrockstats.distrebutions import lognorm


def main():
    thin_section_folder = Path("D:/PycharmProjects/FragmentationStatistics/ThinSection")

    data = {}
    for file_path in thin_section_folder.iterdir():
        name = file_path.name
        print(name)
        file_path = file_path / (name + "_S.mat")
        s, p = get_data(file_path)
        pix2cm = 0.25 / 1000
        pix2m = pix2cm / 100
        pix2m2 = pix2m ** 2

        dist = {
            "empirical": {},
            "lognorm": {}
        }
        areas = s[0]

        x_min = np.log10(np.min(areas))
        x_max = np.log10(np.max(areas))
        s = np.sum(areas)
        bins = np.logspace(x_min, x_max, 10)
        hist, bins = np.histogram(areas, bins)
        bins = bins * pix2m2
        hist = hist / (s * pix2m2)
        data[name] = {
            "bins": bins,
            "hist": hist
        }

        # fig = plt.figure(figsize=(14, 9))
        # axs = [fig.add_subplot(1, 1, 1)]
        # axs[0].stairs(data[name]["hist"], data[name]["bins"], fill=True)
        # axs[0].set_xscale('log')
        # #axs[0].set_yscale('log')
        # plt.show()
        #exit()

    #print(data)
    sp.io.savemat("ThinSection_hists.mat", data)
    #
    # fig = plt.figure(figsize=(16, 4))
    # ax = [fig.add_subplot(1, 1, 1)]
    # ax[0].plot(dist["x"], dist["empirical"]["cdf"], color='black', label='2')
    # ax[0].plot(dist["x"], dist["lognorm"]["cdf"], color='blue', label='2')
    # ax[0].set_xscale('log')
    # ax[0].set_ylim((0, 1))
    # plt.show()


def get_data(file_path: Path):
    mat_dict = sp.io.loadmat(str(file_path), squeeze_me=True)
    s = mat_dict['S']
    p = mat_dict['P']
    return s, p


if __name__ == "__main__":
    main()