import itertools

def two_to_one(c, r, n):
    return c * n + r - n

def verify_day(day, n):
    all_person = []
    for group in day:
        all_person += group
    all_person = list(set(all_person))
    if len(all_person) != (n * n):
        print("duplicate walk today!")

def verify(bibd, n):
    pairs = {}
    for day in bibd:
        print(day)
        verify_day(day, n)
        for group in day:
            for pair in itertools.combinations(group, 2):
                if pair not in pairs:
                    pairs[pair] = 1
                else:
                    print("dubplicated pair of " + str(pair))
    if len(pairs) != n * n * (n * n - 1) / 2:
        print("pairs count is wrong!")

bibd = []
d = 0
n = 3

groups = []
i = 1
while i <= n:
    a = []
    j = 1
    while j <= n:
        a.append(two_to_one(i, j, n))
        j += 1
    groups.append(a)
    i += 1
bibd.append(groups)

groups = []
while d < n:
    groups=[]
    i = 1
    while i <= n:
        a = []
        j = 1
        while j <= n:
            a.append(two_to_one(j, (i + (j - 1) * d - 1) % n + 1, n))
            j += 1
        groups.append(a)
        i += 1
    bibd.append(groups)
    d += 1

verify(bibd, n)
