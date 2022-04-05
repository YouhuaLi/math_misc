#!python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import scipy.integrate


def prime_list(n):
    prime_numbers=[2]
    for num in range(3,n,2):
        if all(num%i!=0 for i in range(3,int(math.sqrt(num))+1, 2)):
            prime_numbers.append(num)
    return prime_numbers

def li(n):
    f=lambda x:1/np.log(x)
    return scipy.integrate.quad(f, 2, n)[0]


def pi(x):
    #prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]
    prime = prime_list(2000)
    assert x <= prime[-1]
    i = 0
    while prime[i] < x:
            i += 1
    return i

x = np.arange(5, 1000, 0.1)

y = x / np.log(x) # Natural log
z = x / (np.log(x)-1.08366) # Natural log
g = [li(i) for i in x]
p = [pi(i) for i in x]

plt.plot(x, g, label='$Li(x)$', color='green')
plt.plot(x, y, label='$x / \ln(x)$', color='red')
plt.plot(x, z, label='$x / (\ln(x)-1.08366)$', color='blue')
plt.plot(x, p, label='$\pi(x)$', color='black')

plt.legend(loc='upper left')
plt.xlim([0, 1000])
plt.ylim([0, 200])

plt.show()
