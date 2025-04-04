import os
from pathlib import Path

import math
import numpy as np
import scipy as sp
import cv2

import matplotlib.pyplot as plt
import json

from pyrockstats.distrebutions import lognorm
from pyrockstats.empirical import ecdf


def main():
	area_data = sp.io.loadmat("./Zirkons/Zirkon_areas.mat", squeeze_me=True)
	keys = [key for key in area_data.keys() if not key.startswith('__')]

	data = {}

	for name in keys:
		print(name)
		areas = area_data[name]
		#theta = lognorm.fit(areas)
		#

		x_min = np.log10(np.min(areas))
		x_max = np.log10(np.max(areas))
		s = np.sum(areas)

		bins = np.logspace(x_min, x_max, 10)

		hist, bins = np.histogram(areas, bins)
		bins = bins
		hist = hist / s

		data[name] = {
			"bins": list(bins),
			"density": list(hist),
			"units": "um2"
		}

		# fig = plt.figure(figsize=(14, 9))
		# axs = [fig.add_subplot(1, 1, 1)]
		# axs[0].stairs(data[name]["hist"], data[name]["bins"], fill=True)
		# axs[0].set_xscale('log')
		# #axs[0].set_yscale('log')
		# plt.show()
		#exit()
	with open("data/zirkon_hists.json", 'w') as json_file:
		json.dump(data, json_file, indent=4)

	#sp.io.savemat("zirkons_hists.mat", data)




if __name__ == "__main__":
	main()
