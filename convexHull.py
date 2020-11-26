import numpy as np
from scipy.spatial import ConvexHull


def getHull(points):
    pts = np.array(points)
    hull = ConvexHull(pts)
    return np.ndarray.tolist(hull.simplices)

#def mergeFaces(faces):
    #for face in faces:

def testHull():
    points = [(0, 0, 0), (1, 0, 0), [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, .5, 1], [0, .5, 1], ]
    print("cube:", getHull(points))

    points = [(0, 0, 0), (1, 0, 0), [0, 1, 0],
            [0, 0, 1]]
    print("tetra:", getHull(points))

    points = [(0, 0, 0), (1, 0, 0), [1,1,0],[0, 1, 0],
            [0, 0, 1],[0,1,1]]
    print("triPrism:", getHull(points))

testHull()
