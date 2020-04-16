from config import graph,match,x,y
import random
import alg1
import numpy as np

def weighted_sampling(dct):
    while 1:
        assert len(dct)>0
        if len(dct)==1:
            l = list(dct.keys())
            return l[0]
        rand_val = random.random()
        total = 0
        for k, v in dct.items():
            total += v
            if rand_val <= total:
                return k

def alg2(v, ngbrs):
    if not len(ngbrs):
        return
    alg1.alg1(v,ngbrs)

    # get the probability z that previous neighbor is free
    z = dict()
    for u in ngbrs:
        z[u] = x[(v,u)]/(1+1e-7 -y[u])
    # Sample (at most) one neighbor according to probability z
    target = weighted_sampling(z)
    if target not in match:
        match[target] = v
        match[v] = target
