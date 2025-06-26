#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def leapfrog1(a,x,v,dt):

    x_new = x + v*dt + 0.5*a*dt**2

    return x_new

def leapfrog2(a,v,a_new,dt):

    v_new = v + 0.5 * (a + a_new) * dt

    return v_new