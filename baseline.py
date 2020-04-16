import random
from config import graph, match, x, y


def greedy(vertex, neighbors):
    if len(neighbors) != 0:
        # if the selected vertex is not in the match list, then match
        # else need to select again
        random.shuffle(neighbors)
        selectedVertex = None
        isValid = False
        for i in range(len(neighbors)):
            # selectedVertex = random.choice(neighbors)
            selectedVertex = neighbors[i]
            if selectedVertex not in match.keys():
                isValid = True
                break
        if selectedVertex is None or isValid is False:
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
        isValid = False
        for i in range(len(neighbors)):
            # selectedVertex = random.choice(neighbors)
            selectedVertex = neighbors[i]
            if selectedVertex not in match.keys():
                isValid = True
                break
        if selectedVertex is None or isValid is False:
            return

        neighbors.remove(selectedVertex)
        # match_pair = (vertex, selectedVertex)
        # match.append(match_pair)
        match[vertex] = selectedVertex
        match[selectedVertex] = vertex


def offline():
    # bipartite graph
    lGraph = {}
    rGraph = {}
    # used for dfs traverse
    visited = {}
    # if the vertex is matched, just for xiongyali
    matchedVL = {}
    matchedVR = {}
    # 1. form the graph
    for vertex in graph:
        if vertex[0] == 'u':
            lGraph[vertex] = graph[vertex]
            matchedVL[vertex] = -1
        else:
            rGraph[vertex] = graph[vertex]
            matchedVR[vertex] = -1
            visited[vertex] = -1
    # 2. match vertices
    hungary = DFS_hungary(lGraph, rGraph, matchedVL, matchedVR, visited)
    print(hungary.max_match())
    # 3. get the results


class DFS_hungary():

    def __init__(self, nx, ny, cx, cy, visited):
        self.nx, self.ny=nx, ny
        self.cx, self.cy=cx,cy
        self.visited=visited

    def max_match(self):
        res=0
        for i in self.nx:
            if self.cx[i]==-1: # if there is no match?
                for key in self.ny:         # 将visited置0表示未访问过
                    self.visited[key] = 0
                res+=self.path(i)
        return res

    def path(self, u):
        # find in neighbor
        for v in self.nx[u]:
            if not self.visited[v]:
                self.visited[v]=1
                if self.cy[v]==-1:
                    self.cx[u] = v
                    self.cy[v] = u
                    match[u] = v
                    match[v] = u
                    return 1
                else:
                    # del match[match[v]]
                    # del match[v]
                    if self.path(self.cy[v]):
                        self.cx[u] = v
                        self.cy[v] = u
                        match[u] = v
                        match[v] = u
                        return 1
        return 0