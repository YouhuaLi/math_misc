#usage: gen_2_list.py <y_order>
#example:
#python3 gen_list.py 5
#(3, 2, 5, 4)

import sys
import itertools

#test list is good when sum n numbers
def test_list(l, n):
    mod_dict = {}
    i = 0
    length = len(l)
    while i+n <= length:
        mod = sum_list_n(l, i, n) % (length + 2)
        if mod == 0 or mod == n  or mod in mod_dict:
            return False
        else:
            mod_dict[mod]=True
        i = i + 1
    return True

#sum list from index start and n number
def sum_list_n(l, start, n):
    sub_list = l[start:start+n]
    return sum(sub_list)


size = int(sys.argv[1])
permutation=itertools.permutations(range(2, size+1))

for l in permutation:
    n = 2
    result = True
    while n < len(l):
        result = result and test_list(l, n)
        if result == False:
            break
        n = n + 1
    if result:
        print(l)
        #注释下一行以获得所有解
        break
