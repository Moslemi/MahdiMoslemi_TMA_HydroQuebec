__author__ = "MAHDI MOSLEMI"
__email__ = "moslemi.mahdi@gmail.com"

import numpy as np
import csv
from operator import itemgetter
from interpolation import interpol
from cut_elements import check_element
from inside_polygon import inside
import math
from mpi4py import MPI
from sum_points import sum_points
import os

comm = MPI.COMM_WORLD

rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

    

if rank ==0:
    if not os.path.exists("OutPut"):
        os.mkdir("OUTPUT_FILES")

    
    with open ('INPUT_FILES/parameters.txt','r') as f:
        for x, line in enumerate(f):
            if x == 0:
                water_depth = line
                water_depth = water_depth.replace("\n","")
                water_depth = "InPut/"+ water_depth
            

            if x == 2:
                epsilon = float(line)

            if x == 3:
                alpha = float(line)

            if x == 4:
                new_points = line
                new_points = new_points.replace("\n","")
                new_points = "OUT_FILES/"+ new_points
                
            if x == 5:
                FOND = line
                FOND = FOND.replace("\n","")
                FOND = "INPUT_FILES/" + FOND

            if x ==6:
                B = str(line)
                B = B.replace("\n","")
                print(B)

            if x ==7:
                all_points = line
                all_points = all_points.replace("\n","")
                all_points = "OUTPUT_FILES/" + all_points

                
    with open ('INPUT_FILES/parameters.txt','r') as f3:
        csvf3 = csv.reader(f3 , delimiter = ' ')
        for x, line in enumerate(csvf3):
            if x==1:
                topology = line
                
                LT= len(topology)
                print(LT)
#Topology is a lidar data file




# this function is for finding bizard points inside the elements
# i , j , k are the free surface values(eta) for three vertices of each element
# A is a list of points inside each element


#open a file related to WATER DEPTH values



  #          print("epsilon",)

#READ VECTOR SOLUTION (either eta or H)

    with open(water_depth, 'r') as f1:
        for x, line in enumerate(f1):        #with enumerate function we make a relationship between 2 parameeters of (x and line). x is the number of the line, and line is the content of each line
            if "EndHeader" in line:
                num1 = x     # x is the number of the line which  coordinate with start

    with open(water_depth, 'r') as f1:
        for x, line in enumerate(f1):
            if "NodeCount" in line:
                num2 = x
    with open(water_depth, 'r') as f:
        for x, line in enumerate(f):
            if x == num2:                          # we want to find when the connectivities start and when they are finished
                total_nodes = float(line.split()[1])   # THIS IS THE TOTAL NUMBER OF NODES


                # READ ALL COORDINATES X, Y and the solution variable (eta or H)
    with open('OUTPUT_FILES/connect','w') as f3:
        with open(water_depth, "r") as f2:
            for x, line in enumerate(f2):
                if num1-2 < x <= (total_nodes +num1):
                    f3.write(line)

    with open('OUTPUT_FILES/connect', "r") as f:
        for x, line in enumerate(f):
            if x>=0:
                points = f.readlines()

    #we want to extract the connectivities of the elements
    with open(water_depth, 'r') as f1:
        for x, line in enumerate(f1):
            if "ElementCount" in line:
                num4 = x

    with open(water_depth, 'r') as f:
        p2 = f.readlines()


    with open(water_depth, 'r') as f:
        
        for x, line in enumerate(f):
            if x == num4:
                total_elements = float(line.split()[1])
                print(total_elements)



    #with open(topology,"r") as f3: 
     #   lidar = f3.readlines()
    


    
    

    
else:
    linenum = None
    water_depth = None
    topology = None
    epsilon = None
    alpha = None
    new_points = None 
    FOND = None
    B = None
    all_points = None
    points = None
    p2 = None
    total_nodes = None
    num1 = None
    total_elements = None
    #lidar = None
    LT = None

    
#lidar = comm.bcast(lidar,root=0)    
#linenum = comm.bcast(linenum,root=0)
water_depth = comm.bcast(water_depth,root=0)
topology= comm.bcast(topology,root=0)
epsilon = comm.bcast(epsilon,root=0)
alpha = comm.bcast(alpha,root=0)
new_points = comm.bcast(new_points,root=0)
FOND = comm.bcast(FOND,root=0)
B = comm.bcast(B,root=0)
all_points = comm.bcast(all_points,root=0)
points = comm.bcast(points,root=0)
p2 = comm.bcast(p2,root=0)
num1 = comm.bcast(num1,root=0)
total_nodes = comm.bcast(total_nodes,root=0)
total_elements = comm.bcast(total_elements,root=0)
LT = comm.bcast(LT,root=0)

if 0<=rank<LT:

    with open(new_points+str(rank),'a') as f:
        None

# open the lidar data. Each line of Lidar contains  x y z
    
    with open("INPUT_FILES/"+str(topology[int(rank)]),"r") as f3:
        lidar = f3.readlines()
    
        

    csvfile = csv.reader(p2, delimiter =' ')  #  Try to read old connectivities

    with open("OUTPUT_FILES/" + str(rank)+'log_file.txt','a') as flog:
        flog.write("epsilon=")
        flog.write(str(epsilon))
        flog.write("\n")

        flog.write("alpha=")
        flog.write(str(alpha))
        flog.write("\n")


    total_number_newpoints = 0
    for x, line in enumerate(csvfile):
        if num1+total_nodes < x <= num1+total_nodes+total_elements:
            with open("OUTPUT_FILES/" + str(rank)+'log_file.txt', 'a') as flog:
                flog.write("processing element=")
                flog.write(str(int(x-total_nodes-num1)))
                flog.write("\n")
            #a ,b,c are node numbers
            a = line[0]
            b = line[1]
            c = line[2]

    # pa,pb,pc are the nodes represented by x,y, eta or H
            pa = points[int(a)]
            pb = points[int(b)]
            pc = points[int(c)]
            cut_element = []
            # first find if the element is wet, dry, or cut elemets
            cut_element = check_element(pa, pb, pc,alpha,epsilon)

    # cut_element contains [(x1,y1),(x2,y2),(x3,y3),(x1,y1)] for defining the polygon
            with open("OUTPUT_FILES/"+str(rank)+'log_file.txt', 'a') as flog:
                flog.write("cut_element=")
                flog.write(str(cut_element))
                flog.write("\n")

            if cut_element != []:
                    #element = Polygon(cut_element)



            #we should do the loop for cut-elements only
            #we want to check all the lidar points to see if they are in the cut element
                A = []
                for nodes in lidar:
            # now we reduce the lidar nodes which we want to check for each element to the min(x1,x2,x3) and min(y1,y2,y3) till max(x1,x2,x3) and max(y1,y2,y3)
                    xmin = min(float(pa.split()[0]),float(pb.split()[0]),float(pc.split()[0]))
                    xmax = max(float(pa.split()[0]),float(pb.split()[0]),float(pc.split()[0]))
                    ymin = min(float(pa.split()[1]),float(pb.split()[1]),float(pc.split()[1]))
                    ymax = max(float(pa.split()[1]),float(pb.split()[1]),float(pc.split()[1]))



                    if ((xmin<float(nodes.split()[0])<xmax) and
                            (ymin<float(nodes.split()[1]) < ymax)):
                                    #coordList = Point([float(nodes.split()[0]), float(nodes.split()[1])])  # check if the lidar point is inside the rectangal
                        x1 = cut_element[0][0]
                        y1 = cut_element[0][1]
                        x2 = cut_element[1][0]
                        y2 = cut_element[1][1]
                        x3 = cut_element[2][0]
                        y3 = cut_element[2][1]

                        xsi, eta = inside(float(nodes.split()[0]),float(nodes.split()[1]),x1,y1,x2,y2,x3,y3)
                                # here we try to find if the the point is inside the element
                                    #if element.contains(coordList) is True:
                        if (0.0 < xsi < 1.0 and 0.0 < eta < 1.0):
                            d1 = math.sqrt(eta**2 + xsi**2)
                            d2 = math.sqrt((eta-1.0)**2 + xsi**2)
                            d3 = math.sqrt((xsi-1.0)**2+(eta**2))
                            if min(d1, d2, d3) > math.sqrt(2)/10.0:                # WE WANT TO AVOID OF COLLECTING POINTS WHICH ARE NEAR THE VERTICES
                                xnew = float(nodes.split()[0])
                                ynew = float(nodes.split()[1])
                                    # "A" is a list which contains all the lidar points inside th element



                                # We want to interpolate H for the Lidar point located in the element
                                Hnew = interpol(float(pa.split()[0]),float(pa.split()[1]),float(pa.split()[2]),float(pb.split()[0]),float(pb.split()[1]),float(pb.split()[2]),float(pc.split()[0]),float(pc.split()[1]),float(pc.split()[2]),xnew,ynew)

                                if Hnew < alpha*epsilon:                           # We changed abs(Hnew) with Hnew
                                    A = A+ [(xnew,ynew,float(nodes.split()[2]))]

                                        # done for the current element
                if A!=[]:
                    with open(new_points+str(rank), "a") as feta:

                                # we are trying to find the points which are  making bump(max of z) or valley(min of z)
                        feta.write(str(max(A,key=itemgetter(2))))
                        feta.write("\n")
                        total_number_newpoints= total_number_newpoints + 1
                        if max(A,key=itemgetter(2)) != min(A,key=itemgetter(2)):
                            feta.write(str(min(A,key=itemgetter(2))))
                            feta.write("\n")
                            total_number_newpoints = total_number_newpoints + 1
                            with open("OUTPUT_FILES/" + str(rank)+'log_file.txt', 'a') as flog:
                                flog.write("done with this cut_element=")
                                flog.write(str(cut_element))
                                flog.write("\n")
                                cut_element = []

    with open("OUTPUT_FILES/" + str(rank)+'log_file.txt', 'a') as flog:
        flog.write("processing element done")
        flog.write("\n")
        flog.write("total number points = ")
        flog.write(str(total_number_newpoints))
        flog.write("\n")


    

else:
    None


comm.barrier()

if rank ==0:
    with open(new_points,'a') as f:
        for i in range(0,LT,1):
            
            with open(new_points+str(i),'r') as f1:
                for x,line in enumerate(f1):
                    f.write(line)

    sum_points(all_points,FOND)

else:
    None

