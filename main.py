import numpy as np
import time
from mdgp import MDGP
from ant import AntColony

start = time.time()

arquivo = MDGP("mdgplib/RanReal/RanReal_n030_ds_01.txt")

distances = arquivo.distances

ant_colony = AntColony(distances, 5, 10, 100, 0.95, alpha=1, beta=1)
shortest_path = ant_colony.run()
print ("shorted_path: {}".format(shortest_path))

arquivo.create_bags(shortest_path)


end = time.time()

print("TIME:", end - start)