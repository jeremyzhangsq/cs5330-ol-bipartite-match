import numpy as np
from config import graph,match,x,y
import sys
import random
import baseline
import alg1
import alg2
import alg3

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
    string = f.readline().rstrip(endreg)
    # shape[0] is user size shape[1] is group size
    shape = [int(s) for s in string.split(delimiter)]
    # adjacent list of the graph
    for l in f.readlines():
        line = l.rstrip(endreg)
        line = line.split(delimiter)
        # extract current edge <userid, groupid>
        userid = "u"+line[0]
        groupid = "g"+line[1]
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



if __name__ == '__main__':
    fid = int(sys.argv[1])
    aid = int(sys.argv[2])
    files = ["revolution.txt","actor-movie.txt", "github.txt", "youtube.txt"]
    algs = ["GREEDY", "RANK", "OFFLINE", "ALG2", "ALG3"]
    endreg = "\r\n"
    delimiter = " "

    # adjacent list of the graph
    read_network("./dataset/" + files[fid])

    if algs[aid] == "OFFLINE":
        baseline.offline()
    else:
        # simulate the general vertex arrival: the vertex comes with edges to previous neighbors
        stream = list(graph.keys())  # random vertex streaming
        # fix seed here
        random.seed(1)
        random.shuffle(stream)
        arrived = []  # already arrived vertex

        if algs[aid] == "ALG3":
            alg3.main_alg3(graph, stream, k=1)
        else:
            while len(stream) != 0:
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

    # for debug
    logger.debug("#Matched: %d tuples: %s" % (len(match), match))