# LinesLib ======  
import random
import numpy as np
import math

#Theta Array Function =====
def theta_array(R_theta):
    array_theta=[]
    H_theta=(np.pi/2)/R_theta
    for i in range(R_theta):
        array_theta.append(i*H_theta)
    return array_theta

#Energy Array Function =====
def energy_array(R_energy,E_max):
    array_energy=[]
    H_energy=(E_max-1)/R_energy
    for i in range(R_energy):
        array_energy.append(i*H_energy+1)
    return array_energy

# Velocity Function ======
def muon_velocity(muon_energy): #GeV
    mass=0.1057                 #GeV/C**2
    return math.sqrt(1-(((muon_energy/(mass*1))+1)**(-2)))*2.99792458E8

#Lines Object =====
class lines:
    def __init__(self,inipoint,direction_vect,fi,theta,muon_energy):  #Both arrays
        self.inipoint=inipoint
        self.direction_vect=direction_vect
        self.fi=fi
        self.theta=theta
        self.muon_energy=muon_energy
    
    def createline(self,orig_distance,R_theta,R_energy,n_theta,n_energy,E_max):     #n is a label, it reprsents the each line (created cosmic ray)
        array_theta=theta_array(R_theta)
        array_energy=energy_array(R_energy,E_max)
        for i in range(0,len(self.inipoint)):
            self.inipoint[i]+=random.uniform(-1, 1)*orig_distance[i]
            self.theta=random.uniform(array_theta[n_theta],array_theta[n_theta+1])
            self.fi=random.uniform(0,2*np.pi)
            self.muon_energy=random.uniform(array_energy[n_energy],array_energy[n_energy+1])
            velocity=muon_velocity(self.muon_energy)
            self.direction_vect[0]=np.sin(self.theta)*np.cos(self.fi)*velocity
            self.direction_vect[1]=np.sin(self.theta)*np.sin(self.fi)*velocity
            self.direction_vect[2]=-np.cos(self.theta)*velocity

#Array of lines=====   
def createline_array(N,R_theta,R_energy,zones_rounded_theta,zones_rounded_energy,E_max):
    line_array=[]
    for i in range(N):
        line_array.append(lines([0.5,1.0,5.],[0.,0.,0.],0,0,0)) #([0.5,1.0,5.0],[0.,0.,0.],0,0,0) DEFAULT
        
    n_theta=0; n_energy=0
    for i in range (N):
        line_array[i].createline([8.,10.,2.],R_theta,R_energy,n_theta,n_energy,E_max) #[1.,2.,2.] DEFAULT
        if i == zones_rounded_theta[n_theta]-1:
            n_theta+=1
        if i == zones_rounded_energy[n_energy]-1:
            n_energy+=1
    return line_array