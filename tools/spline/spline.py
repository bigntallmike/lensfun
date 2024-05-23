#!/usr/bin/env python2.7
# -*- coding: windows-1251 -*-

#
# Visualization of a Hermite spline.
#
# Used to evaluate how much differs a two-interpolated-coordinates spline
# from a single-interpolated-coordinate variant (which is used to interpolate
# lens model terms).
#

from sys import exit
from time import sleep
import pygame

TENSION = 0.5  # 0..1


def spline(P1, P2, P3, P4, t):
    t2 = t * t
    t3 = t2 * t
    if P1 != None:
        tg2 = TENSION * (P3 - P1)
    else:
        tg2 = P3 - P2
    if P4 != None:
        tg3 = TENSION * (P4 - P2)
    else:
        tg3 = P3 - P2
    return (
        (2 * t3 - 3 * t2 + 1) * P2
        + (t3 - 2 * t2 + t) * tg2
        + (-2 * t3 + 3 * t2) * P3
        + (t3 - t2) * tg3
    )


def main():
    pygame.init()
    dpy = pygame.display.set_mode((800, 800))

    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # Control points
    points = (
        (10, 10),
        (100, 200),
        (200, 300),
        (300, 500),
        (400, 400),
        (500, 500),
        (600, 200),
        (700, 100),
        (790, 790),
        (790, 790),
    )

    # Display a single-interpolated-coordinate spline
    pi = 0
    p2 = (None, None)
    p3 = points[0]
    for x in range(points[0][0], points[len(points) - 1][0]):
        if (x >= p3[0]) and (pi < len(points) - 1):
            p1 = p2
            p2 = points[pi]
            p3 = points[pi + 1]
            if pi < len(points) - 2:
                p4 = points[pi + 2]
            else:
                p4 = (None, None)
            pi = pi + 1
        t = float(x - p2[0]) / (p3[0] - p2[0])
        p = spline(p1[1], p2[1], p3[1], p4[1], t)
        pygame.draw.line(dpy, WHITE, (x, p), (x, p))

    # Display a two-interpolated-coordinates spline
    p2 = points[0]
    p3 = points[0]
    p4 = points[0]
    for p in points:
        p1 = p2
        p2 = p3
        p3 = p4
        p4 = p
        t = 0.0
        while t < 1.0:
            px = spline(p1[0], p2[0], p3[0], p4[0], t)
            py = spline(p1[1], p2[1], p3[1], p4[1], t)
            pygame.draw.line(dpy, GREEN, (px, py), (px, py))
            t = t + 0.01

    # Mark control points
    for p in points:
        pygame.draw.line(dpy, RED, (p[0] - 2, p[1] - 2), (p[0] + 2, p[1] + 2))
        pygame.draw.line(dpy, RED, (p[0] - 2, p[1] + 2), (p[0] + 2, p[1] - 2))

    # Display the stuff
    pygame.display.flip()

    # Wait for ESC or close window
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (
                e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE
            ):
                exit()
        sleep(0.1)


if __name__ == "__main__":
    main()
