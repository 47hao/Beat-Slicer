import numpy as np
from scipy.spatial import ConvexHull
import slice3d
import copy

#does it matter if this takes global points? prolly not?
#Source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.ConvexHull.html
def getHull(points):
    pts = np.array(points)
    hull = ConvexHull(pts)
    faces = np.ndarray.tolist(hull.simplices)
    print("faces merged:", mergeFaces(faces, points))
    return mergeFaces(faces, points)

#completely self written code
def mergeFaces(faces, points):
    result = []
    i = 0
    while i < len(faces):
        if i >= len(faces)-1:
            result.append(faces[i])
        elif numsInCommon(faces[i], faces[i+1]) == 2:
            #could be coplanar, do the check
            f = faces[i] #(2,1,0) or some triplet of indices
            p1, p2, p3 = points[f[0]],points[f[1]],points[f[2]]
            (a,b,c,d) = slice3d.pointsToPlane(p1,p2,p3) #plane coeffs
            #find the odd point to check
            uniquePoint2 = oddNumOut(faces[i],faces[i+1])
            (x,y,z) = points[uniquePoint2]
            if(a*x+b*y+c*z == d):
                #face = reorderPoints(faces[i], points)
                #find opposite edge
                uniquePoint1 = oddNumOut(faces[i+1],faces[i]) 
                oppositePointIndex = faces[i].index(uniquePoint1)
                placeIndex = (oppositePointIndex+2)%(len(faces[i]))
                addedFace = copy.copy(faces[i])
                addedFace.insert(placeIndex,uniquePoint2)
                result.append(addedFace)
                i += 1 #extra hop for the second face merged
            else:
                result.append(faces[i])
        else:
            #cannot be coplanar, no two shared points
            result.append(faces[i])
        i += 1
    return result

#input: set of points
#- find the plane they're on
#- project them onto plane
#output: indices of clockwise order
def reorderPoints(face, points):
    (i1, i2, i3) = face #indices of points
    if dist(points[i1],points[i2]) > dist(points[i1],points[i3]):
        return [i1, i3, i2]
    return face

def dist(point1, point2):
    (x,y,z) = point1
    (x1,y1,z1) = point2
    return ((x1-x)**2+(y1-y)**2+(z1-z)**2)**0.5

#points cannot be repeated within a face, so this is ok
def numsInCommon(L1, L2):
    num = 0
    for i in L1:
        if i in L2:
            num += 1
    return num

def oddNumOut(L1, L2):
    for i in L2:
        if i not in L1:
            return i
    return None

def testMerge():
    points = [(0, 0, 0), (1, 0, 0), [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, .5, 1], [0, .5, 1], ]
    hull = getHull(points)
    print("hull:", hull)
    print("merged:", mergeFaces(hull, points))

    points = [(0, 0, 0), (1, 0, 0), [1,1,0],[0, 1, 0],
            [0, 0, 1],[0,1,1]]
    hull = getHull(points)
    print("hull:", hull)
    print("merged:", mergeFaces(hull, points))

def testHull():
    points = [(0, 0, 0), (1, 0, 0), [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1], ]
    print("cube:", getHull(points))

    points = [(0, 0, 0), (1, 0, 0), [1, 0.5, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, .5, 1], [0, 1, 1], ]
    print("trap. prism:", getHull(points))

    '''
    points = [(0, 0, 0), (1, 0, 0), [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1], ]
    print("trap. prism:", getHull(points))
    '''
    
    points = [(0, 0, 0), (1, 0, 0), [0, 1, 0],
            [0, 0, 1]]
    print("tetra:", getHull(points))

    points = [(0, 0, 0), (1, 0, 0), [1,1,0],[0, 1, 0],
            [0, 0, 1],[0,1,1]]
    print("triPrism:", getHull(points))
#testHull()

def testHelpers():
    print("testing numsInCommon...", end="")
    A = [1,2,3]
    B = [3,1,2]
    assert(numsInCommon(A,B) == 3)
    A = [1,2,3]
    B = [5,1,2]
    assert(numsInCommon(A,B) == 2)
    A = [0,2,3]
    B = [5,1,2]
    assert(numsInCommon(A,B) == 1)
    A = [0,7,3]
    B = [5,1,2]
    assert(numsInCommon(A,B) == 0)
    print("passed!")
    print("testing oddNumOut...", end="")
    A = [1,2,3]
    B = [1,2,4]
    assert(oddNumOut(A,B) == 4)
    A = [1,7,3]
    B = [3,5,1]
    assert(oddNumOut(A,B) == 5)
    print("passed!")
#testHelpers()
