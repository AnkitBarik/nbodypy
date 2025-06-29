#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def plot_particle_traj(npart,pos_plot,cmap):

    colors = eval("plt.cm."+cmap+"(np.linspace(0,1,npart))")

    fig, ax = plt.subplots(figsize=(10,10),subplot_kw={"projection":"3d"})
    pos_plot = pos_plot.reshape([pos_plot.shape[0]//npart,npart,3])

    for ipart in range(npart):
        ax.plot(pos_plot[:,ipart,:][:,0],
                pos_plot[:,ipart,:][:,1],
                pos_plot[:,ipart,:][:,2],
                color=colors[ipart])

    ax.set_aspect('equal')
    ax.set_xlabel(r'$x$',fontsize=30)
    ax.set_ylabel(r'$y$',fontsize=30)
    ax.set_zlabel(r'$z$',fontsize=30)
    ax.tick_params(labelsize=20)

    fig.tight_layout()
    return fig,ax
