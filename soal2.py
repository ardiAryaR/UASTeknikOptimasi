import random

matriks = [
    [0, 360, 185, 335, 160, 340, 334, 362, 163, 204],
    [360, 0, 293, 579, 269, 601, 583, 610, 370, 318],
    [185, 293, 0, 405, 261, 408, 409, 202, 80.6, 21.4],
    [335, 579, 405, 0, 313, 4, 24, 56.5, 164, 241],
    [160, 269, 26.1, 313, 0, 383, 382, 225, 104, 45.8],
    [340, 601, 408, 4, 383, 0, 22.5, 56.5, 164, 244],
    [334, 583, 409, 24, 382, 22.5, 0, 75.9, 181, 336],
    [362, 610, 202, 56.5, 225, 56.5, 75.9, 0, 120, 200],
    [163, 370, 80.6, 164, 104, 164, 181, 120, 0, 80.9],
    [204, 318, 21.4, 241, 45.8, 244, 336, 200, 80.9, 0]
]

cityNames = [
    "Kos",
    "Sunan Gunung Jati (Cirebon)",
    "Sunan Kudus",
    "Sunan Giri (Gresik)",
    "Sunan Kalijaga (Demak)",
    "Sunan Gresik",
    "Sunan Ampel (Surabaya)",
    "Sunan Drajat (Lamongan)",
    "Sunan Bonang (Tuban)",
    "Sunan Muria (Kudus)"
]

Q = 100
rho = 0.05
antSize = 17
maxIter = 35

start_city_name = "Kos"
start_city_index = cityNames.index(start_city_name)

class AntColonyOptimizationTSP:
    def __init__(self, matriks, antSize, maxIter, Q, rho, start):
        self.matriks = matriks
        self.antSize = antSize
        self.maxIter = maxIter
        self.Q = Q
        self.rho = rho
        self.start = start
        self.cityCount = len(matriks)
        self.pheromone = [[1 for _ in range(self.cityCount)] for _ in range(self.cityCount)]

    def calculate_distance(self, path):
        total = 0
        for i in range(len(path) - 1):
            total += self.matriks[path[i]][path[i+1]]
        total += self.matriks[path[-1]][path[0]]
        return total

    def run(self):
        best_global_distance = float('inf')
        best_global_path = None
        best_each_iteration = []

        for iteration in range(self.maxIter):
            all_paths = []
            all_distances = []

            for _ in range(self.antSize):
                path = [self.start]
                unvisited = list(range(self.cityCount))
                unvisited.remove(self.start)

                while unvisited:
                    current = path[-1]
                    probabilities = []

                    for city in unvisited:
                        pher = self.pheromone[current][city]
                        dist = self.matriks[current][city]
                        probabilities.append((pher * (1/dist)))

                    total = sum(probabilities)
                    probabilities = [p/total for p in probabilities]

                    next_city = random.choices(unvisited, probabilities)[0]
                    path.append(next_city)
                    unvisited.remove(next_city)

                distance = self.calculate_distance(path)
                all_paths.append(path)
                all_distances.append(distance)

            min_distance = min(all_distances)
            best_each_iteration.append(min_distance)

            if min_distance < best_global_distance:
                best_global_distance = min_distance
                best_global_path = all_paths[all_distances.index(min_distance)]

            for i in range(self.cityCount):
                for j in range(self.cityCount):
                    self.pheromone[i][j] *= (1 - self.rho)

            for path, dist in zip(all_paths, all_distances):
                for i in range(len(path) - 1):
                    self.pheromone[path[i]][path[i+1]] += self.Q / dist

        return best_each_iteration, best_global_distance, best_global_path

aco = AntColonyOptimizationTSP(
    matriks,
    antSize,
    maxIter,
    Q,
    rho,
    start_city_index
)

iter_results, best_distance, best_path = aco.run()

print("\nTabel Nilai Minimum Tiap Iterasi")
print("Iterasi | Nilai Minimum")
print("------------------------")
for i, val in enumerate(iter_results):
    print(f"{i+1:7} | {val:.2f}")

print("\nRute Terpendek Ziarah Wali Songo:")
for city in best_path:
    print("-", cityNames[city])
print("-", cityNames[best_path[0]])

print(f"\nNilai Minimum Global: {best_distance:.2f} km")
