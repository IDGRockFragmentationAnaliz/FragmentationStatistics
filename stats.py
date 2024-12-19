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
	name = keys[0]
	areas = area_data[name]

	x, cdf_e = ecdf(areas)
	theta = lognorm.fit(areas)


	fig = plt.figure(figsize=(14, 9))
	axs = [fig.add_subplot(1, 1, 1)]
	axs[0].plot(x, cdf_e)
	plt.show()

if __name__ == "__main__":
	main()