import numpy as np
import random

if __name__ == '__main__':
    num_vertex = 100
    expected_num_edges = 400
    p = expected_num_edges / (num_vertex*num_vertex/2)

    graph = np.zeros((num_vertex, num_vertex))

    with open('dataset/random_graph.txt', 'w') as out_file:
        out_file.write('%d %d\n'%(num_vertex, num_vertex))
        for i in range(num_vertex):
            for j in range(num_vertex):
                if np.random.rand(1) < p:
                    out_file.write('%d %d\n'%(i, j))