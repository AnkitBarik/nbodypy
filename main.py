#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from particle import Part
from phys import get_accel
from integrator import leapfrog1, leapfrog2
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if __name__=="__main__":

    npart          = 2
    npart_per_rank = int(npart/size)
    nsteps         = 10000
    dt             = 1e-4
    histstep       = 20
    positions      = np.zeros([nsteps,npart,3])
    init_mass = np.array([1e-4,1e4])#np.random.uniform(0,1,npart)
    init_pos  = np.array([[0.5,0.5,0.5],
                          [0,0,0]])#np.random.uniform(0,1,(npart,3))
    init_vel  = np.array([[1e-6,1e-6,0],
                          [0,0,0]])
    #np.random.uniform(0,1e-5,(npart,3))
#    init_mass = np.random.uniform(0,1,npart)
#    init_pos  = np.random.uniform(0,1,(npart,3))
#    init_vel  = np.random.uniform(0,1e-5,(npart,3))

    particles = [Part(init_mass[i],init_pos[i],init_vel[i]) for i in range(npart)]
    npairs = npart*(npart-1)//2

    for istep in range(nsteps):

        # accel_global,pairs = accel_parallel(npart,npairs,particles,istep)
        if istep == 0:
            if rank == 0:
                pairs = np.empty([npairs,2],dtype=int)
                count = 0

                for i in range(npart):
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
            accel_loc[k,...] = get_accel(particles[pairs_loc[k,0]],particles[pairs_loc[k,1]])

        comm.Gather(accel_loc,accel_global,root=0)

        if rank == 0:
            accel = np.empty([npart,3],dtype=np.float32)

            for kpart in range(npart):
                mask1 = pairs[:,0] == kpart
                mask2 = pairs[:,1] == kpart
                accel[kpart,:] = np.sum(accel_global[mask1,0,:],axis=0)
                accel[kpart,:] += np.sum(accel_global[mask2,1,:],axis=0)

            x = np.array([particles[i].pos for i in range(npart)])
            v = np.array([particles[i].vel for i in range(npart)])

            x_new = leapfrog1(accel,x,v,dt)
            for kpart in range(npart):
                particles[kpart].pos = x_new[kpart]
        else:
            accel = None
            x_new = None

        particles=comm.bcast(particles,root=0)

        for k in range(npairs//size):
            accel_loc[k,...] = get_accel(particles[pairs_loc[k,0]],particles[pairs_loc[k,1]])

        comm.Gather(accel_loc,accel_global,root=0)

        if rank == 0:
            accel_new = np.empty([npart,3],dtype=np.float32)

            for kpart in range(npart):
                mask1 = pairs[:,0] == kpart
                mask2 = pairs[:,1] == kpart
                accel_new[kpart,:] = np.sum(accel_global[mask1,0,:],axis=0)
                accel_new[kpart,:] += np.sum(accel_global[mask2,1,:],axis=0)

            v_new = leapfrog2(accel,v,accel_new,dt)
            for kpart in range(npart):
                particles[kpart].vel = v_new[kpart]
        else:
            accel_new=None
            v_new    =None

        if rank == 0 and istep%histstep == 0:
        #     for kpart in range(npart):
        #         positions[istep,kpart,:] = particles[kpart].pos

            fig,ax = plt.subplots(figsize=(10,10),subplot_kw={'projection':'3d'})
            for kpart in range(npart):
                ax.plot(particles[kpart].pos[0],
                        particles[kpart].pos[1],
                        particles[kpart].pos[2],
                        'o',markersize=10)
            #     ax.plot(positions[-1,kpart,...][:,0],
            #             positions[-1,kpart,...][:,1],
            #             positions[-1,kpart,...][:,2])
            plt.savefig("movie/img%05d.png" %(istep/histstep),dpi=300,bbox_inches='tight')
            plt.close(fig)

        particles=comm.bcast(particles,root=0)

