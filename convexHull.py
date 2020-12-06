import numpy as np
from scipy.spatial import ConvexHull
import slice3d
import copy

def get2dHull(points):
    pts = np.array(points)
    hull = ConvexHull(pts)
    return order2dFaces(np.ndarray.tolist(hull.simplices))

#self designed algorithm
def order2dFaces(sides):
    result = []
    i = 0
    prevSide = sides[0]
    prevPoint = prevSide[0]
    while i < len(sides):
        #add a point with each iteration of the while loop

        #find the matching index
        for j in range(len(sides)):
        #look for teh next matching index
            if prevPoint in sides[j] and sides[j] != prevSide:
                matchingSide = sides[j]
                break
        #prevPoint = 5
        #pick the point index that's not the one in common
        if matchingSide[0] == prevPoint:
            newPoint = matchingSide[1]
        else:
            newPoint = matchingSide[0]
        #newPoint = 6
        result.append(prevPoint)
        prevSide = matchingSide
        prevPoint = newPoint

        i += 1
    
    return result
        
def getHull(points):
    pts = np.array(points)

    #Source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.ConvexHull.html
    hull = ConvexHull(pts)
    volume = hull.volume
    faces = np.ndarray.tolist(hull.simplices)
    #merge a couple times for 5 and 6-sided shapes
    for i in range(2):
        try:
            faces = mergeFaces(faces,points)
        except:
            pass
    return faces, volume


#completely self written code
def mergeFaces(inputFaces, points):
    faces = copy.deepcopy(inputFaces)
    result = []
    i = 0
    while i < len(faces):
        merged = False #know whether to add the lone face at the end
        j = 0
        while j < len(faces): #check for merging with all other faces
            if i != j and numsInCommon(faces[i], faces[j]) >= 2:
                f1, f2 = faces[i], faces[j] #(2,1,0), indices of face coords
                p1, p2, p3 = points[f1[0]],points[f1[1]],points[f1[2]]
                (a,b,c,d) = slice3d.pointsToPlane(p1,p2,p3) #plane coeffs
                uniquePoints2 = pointsNotInCommon(f1,f2)
                (x,y,z) = points[uniquePoints2[0]]
                if(almostEqual(a*x+b*y+c*z, d)):
                    #decide order of insertion points
                    uniquePoints1 = pointsNotInCommon(f2,f1) 
                    lastUnique = uniquePoints1[len(uniquePoints1)-1]
                    if (len(uniquePoints2) > 1 and 
                        dist(points[uniquePoints2[0]], points[lastUnique]) >
                        dist(points[uniquePoints2[1]], points[lastUnique]) ):
                        uniquePoints2.reverse()
                    #find the spot for insertion
                    commonIndices = commonPointIndices(f1,f2)
                    if abs(commonIndices[0]-commonIndices[1]) == 1:
                        placeIndex = max(commonIndices[0],commonIndices[1])
                    else:
                        placeIndex = 0
                    #add merged face to result
                    addedFace = f1[:placeIndex] + uniquePoints2 + f1[placeIndex:]
                    result.append(addedFace)
                    merged = True
                    faces.remove(f1)
                    faces.remove(f2)
            j += 1
        if not(merged):
            result.append(faces.pop(i))
    return result

def almostEqual(d1, d2):
    epsilon = 10**-5
    return (abs(d2 - d1) < epsilon)

def dist(point1, point2):
    (x,y,z) = point1
    (x1,y1,z1) = point2
    return ((x1-x)**2+(y1-y)**2+(z1-z)**2)**0.5

def commonPointIndices(L1, L2):
    result = []
    for i in range(len(L1)):
        if L1[i] in L2:
            result.append(i)
    if len(result) > 2:
        raise Exception("Adjacent polygons should never have >2 common points")
    return result

#points cannot be repeated within a face, so this code is ok
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
def test2d():
    shape = [(0,0),(2,1),(1,2),(-1,2),(3,-1),(2,5),(5,2)]
    print(get2dHull(shape))

#test2d()