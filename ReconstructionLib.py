#Reconstruction Lines Library
import math
import LinesLib

#Distance Function ======
def distance_R3(point1,point2):
    sum=0
    for i in range (len(point1)):
        sum+=(point1[i]-point2[i])**2
    d=math.sqrt(sum)
    return d

# Reconstructed Theta Function =====
def reconstructed_theta(z_bottom,z_top,distance):     #Bottom/Top
    new_theta=math.acos((z_bottom-z_top)/distance)
    return new_theta

def reconstructed_fi(x_bottom,x_top,z_bottom,z_top,distance):
    x_y_distance=math.sqrt((distance**2)-((z_bottom-z_top)**2))
    if (x_y_distance) != 0:
        fi=math.acos((x_top-x_bottom)/x_y_distance)
    else:
        fi=0
    return fi

def Energy_muon(velocity):
    velocity/=2.99792458E8
    mass=0.1057 #GeV/c^2
    return ((1/math.sqrt(1-(velocity**2)))-1)*mass

def reconstructed_line_array(transformed_intersections_array,new_time_detectors):
    reconstructed_line_array=[]
    #reconstructed_line=LinesLib.lines([0.,0.,0.],[0.,0.,0.],0,0,0)
    for i in range(len(transformed_intersections_array[0])):        # 0 - Bottom / 1 Top
        reconstructed_line_array.append(LinesLib.lines([0.,0.,0.],[0.,0.,0.],0,0,0))
        distance=distance_R3(transformed_intersections_array[0][i],transformed_intersections_array[1][i])
        velocity=distance/(new_time_detectors[0][i]-new_time_detectors[1][i])
        #print(f"velocity {velocity:E}       Speed of Light 2.99792458E+08")
        reconstructed_line_array[i].theta=reconstructed_theta(transformed_intersections_array[0][i][2],transformed_intersections_array[1][i][2],distance)
        reconstructed_line_array[i].fi=reconstructed_fi(transformed_intersections_array[0][i][0],transformed_intersections_array[1][i][0],transformed_intersections_array[0][i][2],transformed_intersections_array[1][i][2],distance)
        if velocity < 299792458:
            reconstructed_line_array[i].muon_energy=Energy_muon(velocity)
        else:
            reconstructed_line_array[i].muon_energy=0
        #print(f"Energy {reconstructed_line_array[i].muon_energy}")
        reconstructed_line_array[i].direction_vect[0]=math.sin(reconstructed_line_array[i].theta)*math.cos(reconstructed_line_array[i].fi)*velocity
        reconstructed_line_array[i].direction_vect[1]=math.sin(reconstructed_line_array[i].theta)*math.sin(reconstructed_line_array[i].fi)*velocity
        reconstructed_line_array[i].direction_vect[2]=-math.cos(reconstructed_line_array[i].theta)*velocity
        for j in range(len(reconstructed_line_array[i].inipoint)):
            reconstructed_line_array[i].inipoint[j]=transformed_intersections_array[0][j]-reconstructed_line_array[i].direction_vect[j]*new_time_detectors[0][i]
        #reconstructed_line_array.append(reconstructed_line)
    return reconstructed_line_array