from fractions import Fraction
from sortedcontainers import SortedList

#fit (1/(i+1) , 1/i) into a box. adjust linked list of boxes 
def adjust_boxes(i):
    global current_box_index, boxes
    used_box = boxes.pop(current_box_index)
	# Algorithm step a6. pefect fit both edges. just remove current box
    if used_box[0] == Fraction(1, i+1) and used_box[1] == Fraction(1, i):
        pass
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
            #print("adding new box1: ", new_box)
            boxes.add(new_box) #new box of C_i in fig. 7
        new_edge = used_box[1] - Fraction(1, i + 1)
        if new_edge >= Fraction(1, min_box_width_denominator + 1):
            if used_box[0] < new_edge:
                new_box = (used_box[0] , new_edge)
            else:
                new_box = (new_edge, used_box[0])
            #print("adding new box2: ", new_box)
            boxes.add(new_box) #new box of D_i in fig. 7
    #Algorithm step a21. Fig. 8
    else:
        new_edge = used_box[0] - Fraction(1, i+1)
        if new_edge >= Fraction(1, min_box_width_denominator + 1):
            if new_edge < Fraction(1, i):
                new_box = (new_edge, Fraction(1, i))
            else:
                new_box = (Fraction(1, i), new_edge)
            #print("adding new box: ", new_box)
            boxes.add(new_box) #new box of C_i in fig. 8
        new_edge = used_box[1] - Fraction(1, i)
        if new_edge >= Fraction(1, min_box_width_denominator + 1):
            if used_box[0] < new_edge:
                new_box = (used_box[0] , new_edge)
            else:
                new_box = (new_edge, used_box[0])
            #print("adding new box: ", new_box)
            boxes.add(new_box) #new box of D_i in fig. 8

    return True

#packing 1/(i+1) * 1/i into the box
def packing_into_box(i):
    global current_box_index, boxes
    current_box_index = boxes.bisect_left((Fraction(1, i + 1),Fraction(1, i)))
    #print(boxes)
    #print(current_box_index)
    if current_box_index == len(boxes):
        # print((Fraction(1, i + 1),Fraction(1, i)))
        # print("unable to find a enough big box.")
        # print("largest box is:", boxes[-1])
        return False #unable to find a bigger enough box

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
total_rectangles = 10 ** 5


for i in range(2, total_rectangles + 1):
    packing_result = packing_into_box(i)
    if packing_result == False:
        break

if packing_result:
    print("successful to pack rectagle (1 / %d, 1 / %d)" % (i+1, i))
    print("remaining boxes size (width > 1 / %d) is: %d" % (min_box_width_denominator + 1, len(boxes)))
    print("the lagest 5 remaining boxes are:")
    for box in boxes[-5:]:
        print(box, (box[0].numerator / box[0].denominator), " X ", (box[1].numerator / box[1].denominator))
else:
    print("failed to pack rectagle (1 / %d, 1 / %d)" % (i+1, i))
    size = 0
    for j in range(2, i):
        size += (1 / (j + 1)) * (1 / j)
    for box in boxes:
        box_size = box[0] * box[1]
        size += box_size.numerator / box_size.denominator
    print(size)

