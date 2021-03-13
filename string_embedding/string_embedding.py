import itertools
# return True if a can be embedding to b
def test_string_embedding(a, b):
    s_a = str(a)
    s_b = str(b)
    l = len(s_a)
    if l > len(s_b):
        return False
    index_a = 0
    while index_a < l:
        current_a_character = s_a[index_a]
        last_sucessfull = False
        for current_b_character in s_b:
            if current_a_character <= current_b_character:
                last_sucessfull = True
                pos = s_b.index(current_b_character)
                s_b = s_b[(pos+1):]
                #print("new b is %s" % s_b)
                index_a += 1
                break
        if last_sucessfull == False:
            return False
    return True

def search_candidate(seq, candidates_num, digits):
    candidate_seq = itertools.product(candidates_num, repeat=digits)
    for item in candidate_seq:
        item = "".join(item)
        #print("current candidate is %s" % item)
        result = False
        for s in seq:
            result = test_string_embedding(s, item)
            if result:
                # s can embdding in item
                break
        if result == False:
            return item
    return "0"

# generate an non-embedding-sequence with n characters
def gen_embedding_sequence(n):
    step = 3
    seq = [33]
    digits = step
    while digits > 0:
        candidates_num = list("321")
        candidate = search_candidate(seq, candidates_num, digits)
        if candidate != "0":
            seq.append(candidate)
            print("current seq is %s" % str(seq))
            step += 1
            digits = min(step, 48)
            continue
        else:
            digits -= 1
    return seq

#print(smallest_digits(5613123144, 4))
#print(test_string_embedding(211,11211))
print(gen_embedding_sequence(2))
