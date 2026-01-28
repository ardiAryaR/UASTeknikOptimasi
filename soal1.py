from operator import index
import random, sys
from collections import deque

PRODUCTS = [
    {"nama": "Bear Brand Collagen 189ml", "harga": 9900},
    {"nama": "Vidoran Xmart 5+ Cokelat Box", "harga": 49400},
    {"nama": "Vidoran Xmart 1+ Madu Box", "harga": 10900},
    {"nama": "So Good Sosis Korea", "harga": 30000},
    {"nama": "Indomie Hype Abis (2 pcs)", "harga": 5900},
    {"nama": "Richeese Wafer 54g (2 pcs)", "harga": 10000},
    {"nama": "Herbakof Strong Mint", "harga": 20000},
    {"nama": "So Fresh Citrus (2 pcs)", "harga": 12500},
    {"nama": "SoSoft Detergent 700ml", "harga": 16500},
    {"nama": "Bagus Karbol Wangi", "harga": 10900},
    {"nama": "Bebek Pembersih Kloset", "harga": 19900},
    {"nama": "Plossa Blue Mountain", "harga": 14900},
    {"nama": "SpongeBob Buddies Figure", "harga": 29900},
    {"nama": "Gabby's Dollhouse Set", "harga": 24900},
    {"nama": "Hot Wheels Assorted", "harga": 59900}
]

BUDGET = 125000
POPULATION_SIZE = 25
CROSSOVER_RATE = 0.23
MUTATION_RATE = 0.1
MAX_GENERATION = 55


class GeneticAlgorithmParcel:

    def __init__(self):
        self.num_products = len(PRODUCTS)
        self.best_each_generation = []

    def create_chromosome(self):
        return [random.randint(0, 1) for _ in range(self.num_products)]

    def total_price(self, chromosome):
        return sum(
            chromosome[i] * PRODUCTS[i]["harga"]
            for i in range(self.num_products)
        )

    def objective_function(self, chromosome):
        total = self.total_price(chromosome)
        if total > BUDGET:
            return abs(total - BUDGET) + 100000 
        return BUDGET - total  

    def fitness(self, chromosome):
        return 1 / (1 + self.objective_function(chromosome))

    def selection(self, population):
        fitness_values = [self.fitness(c) for c in population]
        total_fit = sum(fitness_values)
        probabilities = [f / total_fit for f in fitness_values]
        return random.choices(population, probabilities, k=2)

    def crossover(self, parent1, parent2):
        if random.random() < CROSSOVER_RATE:
            point = random.randint(1, self.num_products - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1[:], parent2[:]

    def mutation(self, chromosome):
        for i in range(self.num_products):
            if random.random() < MUTATION_RATE:
                chromosome[i] = 1 - chromosome[i]
        return chromosome

    def run(self):
        population = [self.create_chromosome() for _ in range(POPULATION_SIZE)]
        global_best = None
        global_best_value = float("inf")

        for gen in range(MAX_GENERATION):
            new_population = []

            for _ in range(POPULATION_SIZE // 2):
                p1, p2 = self.selection(population)
                c1, c2 = self.crossover(p1, p2)
                new_population.append(self.mutation(c1))
                new_population.append(self.mutation(c2))

            population = new_population

            best_gen = min(population, key=self.objective_function)
            min_value = self.objective_function(best_gen)
            self.best_each_generation.append(min_value)

            if min_value < global_best_value:
                global_best_value = min_value
                global_best = best_gen

        return global_best, global_best_value


ga = GeneticAlgorithmParcel()
best_solution, best_value = ga.run()

print("\nTABEL NILAI MINIMUM TIAP ITERASI")
print("Iterasi | Nilai Minimum (Kembalian)")
print("-----------------------------------")
for i, val in enumerate(ga.best_each_generation):
    print(f"{i+1:7} | Rp.{val:>10,.0f}")

print("\nNILAI MINIMUM GLOBAL / AKHIR")
print(f"Kembalian terkecil: Rp.{best_value:,.0f}")

print("\nPAKET PARCEL TERPILIH:")
total = 0
for i in range(len(best_solution)):
    if best_solution[i] == 1:
        print(f"- {PRODUCTS[i]['nama']} (Rp.{PRODUCTS[i]['harga']:,})")
        total += PRODUCTS[i]['harga']

print(f"\nTotal Harga Paket : Rp.{total:,}")
print(f"Budget            : Rp.{BUDGET:,}")
print(f"Kembalian          : Rp.{BUDGET - total:,}")
