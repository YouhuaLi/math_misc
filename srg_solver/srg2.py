import itertools,numpy
import sys
sys.path.insert(0, '/Users/yli/code/conway99')
from conway99 import *
import numpy as np

def v1_gt_v2(v1, v2): #return true if v1>v2
    if v1[0] > v2[0] or \
       v1[0] == v2[0] and v1[1] > v2[1] or \
       v1[0] == v2[0] and v1[1] == v2[1] and v1[2] == v2[2]:
        return True
    else:
        return False

def max_vertex(sorted_vertex_list): # return max vetex among a sorted list
    if sorted_vertex_list:
        return sorted_vertex_list[-1]
    else:
        return (-1, 0, 0)


def get_blocks_index_list(vertex_list): # return a list of vertex's block index, no duplication
    l = []

    for v in vertex_list:
        if v[0] not in l:
            l.append(v[0])
    return l

def get_next_child_vertex(pre_child):
    vertex = None
    q = len(solution_stack) % 2

    if q != 0:
        last_vertex_group = solution_stack[ -1 * q :]
    else:
        last_vertex_group = []

    #print("last_vertex_group is %s" % str(last_vertex_group))
    used_group_index = get_blocks_index_list(last_vertex_group)
    #print("used_group_index is %s" % str(used_group_index))

    for v in avaiable_vertex:
        if v[0] not in used_group_index and v1_gt_v2(v, pre_child):
            vertex = v
            break
    return vertex

def get_next_sibling_vertex():
    vertex = None
    q = len(solution_stack) % 2
    if q != 0:
        last_vertex_group = solution_stack[ -1 * q:]
    else:
        last_vertex_group = []

    #print("last_vertex_group is %s" % str(last_vertex_group))
    current_max_vertex = max_vertex(sorted(last_vertex_group))
    #print("current_max_vertex is %s" % str(current_max_vertex))

    for v in avaiable_vertex:
        if v1_gt_v2(v, solution_stack[-1]) and v1_gt_v2(v, current_max_vertex):
            vertex = v
            break
    return vertex

blocks ={}
avaiable_vertex = []
for i in range(3):
    blocks[i]=list(itertools.product([i], range(2), range(2)))

for block in blocks:
    for vertex in blocks[block]:
        avaiable_vertex.append(vertex)

#print(avaiable_vertex)

solution_stack = [(0,0,0), (2,1,1)]

for vertex in solution_stack:
    avaiable_vertex.remove(vertex)


search_sibling = False
while True:
    pre_vertex = (-1, 0, 0)
    #print("solution_stack is %s" % str(solution_stack))
    #print("avaiable_vertex is %s" % str(avaiable_vertex))
    #print("search_sibling is %s" % search_sibling)
    if len(avaiable_vertex) == 0: #no more vertex to test. solution is ready \
        #for test
        print("solution is ready for test %s" % solution_stack)
        pre_vertex = solution_stack.pop()
        avaiable_vertex.append(pre_vertex)
        avaiable_vertex.sort()
        search_sibling = True
        #break
        continue
    else:
        if len(solution_stack) < 2: #searching finished
            print("finished searching and no soltion was found.")
            break
        if search_sibling: # need search sibling
            next_vertex = get_next_sibling_vertex()
        else: # need to search child
            next_vertex = get_next_child_vertex(pre_vertex)

        if next_vertex == None: #can't find new vertex, back one level
            pre_vertex = solution_stack.pop()
            avaiable_vertex.append(pre_vertex)
            avaiable_vertex.sort()
            #print(solution_stack[-1])
            #print(avaiable_vertex[-1])
            search_sibling = True
        else:
            if search_sibling:
                avaiable_vertex.append(solution_stack.pop()) #search sibling, pop current last vetex
            solution_stack.append(next_vertex)
            avaiable_vertex.remove(next_vertex)
            avaiable_vertex.sort()
            search_sibling = False
