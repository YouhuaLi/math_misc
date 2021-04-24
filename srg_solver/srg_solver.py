from sympy.logic.boolalg import to_cnf
from sympy import symbols, Symbol
from sympy.logic.inference import satisfiable
import sys
import itertools
import re

v = int(sys.argv[1])
k = int(sys.argv[2])
lbd = int(sys.argv[3])
mu = int(sys.argv[4])

def tuple_to_symbol(t, debug=True): # convert (1,2) to symbol x12, if debug==True
    if debug:
        symbol_index = str(t[0]) + str(t[1])
    else:
        symbol_index = ( (2 * v - 3) * t[0] - t[0] * t[0]  ) // 2 + t[1]

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

def gen_lbd_clause(edge, debug=False):
    neighbors = gen_neighbors(edge)
    #print(edge)
    #print(neighbors)
    c = tuple_to_symbol(edge)
    if lbd == 0:
        for (n1, n2) in neighbors:
            n_s_1 = tuple_to_symbol(n1)
            n_s_2 = tuple_to_symbol(n2)
            l = n_s_1 & n_s_2
            c &= ~l
    elif lbd == 1:
        m = False
        for (postive_neighbor1, postive_neighbor2) in neighbors:
            #print("postive_neighbors %s" % str((postive_neighbor1, postive_neighbor2)))
            s = tuple_to_symbol(postive_neighbor1) & tuple_to_symbol(postive_neighbor2)
            l = True
            negative_neighbors = [n for n in neighbors if n not in [(postive_neighbor1, postive_neighbor2)]]
            #print("negative_neighbors %s" % str(negative_neighbors))
            for (n1, n2) in negative_neighbors:
                #print((n1, n2))
                l &= ~(tuple_to_symbol(n1) & tuple_to_symbol(n2))
            s &= l
            m |= s
            #print(m)
        c &= m
    else: #blow code have bugs
        m = False
        for postive_neighbors in itertools.combinations(neighbors, lbd):
            #print("postive_neighbors %s" % str(postive_neighbors))
            s = True
            l = True
            for (postive_neighbor1, postive_neighbor2) in postive_neighbors:
                l &= tuple_to_symbol(postive_neighbor1) & tuple_to_symbol(postive_neighbor2)
            negative_neighbors = [n for n in neighbors if n not in list(postive_neighbors)]
            #   print("negative_neighbors %s" % str(negative_neighbors))
            for (n1, n2) in negative_neighbors:
                l &= ~(tuple_to_symbol(n1) & tuple_to_symbol(n2))
            s &= l
            m |= s
            #print(s)
        c &=m
    #postive_neighbors = itertools.combinations(neighbors, lbd)
    #print(c)
    return c


def gen_mu_clause(edge, debug=False):
    neighbors = gen_neighbors(edge)
    #print(neighbors)
    c = False
    e = tuple_to_symbol(edge)
    #copyed_neighbors = copy.deepcopy(neighbors)
    if mu == 1:
        for (n1, n2) in neighbors:
            p = ~e & tuple_to_symbol(n1) & tuple_to_symbol(n2)
            for n in neighbors:
                if n != (n1, n2):
                    n_s_1 = tuple_to_symbol(n[0])
                    n_s_2 = tuple_to_symbol(n[1])
                    p = p & ~(n_s_1 & n_s_2)
                    #print(p)
            c |= p
    else:
        m = False
        for postive_neighbors in itertools.combinations(neighbors, mu):
            #print("postive_neighbors %s" % str(postive_neighbors))
            s = True
            l = True
            for (postive_neighbor1, postive_neighbor2) in postive_neighbors:
                l &= tuple_to_symbol(postive_neighbor1) & tuple_to_symbol(postive_neighbor2)
            negative_neighbors = [n for n in neighbors if n not in list(postive_neighbors)]
            #print("negative_neighbors %s" % str(negative_neighbors))
            for (n1, n2) in negative_neighbors:
                l &= ~(tuple_to_symbol(n1) & tuple_to_symbol(n2))
            s &= l
            #print(s)
            m |=s
            #print(m)
        c = ~e & m
    #postive_neighbors = itertools.combinations(neighbors, lbd)
    #print(c)
    return c

#set the first k varialbes to be True, then v-k variables to be False
#only run when debug==False
def gen_k_clause(debug = False):
    if debug: return True
    postive_edges = edges[:k]
    negative_edges = edges[k:v-1]
    c = True
    for p_e in postive_edges:
        c &= tuple_to_symbol(p_e)
    for n_e in negative_edges:
        c &= ~tuple_to_symbol(n_e)

    #print("k_clause is %s" % str(c))
    return c


def gen_clause(edge):
    lbd_clause = gen_lbd_clause(edge)
    mu_clase = gen_mu_clause(edge)
    return lbd_clause | mu_clase

#conver symbols tring to cnf file output
def convert_to_cnf_file_format(s, variabl_count):
    clause_count = s.count('&') + 1
    header = "c srg v=%d k=%d lbd=%d mu=%d\nc\n" % (v, k, lbd, mu)
    header += "p cnf %d %d\n" % (variabl_count, clause_count)
    rep = {"x": "", "~": "-", "& ": "0\n", \
          "(": "", ")": "", "x": "", "|": ""} # define desired replacements here

    # use these three lines to do the replacement
    rep = dict((re.escape(k), v) for k, v in rep.items())

    #Python 3 renamed dict.iteritems to dict.items so use rep.items() for latest versions
    pattern = re.compile("|".join(rep.keys()))
    body = pattern.sub(lambda m: rep[re.escape(m.group(0))], s).strip()
    return header + body + " 0"

vertexs = range(v)
edges = list(itertools.combinations(vertexs, 2))
#print(edges)

#print(edges)
clause = True
for edge in edges:
    #print(tuple_to_symbol(edge))
    e_c = gen_clause(edge)
    clause &= e_c
    #print(e_c)
    #break
clause &= gen_k_clause()
print("start testing satisfiable...")
#print(satisfiable(clause))
