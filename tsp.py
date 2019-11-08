import random
import numpy
import time


distance_table = []
total_genes = None


# class Gene:  # City
#     def __init__(self, id_no):
#         self.id = id_no
#
#     def get_distance_to(self, city):
#         global distance_table
#         return distance_table[self.id][city.id]
#
#     def __str__(self):
#         return str(self.id)
#
#     def __repr__(self):
#         return str(self.id)


class Chromosome:  # Individual Route
    global distance_table

    def __init__(self, cities):
        assert (len(cities) > 3)
        """
        cities :    must be simple array containing numbers from 0 to N-1
                    where N is no. of cities
        """
        self.genes = cities
        self.__reset_params()

    def __len__(self):
        return len(self.genes)

    def __getitem__(self, index):
        return self.genes[index]

    def __setitem__(self, key, value):
        self.genes[key] = value

    def swap(self, gene_1, gene_2):
        a, b = self.genes.index(gene_1), self.genes.index(gene_2)
        self.genes[b], self.genes[a] = self.genes[a], self.genes[b]
        self.__reset_params()

    def add(self, gene):
        self.genes.append(gene)
        self.__reset_params()

    @property
    def fitness(self):
        if self.__fitness == 0:
            self.__fitness = 1 / self.travel_cost  # Normalize travel cost
        return self.__fitness

    @property
    def travel_cost(self):  # Get total travelling cost
        if self.__travel_cost == 0:
            for i in range(len(self.genes)):
                origin = self.genes[i]
                if i == len(self.genes) - 1:
                    dest = self.genes[0]
                else:
                    dest = self.genes[i + 1]
                self.__travel_cost += distance_table[origin][dest]
        return self.__travel_cost

    def __reset_params(self):
        self.__travel_cost = 0
        self.__fitness = 0

    def display(self):
        print("{}     {}".format(str(self.travel_cost), str(self.genes)))


class Population:
    def __init__(self, chromosomes):
        self.chromosomes = chromosomes
        self.__avg_fitness = 0
        self.__avg_distance = 0

    def __len__(self):
        return len(self.chromosomes)

    def __getitem__(self, item):
        return self.chromosomes[item]

    def __setitem__(self, key, value):
        self.chromosomes[key] = value

    def swap(self, i, j):
        self.chromosomes[i], self.chromosomes[j] = self.chromosomes[j], self.chromosomes[i]

    def rmv(self, chromosome):
        self.chromosomes.remove(chromosome)

    def add(self, chromosome):
        self.chromosomes.append(chromosome)

    def get_fittest(self):
        fittest = self.chromosomes[0]
        for route in self.chromosomes:
            if route.travel_cost < fittest.travel_cost:
                fittest = route
        return fittest

    @staticmethod
    def generate_population(sz, genes):
        individuals = []
        for _ in range(sz):
            individuals.append(Chromosome(random.sample(genes, len(genes))))
        return Population(individuals)

    @property
    def avg_fitness(self):
        if self.__avg_fitness == 0:
            for i in range(len(self.chromosomes)):
                self.__avg_fitness = self.__avg_fitness + self.chromosomes[i].fitness
                self.__avg_distance = self.__avg_distance + self.chromosomes[i].travel_cost
            self.__avg_fitness = self.__avg_fitness / len(self.chromosomes)
            self.__avg_distance = self.__avg_distance // len(self.chromosomes)
        return self.__avg_fitness

    @property
    def avg_distance(self):
        if self.__avg_distance == 0:
            for i in range(len(self.chromosomes)):
                self.__avg_fitness = self.__avg_fitness + self.chromosomes[i].fitness
                self.__avg_distance = self.__avg_distance + self.chromosomes[i].travel_cost
            self.__avg_fitness = self.__avg_fitness / len(self.chromosomes)
            self.__avg_distance = self.__avg_distance // len(self.chromosomes)
        return self.__avg_distance

    def reset(self):
        self.__avg_fitness = 0
        self.__avg_distance = 0


class TSP:
    def __init__(self, filename="dantzig42_d.txt"):
        global total_genes
        global distance_table
        distance_table = []
        total_genes = []
        TSP.init_distance_table(filename=filename)
        # creating population with size min(n+5,100) just in case when n=1 it can handle
        self.pop = Population.generate_population(min(150, len(total_genes) + 5), total_genes)
        self.pop.chromosomes = sorted(self.pop.chromosomes, key=lambda x: x.travel_cost)
        self.optimization_matrix = []
        # self.display()

    @staticmethod
    def init_distance_table(filename="dantzig42_d.txt"):
        global distance_table
        global total_genes
        distance_table = numpy.loadtxt(filename)
        n = numpy.shape(distance_table)[1]
        total_genes = []
        for i in range(n):
            total_genes.append(i)

    @staticmethod
    def mutate(chromosome, mut_rate=7):
        if random.randint(0, 99) < mut_rate:
            sel_genes = random.sample(chromosome.genes, 2)
            chromosome.swap(sel_genes[0], sel_genes[1])

    @staticmethod
    def filter_pop(population):
        avg_distance = population.avg_distance
        chromosomes = []
        for i in range(len(population)):
            if population[i].fitness <= avg_distance:
                chromosomes.append(population[i])
        return Population(chromosomes)

    def display(self):
        print("Distance               Route")
        print("Avg Distance values :  {} ".format(str(self.pop.avg_distance)))
        for i in range(len(self.pop)):
            self.pop[i].display()

    def all_gen(self):
        start_time = time.time()
        for i in range(1000):
            # print("Generation : {}".format(str(i)))
            self.pop = self.next_generation(mut_rate=7)
            # self.display()
            # input("")
        self.pop.chromosomes = sorted(self.pop.chromosomes, key=lambda x: x.travel_cost)
        print("Top route")
        self.pop[0].display()
        print("Time taken : {}".format(str(time.time() - start_time)))
        self.plot_graph()

    def plot_graph(self):
        import matplotlib.pyplot as plt
        arr = [self.optimization_matrix[i][1] for i in range(len(self.optimization_matrix))]
        plt.plot(range(len(arr)), arr)
        plt.show()

    def next_generation(self, mut_rate=7):
        from crossover import crossover
        new_gen = Population([])
        self.pop.chromosomes = sorted(self.pop.chromosomes, key=lambda x: x.travel_cost)
        self.optimization_matrix.append((self.pop.avg_distance, self.pop[0].travel_cost))
        n_len = len(self.pop)
        # 25% top population is direct passing
        # to next generation (SELECTION)
        elitism_num = n_len // 4
        for i in range(elitism_num):
            new_gen.add(self.pop[i])

        # Crossover
        for _ in range(n_len - elitism_num):
            parent_1 = self.pop.chromosomes[random.randint(0, n_len - 1)]
            parent_2 = self.pop.chromosomes[random.randint(0, n_len - 1)]
            child = crossover(parent_1, parent_2)
            new_gen.add(child)

        # mutation
        # here top chromosome may get worse
        for i in range(elitism_num, len(new_gen)):
            TSP.mutate(new_gen[i], mut_rate)
        # New Generation
        return new_gen


# Driver Code
# t = TSP()
# t.all_gen()

def clear():
    import os
    os.system("clear")
