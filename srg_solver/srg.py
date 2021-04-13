import itertools,numpy
import sys
sys.path.insert(0, '/Users/yli/code/conway99')
from conway99 import *
import numpy as np

def initial_vertex_clusters(b):
    vertex_clusters = itertools.product(range(3),[0,1],[0,1])
    return vertex_clusters

#测试某点的兄弟是否已经匹配到同一大组，是则返回False
def test_sibling_group(current_vertex, vertex_for_test):
    if current_vertex[2] == 0:
        sibling_vertex = (current_vertex[0], current_vertex[1], 1)
    else:
        sibling_vertex = (current_vertex[0], current_vertex[1], 0)
    #print("the sibling for test is: %s" % str(sibling_vertex))
    #print("current solution stack is %s" % str(current_solution_stack))
    for vertex_group in current_solution_stack:
        #print("the group in current stack is: %s" % str(vertex_group))
        if vertex_group[0] == sibling_vertex and vertex_group[1][0] == \
        vertex_for_test[0] or vertex_group[1] == sibling_vertex and \
        vertex_group[0][0] == vertex_for_test[0]:
            return False
    return True

def search_next_group_vertex():
    if len(pending_vertex) <= 1:
        return None
    vertex_for_group = pending_vertex[0]
    for vertex in pending_vertex[1:]:
        if vertex > last_matched_vertex[vertex_for_group] and vertex[0] != vertex_for_group[0] and test_sibling_group(vertex_for_group, vertex): # 两点大组不同
            return (vertex_for_group, vertex)
    if last_matched_vertex[vertex_for_group] != (-1,-1,-1):
        return (vertex_for_group, last_matched_vertex[vertex_for_group])
    else:
        return None

def test_solution():
    adjancent_matrix = gen_adjacent_matrix()
    if lambda_compatible(adjancent_matrix) and \
      mu_compatible(adjancent_matrix) and \
      meets_adjacency_requirements(adjancent_matrix, debug=True) and \
      graph_is_valid(adjancent_matrix):
        return True
    else:
        return False

def gen_adjacent_matrix():
    adjacent_matrix = numpy.empty((9,9),dtype='int')
    for i in range(9):
        for j in range(9):
            adjacent_matrix[i,j] = 0
    vertex_to_matrix_index = {}

    #初始化各点在图中的序号，solution的第一个序号为3
    i = 3
    for vertex_group in current_solution_stack:
        vertex_to_matrix_index[vertex_group[0]] = i
        vertex_to_matrix_index[vertex_group[1]] = i
        i += 1
    #print(vertex_to_matrix_index)

    for vertex_group in current_solution_stack:
        #print(vertex_group)
        v1 = vertex_group[0]
        v2 = vertex_group[1]
        index = vertex_to_matrix_index[v1]

        adjacent_matrix[index, v1[0]] = 1
        adjacent_matrix[v1[0], index] = 1
        adjacent_matrix[index, v2[0]] = 1
        adjacent_matrix[v2[0], index] = 1

        adjacent_matrix[index, vertex_to_matrix_index[vertex_to_sibling[v1]]] = 1
        adjacent_matrix[vertex_to_matrix_index[vertex_to_sibling[v1]], index] = 1
        adjacent_matrix[index, vertex_to_matrix_index[vertex_to_sibling[v2]]] = 1
        adjacent_matrix[vertex_to_matrix_index[vertex_to_sibling[v2]], index] = 1
    return adjacent_matrix


#初始化工作
srg = (9,4,1,2)
v = srg[0]
k = srg[1]
lbd = srg[2]
mu = srg[3]

#初始块数
block_count = v // ( 2 + lbd )

last_matched_vertex = {}
vertex_to_sibling = {}

pending_vertex = list(initial_vertex_clusters(block_count))
print(pending_vertex)
index = v // block_count
for vertex in pending_vertex:
    vertex_to_sibling[vertex] = (vertex[0], vertex[1], 0 if vertex[2] == 1
            else 1)
    last_matched_vertex[vertex] = (-1,-1,-1)
#print(vertex_to_sibling)

current_solution_stack= [((0,0,0),(1,0,0))] #第一对点可任意
pending_vertex.remove((0,0,0))
pending_vertex.remove((1,0,0))
while len(current_solution_stack) > 0:
    next_vertex_group = search_next_group_vertex()
    if next_vertex_group != None:
        #print("next_vertex_group is %s" % str(next_vertex_group))
        #print(last_matched_vertex[next_vertex_group[0]])
        #测试是否重复匹配，若重复，则需要继续退栈
        if last_matched_vertex[next_vertex_group[0]] == next_vertex_group[1]:
            #清除当前匹配点信息，以便继续匹配
            last_matched_vertex[next_vertex_group[0]] = (-1, -1, -1)
            #print(last_matched_vertex[next_vertex_group[0]])
            last_vertex_group = current_solution_stack.pop()
            pending_vertex.append(last_vertex_group[0])
            pending_vertex.append(last_vertex_group[1])
            pending_vertex.sort()
            #print("current pending vertex is %s" % str(pending_vertex))
            continue
        else:
            last_matched_vertex[next_vertex_group[0]] = next_vertex_group[1]
        current_solution_stack.append(next_vertex_group)
        pending_vertex.remove(next_vertex_group[0])
        pending_vertex.remove(next_vertex_group[1])
        #print(pending_vertex)
        if len(current_solution_stack) == 6:
            if test_solution():
                print("Congratulation, found a soultion!!!")
                #print(current_solution_stack)
                break
            else:
                last_vertex_group = current_solution_stack.pop()
                pending_vertex.append(last_vertex_group[0])
                pending_vertex.append(last_vertex_group[1])
                pending_vertex.sort()
        else:
            continue
    else:
        #print("can't find solution for vertex. now soutlion stack is %s" %
        #        str(current_solution_stack))
        last_vertex_group = current_solution_stack.pop()
        #print("last vertex group is %s" % str(last_vertex_group))
        pending_vertex.append(last_vertex_group[0])
        pending_vertex.append(last_vertex_group[1])
        pending_vertex.sort()
        #print("pending vertex group is %s" % str(pending_vertex))
if len(current_solution_stack) == 0:
    print("No soultion is found.")
else:
    adjancent_matrix = gen_adjacent_matrix()
    print("adjance_matrix is \n %s" % str(adjancent_matrix))
    print(lambda_compatible(adjancent_matrix))
    print(mu_compatible(adjancent_matrix))
    print(meets_adjacency_requirements(adjancent_matrix, debug=True))
    print(graph_is_valid(adjancent_matrix))
