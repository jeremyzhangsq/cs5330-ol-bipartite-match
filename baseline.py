import random


def greedy(vertex, neighbors, graph, match):
    if len(neighbors) != 0:
        selectedVertex = random.choice(neighbors)
        neighbors.remove(selectedVertex)
        match_pair = [vertex, selectedVertex]
        match.append(match_pair)


def rank(vertex, neighbors, graph, match):
    pass


def offline(vertex, neighbors, graph, match):
    pass
