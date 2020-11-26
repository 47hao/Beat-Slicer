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
    for i in range(3):
        faces = mergeFaces(faces,points)
    result = mergeFaces(mergeFaces(faces, points),points)
    print("merged faces:", result)
    return faces

#completely self written code
def mergeFaces(faces, points):
    result = []
    '''
    i = 0
    while i < len(faces):
        if i >= len(faces)-1:
            result.append(faces[i])
        #only bother checking if there's shared edge
        elif countNumsInCommon(faces[i], faces[i+1]) >= 2:
            #MERGE QUADRILATERALS?
            f = faces[i] #(2,1,0) or some triplet of indices
            p1, p2, p3 = points[f[0]],points[f[1]],points[f[2]]
            (a,b,c,d) = slice3d.pointsToPlane(p1,p2,p3) #plane coeffs
            #find the odd point to check

            #check if coplanar:
            uniquePoints2 = pointsNotInCommon(faces[i],faces[i+1])
            (x,y,z) = points[uniquePoints2[0]]
            if(almostEqual(a*x+b*y+c*z, d)):
                #face = reorderPoints(faces[i], points)
                #find opposite edge
                uniquePoints1 = pointsNotInCommon(faces[i+1],faces[i]) 
                lastUniqueIndex1 = faces[i].index(uniquePoints1[len(uniquePoints1)-1])#index of last unique point
                placeIndex = (lastUniqueIndex1+2)%(len(faces[i]))
                resultFace = faces[i][0:placeIndex] + uniquePoints2 + faces[i][placeIndex:]
                result.append(resultFace)
                i += 1 #extra hop for the second face merged
            else:
                result.append(faces[i])
        else:
            #cannot be coplanar, no two shared points
            result.append(faces[i])
        i += 1
    return result
    '''
    #start with a face
    #check if any face touching it is coplanar
    #if it is, merge the faces together
    #move on
    #PROBLEM: FACES STAY IN THE FACES ARRAY AFTER HAVING BEEN MERGED
    
    i = 0
    while i < len(faces):
        if i >= len(faces)-1:
            result.append(faces[i])
        #only bother checking if there's shared edge
        merged = False
        for j in range(i+1,len(faces)):
            if i != j and countNumsInCommon(faces[i], faces[j]) >= 2:
                #MERGE QUADRILATERALS?
                f = faces[i] #(2,1,0) or some triplet of indices
                p1, p2, p3 = points[f[0]],points[f[1]],points[f[2]]
                (a,b,c,d) = slice3d.pointsToPlane(p1,p2,p3) #plane coeffs
                #find the odd point to check

                #check if coplanar:
                coplanar = False
                uniquePoints2 = pointsNotInCommon(faces[i],faces[j])
                if len(uniquePoints2) == 0:
                    uniquePoints1 = pointsNotInCommon(faces[j],faces[i])
                    if(len(uniquePoints1) == 0):
                        break #should be impossible
                    (x,y,z) = points[uniquePoints1[0]]
                else:
                    (x,y,z) = points[uniquePoints2[0]]

                if (almostEqual(a*x+b*y+c*z, d)):
                    coplanar = True
                
                if coplanar:
                    #face = reorderPoints(faces[i], points)
                    #find opposite edge
                    uniquePoints1 = pointsNotInCommon(faces[j],faces[i]) 
                    lastUniqueIndex1 = faces[i].index(uniquePoints1[len(uniquePoints1)-1])#index of last unique point
                    placeIndex = (lastUniqueIndex1+2)%(len(faces[i]))
                    resultFace = faces[i][0:placeIndex] + uniquePoints2 + faces[i][placeIndex:]
                    result.append(resultFace)
                    merged = True
                    faces.pop(j)
                    faces.pop(i)
                    i += 1 #extra hop for the second face merged
                    break #back to the bigger for
        if(not(merged)):
            result.append(faces.pop(i))
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
def countNumsInCommon(L1, L2):
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
testHull()

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
