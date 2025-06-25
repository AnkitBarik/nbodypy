#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from constants import grav_const

class Part:

    def __init__(self,mass,pos,vel):

        self.pos = pos
        self.vel = vel
        self.mass= mass

    def __str__(self):
        return f"Mass={self.mass},\n position={self.pos},\n velocity={self.vel}"

    # def get_accel(self,masses,positions):

    #     r     = self.pos - positions
    #     rnorm = np.linalg.norm(r,axis=1)
    #     a     = grav_const * masses[:,np.newaxis] * r/rnorm[:,np.newaxis]**3
    #     out   = np.sum(a,axis=0)

    #     return out
