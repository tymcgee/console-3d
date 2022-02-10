# useful matrix costructors (taken from vector.py from my previous 3d project)
# changed to return numpy arrays instead of lists

import numpy as np


def make_rot_x(ang):
    """ makes the 4d x-rotation matrix using angle ang and returns it. """
    return np.array([
        [1,           0,            0, 0],
        [0, np.cos(ang), -np.sin(ang), 0],
        [0, np.sin(ang),  np.cos(ang), 0],
        [0,           0,            0, 1]
    ])

def make_rot_y(ang):
    """ makes the 4d y-rotation matrix using angle ang and returns it. """
    return np.array([
        [ np.cos(ang), 0, np.sin(ang), 0],
        [           0, 1,           0, 0],
        [-np.sin(ang), 0, np.cos(ang), 0],
        [           0, 0,           0, 1]
    ])

def make_rot_z(ang):
    """ makes the 4d z-rotation matrix using angle ang and returns it. """
    return np.array([
        [np.cos(ang), -np.sin(ang), 0, 0],
        [np.sin(ang),  np.cos(ang), 0, 0],
        [           0,           0, 1, 0],
        [           0,           0, 0, 1]
    ])

def make_translation(a, b, c):
    """ makes a translation matrix which adds a to x, b to y, c to z.
        only works if w component of vector is 1 (i think). """
    return np.array([
        [1, 0, 0, a],
        [0, 1, 0, b],
        [0, 0, 1, c],
        [0, 0, 0, 1]
    ])

def make_projection(fov, aspect, z_near, z_far):
    """ makes projection matrix for projecting 3d vectors into 2d. 
        
        multiplying a 3d vector (with w component = 1) by this matrix
        will result in its projection into 2d coords. the resulting
        vector after multiplication should look like
        >>[a*f*x, f*y, z*q, n*q, z]

        where a=aspect ratio, f=fov, q=z_far / (z_far - z_near)
        and n=z_near.

        after multiplying a vector by this matrix, divide each component by
        z (which is the fourth component of the resulting vector).
        then the first two components are new (x,y) coords in 2d.
        third component has to do with the original z coord in 3d
        and the fourth component should just be 1 (after normalization by z).
        
        essentially the x component is scaled by the aspect ratio and the fov,
        the y component is scaled by the fov, and the z component is scaled by
        something to do with the depth of the screen/how far you want to see.
        then each component is divided by z to give it perspective. """
    fov = 1 / np.tan(fov / 2)
    q = z_far / (z_far - z_near)
    return np.array([
        [aspect * fov,   0, 0,           0],
        [           0, fov, 0,           0],
        [           0,   0, q, -z_near * q],
        [           0,   0, 1,           0]
    ])

