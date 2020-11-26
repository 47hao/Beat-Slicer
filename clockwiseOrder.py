import math
from cmu_112_graphics import *
from centroid import find_Centroid

def clockwiseOrder(L):
    clockwiseL = list()
    cx,cy = find_Centroid(L)
    part1,part2 = 0,0
    sec1 = dict()
    sec2 = dict()
    L.sort()
    negative = False
    for k in range(len(L)):
        '''part1-end: dotx < cx;
        0-part1: dotx > cx; part3: dotx = cx doty > cy'''
        if ((L[k][0] < 0) or (L[k][1] < 0)):
            negative = True
        if (L[k][0] > cx) and (L[k][1] < cy) and (part1 == 0):
            part1 = k
        if (L[k][0] == cx) and (L[k][1] > cy):
            part2 = k
        if ((L[k][0] == cx) and (L[k][1] < cy)):
            clockwiseL.append(L[k])
    if negative:
        part1 -= 1
    for x,y in L[part1:]:
        k = (y-cy)/(x-cx)
        sec1[k] = (x,y)
    for key in sorted(sec1):
        clockwiseL.append(sec1[key])
    if (part2 != 0):
        clockwiseL.append(L[part2])
    for x,y in L[:part1]:
        k = (y-cy)/(x-cx)
        sec2[k] = (x,y)
    for key in sorted(sec2):
        clockwiseL.append(sec2[key])

    return clockwiseL


""" polygonList1 = [(50,50),(50,100),(100,100),(100,50)]
polygonList2 = [(1.5,5),(1,1),(2.5,4),(3,1),(2,0)]
polygonList3 = [(1,1),(5,6),(2,4),(1.5,2),(2,0),(3,0),(5,2),(5.5,4),(6,5)]
polygonList4 = [(1,0),(1,-1),(-0.5,2),(0.5,4),(1.5,5),(3,3),(2,1)]
print(clockwiseOrder(polygonList1))
print(clockwiseOrder(polygonList2))
print(clockwiseOrder(polygonList3))
print(clockwiseOrder(polygonList4)) """
