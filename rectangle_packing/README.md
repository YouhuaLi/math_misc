# Introduction

a python2 script to implment the algorithm described [here](https://www.sciencedirect.com/science/article/abs/pii/S0012365X1830178X) (On packing of rectangles in a rectangle).


It is known that . In 1968, Meir and Moser (1968) asked for finding the smallest  such that all the rectangles of sizes (1/i, 1/(i+1)) , can be packed into a square or a rectangle of area 1+e.

Referenced Paper:

https://www.sciencedirect.com/science/article/abs/pii/S0012365X1830178X

# Usage
## dependency

This script depends on blist module: https://github.com/DanielStutzbach/blist

I failed to install the blist module with python 3, so I can only run the script with python 2. If you can make blist works with python 3, then you can run the script with python 3.

## run exmaple:
```
time python2 packing_rectangle.py
success to fill till rectagle (1 / 100001, 1 / 100000)

real	1m34.984s
user	1m19.362s
sys	0m2.666s
```
