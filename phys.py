#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from constants import grav_const

def get_accel_par(part1,part2):

    r     = part1.pos - part2.pos #For force on particle 1
    rnorm = np.linalg.norm(r)
    a1    = - grav_const*part2.mass * r/rnorm**3
    a2    = grav_const*part1.mass * r/rnorm**3

    return np.array([a1, a2])

def get_accel(pos,masses,positions):
    # masses and positions of all particles except pos
    r     = pos - positions
    rnorm = np.linalg.norm(r,axis=1)
    a     = -grav_const * masses[:,np.newaxis] * r/rnorm[:,np.newaxis]**3
    out   = np.sum(a,axis=0)
    return out