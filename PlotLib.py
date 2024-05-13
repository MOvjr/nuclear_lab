#Plot Library=====
import matplotlib.pyplot as plt
import numpy as np

def plot_cosmic_rays(N,detectors,new_line_array,time_detectors,z_min,z_max,elev_fix,azim_fix):
    fig = plt.figure()                          #We create the R3 space
    ax = fig.add_subplot(111, projection='3d')

    # Define the axis space limits =====
    ax.set_xlim([0, 1.2])    # Limits for x axis
    ax.set_ylim([0, 2.2])    # Limits for y axis
    ax.set_zlim([z_min, z_max])  # Limits for z axis

    #Plot detectors =====
    for x in detectors:
        for i in range (len(x.edge)): #This loop calls all the detectors edge coordinates and plot them
            ax.plot(x.edge[i][0], x.edge[i][1], x.edge[i][2], marker=None, color="red",linewidth=0.8) #Linewidth 0.8 DEF.

    #Plot Cosmic Rays =====
    for i in range(len(new_line_array)):
        t=np.linspace(time_detectors[len(time_detectors)-1][i],time_detectors[0][i],2)                  
        x=new_line_array[i].direction_vect[0]*t+new_line_array[i].inipoint[0]
        y=new_line_array[i].direction_vect[1]*t+new_line_array[i].inipoint[1]
        z=new_line_array[i].direction_vect[2]*t+new_line_array[i].inipoint[2]
        ax.plot(x,y,z,color="blue",marker=None,linewidth=0.8)

    #Axis Labels =====   
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.view_init(elev=elev_fix, azim=azim_fix)  #Point of view control
    print(f"N° of cosmic rays passing through both detectors: {len(new_line_array)} of {N} in total")
    return plt.show()