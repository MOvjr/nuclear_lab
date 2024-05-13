#Detectorslib
import math
import numpy as np
# Sign Function ======
def sign(a):
    b=math.fabs(a)/a
    return b

# Detector Object ======
class detector:
    def __init__(self,name,pos,lenx,leny,corner,edge):  #pos, corner and edge are arrays
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

#Intersection Function =====    
def intersect(inipoint,direction_vect,z_plane):
    point=[0.,0.,0.]
    for i in range(len(point)):
        point[i]=inipoint[i]+direction_vect[i]*((z_plane-inipoint[2])/direction_vect[2])
        if i == len(point):
            point[i]=z_plane
    return point

#If Intersection Function ===== 
def if_intersect(point,pos,lenx,leny):
    if pos[0]-lenx/2<=point[0]<=pos[0]+lenx/2 and pos[1]-leny/2<=point[1]<=pos[1]+leny/2:
        a=True
    else:
        a=False
    return a

#Cosmic Rays Array Function =====
def array_cosmic_rays(line_array,detectors):
    new_line_array=[]; intersections_array=[[],[]]  #Bottom/Top
    for i in range(len(line_array)):
        point=[]
        value=[]
        u=0
        for x in detectors:
            point.append(intersect(line_array[i].inipoint,line_array[i].direction_vect,x.pos[2]))
            value.append(if_intersect(point[u],x.pos,x.lenx,x.leny))
            u+=1
        if sum(value) == 2:
            new_line_array.append(line_array[i])
            for j in range(len(intersections_array)):
                intersections_array[j].append(point[j])
    return new_line_array, intersections_array

# Time Array Function =====
def time_array(detectors,new_line_array):
    time_detectors=[]                       #Bottom/Top
    time_flight=[]
    for i in range(len(detectors)):
        time_detectors.append([])
    #print(time_detectors)
    for i in range(len(new_line_array)):
        for j in range(len(detectors)):
            time_detectors[j].append((detectors[j].pos[2]-new_line_array[i].inipoint[2])/new_line_array[i].direction_vect[2])
    for i in range(len(new_line_array)):
        time_flight.append(time_detectors[0][i]-time_detectors[len(detectors)-1][i])
    return time_detectors, time_flight