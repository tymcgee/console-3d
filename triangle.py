# triangle creation/helper functions

import numpy as np

class tri:
    def __init__(self, p1, p2, p3, normal):
        # p1,2,3 are 3d coordinates (preferably np arrays)
        # normal is a 3d coordinate (more like a vector).
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.normal = normal

        self.vertices = [p1, p2, p3]


def get_triangles_from_object(filename):
    """ using filename (.obj), create a list of triangle objects
        containing vertex and normal data. """
    with open(filename, 'r') as f:
        verts = []
        vert_norms = []
        tris = []
        for line in f:
            # remove white space
            ln = line.strip()
            # turn into list
            splt = ln.split(' ')
            if splt[0] == 'v':  # vertex
                # append vertex to list of vertices
                verts.append([float(splt[1]), float(splt[2]), float(splt[3]), 1])
            elif splt[0] == 'vn':  # vertex normal
                # append vertex normal to list of vertex normals
                vert_norms.append([float(splt[1]), float(splt[2]), float(splt[3]), 1])
            elif splt[0] == 'f':  # face
                # create and append triangle object
                # splt[1] through splt[3] look like '5//1' or '3//1'
                # the first number is the vertex index
                # the last number is the normal index
                splt[1] = splt[1].split('//')
                splt[2] = splt[2].split('//')
                splt[3] = splt[3].split('//')
                normal = np.array(vert_norms[int(splt[1][-1]) - 1])
                p1 = np.array(verts[int(splt[1][0]) - 1])
                p2 = np.array(verts[int(splt[2][0]) - 1])
                p3 = np.array(verts[int(splt[3][0]) - 1])
                tris.append(tri(p1, p2, p3, normal))
        return tris


#########################
## helper line functions
def line(p1, p2):
    """ returns function which calculates points along the line
        containing the given coordinates. """
    # get displacement vector pointing along the line
    # this is the vector pointed from p2 to p1
    diff = p1 - p2
    # the points we want are from the parametric equation
    # p2 + t*diff
    # for values of t between 0 and 1
    f = lambda t: p2 + t*diff
    return f

def get_line_pixels(p1, p2):
    """ returns list of points (array where each element is a 3d array).
        the points connect vertices p1 = (x1,y1,z1) and p2 = (x2,y2,z2). """
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    f = line(p1, p2)
    # include the min number of pixels that will fit,
    # either vertically or horizontally
    num_of_pixels = round(max(np.ceil(abs(x1-x2)), np.ceil(abs(y1-y2))))
    points = []
    for i in range(num_of_pixels-1):
        # use t values between 0 and 1
        t = (i+1) / num_of_pixels
        points.append(f(t))
    return points


#########################
## triangle functions
def connect_triangle_vertices(t):
    """ given triangle object t with three vertices p1 p2 p3,
        connect each vertex to each other vertex and return
        the list of points to draw. """
    # connect p1 to p2
    # connect p1 to p3
    # connect p2 to p3
    points = []
    points.extend(get_line_pixels(t.p1[:3], t.p2[:3]))
    points.extend(get_line_pixels(t.p1[:3], t.p3[:3]))
    points.extend(get_line_pixels(t.p2[:3], t.p3[:3]))
    return points

def get_bounding_box(t):
    """ returns a function bounding_box(i,j) which
        when evaluated, returns a bool for whether the
        point at (i,j) is in triangle t's bounding box. """
    x1 = t.p1[0]
    x2 = t.p2[0]
    x3 = t.p3[0]
    y1 = t.p1[1]
    y2 = t.p2[1]
    y3 = t.p3[1]

    xmin = min(x1, x2, x3)
    xmax = max(x1, x2, x3)
    ymin = min(y1, y2, y3)
    ymax = max(y1, y2, y3)

    f = lambda x, y: not (x < xmin or x > xmax or y < ymin or y > ymax)
    return f

def get_points_in_tri(t, WIDTH, HEIGHT):
    """ return a list of every point which lies inside the triangle
        t (with vertices t.p1, t.p2, t.p3). """
    # https://totologic.blogspot.com/2014/01/accurate-point-in-triangle-test.html
    # get triangle's bounding box
    bounding_box = get_bounding_box(t)
    x1 = t.p1[0]
    x2 = t.p2[0]
    x3 = t.p3[0]
    y1 = t.p1[1]
    y2 = t.p2[1]
    y3 = t.p3[1]
    # loop through all "pixels" on screen
    inside_points = []
    for j in range(HEIGHT):
        for i in range(WIDTH):
            # step 1: ignore points not in the bounding box
            if bounding_box(i, j):
                # step 2: use parametric equation weights to determine
                # if the point is in the triangle
                denom = (x1*(y2 - y3) + y1*(x3 - x2) + x2*y3 - y2*x3)
                t1 = (i*(y3 - y1) + j*(x1 - x3) - x1*y3 + y1*x3) / denom
                t2 = (i*(y2 - y1) + j*(x1 - x2) - x1*y2 + y1*x2) / -denom
                if t1 <= 1 and t1 >= 0 and t2 <= 1 and t2 >= 0 and t1 + t2 <= 1:
                    inside_points.append([i, j])
    return inside_points