#!/usr/bin/python3.6
from copy import copy, deepcopy

Z = [[0,0,0,0,0,0],
     [0,0,0,0,0,0],
     [0,0,1,1,0,0],
     [0,1,0,1,0,0],
     [0,0,0,1,0,0],
     [0,0,0,0,0,0],
     [0,0,0,0,0,0]]

def show(Z, pretty = False):
    if pretty:
        for row in Z[1:-1]:
            s = ' '.join([str(x) for x in row[1:-1]])
            s = s.replace('0', ' ').replace('1', '*')
            print(s)
    else:
        for row in Z[1:-1]:
            print(row[1:-1])
    print

def compute_neighbours(Z):
    shape = len(Z), len(Z[0])
    ngbs = [[0]*shape[1] for _ in range(shape[0])]
    for y in range(1,shape[0]-1):
        for x in range(1,shape[1]-1):
            t = -Z[y][x]  # simple trick to avoid special handling of "self" - calculate it in loop and subtract
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    t += Z[y + dy][x + dx]
            ngbs[y][x] = t
    return ngbs

def iterate(Z):
    shape = len(Z), len(Z[0])
    ngbs = compute_neighbours(Z)
    N = deepcopy(Z)
    for y in range(1,shape[0]-1):
        for x in range(1,shape[1]-1):
            if N[y][x] == 1 and (ngbs[y][x] < 2 or ngbs[y][x] > 3):
                N[y][x] = 0
            elif N[y][x] == 0 and ngbs[y][x] == 3:
                N[y][x] = 1
    return N

pretty = True
print ('init')
show(Z, pretty)
for i in range(4):
    print (i)
    Z = iterate(Z)
    show(Z, pretty)
