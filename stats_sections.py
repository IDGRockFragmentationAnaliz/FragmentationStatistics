from pathlib import Path

import numpy as np

from rocknetmanager.tools.shape_load import shape_load
from rocknetmanager.tools.image_data import ImageData
import cv2
import matplotlib.pyplot as plt
from pyrocksegmentation.basic_segmentator import Segmentator
import scipy as sp

from pyrockstats.distrebutions import lognorm
from pyrockstats.empirical import ecdf
import json


def main():
	data_folder = Path("D:/1.ToSaver/profileimages/photo_database_complited")
	data = {}
	with open("./Section/config.json") as file:
		config = json.load(file)

		#config[]

	for image_folder in data_folder.iterdir():
		name = image_folder.name
		print(name)
		image_data, _ = ImageData.load(image_folder)

		label, _, _ = cv2.split(255 - image_data.label)
		_, area_marks = cv2.connectedComponents(label)
		area, _, _ = cv2.split(255 - image_data.area)

		img = np.zeros(area_marks.shape, np.uint8)
		img = cv2.merge((img, img, img))
		area_marks = cv2.watershed(img, area_marks)
		area_marks[area == 255] = -1
		#
		# unique, s = np.unique(area_marks, return_counts=True)
		#
		# s = s[1:]
		# areas = s
		#
		# x_min = np.log10(np.min(areas))
		# x_max = np.log10(np.max(areas))
		# s = np.sum(areas)
		# bins = np.logspace(x_min, x_max, 10)
		# hist, bins = np.histogram(areas, bins)
		# pix2m = config[name]["m"] / config[name]["pix"]
		# pix2m2 = pix2m ** 2
		# bins = bins * pix2m2
		# hist = hist / (s * pix2m2)
		#
		# data[name] = {
		# 	"bins": bins,
		# 	"hist": hist
		# }

		# x, cdf = ecdf(s)
		# theta = lognorm.fit(s)
		# data[name] = (theta[0], theta[1] * pix2m2)

	# 	fig = plt.figure(figsize=(16, 4))
	# 	ax = [fig.add_subplot(1, 1, 1)]
	# 	ax[0].plot(x, cdf)
	# 	ax[0].plot(x, lognorm(*theta).cdf(x))
	# 	ax[0].set_xscale('log')
	# 	ax[0].set_ylim((0, 1))
	# 	plt.show()
	#
	# sp.io.savemat("./Section_hists.mat", data)

		fig = plt.figure(figsize=(16, 4))
		ax = [fig.add_subplot(1, 1, 1)]
		ax[0].imshow(image_data.image)
		plt.show()
		exit()


if __name__ == "__main__":
	main()

