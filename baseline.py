import random
from config import graph,match,x,y

def greedy(vertex, neighbors):
    if len(neighbors) != 0:
        selectedVertex = random.choice(neighbors)
        neighbors.remove(selectedVertex)
        match_pair = (vertex, selectedVertex)
        match.append(match_pair)


def rank(vertex, neighbors):
    pass


def offline():
    pass
