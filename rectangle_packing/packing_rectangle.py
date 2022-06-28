from fractions import Fraction
from blist import sortedlist

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
        if used_box[1] - Fraction(1, i) < used_box[0]:
            new_box = (used_box[1] - Fraction(1, i), used_box[0])
        else:
        	new_box = (used_box[0], used_box[1] - Fraction(1, i))
        boxes.add(new_box) #new box of P_i in fig. 6
        #current_box_index -= 1 #should always be successful beacuse we just add a smaller box before this step.
    #Algorithm step a13. pefect fit on length.
    elif used_box[0] == Fraction(1, i):
        if used_box[1] - Fraction(1, i+1) < used_box[0]:
            new_box = (used_box[1] - Fraction(1, i+1), used_box[0])
        else:
        	new_box = (used_box[0], used_box[1] - Fraction(1, i+1))
        boxes.add(new_box)
        #current_box_index -= 1 #should always be successful beacuse we just add a smaller box before this step.
    #Algorithm step a17. Fig. 7
    elif used_box[0] > Fraction(1, i):
        if used_box[0] - Fraction(1, i) < Fraction(1, i+1):
            new_box = (used_box[0] - Fraction(1, i), Fraction(1, i+1))
        else:
            new_box = (Fraction(1, i+1), used_box[0] - Fraction(1, i))
        #print("adding new box1: ", new_box)
        boxes.add(new_box) #new box of C_i in fig. 7
        if used_box[0] < used_box[1] - Fraction(1, i+1):
            new_box = (used_box[0] , used_box[1] - Fraction(1, i+1))
        else:
            new_box = (used_box[1] - Fraction(1, i+1), used_box[0])
        #print("adding new box2: ", new_box)
        boxes.add(new_box) #new box of D_i in fig. 7
        #current_box_index -= 1 #should always be successful beacuse we just add two smaller boxes before this step.
    #Algorithm step a21. Fig. 8
    else:
        if used_box[0] - Fraction(1, i+1) < Fraction(1, i):
            new_box = (used_box[0] - Fraction(1, i+1), Fraction(1, i))
        else:
            new_box = (Fraction(1, i), used_box[0] - Fraction(1, i+1))
        #print("adding new box: ", new_box)
        boxes.add(new_box) #new box of C_i in fig. 8
        if used_box[0] < used_box[1] - Fraction(1, i):
            new_box = (used_box[0] , used_box[1] - Fraction(1, i))
        else:
            new_box = (used_box[1] - Fraction(1, i), used_box[0])
        #print("adding new box: ", new_box)
        boxes.add(new_box) #new box of D_i in fig. 8
        current_box_index -= 1 #should always be successful beacuse we just add two smaller boxes before this step.
    
    #print("current boxes list BEFORE delete is:", boxes)
    #print("the box", boxes[current_box_index],  " is used by rectangle (1/%d, 1/%d) and being deleted." \
    #     % (i+1, i))
    #print("old box is: " , old_box.data)
    boxes.remove(used_box)
    #print("current boxes list AFTER delete is:", boxes)
    #print("\n")

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

    if adjust_boxes(i) == False:
        return False
    else:
        return True

'''
boxes is a sorted list of avaiable boxes to be filled. 
element is a tuple of (width, length) while width < length.
in the beginning, start with a (1/2, 1) box, and a rectangle of (1/2, 1) is already filled in.
'''

boxes = sortedlist()
boxes.add((Fraction(1, 2),  Fraction(1, 1)))

current_box_index = 0

for i in range(2, 10 ** 6 + 1):
	packing_result = packing_into_box(i)
	if (packing_result == False):
		break

if packing_result:
	print("success to fill till rectagle (1 / %d, 1 / %d)" % (i+1, i))
else:
	print("failed")