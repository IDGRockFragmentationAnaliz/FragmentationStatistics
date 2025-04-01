import os
from pathlib import Path

import math
import numpy as np
import scipy as sp
import cv2
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import json

from pyrockstats.distrebutions import lognorm


def main():
    paths = {
        "Zirkon": Path("./data/zirkon_hists.json"),
        "ThinSection": Path("./data/thin_section_hists.json"),
        "Section": Path("./data/section_hists.json"),
        "Lineaments": Path("./data/lineaments_hists.json")
    }

    data = {
        "Zirkon": load_data(paths["Zirkon"]),
        "ThinSection": load_data(paths["ThinSection"]),
        "Section": load_data(paths["Section"]),
        "Lineaments": load_data(paths["Lineaments"])
    }
    
    Names = {
        "Zirkon": "Цирконы",
        "ThinSection": "Шлифы",
        "Section": "Обнажения",
        "Lineaments": "ЦМР"
    }

    hists = {}
    for type_name in data:
        hists[type_name] = {}
        data_type = data[type_name]
        for i, name in enumerate(data_type):
            hists[type_name][i] = data_type[name]

    keys = [key for key in data.keys()]

    fig = plt.figure(figsize=(7, 7))
    axs = [fig.add_subplot(1, 1, 1)]
    colors = ["red", "blue", "purple", "green"]
    font_path = Path(".") / "assets" / "timesnewromanpsmt.ttf"
    custom_font = mpl.font_manager.FontProperties(fname=font_path, size=16)
    fig.subplots_adjust(bottom=0.3)
    for i in range(4):
        l1 = len(hists[keys[i]])
        for j in range(l1):
            x, y = get_plot_data(hists[keys[i]][j])
            line, = axs[0].plot(x, y, color=colors[i],
                                linewidth=3,
                                solid_capstyle='round',
                                solid_joinstyle='round')
            if j == 0:
                line.set_label(Names[keys[i]])
    axs[0].plot([5, -6], [-20, 25], color="black", linestyle="--", linewidth=3, dash_capstyle='round')

    #axs[0].plot([min, max], [min ** (-2), max ** (-2)], color="black")
    #axs[0].set_xscale('log')
    #
    axs[0].legend(prop=custom_font)
    axs[0].grid(True)
    #axs[0].set_xlim([min, max])
    axs[0].set_xlabel("Площадь частиц $s$, $м^2$", fontproperties=custom_font)
    axs[0].set_ylabel(r"Плотность частиц $\rho$, $м^{-4}$", fontproperties=custom_font)
    ax2 = axs[0].twiny()
    ax2.set_xlim(axs[0].get_xlim())
    ax2.spines['bottom'].set_position(('outward', 60))
    ax2.spines['bottom'].set_visible(True)
    ax2.xaxis.set_ticks_position('bottom')
    ax2.xaxis.set_label_position('bottom')
    ax2.set_xlabel("Характерный размер $d$, $м$", fontproperties=custom_font)
    
    def exp_formatter(x, pos):
        return f'$10^{{{x*2:.0f}}}$'
    
    def exp_formatter2(x, pos):
        return f'$10^{{{x:.0f}}}$'
    
    axs[0].xaxis.set_major_formatter(plt.FuncFormatter(exp_formatter))
    axs[0].yaxis.set_major_formatter(plt.FuncFormatter(exp_formatter2))
    
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(exp_formatter2))
    
    for label in axs[0].get_xticklabels() + axs[0].get_yticklabels():
        label.set_fontproperties(custom_font)
    
    for label in ax2.get_xticklabels():
        label.set_fontproperties(custom_font)
    
    fig.savefig("./data/" + "all_stat" + ".png", dpi=300, bbox_inches='tight')
    plt.show()


def get_plot_data(hist):
    density = hist["density"]
    bins = hist["bins"]
    units = hist["units"]
    x = np.log10(bins)/2
    x = (x[0:-1] + x[1:])/2
    # try:
    y = np.log10(density) - np.log10(np.diff(bins))
    # except Warning as w:
    # 	print("error")
    # 	density_safe = np.where(density <= 0, 1, density)
    # 	y = np.log10(density_safe) - np.log10(np.diff(bins))

    if units == "um" or units == "um2":
        x = x - 6
        y = y + 6*4
    
    if units == "m" or units == "m2":
        x = x + 2
        y = y - 2*4
        
    if units == "km" or units == "km2":
        y = y

    return x, y


def load_data(path: Path):
    with open(path) as file:
        data = json.load(file)
    for key in data:
        data[key]["name"] = key
        data[key]["bins"] = np.array(data[key]["bins"])
        data[key]["density"] = np.array(data[key]["density"])
    return data


if __name__ == "__main__":
    main()
