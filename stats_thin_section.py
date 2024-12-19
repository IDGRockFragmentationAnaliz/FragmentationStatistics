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
        # x пикс = 0.25 / 1000 - см
        dist = {
            "empirical": {},
            "lognorm": {}
        }
        x, cdf = ecdf(s[0])
        dist["empirical"]["cdf"] = cdf
        dist["x"] = x

        theta = lognorm.fit(s[0])
        dist["lognorm"]["theta"] = theta
        dist["lognorm"]["cdf"] = lognorm(*theta).cdf(x)
        #
        data[name] = theta

    print(data)
    sp.io.savemat("ThinSection_lognorm_theta.mat", data)
    #
    fig = plt.figure(figsize=(16, 4))
    ax = [fig.add_subplot(1, 1, 1)]
    ax[0].plot(dist["x"], dist["empirical"]["cdf"], color='black', label='2')
    ax[0].plot(dist["x"], dist["lognorm"]["cdf"], color='blue', label='2')
    ax[0].set_xscale('log')
    ax[0].set_ylim((0, 1))
    plt.show()


def get_data(file_path: Path):
    mat_dict = sp.io.loadmat(str(file_path), squeeze_me=True)
    s = mat_dict['S']
    p = mat_dict['P']
    return s, p


if __name__ == "__main__":
    main()