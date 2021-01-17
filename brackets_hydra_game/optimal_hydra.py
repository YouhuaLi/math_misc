def brackets_count(m, n, s):
    n = m - 1
    m = s + 2
    s += 1
    while n > 0:
        new_brackets_count = m * (2 * s + m + 1) // 2
        s += m
        m += new_brackets_count
        n -= 1
    return (m, s)

def optimal_hydra(i):
    s = 0
    m = 1
    n = 1
    while i - 1 > 0:
        (m, s) = brackets_count(m, n, s)
        i -= 1
    return s + m

i = 4
print(optimal_hydra(i))
