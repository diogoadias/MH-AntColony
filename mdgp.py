"""
The first line has the following fields separed with spaces:
M: Integer indicating the number of elements 
G: Integer indicating the number of groups
Group Type: The value can be "ss" or "ds" and represent "same size group" or "different size group"
Group limits: The last numbers of the line correspond to the lower and upper limits of each group

The following lines contain the distance between elements with the format:
elementA elementB distance
"""
import pandas as pd
import numpy as np

class MDGP:
    def __init__(self, filename):
        self.read_file(filename)
        self.bags_values = []
    
    def read_file(self, filename):
        file = pd.read_csv(filename, delimiter=" ", skiprows=0, header=None, engine='python')
        info = file.iloc[0]
              
        self.size = int(info[0])
        self.group_size = int(info[1])
        self.type = info[2]
        self.groups = []
        
        count = 0
        max_group = (self.group_size * 2) -1
        
        while count <= max_group:
            self.groups.append(info.iloc[3+count])
            self.groups.append(info.iloc[3+count+1])
            count += 2

        self.data = file[1:]
        #file.columns = ["start", "end", "distance"]
        self.create_matrix()

    def create_matrix(self):
        distances = np.zeros((self.size, self.size))
        for i in range(0, len(self.data)):
            start = self.data[0].values[i]
            end = self.data[1].values[i]
            
            distances[start][end] = float(self.data[2].values[i])                

        self.distances = distances

    def create_bags(self, path):
        start_bag = []
        bags = []
        for i in range(0, len(path[0])):
            for j in path[0][i]:
                if j not in start_bag:
                    start_bag.append(j)      
        
        position = 0        
        for i in range(0, len(self.groups), 2):
            count = 0
            temp_bag = []
            min = self.groups[i]
            max = self.groups[i+1]            
            while count < max:
                if position < len(start_bag):
                    temp_bag.append(start_bag[position])
                    
                position += 1
                count +=1
            bags.append(temp_bag)
        
        self.values = self.adjust_bags(bags) 
        return self.values
        #print(bags)

    def adjust_bags(self, bags):
        count = 0
       
        for i in range(0, self.group_size):
            min = self.groups[count]
            max = self.groups[count+1]
            if len(bags[i]) < min or len(bags[i]) > max:                               
                while len(bags[i]) < min or len(bags[i]) > max:
                    bags[i].append(bags[i-1][0])
                    bags[i-1].remove(bags[i-1][0])
                    self.adjust_bags(bags)
            count += 2
                
        all_values = []
        for i in range(0, len(bags)):
            total = 0
            count = 0
            while count < len(bags[i]) -1:
                start = bags[i][count]
                end = bags[i][count+1] 
                total += self.distances[start][end]
                count += 1
            all_values.append(total)
        return all_values
        

        #print(bags)
        #print(all_values)   
    
    @staticmethod
    def stats(values, iteration=1):
        #fitnesses = [ individual.fitness.values[0] for individual in population ]
        return {
            'mean': np.mean(values),
            'std': np.std(values),
            'max': np.max(values),
            'min': np.min(values),
            'total': np.sum(values)
        }  
        
#arquivo = MDGP("RanReal_n010_ds_01.txt")


#print(arquivo.data[0].values[11])
#print(arquivo.distances)