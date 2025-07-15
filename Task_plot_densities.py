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


def main():
    font_path = Path(".") / "assets" / "timesnewromanpsmt.ttf"
    custom_font = mpl.font_manager.FontProperties(fname=font_path, size=16)
    
    with open("./data/zirkons_densities.json") as file:
        zirkons_data = json.load(file)
    
    with open("./data/thin_section_densities.json") as file:
        thin_section_data = json.load(file)
    
    with open("./data/outcrops_densities.json") as file:
        outcrops_data = json.load(file)
        
    with open("./data/lineaments_densities.json") as file:
        lineaments_densities = json.load(file)
    
    fig = plt.figure(figsize=(8, 8))
    colors = ["red", "blue", "purple", "green"]
    
    y_label_1 = r"$\rho$, $m^{-4}$"
    x_label_1 = "$s$, $m^2$"
    x_label_2 = "$d$, $m$"
    def get_line_config(i):
        _config = {
            "color": colors[i],
            "linewidth": 3,
            "solid_capstyle": 'round',
            "solid_joinstyle": 'round'
        }
        return _config
    
    axs = [fig.add_subplot(1, 1, 1)]
    fig.subplots_adjust(bottom=0.2, left=0.2)
    axs[0].grid(True)
    for name in zirkons_data:
        x = np.array(zirkons_data[name]["s"]) - 12
        y = np.array(zirkons_data[name]["rho"]) + 2*12
        axs[0].plot(x, y, **get_line_config(0))
    for name in thin_section_data:
        x = np.array(thin_section_data[name]["s"]) - 12
        y = np.array(thin_section_data[name]["rho"]) + 2*12
        axs[0].plot(x, y, **get_line_config(1))
    for name in outcrops_data:
        x = np.array(outcrops_data[name]["s"])
        y = np.array(outcrops_data[name]["rho"])
        axs[0].plot(x, y, **get_line_config(2))
    for name in lineaments_densities:
        x = np.array(lineaments_densities[name]["s"])
        y = np.array(lineaments_densities[name]["rho"])
        axs[0].plot(x, y, **get_line_config(3))
    for i in range(4):
        axs[0].plot(0, 0, **get_line_config(i), label=str(i+1))
    axs[0].plot([10.5, -12], [-20, 25], color="black", linestyle="--", linewidth=3, dash_capstyle='round')
    axs[0].set_xlabel(x_label_1, fontproperties=custom_font)
    axs[0].set_ylabel(y_label_1, fontproperties=custom_font)
    axs[0].legend(prop=custom_font)
    def exp_formatter(x, pos):
        return f'$10^{{{x:.0f}}}$'

    def exp_formatter2(x, pos):
        return f'$10^{{{x/2:.1f}}}$'
    
    ax2 = axs[0].twiny()
    ax2.set_xlim(axs[0].get_xlim())
    ax2.spines['bottom'].set_position(('outward', 60))
    ax2.spines['bottom'].set_visible(True)
    ax2.xaxis.set_ticks_position('bottom')
    ax2.xaxis.set_label_position('bottom')
    ax2.set_xlabel(x_label_2, fontproperties=custom_font)
    
    axs[0].xaxis.set_major_formatter(plt.FuncFormatter(exp_formatter))
    axs[0].yaxis.set_major_formatter(plt.FuncFormatter(exp_formatter))
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(exp_formatter2))
    for label in axs[0].get_xticklabels() + axs[0].get_yticklabels():
        label.set_fontproperties(custom_font)
    for label in ax2.get_xticklabels():
        label.set_fontproperties(custom_font)
    fig.savefig("./data/" + "all_stat_2" + ".png", dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
