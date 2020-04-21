from config import graph,match,x,y
import alg1
import numpy as np
import math
import time

prob_fuv = dict()
prob_fwuv = dict()
prob_fwuv_total = dict()
monte_carlo_times = 100
vertex_list = []

def alg3(graph, stream, k=1.1997, monte_carlo=False, next_vertex=None):
    global vertex_list
    if not monte_carlo:
        print('init...')
        vertex_list = list(graph.keys())
        for i in vertex_list:
            prob_fuv[i] = dict()
            prob_fwuv[i] = dict()
            prob_fwuv_total[i] = dict()
            for j in vertex_list:
                prob_fuv[i][j] = 0
                prob_fwuv[i][j] = dict()
                prob_fwuv_total[i][j] = dict()
                for l in vertex_list:
                    prob_fwuv[i][j][l] = 0
                    prob_fwuv_total[i][j][l] = 0
        
    # print(k)
    epsilon = (k - 1) /2
    sqrt_epsilon = math.sqrt(epsilon)
    beta = 2 - epsilon
    if not monte_carlo:
        print('k:%f beta:%f epsilon:%f'%(k, beta, epsilon))

    global x, y
    match = dict()
    arrived_vertex = []
    non_free_vertex = set()

    data_len = len(stream)
    print_len = int(data_len/20)

    start_time = time.time()
    for i in range(len(stream)):

        if not monte_carlo:
            v = stream[i]
            neighbor_v = list(set(graph[v]).intersection(arrived_vertex))
            alg1.alg1(v, neighbor_v, beta=beta, k=k)

        if not monte_carlo and i%print_len == 0:
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
            z_u[u] = x[(u, v)]/(prob_fuv[u][v]/monte_carlo_times+1/monte_carlo_times)
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

        if not monte_carlo:
            for _ in range(monte_carlo_times):
                alg3(graph, stream[:i], monte_carlo=True, next_vertex=v)

        # sample u2
        u2 = None
        if normal_factor > 1.0:
            if np.random.rand(1) < sqrt_epsilon:
                u2 = rng.choice(z_u_list, 1, z_u_prob_list)[0]

            # todo: drop u2 with p, Monte Carlo
            if u2 is not None:
                z_u2 = z_u_prob_list[z_u_list.index(u2)]
                temp = 0
                for w in neighbor_v:
                    z_w = z_u_prob_list[z_u_list.index(w)]
                    temp += z_w*(1 - prob_fwuv[w][u][v]/(prob_fwuv_total[w][u][v]+1))
                p = prob_fuv[u][v]/monte_carlo_times * (z_u2 + z_u2*sqrt_epsilon*temp)
                if np.random.rand(1) < p:
                    u2 = None

        if u1 is not None and u1 not in non_free_vertex:
            match[u1] = v
            match[v] = u1
            non_free_vertex.add(u1)
            non_free_vertex.add(v)
        elif u2 is not None and u2 not in non_free_vertex:
            match[u1] = v
            match[v] = u1
            non_free_vertex.add(u2)
            non_free_vertex.add(v)

        arrived_vertex.append(v)

    if monte_carlo:
        for vertex in vertex_list:
            if vertex not in non_free_vertex:
                prob_fuv[vertex][next_vertex] += 1
                for vertex2 in vertex_list:
                    if vertex2 not in non_free_vertex:
                        prob_fwuv[vertex2][vertex][next_vertex] += 1
                    prob_fwuv_total[vertex2][vertex][next_vertex] += 1

    return match
