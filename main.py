import numpy as np
import math
import time

from config import *
from GA import *


def GA_read_parse_file(file_path):
    file = open(file_path, 'r')
    lines = file.readlines()

    meta_info = "".join(lines[:5])
    lines = lines[6:len(lines) - 1]  # last eof

    nodes = []
    for line in lines:
        nodes.append([float(line.split(" ")[1]), float(line.split(" ")[2])])
    adjacency_matrix = create_adjacency_matrix(nodes)
    return meta_info, adjacency_matrix



def print_logs(algorithm, data_meta_info):
    print("POPULATION SIZE: ", GA_POPULATION_SIZE)
    print("MAX ITERATIONS: ", GA_MAX_ITERATIONS)
    print("MUTATION PROBABILITY: ", GA_MUTATION_PROBABILITY)
    print("CROSSOVER PROBABILITY: ", GA_CROSSOVER_PROBABILITY)
    print("DATA INFO: ")
    print(data_meta_info)


def create_adjacency_matrix(nodes):
    adj = np.zeros((len(nodes), len(nodes)))
    for i in range(len(adj)):
        for j in range(len(adj)):
            if not i == j:
                adj[i][j] = math.dist([nodes[i][0], nodes[i][1]], [nodes[j][0], nodes[j][1]])
    return adj


if __name__ == "__main__":

    if ALGORITHM == "GA":
        meta_info, nodes = GA_read_parse_file(FILE_PATH)
        print_logs(ALGORITHM, meta_info)
        adjacency_matrix = create_adjacency_matrix(nodes)
        start = time.time()
        ga = GA(GA_MAX_ITERATIONS, GA_POPULATION_SIZE, adjacency_matrix, CITIES, SALESMAN, GA_MUTATION_PROBABILITY,
                GA_CROSSOVER_PROBABILITY)
        ga.run()
        solution, cost  = ga.get_results()
        end = time.time()
        #plot_and_save(FILE_PATH, SALESMAN, CITIES, solution, "GA")
        print(end-start)