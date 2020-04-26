from config import graph, match, x, y
import pulp as p

'''
auxiliary function for LP constrain in fractional matching
:param
theta: input parameter
k: function constant parameter
'''


def f(theta, k=1):
    a = ((1 + k) / 2.0 - theta) ** ((1 + k) / (2.0 * k))
    b = (theta + (k - 1) / 2.0) ** ((k - 1) / (2.0 * k))
    # print('f: %f %f %f %f'%(a, b, k, theta))
    return a * b + 1e-7


"""
:param
vertex: current coming vertex
ngbrs: previous arrived neighbors of vertex
beta: a constant beta (type = float), defaulted by 2
k: a constant in function f, defaulted by 1
:LPSolver tutorial
https://www.geeksforgeeks.org/python-linear-programming-in-pulp/
:return
x,y
"""


def alg1(v, ngbrs, beta=2.0, k=1):
    # print('!')
    global x, y
    # Create a LP Minimization problem
    Lp_prob = p.LpProblem('Problem', p.LpMaximize)
    # Create problem Variables x >= 0
    t = p.LpVariable("t", upBound=1, cat='Continuous')
    # Objective Function
    Lp_prob += t
    # Constraints:
    t.setInitialValue(1.)
    # add the max(t-y[0],0)
    lhs = p.lpSum([t - y[u] if t.value() > y[u] else 0 for u in ngbrs])
    rhs = p.LpAffineExpression((1 - t))
    # add the constraint
    Lp_prob += lhs <= rhs
    # Solve the problem
    Lp_prob.solve()
    # get the theta value from the LP
    theta = t.value()

    # update x,y array
    for u in ngbrs:
        val = (max(theta - y[u], 0) / beta) * (1 + (1 - theta) / f(theta, k=k))
        x[(u, v)] = val
        x[(v, u)] = val
        y[u] = max(y[u], theta)
    y[v] = 1 - theta
