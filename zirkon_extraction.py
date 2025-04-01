import os
from pathlib import Path

import math
import numpy as np
import scipy as sp
import cv2

import matplotlib.pyplot as plt
import json


def main():
    zirkon_folder = Path("D:\PycharmProjects\FragmentationStatistics\Zirkons\ZirkonEdges")
    data = {}

    for path_img in zirkon_folder.iterdir():
        config = get_image_config(path_img.name)
        print(config["name"])
        areas, edges = get_image(path_img)
        area_marks = get_marks(edges, areas)
        s = extract_areas(area_marks)
        s = s * config["pix2um2"]
        data[config["name"]] = s
        
        # fig = plt.figure(figsize=(14, 9))
        # axs = [fig.add_subplot(1, 1, 1)]
        # axs[0].imshow(area_marks)
        # plt.show()

    print(data)

    sp.io.savemat("./Zirkons/Zirkon_areas.mat", data)


def get_image_config(img_name):
    with open("./Zirkons/config.json") as file:
        config = json.load(file)
        name_split = img_name.split("_")
        name = name_split[0]
        name = name[0:-1]
        config = config[name]
        config["scale"] = 1
        config["name"] = name
        if "up8" in name_split:
            config["scale"] = 8

        config["pix2um"] = config["um"] / (config["pix"] * config["scale"])
        config["pix2um2"] = config["pix2um"] ** 2
        config["pix2m2"] = config["pix2um2"] / (10 ** 12)

        return config


def get_marks(edges, areas):
    image = np.zeros(edges.shape, np.uint8)
    image = cv2.merge((image, image, image))
    _, area_marks = cv2.connectedComponents(areas)
    area_marks = cv2.watershed(image, area_marks)
    area_marks[edges == 255] = -1
    return area_marks


def extract_areas(area_marks):
    unique, s = np.unique(area_marks, return_counts=True)
    unique = np.array(unique)[1:]
    s = np.array(s)[1:]
    return s


def get_image_areas(path: Path):
    areas, edges = get_image(path)
    area_marks = get_marks(edges, areas)
    s = extract_areas(area_marks)
    return s


def get_image(path_img: Path):
    img_edges = cv2.imread(str(path_img))
    b, g, r = cv2.split(img_edges)
    shape = b.shape
    areas = 255*np.ones(shape, np.uint8)
    areas[r == 255] = 0
    edges = 255*np.zeros(shape, np.uint8)
    edges[(r == 255) & (b == 0)] = 255
    return areas, edges


if __name__ == "__main__":
    main()
