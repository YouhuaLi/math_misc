def step(k, n, m):
    if n == 0:
        return k + m
    return step(k+m, n-1, (2*k+m+3)*m // 2)

print(step(5,15,1))
