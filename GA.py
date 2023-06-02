import numpy as np
import copy

from stat_utils import plot_and_save


class Chromosome(object):

    def __init__(self, n_cities, n_salesman, adjacency_matrix):
        self.n_cities = n_cities
        self.n_salesman = n_salesman
        self.adjacency_matrix = adjacency_matrix
        self.cost = 0
        self.minmax = 0
        self.fitness = 0
        self.genome = None
        self.generate_genome()

    def generate_genome(self):
        random_genome = np.array(range(1, self.n_cities))
        np.random.shuffle(random_genome)
        self.genome = np.array_split(random_genome, self.n_salesman)
        for i in range(len(self.genome)):
            self.genome[i] = np.insert(self.genome[i], 0, 0)
            self.genome[i] = np.append(self.genome[i], 0)
        self.compute_fitness()

    def compute_fitness(self):
        self.cost = 0
        longest_salesman_length = 0
        for i in range(self.n_salesman):
            salesman = self.genome[i]
            salesman_fitness = 0
            for j in range(len(salesman) - 1):
                salesman_fitness = salesman_fitness + self.adjacency_matrix[salesman[j]][salesman[j + 1]]
            self.cost = self.cost + salesman_fitness
            if len(salesman) > longest_salesman_length or (
                    len(salesman) == longest_salesman_length and salesman_fitness > self.minmax):
                longest_salesman_length = len(salesman)
                self.minmax = salesman_fitness
        self.fitness = self.cost + self.minmax

    def local_mutation(self):
        idx = np.random.randint(0, self.n_salesman)
        to_mutate = self.genome[idx]
        i, j = np.random.randint(1, len(to_mutate) - 1), np.random.randint(1, len(to_mutate) - 1)
        to_mutate[i], to_mutate[j] = to_mutate[j], to_mutate[i]
        self.compute_fitness()

    def global_mutation(self):
        index1, index2 = np.random.randint(0, self.n_salesman), np.random.randint(0, self.n_salesman)
        while index1 == index2:
            index1, index2 = np.random.randint(0, self.n_salesman), np.random.randint(0, self.n_salesman)
        while len(self.genome[index1]) < 4:
            index1, index2 = np.random.randint(0, self.n_salesman), np.random.randint(0, self.n_salesman)
        mutant1, mutant2 = self.genome[index1], self.genome[index2]
        i, j = np.random.randint(1, len(mutant1) - 1), np.random.randint(1, len(mutant2) - 1)
        self.genome[index2] = np.insert(mutant2, j, mutant1[i])
        self.genome[index1] = np.delete(mutant1, i)
        self.compute_fitness()

    def crossover(self, other_chromosome):
        for i in range(self.n_salesman):
            salesman1, salesman2 = self.genome[i], other_chromosome.genome[i]
            for i in range(1, min(len(salesman1), len(salesman2)) - 1):
                if salesman2[i] in salesman1:
                    salesman1[i], salesman1[salesman1.tolist().index(salesman2[i])] = salesman1[
                                                                                          salesman1.tolist().index(
                                                                                              salesman2[i])], salesman1[
                                                                                          i]
        self.compute_fitness()


class GA(object):
    SELECTION_PERCENT = 0.6

    def __init__(self, max_iterations, population_size, adjacency_matrix, n_cities, n_salesman, mutation_probability,
                 crossover_probability):
        self.n_salesmanAX_ITERATIONS = max_iterations
        self.POPULATION_SIZE = population_size
        self.adjacency_matrix = adjacency_matrix
        self.n_cities = n_cities
        self.n_salesman = n_salesman
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.population = []
        self.create_population()

    def create_population(self):
        for i in range(self.POPULATION_SIZE):
            self.population.append(Chromosome(self.n_cities, self.n_salesman, self.adjacency_matrix))

    def tournament_selection(self):
        current_pop_size = self.POPULATION_SIZE
        j = (int)(self.POPULATION_SIZE * self.SELECTION_PERCENT)
        for _ in range(self.POPULATION_SIZE - current_pop_size):
            del self.population[-np.random.randint(0, len(self.population))]
        for _ in range(current_pop_size - j):
            worst_index = 0
            for i in range(1, len(self.population)):
                if self.population[i].fitness == self.population[i].fitness:
                    worst_index = i
            del self.population[-worst_index]

        for _ in range(self.POPULATION_SIZE - len(self.population)):
            self.population.append(Chromosome(self.n_cities, self.n_salesman, self.adjacency_matrix))

    def global_mutation(self):
        for index in range(len(self.population)):
            if np.random.random(1)[0] < self.mutation_probability:
                chromosome = copy.deepcopy(self.population[index])
                chromosome.global_mutation()
                if chromosome.fitness < self.population[index].fitness:
                    self.population[index] = chromosome

    def local_mutation(self):
        for index in range(len(self.population)):
            if np.random.random(1)[0] < self.mutation_probability:
                chromosome = copy.deepcopy(self.population[index])
                chromosome.local_mutation()
                if chromosome.fitness < self.population[index].fitness:
                    self.population[index] = chromosome

    def crossover(self):
        for index1 in range(len(self.population)):
            if np.random.random(1)[0] < self.crossover_probability:
                index2 = np.random.randint(0, len(self.population))
                if index1 == index2:
                    index2 = np.random.randint(0, len(self.population))
                child1 = copy.deepcopy(self.population[index1])
                child2 = copy.deepcopy(self.population[index2])
                child1.crossover(self.population[index2])
                child2.crossover(self.population[index1])
                if child1.fitness < self.population[index1].fitness:
                    self.population[index1] = child1
                if child2.fitness < self.population[index2].fitness:
                    self.population[index2] = child2

    def evaluation(self):
        best_chromosome = self.population[0]
        for i in range(1, self.POPULATION_SIZE):
            if self.population[i].fitness < best_chromosome.fitness:
                best_chromosome = self.population[i]
        print("Overall cost: ", best_chromosome.cost)

    def run(self):
        for iteration in (range(self.n_salesmanAX_ITERATIONS)):
            # selection
            self.tournament_selection()
            # mutation
            self.global_mutation()
            self.local_mutation()
            # crossover
            self.crossover()

    def get_results(self):
        best_chromosome = self.population[0]
        for i in range(1, self.POPULATION_SIZE):
            if self.population[i].fitness < best_chromosome.fitness:
                best_chromosome = self.population[i]

        # Print best solution
        solution = []
        for i in range(best_chromosome.n_salesman):
            sol = []
            print(i + 1, ":  ", best_chromosome.genome[i][0] + 1, end="", sep="")
            for j in range(1, len(best_chromosome.genome[i])):
                sol.append(best_chromosome.genome[i][j])
                print("-", best_chromosome.genome[i][j] + 1, end="", sep="")
            print(" --- #", len(best_chromosome.genome[i]))
            solution.append(sol)
        print()

        # Print cost
        print("Cost: ", best_chromosome.cost)
        return solution, best_chromosome.cost