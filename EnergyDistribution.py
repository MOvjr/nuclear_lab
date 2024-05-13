#Energy Distribution
import numpy as np
import random
import matplotlib.pyplot as plt
#==============================================================================================================
def prob(x):
    a=3; b=115 #GeV
    integral_value=0.49166
    return (1/integral_value)*(x**(-a))/(1+x/b)
#==============================================================================================================
def distribenergy(N,R_energy,E_max):
    H=(E_max-1)/R_energy
    zones=[]
    for i in range(R_energy):
        L=100; k=0
        points_intx=points_inty=0
        for j in range(L):
            points_intx=random.uniform(i*H+1,(i+1)*H+1)
            points_inty=random.uniform(0,prob(1))
            if points_inty<=prob(points_intx):
                k+=1
        zones.append(N*(k/L)*H*prob(1))
    return zones
#==============================================================================================================
def round_zones(zones,N,R_energy):
    w=N; q=0 ;zones_rounded=[]
    for i in range(R_energy):
        zones_rounded.append(round(zones[i]))
    q=sum(zones_rounded)
    q=N-q
    if q < 0:
        while q < 0:
            S=random.randint(0,R_energy-1)
            while zones_rounded[S] <= 0:
                S=random.randint(0,R_energy-1)
            zones_rounded[S]-=1
            q+=1
    if q > 0:
        while q > 0:
            S=random.randint(0,R_energy-1)
            zones_rounded[S]+=1
            q-=1
    return zones_rounded
#==============================================================================================================
def energy_plot(N,zones,R_energy,E_max):
    range_hist=[]
    for i in range(R_energy):
        range_hist.append(1+(i+0.5)*(E_max-1)/R_energy)
    plt.bar(range_hist,zones, width=(E_max-1)/R_energy,color="Blue", edgecolor=None)
    energy_dom=np.linspace(1,E_max,100)
    function_max=zones[0]*(1/prob(1))*prob(energy_dom)
    plt.plot(energy_dom,function_max, linewidth=2, color="red", linestyle="--")
    plt.xlim(1, E_max)
    # Add labels and Head
    plt.xlabel('Energy (GeV)')
    plt.ylabel('N° of cosmic Rays / interval')
    plt.title(f'Histogram of dN/dE        Total Cosmic Rays={N}')
    # Show graph
    return plt.show()