from config import graph,match,x,y
import alg1
import numpy as np



def alg2(vertex, neighbors):
    if not len(neighbors):
        return
    alg1.alg1(vertex,neighbors)
    pass