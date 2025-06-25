#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from particle import Part
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

npart     = 8
npart_per_rank = int(npart/size)
nsteps    = 100

# init_mass = np.array([1e-4,1e4])#np.random.uniform(0,1,npart)
# init_pos  = np.array([[0.5,0.5,0.5],
#                       [0,0,0]])#np.random.uniform(0,1,(npart,3))
# init_vel  = np.array([[1e-6,1e-6,0],
#                       [0,0,0]])
# #np.random.uniform(0,1e-5,(npart,3))
init_mass = np.random.uniform(0,1,npart)
init_pos  = np.random.uniform(0,1,(npart,3))
init_vel  = np.random.uniform(0,1e-5,(npart,3))

particles = [Part(init_mass[i],init_pos[i],init_vel[i]) for i in range(npart)]
npairs = npart*(npart-1)//2
pairs = np.zeros([npairs,2])

count = 0

for i in range(npart):
    for j in range(i+1,npart):
        pairs[count,:] = [i,j]
        count += 1

# Bcast
particles=comm.bcast(particles,root=0)
# pairs    =comm.bcast(np.int32(pairs),root=0)

part_pairs = np.zeros([npairs//size,2])
comm.Scatter(pairs,part_pairs,root=0)

print(rank,part_pairs)