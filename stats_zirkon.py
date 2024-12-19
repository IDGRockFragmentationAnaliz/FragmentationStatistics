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
		theta = lognorm.fit(areas)
		data[name] = theta

	sp.io.savemat("Zirkons_lognorm_theta.mat", data)

	# fig = plt.figure(figsize=(14, 9))
	# axs = [fig.add_subplot(1, 1, 1)]
	# axs[0].plot(x / (10**12), cdf_e)
	# axs[0].plot(x / (10**12), lognorm(*theta).cdf(x))
	# axs[0].set_xscale('log')
	# axs[0].set_ylim((0, 1))
	# plt.show()


if __name__ == "__main__":
	main()
