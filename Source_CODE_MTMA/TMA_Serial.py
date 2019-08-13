 __author__ = "MAHDI MOSLEMI"
__email__ = "moslemi.mahdi@gmail.com"
  
  ### THIS CODE IS WRITTEN BY "MAHDI MOSLEMI", MASTER STUDENT (WITH THESIS) OF MECHANICAL ENGINEERING, ECOLE DE TECHNOLOGIES SUPERRIOR ###
import os
import csv
from sum_points import sum_points
from operator import itemgetter
from interpolation import interpol
from cut_elements import check_element
from inside_polygon import inside
import math
import numpy as np
import random

if not os.path.exists("OUTPUT_FILES"):
    os.mkdir("OUTPUT_FILES")
    
with open ('INPUT_FILES/parameters.txt','r') as f:
    for x, line in enumerate(f):
        if x == 0:
            water_depth = line
            water_depth = water_depth.replace("\n","")
            water_depth = "INPUT_FILES/" + water_depth
            
        if x == 1:
            topology = line                 # TOPOLOGY IS A LIDAR DATA FILE
            topology = topology.replace("\n","")
            topology = "INPUT_FILES/" + topology
            
        if x == 2:
            epsilon = float(line)

        if x == 3:
            alpha = float(line)

        if x == 4:
            new_points = line
            new_points = new_points.replace("\n","")
            new_points = "OUTPUT_FILES/"+ new_points

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

        if x ==8:
            water_depth_difference = line
            water_depth_difference = water_depth_difference.replace("\n","")
            water_depth_difference = "INPUT_FILES/" + water_depth_difference

        if x == 9:
            DH = float(line)
                
        if x == 10:
            DH1 = float(line.split()[0])
            DHanswer1 = line.split()[1]
        if x == 11:
            DH2 = float(line.split()[0])
            DHanswer2 = line.split()[1]
        if x == 12:
            DH3 = float(line.split()[0])
            DHanswer3 = line.split()[1]
            
        
            
if B == "first":

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


                # READ ALL COORDINATES X, Y and the solution variable (H)
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
        for x, line in enumerate(f):
            if x == num4:
                total_elements = float(line.split()[1])




    # open the lidar data. Each line of Lidar contains  x y z
    with open(topology, "r") as f3:
        lidar = f3.readlines()



    with open(water_depth,"r") as f:
        csvfile = csv.reader(f, delimiter =' ')  #  Try to read old connectivities

        with open('OUTPUT_FILES/log_file.txt','a') as flog:
            flog.write("epsilon=")
            flog.write(str(epsilon))
            flog.write("\n")

            flog.write("alpha=")
            flog.write(str(alpha))
            flog.write("\n")


        total_number_newpoints = 0
        for x, line in enumerate(csvfile):
            if num1+total_nodes < x <= num1+total_nodes+total_elements:
                with open('OUTPUT_FILES/log_file.txt', 'a') as flog:
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
                cut_element = check_element(pa, pb, pc,alpha, epsilon)

    # cut_element contains [(x1,y1),(x2,y2),(x3,y3),(x1,y1)] for defining the polygon
                with open('OUTPUT_FILES/log_file.txt', 'a') as flog:
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
                            # "A" is a list which contains all the lidar points inside th element which are dry



                        # We want to interpolate H for the Lidar point located in the element
                                    Hnew = interpol(float(pa.split()[0]),float(pa.split()[1]),float(pa.split()[2]),float(pb.split()[0]),float(pb.split()[1]),float(pb.split()[2]),float(pc.split()[0]),float(pc.split()[1]),float(pc.split()[2]),xnew,ynew)

                                    if Hnew < alpha*epsilon:                           # MAYBE IT IS BETTER TO REMOVE THIS LINE
                                        A = A+ [(xnew,ynew,float(nodes.split()[2]))]

                                # done for the current element
                    if A!=[]:
                        with open(new_points, "a") as feta:

                        # we are trying to find the points which are  making bump(max of z) or valley(min of z)
                            feta.write(str(max(A,key=itemgetter(2))))
                            feta.write("\n")
                            total_number_newpoints= total_number_newpoints + 1
                            if max(A,key=itemgetter(2)) != min(A,key=itemgetter(2)):
                                feta.write(str(min(A,key=itemgetter(2))))
                                feta.write("\n")
                                total_number_newpoints = total_number_newpoints + 1
                                with open('OUTPUT_FILES/log_file.txt', 'a') as flog:
                                    flog.write("done with this cut_element=")
                                    flog.write(str(cut_element))
                                    flog.write("\n")
                                    cut_element = []

    with open('OUTPUT_FILES/log_file.txt', 'a') as flog:
        flog.write("processing element done")
        flog.write("\n")
        flog.write("total number points = ")
        flog.write(str(total_number_newpoints))
        flog.write("\n")


    sum_points(all_points,FOND)




        
if B == "second":
    
    #water_depth_difference = 'error.t3s'
    with open(water_depth_difference, 'r') as f1:
        for x, line in enumerate(f1):  # with enumerate function we make a relationship between 2 parameeters of (x and line). x is the number of the line, and line is the content of each line
            if "EndHeader" in line:
                num1 = x  # x is the number of the line which  coordinate with start

    with open(water_depth_difference, 'r') as f1:
        for x, line in enumerate(f1):
            if "NodeCount" in line:
                num2 = x
    with open(water_depth_difference, 'r') as f:
        for x, line in enumerate(f):
            if x == num2:  # we want to find when the connectivities start and when they are finished
                total_nodes = float(line.split()[1])  # THIS IS THE TOTAL NUMBER OF NODES


                    # READ ALL COORDINATES X, Y and the solution variable (Delta H max)
    with open('OUTPUT_FILES/connect', 'w') as f3:
        with open(water_depth_difference, "r") as f2:
            for x, line in enumerate(f2):
                if num1 - 2 < x <= (total_nodes + num1):
                    f3.write(line)

    with open('OUTPUT_FILES/connect', "r") as f:
        for x, line in enumerate(f):
            if x >= 0:
                points_new = f.readlines()

        # we want to extract the connectivities of the elements
    with open(water_depth_difference, 'r') as f1:
        for x, line in enumerate(f1):
            if "ElementCount" in line:
                num4 = x

    with open(water_depth_difference, 'r') as f:
        for x, line in enumerate(f):
            if x == num4:
                total_elements = float(line.split()[1])

        # open the lidar data. Each line of Lidar contains  x y z
    #with open(topology, "r") as f3:
     #   lidar = f3.readlines()

    with open(water_depth_difference, "r") as f:
        csvfile = csv.reader(f, delimiter=' ')  # Try to read old connectivities



        for x, line in enumerate(csvfile):
            if num1 + total_nodes < x <= num1 + total_nodes + total_elements:
                with open('OUTPUT_FILES/log_file.txt', 'a') as flog:
                    flog.write("processing element=")
                    flog.write(str(int(x - total_nodes - num1)))
                    flog.write("\n")
                        # a ,b,c are node numbers
                a = line[0]
                b = line[1]
                c = line[2]

                    # pa,pb,pc are the nodes represented by x,y, eta or H
                pa = points_new[int(a)]
                pb = points_new[int(b)]
                pc = points_new[int(c)]
                cut_element_new = []
                    # first find if the element is wet, dry, or cut elemets
                if max(abs(float(pa.split()[2])),abs(float(pb.split()[2])),abs(float(pc.split()[2]))) > DH:
                    cut_element_new = str(a+" "+b+" "+c)



                    # cut_element contains [(x1,y1),(x2,y2),(x3,y3),(x1,y1)] for defining the polygon
                    with open('OUTPUT_FILES/log_file2.txt', 'a') as flog:
                        #flog.write("cut_element=")
                        flog.write(str(cut_element_new))
                        flog.write("\n")


    

                
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
    with open('OUTPUT_FILES/coordinate','w') as f3:
        with open(water_depth, "r") as f2:
            for x, line in enumerate(f2):
                if num1-2 < x <= (total_nodes +num1):
                    f3.write(line)

    with open('OUTPUT_FILES/coordinate', "r") as f:
        for x, line in enumerate(f):
            if x>=0:
                points = f.readlines()





    # open the lidar data. Each line of Lidar contains  x y z
    with open(topology, "r") as f3:
        lidar = f3.readlines()

    #we want to extract the connectivities of the elements


    with open("OUTPUT_FILES/log_file2.txt","r") as f:
        csvfile = csv.reader(f, delimiter =' ')  #  Try to read old connectivities

        with open('OUTPUT_FILES/log_file3.txt','a') as flog:
            flog.write("epsilon=")
            flog.write(str(epsilon))
            flog.write("\n")

            flog.write("alpha=")
            flog.write(str(alpha))
            flog.write("\n")


        total_number_newpoints = 0
        for x, line in enumerate(csvfile):
            if x>=0:
                with open('OUTPUT_FILES/log_file3.txt', 'a') as flog:
                    flog.write("processing element=")
                    flog.write("line"+str(int(x+1)))
                    flog.write("\n")
            #a ,b,c are node numbers
                a = line[0]
                b = line[1]
                c = line[2]

    # pa,pb,pc are the nodes represented by x,y,  H
                pa = points[int(a)]
                pb = points[int(b)]
                pc = points[int(c)]
                cut_element = []
            # first find if the element is wet, dry, or cut elemets
                cut_element = check_element(pa, pb, pc,alpha, epsilon)

    # cut_element contains [(x1,y1),(x2,y2),(x3,y3),(x1,y1)] for defining the polygon
                with open('OUTPUT_FILES/log_file3.txt', 'a') as flog:
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

                                    if Hnew < alpha*epsilon:                           
                                        A = A+ [(xnew,ynew,float(nodes.split()[2]))]

                                # done for the current element
                    if A!=[]:
                        with open(new_points, "a") as feta:

                        # we are trying to find the points which are  making bump(max of z) or valley(min of z)
                            feta.write(str(max(A,key=itemgetter(2))))
                            feta.write("\n")
                            total_number_newpoints= total_number_newpoints + 1
                            if max(A,key=itemgetter(2)) != min(A,key=itemgetter(2)):
                                feta.write(str(min(A,key=itemgetter(2))))
                                feta.write("\n")
                                total_number_newpoints = total_number_newpoints + 1
                                with open(water_depth_difference,'r') as f:
                                    points2=f.readlines()
                                    pa2 = points2[int(a)]
                                    pb2 = points2[int(b)]
                                    pc2 = points2[int(c)]
                                    DeltaH= max(abs(float(pa2.split()[2])),abs(float(pb2.split()[2])),abs(float(pc2.split()[2])))
                                    if DHanswer1 == "yes":
                                        if DH1<=DeltaH<DH2:
                                            A.remove(max(A,key=itemgetter(2)))
                                            A.remove(min(A,key=itemgetter(2)))
                                            random.shuffle(A)
                                            AA=len(A)
                                            for j in range(1,3,1):
                                                if j<=AA:
                                                    feta.write(str(A[j-1]))
                                                    feta.write("\n")
                                                    total_number_newpoints = total_number_newpoints + 1

                                    if DHanswer2 == "yes":
                                        if  DH2<DeltaH<=DH3:
                                            A.remove(max(A,key=itemgetter(2)))
                                            A.remove(min(A,key=itemgetter(2)))
                                            random.shuffle(A)
                                            
                                            for j in range(1,5,1):
                                                if j<=AA:
                                                    feta.write(str(A[j-1]))
                                                    feta.write("\n")
                                                    total_number_newpoints = total_number_newpoints + 1

                                    if DHanswer3 == "yes":
                                        if  DeltaH>DH3:
                                            A.remove(max(A,key=itemgetter(2)))
                                            A.remove(min(A,key=itemgetter(2)))
                                            random.shuffle(A)
                                            for j in range(1,7,1):
                                                if j<=AA:
                                                    feta.write(str(A[j-1]))
                                                    feta.write("\n")
                                                    total_number_newpoints = total_number_newpoints + 1
                                    
                                    with open('OUTPUT_FILES/log_file3.txt', 'a') as flog:
                                        flog.write("done with this cut_element=")
                                        flog.write(str(cut_element))
                                        flog.write("\n")
                                        cut_element = []

    with open('OUTPUT_FILES/log_file3.txt', 'a') as flog:
        flog.write("processing element done")
        flog.write("\n")
        flog.write("total number points = ")
        flog.write(str(total_number_newpoints))
        flog.write("\n")


    sum_points(all_points,FOND)


