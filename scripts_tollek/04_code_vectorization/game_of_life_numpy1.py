#!/usr/bin/python3.6
from copy import copy, deepcopy
import numpy as np

Z = [[0,0,0,0,0,0],
     [0,0,0,0,0,0],
     [0,0,1,1,0,0],
     [0,1,0,1,0,0],
     [0,0,0,1,0,0],
     [0,0,0,0,0,0],
     [0,0,0,0,0,0]]
Z = [[0,0,0,0,0,0],
     [0,0,0,0,0,0],
     [0,0,1,0,0,0],
     [0,0,0,1,0,0],
     [0,1,1,1,0,0],
     [0,0,0,0,0,0],
     [0,0,0,0,0,0]]
Z = np.array(Z)

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
    # N is initialized with zeros of size Z
    N = np.zeros(Z.shape, dtype=int)
    # We take 8 subarrays (lef up corner, up, right up corner,
    #                      left,            , right   ) ...
    # and add all of them into counters of neighbors.
    # left_uper_corner = Z[ :-2, :-2] (everything from start to last -2 rows; remember about the "0" border)
    # up = Z[ :-2,1:-1] (all rows but last 2, all columns from 1 to -1; remember about the "0" border)
    N[1:-1,1:-1] += (Z[ :-2, :-2] + Z[ :-2,1:-1] + Z[ :-2,2:] +
                     Z[1:-1, :-2]                + Z[1:-1,2:] +
                     Z[2:  , :-2] + Z[2:  ,1:-1] + Z[2:  ,2:])
    return N

def iterate_book(Z):
    N = compute_neighbours(Z)
    # Flatten arrays
    N_ = N.ravel()
    Z_ = Z.ravel()

    # Apply rules
    R1 = np.argwhere( (Z_==1) & (N_ < 2) )
    R2 = np.argwhere( (Z_==1) & (N_ > 3) )
    R3 = np.argwhere( (Z_==1) & ((N_==2) | (N_==3)) )
    R4 = np.argwhere( (Z_==0) & (N_==3) )

    # Set new values
    Z_[R1] = 0
    Z_[R2] = 0
    Z_[R3] = Z_[R3]
    Z_[R4] = 1

    # Make sure borders stay null
    Z[0,:] = Z[-1,:] = Z[:,0] = Z[:,-1] = 0
    return Z


def iterate(Z):
    N = compute_neighbours(Z)
    # dying from loneliness
    R1 = np.argwhere( (Z == 1) & (N < 2))
    # dying from overcrowding
    R2 = np.argwhere( (Z == 1) & (N > 3))
    # # survives
    R3 = np.argwhere( (Z == 1) & ((N == 2) | (N == 3)))
    # # creates new cell
    R4 = np.argwhere( (Z == 0) & (N == 3))

    # simply updating by Z[R1] is invalid - it will update whole rows/cols
    # https://stackoverflow.com/questions/7761393/how-to-modify-a-2d-numpy-array-at-specific-locations-without-a-loop
    # print(rows, cols)
    Z[R1[:,0], R1[:,1]] = 0
    Z[R2[:,0], R2[:,1]] = 0
    Z[R3[:,0], R3[:,1]] = Z[R3[:,0], R3[:,1]]
    Z[R4[:,0], R4[:,1]] = 1

    # clean up the boundaries
    Z[0,:] = Z[-1,:] = Z[:,0] = Z[:,-1] = 0
    return Z



pretty = True
print ('init')
show(Z, pretty)
for i in range(4):
    print('-------------')
    print (i)
    Z = iterate(Z)
    show(Z, pretty)
