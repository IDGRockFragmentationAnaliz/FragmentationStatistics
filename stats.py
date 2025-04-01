import os
from pathlib import Path

import math
import numpy as np
import scipy as sp
import cv2

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

	fig = plt.figure(figsize=(7, 5))
	axs = [fig.add_subplot(1, 1, 1)]
	colors = ["red", "blue", "purple", "green"]
	for i in range(4):
		l1 = len(hists[keys[i]])
		for j in range(l1):
			x, y = get_plot_data(hists[keys[i]][j])
			line, = axs[0].plot(x, y, color=colors[i])
			if j == 0:
				line.set_label(Names[keys[i]])
	axs[0].plot([5, -6],[-20, 25], color="black", linestyle="--")

	#axs[0].plot([min, max], [min ** (-2), max ** (-2)], color="black")
	#axs[0].set_xscale('log')
	#
	axs[0].legend()
	axs[0].grid(True)
	#axs[0].set_xlim([min, max])
	axs[0].set_xlabel("Характерный размер $d$, $m$")
	axs[0].set_ylabel(r"Плотность частиц $\rho$, $m^{-4}$")

	def exp_formatter(x, pos):
		return f'$10^{{{x:.0f}}}$'

	axs[0].xaxis.set_major_formatter(plt.FuncFormatter(exp_formatter))
	axs[0].yaxis.set_major_formatter(plt.FuncFormatter(exp_formatter))

	plt.show()


def get_plot_data(hist):
	density = hist["density"]
	bins = hist["bins"]
	units = hist["units"]
	x = np.log10(bins)/2
	x = (x[0:-1] + x[1:])/2
	y = np.log10(density) - np.log10(np.diff(bins))

	if units == "um" or units == "um2":
		x = x - 6
		y = y + 6*4

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
