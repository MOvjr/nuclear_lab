#Theta Distribution
import numpy as np
import random
import matplotlib.pyplot as plt
#==============================================================================================================
def prob(x):
    return (4/np.pi)*(np.cos(x)**2)
#==============================================================================================================
def distribtheta(N,R_theta):
    H=(np.pi/2)/R_theta
    zones=[]
    for i in range(R_theta):
        L=100; k=0
        points_intx=points_inty=0
        for j in range(L):
            points_intx=random.uniform(i*H,(i+1)*H)
            points_inty=random.uniform(0,4/np.pi)
            if points_inty<=prob(points_intx):
                k+=1
        zones.append(N*(k/L)*H*4/np.pi)
    return zones
#==============================================================================================================
def round_zones(zones,N,R_theta):
    w=N; q=0 ;zones_rounded=[]
    for i in range(R_theta):
        zones_rounded.append(round(zones[i]))
    q=sum(zones_rounded)
    q=N-q
    if q < 0:
        while q < 0:
            S=random.randint(0,R_theta-1)
            while zones_rounded[S] <= 0:
                S=random.randint(0,R_theta-1)
            zones_rounded[S]-=1
            q+=1
    if q > 0:
        while q > 0:
            S=random.randint(0,R_theta-1)
            zones_rounded[S]+=1
            q-=1
    return zones_rounded
#==============================================================================================================
def theta_plot(N,zones,R_theta):
    range_hist=[]
    for i in range(R_theta):
        range_hist.append((i+0.5)*(np.pi/2)/R_theta)
    plt.bar(range_hist,zones, width=(np.pi/2)/R_theta,color="Blue", edgecolor=None)
    tetha_dom=np.linspace(0,np.pi/2,100)
    function_max=zones[0]*(np.pi/4)*prob(tetha_dom)
    plt.plot(tetha_dom,function_max, linewidth=2, color="red", linestyle="--")
    plt.xlim(0, np.pi/2)
    # Add labels and Head
    plt.xlabel('Tetha angle (rad)')
    plt.ylabel('N° of cosmic Rays / interval')
    plt.title(f'Histogram of dN/d0        Total Cosmic Rays={N}')
    # Show graph
    return plt.show()