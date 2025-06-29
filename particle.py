#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from constants import grav_const

class Part:

    def __init__(self,mass=None,pos=None,vel=None,name=None):

        if name is not None:
            self.name = name
        if mass is not None:
            self.mass=mass
        if pos is not None:
            self.pos=pos
        if vel is not None:
            self.vel=vel

    def __str__(self):
        if hasattr(self,'name'):
            return f"Name={self.name}\nMass={self.mass}\nposition={self.pos}\nvelocity={self.vel}"
        else:
            return f"Mass={self.mass}\nposition={self.pos}\nvelocity={self.vel}"


