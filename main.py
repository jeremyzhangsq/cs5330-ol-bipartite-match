import numpy as np
import sys
import random
import baseline
import alg1
import alg2
import alg3


def read_network(fname):
    f = open(fname, "r")
    string = f.readline().rstrip(endreg)
    # shape[0] is user size shape[1] is group size
    shape = [int(s) for s in string.split(delimiter)]
    # adjacent list of the graph
    graph = dict()
    for line in f.readlines():
        line = line.rstrip(endreg)
        line = line.split(delimiter)
        # extract current edge <userid, groupid>
        userid = int(line[0])
        groupid = int(line[1]) + shape[0]
        # store current edge into adjacent list
        if userid not in graph:
            graph[userid] = [groupid]
        else:
            graph[userid].append(groupid)
        if groupid not in graph:
            graph[groupid] = [userid]
        else:
            graph[groupid].append(userid)
    return graph


if __name__ == '__main__':
    fid = int(sys.argv[1])
    aid = int(sys.argv[2])
    files = ["actor-movie.txt", "github.txt", "youtube.txt"]
    algs = ["GREEDY", "RANK", "OFFLINE", "ALG2", "ALG3"]
    endreg = "\r\n"
    delimiter = " "

    # adjacent list of the graph
    graph = read_network("./dataset/" + files[fid])

    # simulate the general vertex arrival: the vertex comes with edges to previous neighbors
    stream = list(graph.keys())  # random vertex streaming
    random.shuffle(stream)
    arrived = []  # already arrived vertex
    match = []  # result
    while len(stream) != 0:
        vertex = stream.pop()  # get next vertex
        # get previous neighbors of current vertex
        neighbors = list(set(graph[vertex]).intersection(arrived))
        # main subroutine:
        # args: coming vertex, its previous neighbors, the whole graph(if needed) and result match list
        if algs[aid] == "GREEDY":
            baseline.greedy(vertex, neighbors, graph, match)
        elif algs[aid] == "RANK":
            baseline.rank(vertex, neighbors, graph, match)
        elif algs[aid] == "OFFLINE":
            baseline.offline(vertex, neighbors, graph, match)
        elif algs[aid] == "ALG2":
            alg2.alg2(vertex, neighbors, graph, match)
        elif algs[aid] == "ALG3":
            alg3.alg3(vertex, neighbors, graph, match)
        else:
            exit(-1)
        arrived.append(vertex)
