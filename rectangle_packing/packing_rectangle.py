from fractions import Fraction
from sortedcontainers import SortedList

#fit (1/(i+1) , 1/i) into a box. adjust linked list of boxes 
def adjust_boxes(i):
    global current_box_index, boxes
    used_box = boxes[current_box_index]
	# Algorithm step a6. pefect fit both edges. just remove current box
    if used_box[0] == Fraction(1, i+1) and used_box[1] == Fraction(1, i):
        if current_box_index > 0: #try set current box to a smaller one
            current_box_index -= 1
        elif current_box_index != len(boxes): #try set current box to a bigger one
            current_box_index += 1
        else:
            #used out boxes which should not happen. failing
            return False
    #Algorithm step a6, Fig. 6. pefect fit on width.
    elif used_box[0] == Fraction(1, i+1):
        new_edge = used_box[1] - Fraction(1, i)
        if new_edge >= Fraction(1, min_box_width_denominator + 1):
            if new_edge < used_box[0]:
                new_box = (new_edge, used_box[0])
            else:
                new_box = (used_box[0], new_edge)
            boxes.add(new_box) #new box of P_i in fig. 6
    #Algorithm step a13. pefect fit on length.
    elif used_box[0] == Fraction(1, i):
        new_edge = used_box[1] - Fraction(1, i+1)
        if new_edge >= Fraction(1, min_box_width_denominator + 1):
            if new_edge < used_box[0]:
                new_box = (new_edge, used_box[0])
            else:
                new_box = (used_box[0], new_edge)
            boxes.add(new_box)
    #Algorithm step a17. Fig. 7
    elif used_box[0] > Fraction(1, i):
        new_edge = used_box[0] - Fraction(1, i)
        if new_edge >= Fraction(1, min_box_width_denominator + 1): 
            if new_edge < Fraction(1, i+1):
                new_box = (new_edge, Fraction(1, i+1))
            else:
                new_box = (Fraction(1, i+1), new_edge)
            boxes.add(new_box) #new box of C_i in fig. 7
        
        new_edge = used_box[1] - Fraction(1, i + 1)
        if new_edge >= Fraction(1, min_box_width_denominator + 1): 
            if used_box[0] < new_edge:
                new_box = (used_box[0] , new_edge)
            else:
                new_box = (new_edge, used_box[0])
            boxes.add(new_box) #new box of D_i in fig. 7
    #Algorithm step a21. Fig. 8
    else:
        new_edge = used_box[0] - Fraction(1, i+1)
        if new_edge >= Fraction(1, min_box_width_denominator + 1): 
            if new_edge < Fraction(1, i):
                new_box = (new_edge, Fraction(1, i))
            else:
                new_box = (Fraction(1, i), new_edge)
            boxes.add(new_box) #new box of C_i in fig. 8
        
        new_edge = used_box[1] - Fraction(1, i)
        if new_edge >= Fraction(1, min_box_width_denominator + 1): 
            if used_box[0] < new_edge:
                new_box = (used_box[0] , new_edge)
            else:
                new_box = (new_edge, used_box[0])
            boxes.add(new_box) #new box of D_i in fig. 8
    
    boxes.remove(used_box)

    return True

#packing 1/(i+1) * 1/i into the box
def packing_into_box(i):
    global current_box_index, boxes
    #print("i=" , i)
    #print("current_box_index=", current_box_index)
    # if current box is big enough, find a smallest box that can fit (1/(i+1) , 1/i)
    if boxes[current_box_index][0] >=  Fraction(1, i+1) and boxes[current_box_index][1] >= Fraction(1, i):
        while current_box_index != 0 and boxes[current_box_index - 1][0] >= Fraction(1, i+1) and boxes[current_box_index - 1][1] >= Fraction(1, i):
            current_box_index -= 1
            #print("move to bigger one")
        #print("found box for use: ", boxes[current_box_index])
    #if current box is too small, find the first bigger box can fit. otherwise, failing.
    else:
        boxes_count = len(boxes)
        current_box_index += 1
        while current_box_index < boxes_count and not (boxes[current_box_index][0] >= Fraction(1, i+1) and boxes[current_box_index][1] >= Fraction(1, i)) :
            current_box_index += 1
        if current_box_index == boxes_count:
            return False #failed to find a box. Failing.
        else:
            pass
            #print("found box for use: ", boxes[current_box_index])

    return adjust_boxes(i)

'''
boxes is a sorted list of avaiable boxes to be filled. 
element is a tuple of (width, length) while width < length.
in the beginning, start with a (1/2, 1) box, and a rectangle of (1/2, 1) is already filled in.
'''

boxes = SortedList()
boxes.add((Fraction(1, 2),  Fraction(1, 1)))

current_box_index = 0
min_box_width_denominator = 10 ** 9
total_rectangles = 10 ** 6


for i in range(2, total_rectangles + 1):
    packing_result = packing_into_box(i)
    if packing_result == False:
        break

if packing_result:
    print("successful to pack rectagle (1 / %d, 1 / %d)" % (i + 1, i))
    print("remaining boxes size (width > 1 / %d) is: %d" % (min_box_width_denominator + 1, len(boxes)))
    print("the lagest 5 remaining boxes are:")
    for box in boxes[-5:]:
        print(box, (box[0].numerator / box[0].denominator), " X ", (box[1].numerator / box[1].denominator))
else:
    print("failed to pack rectagle (1 / %d, 1 / %d)" % (i+1, i))

# size = 0
# for j in range(2, i + 1 ):
#     size += (1 / (j + 1)) * (1 / j)
# for box in boxes:
#     box_size = box[0] * box[1]
#     size += box_size.numerator / box_size.denominator
# print(size)
