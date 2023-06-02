from matplotlib import pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import ntpath



def get_coordinates(file_path):
    file = open(file_path, 'r')
    lines = file.readlines()
    lines = lines[6:len(lines) - 1]  # last eof
    xs, ys = [], []
    for line in lines:
        xs.append(float(line.split(" ")[1]))
        ys.append(float(line.split(" ")[2]))
    return xs, ys


def points_to_coordinates(tour, xs, ys):
    result_x = []
    result_y = []
    for t in tour:
        result_x.append(xs[t - 1])
        result_y.append(ys[t - 1])
    return result_x, result_y


def plot_and_save(instance_path, m,n, tours, alg):
    _ , instance_name = ntpath.split(instance_path)
    xs, ys = get_coordinates(instance_path)
    color = iter(cm.rainbow(np.linspace(0, 1, m)))
    for i in range(0, m):
        tour = tours[i]
        x, y = points_to_coordinates(tour, xs, ys)
        c = next(color)
        plt.plot(x, y, linestyle='-', marker='o', c=c)
    plt.title(alg + " on " + instance_name + " with " + str(m) + " salesman.")
    plt.savefig("plots\\" + alg + str(m) + "_" + str(n) + ".png")


