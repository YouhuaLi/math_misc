def two_to_one(c, r, n):
    return c * n + r - n

bibd = []
d = 0
n = 7

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

for day in bibd:
    print(day)
