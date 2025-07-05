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
        areas = s[2]
        data[name] = get_density_data(areas)

    with open("data/thin_section_densities.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)


def get_data(file_path: Path):
    mat_dict = sp.io.loadmat(str(file_path), squeeze_me=True)
    s = mat_dict['S']
    p = mat_dict['P']
    return s, p


def get_density_data(s):
    # вычисление размера пикселя
    pix2um = 2.5
    s = np.delete(s, np.argmax(s))
    xmin = np.min(s)
    xmax = np.max(s)

    # Начальное число бинов
    n_bins = 10
    min_bins = 7  # минимальное допустимое число бинов

    # Логарифмические бины
    hist = None
    bins = None
    while True:
        bins = np.logspace(np.log10(xmin), np.log10(xmax), n_bins)
        hist, bins = np.histogram(s, bins=bins)
        if np.all(hist > 0):
            break
        elif n_bins > min_bins:
            n_bins -= 1
        else:
            break

    # маска для ненулевых значений гистограммы
    mask = hist > 0

    # Вычисляем плотность
    bin_widths = np.diff(bins)
    rho = np.log10(hist[mask]) - np.log10(bin_widths[mask] * np.sum(s)) + 4*np.log10(pix2um)

    # Средние точки бинов
    s_rho = (bins[:-1] + bins[1:]) / 2
    s_rho = np.log(s_rho[mask]) + 2*np.log10(pix2um)

    # Преобразуем в список для JSON-сериализации
    data = {
        "s": s_rho.tolist(),
        "rho": rho.tolist(),
        "unit": "log mu2"
    }
    return data


if __name__ == "__main__":
    main()