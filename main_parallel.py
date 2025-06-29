#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import sys
from mpi4py import MPI
from timeit import default_timer as timer
from particle import Part
from phys import get_accel_par
from plotlib import plot_particle_traj

if __name__=="__main__":

    dt             = 3600 # one hour
    fintime        = 365*24*3600 # one Earth year
    nsteps         = int(fintime/dt)
    checkpointstep = 300 # Save checkpoint data
    histstep       = 100 # Steps at which to save data
    cmap           = "viridis_r"

    dat        = np.loadtxt('./input_data.solar_system',dtype='str')
    npart      = dat.shape[0]
    names      = dat[:,0]
    mass       = np.float32(dat[:,1])
    positions  = np.float32(dat[:,2:5])
    velocities = np.float32(dat[:,5:])
    pos_plot   = positions

    # Random particles - to be tested
    # npart      = 100
    # mass       = 10**np.random.uniform(23,30,npart)
    # positions  = 10**np.random.uniform(5,9,npart*3).reshape([npart,3])
    # velocities = 10**np.random.uniform(-3,2,npart*3).reshape([npart,3])
    # pos_plot   = positions
    timing     = []

    particles  = [Part(mass[i],
                       positions[i,...],
                       velocities[i,...]) for i in range(npart)]

    npairs = npart*(npart-1)//2
    t = 0

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    if size > npart:
        print("Too many ranks, total ranks must be <= number of bodies")
        sys.exit(1)

    for istep in range(nsteps):
        tic = timer()
        if istep == 0:
            if rank == 0:
                pairs = np.empty([npairs,2],dtype=int)
                count = 0

                for i in range(npart):
                    particles[i].pos += 0.5*dt*particles[i].vel
                    for j in range(i+1,npart):
                        pairs[count,:] = [i,j]
                        count += 1
            else:
                pairs = None

            pairs_loc         = np.empty([npairs//size,2],dtype=int)
            accel_loc         = np.empty([npairs//size,2,3],dtype=np.float32)
            accel_global      = np.empty([npairs,2,3],dtype=np.float32)

            comm.Scatter(pairs,pairs_loc,root=0)
            comm.barrier()

        for k in range(npairs//size):
            accel_loc[k,0,:], accel_loc[k,1,:] = get_accel_par(particles[pairs_loc[k,0]],
                                             particles[pairs_loc[k,1]])

        comm.Gather(accel_loc,accel_global,root=0)

        if rank == 0:

            for kpart in range(npart):
                mask1 = pairs[:,0] == kpart
                mask2 = pairs[:,1] == kpart
                accel = np.sum(accel_global[mask1,0,:],axis=0)
                accel += np.sum(accel_global[mask2,1,:],axis=0)

                particles[kpart].vel += dt*accel
                particles[kpart].pos += 0.5*dt*particles[kpart].vel
                t += dt
            toc = timer()
            timing.append(toc-tic)
        else:
            accel = None
            x_new = None

        if rank == 0 and istep%histstep == 0:
            for kpart, particle in enumerate(particles):
                pos_plot = np.vstack([pos_plot,particle.pos])

    if rank == 0:
        print("Mean time per step: %f" %(np.mean(timing)))
        fig,ax = plot_particle_traj(npart,pos_plot,cmap)
        plt.show()