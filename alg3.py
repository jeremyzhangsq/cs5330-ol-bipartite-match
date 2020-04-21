from config import graph,match,x,y
import alg1
import numpy as np
import math
import time
import numpy

prob_fuv = None
prob_fwuv_total = None
prob_fwuv = None
monte_carlo_times = 20
vertex_list = []
num_vertex = 0

def alg3(graph, stream, k=1.1997, monte_carlo=False, next_vertex=None):
    global vertex_list
    global prob_fwuv_total
    global prob_fwuv
    global prob_fuv
    global num_vertex
    if not monte_carlo:
        print('init...')
        vertex_list = list(graph.keys())
        # print(vertex_list)
        num_vertex = len(vertex_list)
        print('num vertex: %d'%num_vertex)
        i = 0
        prob_fwuv_total = np.zeros((num_vertex, num_vertex, num_vertex))
        prob_fwuv = np.zeros((num_vertex, num_vertex, num_vertex))
        prob_fuv = np.zeros((num_vertex, num_vertex))
        
    # print(k)
    epsilon = (k - 1) /2
    sqrt_epsilon = math.sqrt(epsilon)
    beta = 2 - epsilon
    if not monte_carlo:
        print('k:%f beta:%f epsilon:%f'%(k, beta, epsilon))

    global x, y
    match = dict()
    arrived_vertex = []
    free_vertx = set(vertex_list.copy())

    data_len = len(stream)
    print_len = 1 # int(data_len/200)

    start_time = time.time()
    for i in range(len(stream)):

        if not monte_carlo:
            v = stream[i]
            neighbor_v = list(set(graph[v]).intersection(arrived_vertex))
            alg1.alg1(v, neighbor_v, beta=beta, k=k)

        if not monte_carlo and i%print_len == 0:
            print('  processing stream: %d/%d time: %f'%(i, data_len, time.time()-start_time))
            # time.sleep(0.5)
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
            for monte_i in range(monte_carlo_times):
                # print('    monte i: %d'%monte_i)
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

        if u1 is not None and u1 in free_vertx:
            match[u1] = v
            match[v] = u1
            free_vertx.remove(u1)
            free_vertx.remove(v)
        elif u2 is not None and u2 in free_vertx:
            match[u1] = v
            match[v] = u1
            free_vertx.remove(u2)
            free_vertx.remove(v)

        arrived_vertex.append(v)

    if monte_carlo:
        for a in free_vertx:
            prob_fuv[a][next_vertex] += 1
            for b in free_vertx:
                prob_fwuv[a][b][next_vertex] += 1
        prob_fwuv_total[:][:][next_vertex] += 1

    return match
