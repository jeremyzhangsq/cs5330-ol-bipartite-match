import numpy as np
from config import graph,match,x,y
import sys
import random
import baseline
import alg1
import alg2
import alg3
import time

import logging
# Create and configure logger
logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def read_network(fname):
    global x, y, graph
    f = open(fname, "r")
    string = f.readline()
    # adjacent list of the graph
    uid_dict = dict()
    gid_dict = dict()
    uid = 0
    gid = 0
    line_list = f.readlines()
    for l in line_list:
        line = l.rstrip(endreg)
        line = line.split(delimiter)
        # extract current edge <userid, groupid>
        if line[0] not in uid_dict:
            uid_dict[line[0]] = uid
            uid += 1
        if line[1] not in gid_dict:
            gid_dict[line[1]] = gid
            gid += 1

    uid_size = uid
    print('uid_size: %d'%uid_size)
    for l in line_list:
        line = l.rstrip(endreg)
        line = line.split(delimiter)
        userid = uid_dict[line[0]]
        groupid = gid_dict[line[1]] + uid_size
        x[(userid, groupid)] = 0 # init the fractional matching x as map with key = tuple(id,id) value = fractional prob
        # store current edge into adjacent list
        if userid not in graph:
            graph[userid] = [groupid]
            y[userid] = 0 # init the fractional vertex cover y as map with key = id value = fractional prob
        else:
            graph[userid].append(groupid)
        if groupid not in graph:
            graph[groupid] = [userid]
            y[groupid] = 0
        else:
            graph[groupid].append(userid)
    f.close()
    return uid_size

def is_match(match):
    l = list(match.keys())
    s = set(l)
    return len(l)==len(s)

if __name__ == '__main__':
    fid = int(sys.argv[1])
    aid = int(sys.argv[2])
    files = ["revolution.txt","crime.txt", "ucforum.txt", "actor-movie.txt", "github.txt", "youtube.txt", "actor_movie_sample.txt", "random_graph.txt"]
    algs = ["GREEDY", "RANK", "OFFLINE", "ALG2", "ALG3"]
    endreg = "\r\n"
    delimiter = " "

    # adjacent list of the graph
    uid_size = read_network("./dataset/" + files[fid])

    if algs[aid] == "OFFLINE":
        print('processing alg: ' + str(algs[aid]))
        baseline.offline(uid_size)
        offline_num_match = len(match)
        print('num_match: %d'%(offline_num_match))
    else:
        print('shuffling data')
        # simulate the general vertex arrival: the vertex comes with edges to previous neighbors
        stream = list(graph.keys())  # random vertex streaming
        # fix seed here
        random.seed(time.time())
        random.shuffle(stream)
        arrived = []  # already arrived vertex

        print('processing alg: ' + str(algs[aid]))
        data_len = len(stream)
        print_len = int(len(stream)/20)
        i = 0
    
        start_time = time.time()
        total_start_time = start_time
        if algs[aid] == "ALG3":
            alg3_match = alg3.alg3(graph, stream, k=1.1997)
        else:
            while len(stream) != 0:
                
                if i%print_len == 0:
                    print('  processing stream: %d/%d time: %f'%(i, data_len, time.time()-start_time))
                    start_time = time.time()
                i += 1

                vertex = stream.pop()  # get next vertex
                # get previous neighbors of current vertex
                neighbors = list(set(graph[vertex]).intersection(arrived))
                # main subroutine:
                # args: coming vertex, its previous neighbors
                if algs[aid] == "GREEDY":
                    baseline.greedy(vertex, neighbors)
                elif algs[aid] == "RANK":
                    baseline.rank(vertex, neighbors)
                elif algs[aid] == "ALG2":
                    alg2.alg2(vertex, neighbors)
                else:
                    exit(-1)
                arrived.append(vertex)
        print('total time: %f'%(time.time()-total_start_time))

    if algs[aid] == 'ALG3':
        assert is_match(alg3_match)
        num_match = len(alg3_match)
    else:
        assert is_match(match)
        num_match = len(match)
    # for debug
    # logger.debug("#Matched: %d tuples: %s" % (len(match), match))

    # print(match)
    if algs[aid] != "OFFLINE":
        print('processing alg: OFFLINE')
        match.clear()
        baseline.offline(uid_size)
        offline_num_match = len(match)
        # logger.debug("#Matched: %d tuples: %s" % (len(match), match))
        # print('num_match: %d'%(offline_num_match))
        print('competitive ratio: %f'%(num_match/offline_num_match))