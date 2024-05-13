#Gaussian Distribution Library
import numpy as np
import random
import matplotlib.pyplot as plt

#==============================================================================================================
def prob(x,x_center):
    sigma=200E-12       #ps
    return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-1*((x-x_center)**2)/(2*(sigma**2)))

#==============================================================================================================
def distribtime(Ntrial,R_time,Time_min,Time_max,x_center):
    H=(Time_max-Time_min)/R_time
    zones=[]
    for i in range(R_time):
        L=100; k=0
        points_intx=points_inty=0
        for j in range(L):
            points_intx=random.uniform(i*H+Time_min,(i+1)*H+Time_min)
            points_inty=random.uniform(0,prob(x_center,x_center))
            if points_inty<=prob(points_intx,x_center):
                k+=1
        zones.append(Ntrial*(k/L)*H*prob(x_center,x_center))
    return zones
#==============================================================================================================
def round_zones(zones,Ntrial,R_time):
    q=0 ;zones_rounded=[]
    for i in range(R_time):
        zones_rounded.append(round(zones[i]))
    q=sum(zones_rounded)
    q=Ntrial-q
    if q < 0:
        while q < 0:
            S=random.randint(0,R_time-1)
            while zones_rounded[S] <= 0:
                S=random.randint(0,R_time-1)
            zones_rounded[S]-=1
            q+=1
    if q > 0:
        while q > 0:
            S=random.randint(0,R_time-1)
            zones_rounded[S]+=1
            q-=1
    return zones_rounded

#==============================================================================================================
def time_plot(Ntrial,zones,R_time,Time_min,Time_max,x_center):
    range_hist=[]
    for i in range(R_time):
        range_hist.append(Time_min+(i+0.5)*(Time_max-Time_min)/R_time)
    plt.bar(range_hist,zones, width=(Time_max-Time_min)/R_time,color="Blue", edgecolor=None)
    time_dom=np.linspace(Time_min,Time_max,100)
    function_max=max(zones)*(1/prob(x_center,x_center))*prob(time_dom,x_center)
    plt.plot(time_dom,function_max, linewidth=2, color="red", linestyle="--")
    plt.xlim(Time_min,Time_max)
    # Add labels and Head
    plt.xlabel('Time (s)')
    plt.ylabel('N° of time instant / interval')
    plt.title(f'Histogram of dN/dt        Trials={Ntrial}')
    # Show graph
    return plt.show()

#==============================================================================================================
def assign_randtime(zones_rounded,R_time,Time_min,Time_max,dislocation): #Obtain a random t value of the Histogram
    total=sum(zones_rounded); t_new=0
    accumulated=0; H=(Time_max-Time_min)/R_time
    n_range=random.uniform(0,total)
    #print("n_range",n_range)
    for i in range(len(zones_rounded)):
        accumulated+=zones_rounded[i]
        if n_range <= accumulated:
            t_new=random.uniform(i*H+Time_min,(i+1)*H+Time_min)
            break
    return t_new+dislocation

#==============================================================================================================
def transform_times(time_detectors):
    new_time_detectors=[]
    Ntrial=10000; R_time=500
    t_center=0   #time_detectors[i]
    Time_min=t_center-3.37E-9; Time_max=t_center+3.37E-9
    zones_time=distribtime(Ntrial,R_time,Time_min,Time_max,t_center)
    zones_rounded_time=round_zones(zones_time,Ntrial,R_time)
    for i in range(len(time_detectors)):
        dislocation=time_detectors[i]
        new_time_detectors.append(assign_randtime(zones_rounded_time,R_time,Time_min,Time_max,dislocation))
    return new_time_detectors

#==============================================================================================================
def show_example(x_center,Ntrial,R_time,turn):  #Default x_center=3E-9;  Ntrial=10000;  R_time=500
    if turn == "ON":
        Time_min=x_center-1E-9; Time_max=x_center+1E-9
        zones_time=distribtime(Ntrial,R_time,Time_min,Time_max,x_center)
        zones_rounded_time=round_zones(zones_time,Ntrial,R_time)
        time_plot(Ntrial,zones_rounded_time,R_time,Time_min,Time_max,x_center)