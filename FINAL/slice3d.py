import numpy

def slicePoly(points, edges, plane):
    half1 = []
    half2 = []
    (a,b,c,d) = plane
    #distribute existing coordinates
    for (x,y,z) in points:
        if (a*x+b*y+c*z >= d):
            half1.append((x,y,z))
        else:
            half2.append((x,y,z))
    if half1 == [] or half2 == []:
        return None
    #then add the intersection points
    for edge in edges: #each edge
        (index1, index2) = edge
        p1, p2 = points[index1], points[index2]
        intersect = findIntersect(p1, p2, plane)
        if(intersect != None):
            half1.append(intersect)
            half2.append(intersect)
    return half1, half2

#Find plane equation in form: ax+by+cz = 1
#general idea: finding plane from 3 points inspired by
#https://tutorial.math.lamar.edu/classes/calciii/eqnsofplanes.aspx
#to create orthogonal vectors
def pointsToPlane(a,b,c): 
    #make two vectors in plane
    (xa,ya,za),(xb,yb,zb),(xc,yc,zc) = a,b,c
    vector1 = (xb-xa, yb-ya, zb-za)
    vector2 = (xc-xb,yc-yb,zc-zb)
    #find orthogonal vector
    orth = numpy.cross(vector1, vector2)
    (i,j,k) = orth 
    #solve for d
    d = xa*i+ya*j+za*k
    #convert to general form coefficients
    return (i,j,k,d)

#takes in points of vertices, returns point of intersect or none
def findIntersect(p1, p2, plane):
    if lineIntersectsPlane(p1, p2, plane):
        line = lineFromPoints(p1, p2)
        return linePlaneIntersect(line, plane)
    else:
        return None

def lineIntersectsPlane(p1, p2, plane):
    (x1,y1,z1) = p1
    (x2,y2,z2) = p2
    (a,b,c,d) = plane
    #make sure points straddle plane
    if (x1*a+y1*b+z1*c) > d and (x2*a+y2*b+z2*c) < d:
        return True
    elif (x1*a+y1*b+z1*c) < d and (x2*a+y2*b+z2*c) > d:
        return True
    else:
        return False

def lineFromPoints(p1, p2):
    (x1,y1,z1) = p1
    (x2,y2,z2) = p2
    #v = (x2-x1, y2-y1, z2-z1) #directional vector
    #x =x0 + dt parametric form
    return (x1, (x2-x1)),(y1,(y2-y1)),(z1,(z2-z1))

def linePlaneIntersect(line, plane):
    (a,b,c,d) = plane
    ((e,f),(g,h),(i,j)) = line
    t = (d-a*e-b*g-c*i)/(a*f+b*h+c*j)
    return e+f*t, g+h*t, i+j*t