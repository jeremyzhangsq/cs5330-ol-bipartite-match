from config import graph,match,x,y
import alg1
import numpy as np
import math
import time

def alg3(graph, stream, k=1.1997):
    epsilon = (k - 1) /2
    sqrt_epsilon = math.sqrt(epsilon)
    beta = 2 - epsilon
    print('k:%f beta:%f epsilon:%f'%(k, beta, epsilon))

    global x, y, match
    arrived_vertex = []
    non_free_vertex = set()

    data_len = len(stream)
    print_len = int(data_len/20)

    start_time = time.time()
    for i in range(len(stream)):

        v = stream[i]
        neighbor_v = list(set(graph[v]).intersection(arrived_vertex))
        alg1.alg1(v, neighbor_v, beta=beta, k=k)

        if i%print_len == 0:
            print('  processing stream: %d/%d time: %f'%(i, data_len, time.time()-start_time))
            time.sleep(0.5)
            start_time = time.time()

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
        u1 = rng.choice(z_u_list, 1, z_u_prob_list)[0]
        # print(z_u_prob_list)

        # sample u2
        u2 = None
        if normal_factor > 1.0:
            if np.random.rand(1) < sqrt_epsilon:
                u2 = rng.choice(z_u_list, 1, z_u_prob_list)[0]
            # todo: drop u2 with p, Monte Carlo

        if u1 is not None and u1 not in non_free_vertex:
            print(u1)
            match[u1] = v
            match[v] = u1
            non_free_vertex.add(u1)
        elif u2 is not None and u2 not in non_free_vertex:
            match[u1] = v
            match[v] = u1
            non_free_vertex.add(u2)

        arrived_vertex.append(v)

