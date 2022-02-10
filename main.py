# Tynan McGee
# 12/18/2021
# rotating cube in console window!
# note: this is a left-handed system, which means
# positive z-axis goes into the screen.

# resources:
# https://www.a1k0n.net/2011/07/20/donut-math.html
# https://docs.python.org/3/howto/curses.html
# the triangle filling came from https://totologic.blogspot.com/2014/01/accurate-point-in-triangle-test.html
# check out my old 3d project (rotating 3d objects in pygame, or openGL
# instead of ascii in the console).
# that's where a lot of the 3d triangle projection type code
# comes from.
# much of that code is based heavily on code from https://youtu.be/ih20l3pJoeU


# to do:
# - implement a proper z buffer so that the donut works better
# - ^ that may not be realistically doable without filling triangles

import sys
import os
import numpy as np
import time
import random
import curses
from curses import wrapper

import constructors
import triangle


def draw(points, char, stdscr, WIDTH, HEIGHT):
    """ draws each point to the screen using char. """
    for p in points:
        py = round(p[1])
        px = round(p[0])
        # don't try to draw the point if it's outside the range of the screen
        if py >= HEIGHT or py <= 0:
            continue
        if px >= WIDTH or px <= 0:
            continue
        stdscr.addstr(py, px, char)


#########################
## main function
def main(stdscr, obj):
    curses.curs_set(0)
    stdscr.nodelay(True)  # comment to go frame-by-frame with keypresses
    stdscr.clear()

    WIDTH = curses.COLS
    HEIGHT = curses.LINES
    ASPECT = HEIGHT / WIDTH
    CENTER = [WIDTH // 2, HEIGHT // 2]
    LIGHT = ".,-~:;=!*#$@"
    FILL = False
    USE_LIGHTING = True
    SLEEP = True
    slash = '\\'
    if os.name == 'posix':
        slash = '/'
    triangles = triangle.get_triangles_from_object("objects" + slash + obj + ".obj")
    camera = np.array([0, 0, 0, 1])
    theta = 0
    rotate_by = 0.02
    zoom = 2.5  # small zoom levels may cause division by zero
    projection_mat = constructors.make_projection(np.pi/2, ASPECT, 0.1, 100)

    while True:
        stdscr.erase()
        z_rot = constructors.make_rot_z(theta)
        x_rot = constructors.make_rot_x(theta)
        y_rot = constructors.make_rot_y(theta)
        translate_mat = constructors.make_translation(0, 0, zoom)
        transform_mat = translate_mat @ y_rot @ z_rot
        # transform_mat = translate_mat @ z_rot

        triangles_to_draw = []
        for t in triangles:
            # do transformation (rotation+translation)
            trans_p1 = transform_mat @ t.p1
            trans_p2 = transform_mat @ t.p2
            trans_p3 = transform_mat @ t.p3

            # determine whether we can see triangle
            # based on normal vector.
            line1 = trans_p2 - trans_p1
            line2 = trans_p3 - trans_p1
            # line1 cross line2 gives normal vector
            normal = np.cross(line1[:3], line2[:3])
            # normalize and add homogeneous coordinate
            normal /= np.linalg.norm(normal)
            normal = np.append(normal, 1)
            # if the normal vector is facing towards the camera
            # then draw the triangle
            sim = np.dot(normal, trans_p1 - camera)
            if sim < 0:
                # illumination/lighting
                light_dir = np.array([0., 0., -1.])  # make sure these are floats
                light_dir /= np.linalg.norm(light_dir)
                light_dir = np.append(light_dir, 1)

                # do the dot product only in the 3d coords.
                dp = np.dot(normal[:3], light_dir[:3])
                # choose lighting character (out of the twelve)
                n = max(round(11 * dp), 0)
                ch = LIGHT[n]

                # do the projection
                proj_p1 = projection_mat @ trans_p1
                proj_p2 = projection_mat @ trans_p2
                proj_p3 = projection_mat @ trans_p3
                proj_p1 /= proj_p1[3]
                proj_p2 /= proj_p2[3]
                proj_p3 /= proj_p3[3]

                # scale components
                # x is scaled more than y since monospace
                # fonts are taller than they are wide.
                # scale horizontally based on the height
                # since height is (usually) the constraining dimension
                sf = 7  # change this to change the sidelength in x direction
                proj_p1[0] *= sf*HEIGHT
                proj_p1[1] *= HEIGHT
                proj_p2[0] *= sf*HEIGHT
                proj_p2[1] *= HEIGHT
                proj_p3[0] *= sf*HEIGHT
                proj_p3[1] *= HEIGHT

                # translate the original center (0,0) to
                # the screen center
                proj_p1 += np.array([WIDTH // 2, HEIGHT // 2, 0, 0])
                proj_p2 += np.array([WIDTH // 2, HEIGHT // 2, 0, 0])
                proj_p3 += np.array([WIDTH // 2, HEIGHT // 2, 0, 0])

                proj_tri = triangle.tri(proj_p1, proj_p2, proj_p3, normal)
                # ch is the lighting character
                proj_tri.ch = ch
                triangles_to_draw.append(proj_tri)

        # for each triangle to draw, connect up the lines
        # and then draw all the points.
        # done triangle-by-triangle to allow for lighting.
        for t in triangles_to_draw:
            vertices = [t.p1, t.p2, t.p3]
            edges = triangle.connect_triangle_vertices(t)
            # don't fill unless we need to, it takes
            # a lot of computation to do this
            fill = []
            if FILL:
                fill = triangle.get_points_in_tri(t, WIDTH, HEIGHT)
            points = vertices + edges + fill
            if USE_LIGHTING:
                ch = t.ch
            else:
                ch = "#"
            draw(vertices, ch, stdscr, WIDTH, HEIGHT)
            draw(edges, ch, stdscr, WIDTH, HEIGHT)
            if FILL:
                draw(fill, ch, stdscr, WIDTH, HEIGHT)

        ch = stdscr.getch()
        # stdscr.addstr(10,0,str(ch))
        if ch == 260:  # left arrow
            rotate_by -= 0.005
        elif ch == 261:  # right arrow
            rotate_by += 0.005
        elif ch == 259:  # up arrow
            zoom -= 0.25
        elif ch == 258:  # down arrow
            zoom += 0.25
        elif ch == 102:  # f key
            FILL = not FILL
        elif ch == 108:  # l key
            USE_LIGHTING = not USE_LIGHTING
        elif ch == 115:  # s key
            SLEEP = not SLEEP
        elif ch == 27:  # escape
            sys.exit()
        
        stdscr.addstr(0, 0, "increase rotation speed with R/L arrow keys")
        stdscr.addstr(1, 0, "change zoom level with U/D arrow keys")
        stdscr.addstr(2, 0, "toggle filling with F key")
        stdscr.addstr(3, 0, "toggle lighting with L key")
        stdscr.addstr(4, 0, "toggle framerate capping with S key")
        stdscr.addstr(5, 0, "exit with CTRL+C or ESC")
        stdscr.addstr(8, 0, f"rotation increment: {rotate_by}")
        stdscr.addstr(9, 0, f"zoom: {1 / zoom} ({zoom})")
        stdscr.addstr(10, 0, f"filling? {FILL}")
        stdscr.addstr(11, 0, f"lighting? {USE_LIGHTING}")
        stdscr.addstr(12, 0, f"capped framerate? {SLEEP}")
        stdscr.refresh()
        # control "framerate" with this sleep
        if SLEEP:
            time.sleep(0.02)
        # don't let theta get huge
        theta = (theta + rotate_by) % (np.pi*4)


if __name__ == '__main__':
    print("here are the available object files:")
    for o in os.listdir('objects'):
        if o.endswith(".obj"):
            print(o)
    obj = input("choose object filename (not including .obj): ")
    wrapper(main, obj)