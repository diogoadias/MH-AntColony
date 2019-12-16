class ACO():
    def __init__(self, ant_count: int,  alpha: float, beta: float, q: int, rq:float):
        self.ant_count = ant_count
        self.alpha = alpha
        self.beta = beta
        self.Q = q
        self.rq = rq
        self.pheromone = 

    def update_pheromone(self, route:list ants:list):
        for i, row in enumerate(self.pheromone):
            for j, col in enumerate(row):
                route[i][j] += self.rq
                for ant in ants: