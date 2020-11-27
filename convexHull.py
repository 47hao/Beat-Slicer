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
    #merge a couple times
    #for i in range(3):
        #faces = mergeFaces(faces,points)
    result = mergeFaces(mergeFaces(faces, points),points)
    print("merged faces:", result)
    return result

#completely self written code
def mergeFaces(inputFaces, points):
    faces = copy.deepcopy(inputFaces)
    result = []
    i = 0
    while i < len(faces):
        merged = False
        j=0
        while j < len(faces):
            if i != j and numsInCommon(faces[i], faces[j]) >= 2:
                #these faces are touching
                #find the plane of the first face:
                f1, f2 = faces[i], faces[j] #(2,1,0), indices of face coords
                p1, p2, p3 = points[f1[0]],points[f1[1]],points[f1[2]]
                (a,b,c,d) = slice3d.pointsToPlane(p1,p2,p3) #plane coeffs
                #find the odd point to check
                uniquePoints2 = pointsNotInCommon(f1,f2)
                (x,y,z) = points[uniquePoints2[0]]
                if(almostEqual(a*x+b*y+c*z, d)):
                    #face = reorderPoints(faces[i], points)
                    #find opposite edge
                    uniquePoints1 = pointsNotInCommon(f2,f1) 
                    #find the last unique point in  1:
                    lastUnique = uniquePoints1[len(uniquePoints1)-1]
                    lastUniqueIndex = f1.index(lastUnique) 
                    #skip 1 point, and it's safe to place new points:
                    placeIndex = (lastUniqueIndex+2)%(len(f1))
                    #SHOULD WE FLIP UNIQUEPOINTS?
                    #ONLY WORKS FOR UP TO HEXAGONS
                    if ( len(uniquePoints2) > 1 and 
                        dist(points[uniquePoints2[0]], points[lastUnique]) >
                        dist(points[uniquePoints2[1]], points[lastUnique]) ):
                        uniquePoints2.reverse()
                    addedFace = f1[:placeIndex] + uniquePoints2 + f1[placeIndex:]
                    result.append(addedFace)
                    merged = True
                    faces.remove(f1)
                    faces.remove(f2)
            j += 1
        if not(merged):
            result.append(faces.pop(i))
        #i += 1
    return result

def almostEqual(d1, d2):
    epsilon = 10**-5
    return (abs(d2 - d1) < epsilon)
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

def pointsNotInCommon(L1, L2):
    result = []
    for i in L2:
        if i not in L1:
            result.append(i)
    return result

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

    points = [(0, 0, 0), (1, 0, 0), (0,1,0), (1,1,0),
            [0, 0, 1], (1, 0, 1), (0, 1, 1), (1, 1, 1), ]
    print("lexiCube:", getHull(points))

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
