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
		"Zirkon": Path("./Zirkons_hists.mat"),
		"ThinSection": Path("ThinSection_hists.mat"),
		"Section": Path("./Section_hists.mat"),
		"Lineaments": Path("./Lineaments_hists.mat")
	}

	data = {
		"Zirkon": load_data(paths["Zirkon"]),
		"ThinSection": load_data(paths["ThinSection"]),
		"Section": load_data(paths["Section"]),
		"Lineaments": load_data(paths["Lineaments"])
	}

	keys = [key for key in data["Lineaments"].keys()]
	key = keys[0]
	hist_3 = data["Lineaments"][key]["hist"].copy()[0][0][0]
	bins_3 = data["Lineaments"][key]["bins"].copy()[0][0][0]

	keys = [key for key in data["Section"].keys()]
	key = keys[0]
	hist_2 = data["Section"][key]["hist"].copy()[0][0][0]
	bins_2 = data["Section"][key]["bins"].copy()[0][0][0]

	keys = [key for key in data["ThinSection"].keys()]
	key = keys[0]
	hist_1 = data["ThinSection"][key]["hist"].copy()[0][0][0]
	bins_1 = data["ThinSection"][key]["bins"].copy()[0][0][0]
	#
	hist = data["Zirkon"]["Z-20"]["hist"].copy()[0][0][0]
	bins = data["Zirkon"]["Z-20"]["bins"].copy()[0][0][0]

	print(hist)
	print(bins)
	#exit()

	# x = np.logspace(-15.0, 4.0, num=1000)
	# pdf = lognorm(*theta).pdf(x)
	# pdf_2 = lognorm(*theta_2).pdf(x)
	# pdf_3 = lognorm(*theta_3).pdf(x)
	#dict = sp.io.loadmat(str(file_path), squeeze_me=True)
	bins_all = np.concatenate((bins, bins_1, bins_2, bins_3))
	min = np.min(bins_all)
	max = np.max(bins_all)

	fig = plt.figure(figsize=(7, 5))
	axs = [fig.add_subplot(1, 1, 1)]
	axs[0].stairs(hist/np.diff(bins), bins, fill=True, label="Zirkon")
	axs[0].stairs(hist_1/np.diff(bins_1), bins_1, fill=True, label="ThinSection")
	axs[0].stairs(hist_2/np.diff(bins_2), bins_2, fill=True, label="Section")
	axs[0].stairs(hist_3/np.diff(bins_3), bins_3, fill=True, label="Lineaments")
	axs[0].plot([min, max], [min ** (-2), max ** (-2)], color="black")
	axs[0].set_xscale('log')
	axs[0].set_yscale('log')
	axs[0].legend()
	axs[0].grid(True)
	axs[0].set_xlim([min, max])
	axs[0].set_xlabel("$1/m^2$")
	axs[0].set_ylabel("$1/m^4$")
	plt.show()


def load_data(path: Path):
	data = sp.io.loadmat(str(path))
	keys_to_remove = ['__header__', '__version__', '__globals__']
	for key in keys_to_remove:
		if key in data:
			del data[key]
	return data


if __name__ == "__main__":
	main()
