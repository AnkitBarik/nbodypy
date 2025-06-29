#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import json
import os
from timeit import default_timer as timer
from phys import get_accel
from plotlib import plot_particle_traj


if __name__=="__main__":

    dt             = 3600 # one hour
    fintime        = 365*24*3600 # one Earth year
    nsteps         = int(fintime/dt)
    checkpointstep = nsteps+1 # Save checkpoint data, turned off for now
    histstep       = 20 # Steps at which to save output
    cmap           = "viridis_r"
    iplot          = True # To show plot
    isave          = True # To save plot

    dat        = np.loadtxt('./input_data.solar_system',dtype='str')
    npart      = dat.shape[0]
    names      = dat[:,0]
    mass       = np.float32(dat[:,1])
    positions  = np.float32(dat[:,2:5])
    velocities = np.float32(dat[:,5:])
    accel      = np.zeros([npart,3])

    # Random particles
    # npart      = 100
    # mass       = 10**np.random.uniform(23,30,npart)
    # positions  = 10**np.random.uniform(5,9,npart*3).reshape([npart,3])
    # velocities = 10**np.random.uniform(-3,1,npart*3).reshape([npart,3])
    # accel      = np.zeros([npart,3])
    pos_plot   = positions
    timing     = []

    t = 0

    checkpoint_counter=0
    step_counter=0 #Actual number of steps run

    for istep in range(nsteps):
        tic = timer()

        positions += 0.5*dt*velocities

        for ipart in range(npart):
            accel[ipart,:] = get_accel( positions[ipart,:],
                                        np.delete(mass,ipart),
                                        np.delete(positions,ipart,axis=0)
                                        )

        velocities += dt*accel
        positions  += 0.5*dt*velocities

        toc = timer()
        timing.append(toc-tic)
        if not istep%histstep:
             v_sq   = np.sum(velocities**2,axis=1)
             ke     = np.sum(0.5 * mass * v_sq)
             X = np.array([t, ke])
             fmt = ['%.5e','%.5e']
             with open('kinetic_energy.dat','a') as ke_file:
                np.savetxt(ke_file,X.reshape(1,X.shape[0]),fmt=fmt)
             pos_plot = np.vstack([pos_plot,positions])
             print("Saving KE at step %d/%d , time=%.5e" %(istep,nsteps,t))

        if not istep%checkpointstep:
            # Save some parameters
            params_dict = {'npart' : npart,
                           'dt'    : dt,
                           'steps' : step_counter,
                           'time'  : t
                            }
            with open('params.json','w') as params_file:
                json.dump(params_dict,params_file)

            X = np.hstack([positions,velocities])
            with open('checkpoint_%d.dat' %checkpoint_counter,'w') as chk_file:
                np.savetxt(chk_file,X,fmt='%.5e')

            checkpoint_counter += 1

        t += dt
        step_counter += 1

    print("Mean time per step: %f" %(np.mean(timing)))
    if iplot:
        fig,ax = plot_particle_traj(npart,pos_plot,cmap)
        if isave:
            if not os.path.exists('images'):
                os.mkdir('images')
            plt.savefig('images/trajectories.pdf',bbox_inches='tight')
            plt.savefig('images/trajectories.png',dpi=300,bbox_inches='tight')
        plt.show()
