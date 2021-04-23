import sys
import numpy

def gen_adjacent_matrix(v, edges):
    adjacent_matrix = numpy.empty((v,v),dtype='int')
    for i in range(v):
        for j in range(v):
            adjacent_matrix[i,j] = 0
    row = 0
    column = 1
    for e in edges:
        if int(e) > 0:
            adjacent_matrix[row,column] = 1
            adjacent_matrix[column,row] = 1
        column += 1
        if column == v:
            row += 1
            column = row + 1
    return adjacent_matrix

def gen_sage_code(v, edges):
    l = []
    row = 0
    column = 1
    for e in edges:
      if int(e) > 0:
          l.append((row,column))
      column += 1
      if column == v:
          row += 1
          column = row + 1
    s = "G = Graph(%s)\n" % str(l)
    s += "G.is_strongly_regular()\n"
    s += "#G.plot()"
    return s

#total vertex count
v = int(sys.argv[1])
result = sys.argv[2]
#result = "v 1 2 3 -4 -5 -6 -7 8 9 -10 11 12 13 14 -15 0" #6 3 0 3 

edge_list = result.split(" ")[1:-1] #remove the beginning 'v' and the end 0
if len(edge_list) != (v * (v - 1) / 2):
    print("result not match vertex count.")
    sys.exit(1)

matrix =  gen_adjacent_matrix(v, edge_list)
print(matrix)

print(gen_sage_code(v, edge_list))
