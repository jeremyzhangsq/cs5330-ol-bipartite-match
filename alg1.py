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
    print('f: %f %f %f %f'%(a, b, k, theta))
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
    global x, y
    # Create a LP Minimization problem
    print('alg1 beta: %f k: %f'%(beta, k))
    Lp_prob = p.LpProblem('Problem', p.LpMaximize)

    # Create problem Variables
    t = p.LpVariable("t", upBound=1, cat='Continuous')  # Create a variable x >= 0

    # Objective Function
    Lp_prob += t
    # Constraints:
    t.setInitialValue(1.)
    # add the max(t-y[0],0)
    lhs = p.lpSum([t - y[u] if t.value() > y[u] else 0 for u in ngbrs])
    # todo: only take k=1 here
    rhs = p.LpAffineExpression((1 - t))
    Lp_prob += lhs <= rhs

    # Display the problem
    # print(Lp_prob)
    status = Lp_prob.solve()  # Solver
    # print(p.LpStatus[status])  # The solution status

    # Printing the final solution
    # print(p.value(t), p.value(Lp_prob.objective))

    # get the t value from the LP
    theta = t.value()
    # update x,y array
    for u in ngbrs:
        val = (max(theta - y[u], 0) / beta) * (1 + (1 - theta) / f(theta, k=k))
        x[(u, v)] = val
        x[(v, u)] = val
        y[u] = max(y[u], theta)
    y[v] = 1 - theta
