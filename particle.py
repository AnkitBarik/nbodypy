#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from constants import grav_const

class Part:

    def __init__(self,mass=None,pos=None,vel=None):

        if mass is not None:
            self.mass=mass
        if pos is not None:
            self.pos=pos
        if vel is not None:
            self.vel=vel

    def __str__(self):
        return f"Mass={self.mass},\n position={self.pos},\n velocity={self.vel}"

    # def get_accel(self,masses,positions):

    #     r     = self.pos - positions
    #     rnorm = np.linalg.norm(r,axis=1)
    #     a     = grav_const * masses[:,np.newaxis] * r/rnorm[:,np.newaxis]**3
    #     out   = np.sum(a,axis=0)

    #     return out
