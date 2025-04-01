from pathlib import Path

import numpy as np

from rocknetmanager.tools.shape_load import shape_load
from rocknetmanager.tools.image_data import ImageData
import cv2
import matplotlib.pyplot as plt
from pyrocksegmentation.basic_segmentator import Segmentator
import scipy as sp

from pyrockstats.distrebutions import lognorm, weibull, paretoexp
from pyrockstats.bootstrap.ks_statistics import get_ks_distribution
from pyrockstats.bootstrap.ks_statistics import get_confidence_value
from pyrockstats.empirical import ecdf
import json


def main():
    data_folder = Path("D:/1.ToSaver/profileimages/photo_database_complited")
    data = {}
    with open("./Section/config.json") as file:
        config = json.load(file)

        #config[]
    out_data = {}
    for image_folder in data_folder.iterdir():
        name = image_folder.name
        print(name)
        image_data, _ = ImageData.load(image_folder)
        
        pix2m = config[name]["m"] / config[name]["pix"]
        pix2m2 = pix2m ** 2

        label, _, _ = cv2.split(255 - image_data.label)
        _, area_marks = cv2.connectedComponents(label)
        area, _, _ = cv2.split(255 - image_data.area)

        img = np.zeros(area_marks.shape, np.uint8)
        img = cv2.merge((img, img, img))
        area_marks = cv2.watershed(img, area_marks)
        area_marks[area == 255] = -1

        unique, s = np.unique(area_marks, return_counts=True)
        
        s = s[1:]
        areas = s*pix2m2
    
        xmin = np.min(areas)
        xmax = np.max(areas)
        
        models = {"lognorm": lognorm, "paretoexp": paretoexp, "weibull": weibull}
        tests = {name: DistributionTest(areas, model) for name, model in models.items()}
        
        ks_tests = {name: test.ks_test(0.05) for name, test in tests.items()}
        thetas = {name: (float(test.theta[0]), float(test.theta[1])) for name, test in tests.items()}
        values, e_freq = ecdf(areas)
        x = np.logspace(np.log10(xmin), np.log10(xmax), 100)
        
        alpha = 0.05
        data = {
            "x": x.tolist(),
            "xmin": xmin,
            "xmax": xmax,
            "alpha": alpha,
            "test_data": {name: test.get_data(x, alpha) for name, test in tests.items()},
            "ecdf": {"values": values.tolist(), "freqs": e_freq.tolist()},
            "theta": {name: tests[name].theta for name, test in tests.items()}
        }
        
        # fig = plt.figure(figsize=(12, 4))
        # axs = [fig.add_subplot(1, 1, 1)]
        # axs[0].plot(x, tests["lognorm"].model_cdf(x))
        # axs[0].plot(data["ecdf"]["values"], data["ecdf"]["freqs"], color="black", linestyle="--", label="2")
        # axs[0].set_xscale('log')
        # plt.show()
        # exit()
        out_data[name] = data
        # print(ks_tests)
        print(thetas)
        # exit()
        # s = np.sum(areas)
        # bins = np.logspace(x_min, x_max, 10)
        # hist, bins = np.histogram(areas, bins)
    exit()
    with open("./data/outcrops_tests.json", 'w+') as json_file:
        json.dump(out_data, json_file, indent=4)
    
    #     bins = bins * pix2m2
    #     hist = hist / (s * pix2m2)
    #
    #     data[name] = {
    #         "bins": list(bins),
    #         "density": list(hist),
    #         "units": "m2"
    #     }
    #
    # with open("data/section_hists.json", 'w') as json_file:
    #     json.dump(data, json_file, indent=4)

    exit()
    #sp.io.savemat("./Section_hists.mat", data)

        # fig = plt.figure(figsize=(16, 4))
        # ax = [fig.add_subplot(1, 1, 1)]
        # ax[0].imshow(image_data.image)
        # plt.show()
        # exit()


class DistributionTest:
    def __init__(self, areas, model):
        self.xmin = np.min(areas)
        self.xmax = np.max(areas)
        self.areas = areas
        self.model = model
        self.ks = get_ks_distribution(areas, model, n_ks=500)
        self.theta = self.model.fit(areas, xmin=self.xmin, xmax=self.xmax)
        self.dist = self.model(*self.theta, xmin=self.xmin, xmax=self.xmax)
        self.confidence_value = None
        self.alpha = None
        self.hypothesis = None

    def get_confidence_value(self, alpha):
        if self.alpha is not None and alpha == self.alpha:
            return self.confidence_value
        self.alpha = alpha
        self.confidence_value = get_confidence_value(self.ks, significance=alpha)
        return self.confidence_value

    def model_cdf(self, x):
        return self.dist.cdf(x, xmin=self.xmin, xmax=self.xmax)

    def ks_test(self, alpha, e_values = None, e_cdf = None):
        if e_values is None or e_cdf is None:
            e_values, e_cdf = ecdf(self.areas)
        confidence_value = self.get_confidence_value(alpha)
        cdf_min = self.model_cdf(e_values) - confidence_value
        cdf_max = self.model_cdf(e_values) + confidence_value
        self.hypothesis = np.all(cdf_min < e_cdf) and np.all(cdf_max > e_cdf)
        return self.hypothesis

    def get_data(self, x, alpha):
        confidence_value = self.get_confidence_value(alpha)
        cdf = self.model_cdf(x)
        cdf_min = cdf - confidence_value
        cdf_max = cdf + confidence_value
        data = {
            "cdf": cdf.tolist(),
            "cdf_min": cdf_min.tolist(),
            "cdf_max": cdf_max.tolist(),
            "ks_test": str(self.ks_test(alpha))
        }
        return data


if __name__ == "__main__":
    main()

