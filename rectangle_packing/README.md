# Introduction

a python2 script to implment the algorithm described [here](https://www.sciencedirect.com/science/article/abs/pii/S0012365X1830178X) (On packing of rectangles in a rectangle).


It is known that . In 1968, Meir and Moser (1968) asked for finding the smallest  such that all the rectangles of sizes (1/i, 1/(i+1)) , can be packed into a square or a rectangle of area 1+e.

Referenced Paper:

https://www.sciencedirect.com/science/article/abs/pii/S0012365X1830178X

# Usage
## dependency

This script depends on sortedcontainers module: https://grantjenks.com/docs/sortedcontainers

Tested sucessfully with python3

## run exmaple:
```
time python packing_rectangle.py

success to fill till rectagle (1 / 100001, 1 / 100000)

real	0m3.628s
user	0m3.115s
sys	0m0.079s
```
