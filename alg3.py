from config import graph,match,x,y
import alg1
import numpy as np
import math

def alg3(graph, stream, sqrt_epsilon):
    global x, y, match
    arrived_vertex = []
    non_free_vertex = []
    for i in range(len(stream)):

        # new vertex and its neighbors
        v = stream[i]
        neighbor_v = list(set(graph[v]).intersection(arrived_vertex))

        # calculate distribution
        z_u = {}
        normal_factor = 0
        for u in neighbor_v:
            z_u[u] = x[(u, v)]
            normal_factor += z_u[u]
        if normal_factor > 1.0:
            for u in neighbor_v:
                z_u[u] = z_u[u]/normal_factor

        # sample u1
        z_u_list = list(z_u.keys())
        z_u_prob_list = list(z_u.values())
        if normal_factor < 1.0:
            z_u_list.append(None)
            z_u_prob_list.append(1-normal_factor)
        rng = np.random.default_rng()
        u1 = rng.choice(z_u_list, 1, z_u_prob_list)

        # sample u2
        if normal_factor > 1.0:
            if np.random.rand(1) < sqrt_epsilon:
                u2 = rng.choice(z_u_list, 1, z_u_prob_list)
            # todo: drop u2 with p, Monte Carlo

        if u1 is not None and u1 not in non_free_vertex:
            match[u1] = v
            match[v] = u1
            non_free_vertex.append(u1)
        elif u2 is not None and u2 not in non_free_vertex:
            match[u1] = v
            match[v] = u1
            non_free_vertex.append(u2)

        arrived_vertex.append(v)


def main_alg3(graph, stream, k=1.1997):
    epsilon = (k - 1) /2
    beta = 2 - epsilon

    # get global solution: x, y
    print('%f %f %f'%(k, beta, epsilon))

    arrived_vertex = []  # already arrived vertex
    for i in range(len(stream)):
        v = stream[i]
        neighbor_v = list(set(graph[v]).intersection(arrived_vertex))
        alg1.alg1(v, neighbor_v, beta=beta, k=k)
        arrived_vertex.append(v)

    # run alg3
    alg3(graph, stream, math.sqrt(epsilon))
