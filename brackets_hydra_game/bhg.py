import re

def next_step(brackets_hydra, step_count):
    (new_brackets_hydra, right_parent_bracket_index) = remove_right_most_brackets(brackets_hydra)
    if right_parent_bracket_index != len(new_brackets_hydra) - 1:
        new_brackets_hydra = regrow_brackets_hydra(new_brackets_hydra, right_parent_bracket_index, step_count)
    return new_brackets_hydra

def regrow_brackets_hydra(brackets_hydra, right_parent_bracket_index, step_count):
    left_parent_bracket_index = left_bracket_search(brackets_hydra[0:right_parent_bracket_index])
    regrow_part = brackets_hydra[right_parent_bracket_index-left_parent_bracket_index-1:
                                 right_parent_bracket_index+1] 
    regrow_part = regrow_part * step_count
    new_brackets_hydra = brackets_hydra[:right_parent_bracket_index+1] \
                         + regrow_part \
                         + brackets_hydra[right_parent_bracket_index+1:]
    return new_brackets_hydra

def left_bracket_search(s):
    stack = []
    for i, c in enumerate(reversed(s)):
	    if c == ')':
		    stack.append(i)
	    if c == '(':
		    if len(stack) == 0:
			    #print(i)
			    return i
		    else:
		        stack.pop()

# return (new hydra string, the right parent ')' index'
def remove_right_most_brackets(brackets_hydra):
    regex = r"(\(\))"
    matches = re.finditer(regex, brackets_hydra)
    last_match = list(matches)[-1]
    start_pos=last_match.span()[0]
    return (brackets_hydra[:start_pos] + brackets_hydra[start_pos+2:], start_pos)

hydra = "(((())))"
print("start hydra is: " + hydra)
step = 1
while(step < 101 and len(hydra) > 2 ):
    hydra  = next_step(hydra, step)
    print("step %d: %s" % (step, hydra))
    step = step + 1