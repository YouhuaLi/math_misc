from sympy.logic.boolalg import to_cnf
from sympy import symbols
import numpy as np
import sys
import itertools
import copy

v = int(sys.argv[1])
k = int(sys.argv[2])
lbd = int(sys.argv[3])
mu = int(sys.argv[4])

def tuple_to_symbol(t): # convert (1,2) to symbol x12
    symbol_index = t[0] * (v - t[0]) + t[1]
    return symbols('x%s' % str(symbol_index))

#return list of tuples (edges) that share one vertex in edge e
def neighbors_of_edge(edge, edges): #return list of tuples that share one
    r = []
    for p in edges: #find 
        if p == edge: continue
        if p[0] == edge[0] or p[0] == edge[1] or p[1] == edge[0] or p[1] == edge[0]:
            r.append(p)
    #print(e)
    #print(r)
    return r


#return list of tupel pairs like [(x1,y1)..(x1,y2)] and each tuple form a triangle with e
def gen_neighbors(e):
    r = []
    #print(list(itertools.combinations(neighbors_of_edge(e, edges), 2)))
    for v in vertexs:
        if v != e[0] and v!= e[1]:
            e1 = tuple(sorted((v, e[0])))
            e2 = tuple(sorted((v, e[1])))
            r.append((e1, e2))
            #print("neighbor of %s is %s" % (str(e), str(r[-1])))
    return r

def gen_lbd_clause(edge):
    neighbors = gen_neighbors(edge)
    #print(neighbors)
    c = tuple_to_symbol(edge)
    if lbd == 0:
        for (n1, n2) in neighbors:
            n_s_1 = tuple_to_symbol(n1)
            n_s_2 = tuple_to_symbol(n2)
            l = n_s_1 & n_s_2 
            c &= ~l 
    #postive_neighbors = itertools.combinations(neighbors, lbd)
    #print(c)
    return c


def gen_mu_clause(edge):
    neighbors = gen_neighbors(edge)
    #print(neighbors)
    c = False
    e = tuple_to_symbol(edge)
    copyed_neighbors = copy.deepcopy(neighbors)
    if mu == 1:
        for (n1, n2) in neighbors:
            p = ~e & tuple_to_symbol(n1) & tuple_to_symbol(n2)
            for n in copyed_neighbors:
                if n != (n1, n2):
                    n_s_1 = tuple_to_symbol(n[0])
                    n_s_2 = tuple_to_symbol(n[1])
                    p = p & ~(n_s_1 & n_s_2)
                    #print(p)
            c |= p
    #postive_neighbors = itertools.combinations(neighbors, lbd)
    #print(c)
    return c

def gen_clause(edge):
    lbd_clause = gen_lbd_clause(edge)
    mu_clase = gen_mu_clause(edge)
    return lbd_clause | mu_clase


vertexs = range(v)
edges = set(itertools.combinations(vertexs, 2))

#print(edges)
clause = True
for edge in edges:
    clause &= gen_clause(edge)

print(clause)
cnf_clause_string = str(to_cnf(clause, simplify=False))
print(cnf_clause_string)

