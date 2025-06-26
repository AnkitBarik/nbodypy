#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def get_accel(part1,part2):

    r = part1.pos - part2.pos #For force on particle 1
    rnorm = np.linalg.norm(r)
    a1 = part2.mass * r/rnorm**3
    a2 = - part1.mass * r/rnorm**3

    return np.array([a1, a2])