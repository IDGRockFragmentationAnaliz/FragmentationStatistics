import os
from pathlib import Path

import math
import numpy as np
import scipy as sp
import cv2
import matplotlib.pyplot as plt

from rocknetmanager.tools.shape_load import shape_load
from pyrocksegmentation.basic_segmentator import Segmentator
from pyrocksegmentation import Extractor


def main():
	root_path = Path("D:/1.ToSaver/profileimages/ShapeBaikal")
	shape_path = (
		root_path / "9_200ГГК" / "all.shp")

	lines, bbox = shape_load(shape_path)
	shape = (bbox[2] - bbox[0] + 1, bbox[3] - bbox[1] + 1)
	new_shape = (4000, 4000)
	for i, line in enumerate(lines):
		lines[i] = (line * [1, -1] - bbox[0:2]) / shape * new_shape
		lines[i] = lines[i].astype(np.int32)

	p2m2 = get_p2m2(shape, new_shape)

	line_width = 13

	zero_image = np.zeros(new_shape, np.uint8)
	image = zero_image.copy()
	image = cv2.merge((image, image, image))
	image = cv2.polylines(image, lines, False, (255, 255, 255), line_width)
	image = image[2000:4000, 0:2000]
	areas, _, _ = cv2.split(255 - image)

	_, area_marks = cv2.connectedComponents(areas)
	img = np.zeros(areas.shape, np.uint8)
	img = cv2.merge((img, img, img))
	area_marks = cv2.watershed(img, area_marks)

	unique, s = np.unique(area_marks, return_counts=True)
	unique = np.array(unique)[1:]
	areas = np.array(s)[1:]
	#print(len(areas))
	#exit()
	x_min = np.log10(np.min(areas))
	x_max = np.log10(np.max(areas))
	s = np.sum(areas)
	bins = np.logspace(x_min, x_max, 10)
	hist, bins = np.histogram(areas, bins)
	bins = bins * p2m2
	hist = hist / (s * p2m2)

	data = {}
	data["9-200"] = {
		"bins": bins,
		"hist": hist
	}
	sp.io.savemat("Lineaments_hists.mat", data)


	# fig = plt.figure(figsize=(14, 9))
	# axs = [fig.add_subplot(1, 1, 1)]
	# axs[0].stairs(hist, bins)
	# plt.show()

	# fig = plt.figure(figsize=(14, 9))
	# axs = [fig.add_subplot(1, 1, 1)]
	# axs[0].stairs(hist, bins)
	# plt.show()


def get_p2m2(shape, new_shape):
	new_shape = np.array(new_shape, np.float64)
	shape = np.array(shape, np.float64)
	p2m2 = shape[0] * shape[1] / (new_shape[0] * new_shape[1])
	return p2m2


if __name__ == "__main__":
	main()
