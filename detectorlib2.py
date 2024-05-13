import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

# Sign Function ====================================================================================================

def sign(a):
    b=math.fabs(a)/a
    return b

# Detector Object ==================================================================================================

class detector:
    def __init__(self,name,pos,lenx,leny,corner,edge):  #pos & corner are arrays
        self.name=name
        self.pos=pos
        self.lenx=lenx
        self.leny=leny
        self.corner=corner
        self.edge=edge
    
    def corners(self):
        self.corner=np.zeros((4,3), dtype=float)   #Define an array 4X3 saving the corners position
        for i in range(0,len(self.corner)):
            self.corner[i]=[self.pos[0]+sign(math.cos((i+1)*math.pi/2))*self.lenx/2,self.pos[1]+sign(math.sin((i+1)*math.pi/2))*self.leny/2,self.pos[2]]
        return self.corner
    
    def edges(self):
        self.edge=np.zeros((4,3), dtype=list) #It contains and array 4X3 with the edges coordinates
        k=0
        for i in range(0,len(self.edge)):
            k=0
            for j in range(k,len(self.edge[i])):
                if i < 3:
                    self.edge[i][j]=[self.corner[i,j],self.corner[i+1,j]]
                k+=1
        for j in range(0,len(self.edge[3])):
            self.edge[3][j]=[self.corner[3,j],self.corner[0,j]]
        return self.edge
    
# Probability Function for Theta (Histogram) ========================================================

def prob(x):
    return (4/np.pi)*(np.cos(x)**2)

def distribtetha(N,R):
#N Number of total random points
#R Number of intervals to divide the domain of P(tetha)
    H=(np.pi/2)/R
    zones=np.zeros(R, dtype=float)
    for i in range(R):
        L=100          #N° points inside the i-interval
        points_intx=np.zeros(L, dtype=float)  
        points_inty=np.zeros(L, dtype=float)
        k=0
        for j in range(L):
            points_intx[j]=random.uniform(i*H,(i+1)*H)
            points_inty[j]=random.uniform(0,4/np.pi)
            if points_inty[j]<=prob(points_intx[j]):
                k+=1
        zones[i]=N*(k/L)*H*4/np.pi
    #for i in range(R):                       #To check prob = 1
        #a+=zones[i]
    return zones

# Probability Function for Energy (Histogram) ========================================================
def probE(x):
    a=3; b=115 #GeV
    return (1/0.49166)*(x**(-a))/(1+x/b)

def distribEnergy(N,R_energy,max_energy):
#N Number of total random points
#R Number of intervals to divide the domain of P(tetha)
    H=(max_energy-1)/R_energy
    zones=np.zeros(R_energy, dtype=float)
    for i in range(R_energy):
        L=100          #N° points inside the i-interval
        points_intx=np.zeros(L, dtype=float)  
        points_inty=np.zeros(L, dtype=float)
        k=0
        for j in range(L):
            points_intx[j]=random.uniform(i*H+1,(i+1)*H+1)
            points_inty[j]=random.uniform(0,probE(1))
            if points_inty[j]<=probE(points_intx[j]):
                k+=1
        zones[i]=N*(k/L)*H*probE(1)
    #for i in range(R):                       #To check prob = 1
        #a+=zones[i]
    return zones     
    
# Lines Objetc (Cosmic Rays) =====================================================================================
    
class lines:
    def __init__(self,inipoint,direction_vect,tetha,muon_energy):  #Both arrays
        self.inipoint=inipoint
        self.direction_vect=direction_vect
        self.tetha=tetha
        self.muon_energy=muon_energy
    
    def createline(self,orig_distance,R_tetha,R_energy,n):     #n is a label, it reprsents the each line (created cosmic ray)
        #self.inipoint=[.0,.0,.0]
        #self.direction_vect=[.0,.0,.0]
        planes_center=[0.5,1.,2.]               #We can select the origin of the random paths
        for i in range(0,len(self.inipoint)):
            self.inipoint[i]+=random.uniform(-1, 1)*orig_distance[i]
            H_tetha=(np.pi/2)/R_tetha; H_energy=(max_energy-1)/R_energy
            tetha=random.uniform(n*H_tetha,(n+1)*H_tetha)
            fi=random.uniform(0,2*np.pi)
            self.direction_vect[0]=np.sin(tetha)*np.cos(fi)
            self.direction_vect[1]=np.sin(tetha)*np.sin(fi)
            self.direction_vect[2]=-np.cos(tetha)
        return [self.inipoint,self.direction_vect]
    
#Intersect Function ================================================================================================
#This function finds the intersection point between a line and the plane z_plane.
#The line has parameters: initial points (inipoint) and its directional vector (direction_vect)

def intersect(inipoint,direction_vect,z_plane):
    point=[0.,0.,0.]
    for i in range(0,len(point)):
        point[i]=inipoint[i]+direction_vect[i]*((z_plane-inipoint[2])/direction_vect[2])
        if i==len(point):
            point[i]=z_plane
    return point

#If intersect Function =============================================================================================
# This function says the user if a specific line pass through the inner area of a specific detector

def if_intersect(point,pos,lenx,leny):
    if pos[0]-lenx/2<=point[0]<=pos[0]+lenx/2 and pos[1]-leny/2<=point[1]<=pos[1]+leny/2:
        a=True
    else:
        a=False
    return a

# Unit vector Function ==============================================================================================
# This function take as input a specific vector and returns the unit vector
def vec_unit(vector):
    module=0
    for i in range(len(vector)):
        module+=vector[i]**2
    module=math.sqrt(module)
    for i in range(len(vector)):
        vector[i]=vector[i]/module
    return vector

# Velocity Function ========================================================
def velocity_beta(muon_energy,mass): #GeV / GeV/C**2
    return math.sqrt(1-(((muon_energy/(mass*1))+1)**(-2)))
#2.99792458E8