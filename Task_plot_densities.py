from pathlib import Path
import numpy as np
import json
import matplotlib.pyplot as plt


def main():
    with open("./data/zirkons_densities.json") as file:
        zirkons_data = json.load(file)
    
    with open("./data/thin_section_densities.json") as file:
        thin_section_data = json.load(file)
    
    fig = plt.figure(figsize=(12, 4))
    axs = [fig.add_subplot(1, 1, 1)]
    for name in zirkons_data:
        x = np.array(zirkons_data[name]["s"])
        y = np.array(zirkons_data[name]["rho"])
        #print(zirkons_data[name]["unit"])
        axs[0].plot(x, y, color="blue")
    for name in thin_section_data:
        x = thin_section_data[name]["s"]
        y = thin_section_data[name]["rho"]
        #print(thin_section_data[name]["unit"])
        axs[0].plot(x, y, color="red")
    
    plt.show()


if __name__ == "__main__":
    main()
