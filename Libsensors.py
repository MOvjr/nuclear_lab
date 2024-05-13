#Library for sensors
import numpy as np
import random
#Sensors Object =====
class sensors:
    def __init__(self,array_sensors,long_x,long_y,longx_sensor,longy_sensor,Turn,Random_turn):
        self.array_sensors=array_sensors
        self.long_x=long_x
        self.long_y=long_y
        self.longx_sensor=longx_sensor
        self.longy_sensor=longy_sensor
        self.Turn=Turn
        self.Random_turn=Random_turn

    def create_sensors(self):
        i_sensor=round(self.long_x/self.longx_sensor)
        j_sensor=round(self.long_y/self.longy_sensor)
        self.array_sensors=np.zeros((i_sensor,j_sensor),dtype=list)
        self.Turn=np.zeros((i_sensor,j_sensor),dtype=list)
        for i in range(i_sensor):
            for j in range(j_sensor):
                self.array_sensors[i,j]=[(i+0.5)*self.longx_sensor,(j+0.5)*self.longy_sensor,0]
                if self.Random_turn == "YES":
                    r=random.randint(0,1)
                    if r == 1:
                        self.Turn[i,j]="ON"
                    else:
                        self.Turn[i,j]="OFF"
                else:
                        self.Turn[i,j]="ON"
        return self.array_sensors
    
    def check_inside(self,point_R3,z_detector):  #We check if a random point is inside the bounds of the sensor
        new_point_R3=[0.,0.,z_detector]
        for i in range(len(self.array_sensors)):
            for j in range(len(self.array_sensors[0])):
                if abs(point_R3[0]-self.array_sensors[i][j][0]) <= self.longx_sensor/2:
                    new_point_R3[0]=self.array_sensors[i][j][0]
                if abs(point_R3[1]-self.array_sensors[i][j][1]) <= self.longy_sensor/2:
                    new_point_R3[1]=self.array_sensors[i][j][1]
        return new_point_R3

# Transform Intersections Function =====    
def transform_intersections(intersections_array,sensors_array):
    transformed_intersections_array=[[],[]]
    for i in range(len(intersections_array)):
        for j in range(len(intersections_array[0])):
                transformed_intersections_array[i].append(sensors_array[i].check_inside(intersections_array[i][j],intersections_array[i][j][2]))
    return transformed_intersections_array

#Random 
