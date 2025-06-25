#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def leapfrog(a,dt):

    x_new = x + v*dt + 0.5*a*dt**2
    v_new = v + 0.5 * (a + a_new) * dt
