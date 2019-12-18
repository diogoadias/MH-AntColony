import numpy as np
from numpy.random import choice as np_choice

class AntColony(object):

    def __init__(self, distances, n_ants, n_best, n_iterations, evaporation, alpha=1, beta=1):
       
        self.distances  = distances
        self.pheromone = np.zeros(self.distances.shape) / len(distances)       
        self.all_itens = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.evaporation = evaporation
        self.alpha = alpha
        self.beta = beta

    def path_dist(self, path):
        total_dist = 0
        for pair in path:
            total_dist += self.distances[pair]
        return total_dist

    def spread_pheronome(self, paths, n_best, shortest_path):
        sorted_paths = sorted(paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def run(self):
        shortest_path = None
        
        for i in range(self.n_iterations):
            paths = self.gen_paths()
            self.spread_pheronome(paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(paths, key=lambda x: x[1])
            
            if shortest_path[1] < best_path[1]:
                best_path = shortest_path            
            self.pheromone * self.evaporation 

        return best_path    

    def gen_paths(self):
        paths = []
        for i in range(self.n_ants):
            path = self.gen_ant_path(0)
            paths.append((path, self.path_dist(path)))
        return paths

    def gen_ant_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.move_to_next(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # going back to where we started    
        return path

    def move_to_next(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)

        move = np.random.choice(self.all_itens, 1, p=None)[0]
        while move in visited:
            move = np.random.choice(self.all_itens, 1, p=None)[0]
        return move