import random
from config import graph, match, x, y


def greedy(vertex, neighbors):
    if len(neighbors) != 0:
        # if the selected vertex is not in the match list, then match
        # else need to select again
        random.shuffle(neighbors)
        selectedVertex = None
        for i in range(len(neighbors)):
            # selectedVertex = random.choice(neighbors)
            selectedVertex = neighbors[i]
            if selectedVertex not in match.keys():
                break
        if selectedVertex is None:
            return

        neighbors.remove(selectedVertex)
        # match_pair = (vertex, selectedVertex)
        # match.append(match_pair)
        match[vertex] = selectedVertex
        match[selectedVertex] = vertex


def rank(vertex, neighbors):
    if len(neighbors) != 0:
        # TODO: compared to greedy, ranking has a permutation at beginning
        # TODO: I assume that random.shuffle(stream) has done this operation
        # TODO: then every vertex follows the ranking order goes into the system
        # TODO: so the first tuple in the neighbor list should be the vertex with highest rank
        # TODO: I just need to check from 0 to len(neighbors) one by one
        # if the selected vertex is not in the match list, then match
        # else need to select again
        selectedVertex = None
        for i in range(len(neighbors)):
            # selectedVertex = random.choice(neighbors)
            selectedVertex = neighbors[i]
            if selectedVertex not in match.keys():
                break
        if selectedVertex is None:
            return

        neighbors.remove(selectedVertex)
        # match_pair = (vertex, selectedVertex)
        # match.append(match_pair)
        match[vertex] = selectedVertex
        match[selectedVertex] = vertex


def offline():
    pass
