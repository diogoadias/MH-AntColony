import numpy as np
import time
import os
from mdgp import MDGP
from ant import AntColony

files = os.listdir("mdgplib/RanReal/")

for arquivo in files:
    start = time.time()
    print("INSTANCE:", arquivo)
    arquivo = MDGP("mdgplib/RanReal/" + arquivo)

    distances = arquivo.distances

    ant_colony = AntColony(distances, 5, 10, 100, 0.95, alpha=1, beta=1)
    shortest_path = ant_colony.run()

    values = arquivo.create_bags(shortest_path)
    results = MDGP.stats(values)
    print(results)

    end = time.time()

    print("TIME:", end - start)