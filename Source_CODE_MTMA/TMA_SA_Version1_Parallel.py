import os
import csv
from sum_points import sum_points
from operator import itemgetter
from interpolation import interpol
from cut_elements import check_element
from inside_polygon import inside
import math
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD

rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()


    
if rank ==0:

    if not os.path.exists("OUTPUT_FILES"):
        os.mkdir("OUTPUT_FILES")

    
    with open ('INPUT_FILES/parameters.txt','r') as f:
        for x, line in enumerate(f):
            if x == 0:
                water_depth = line
                water_depth = water_depth.replace("\n","")
                water_depth = "INPUT_FILES/"+water_depth

            if x == 2:
                epsilon = float(line)

            if x == 3:
                alpha = float(line)

            if x == 4:
                new_points = line
                new_points = new_points.replace("\n","")
                new_points = "OUTPUT_FILES/"+new_points
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
            


    with open ('INPUT_FILES/parameters.txt','r') as f3:
        csvf3 = csv.reader(f3 , delimiter = ' ')
        for x, line in enumerate(csvf3):
            if x==1:
                topology = line
                LT= len(topology)
                print(LT)

    


    



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


                    # READ ALL COORDINATES X, Y and the solution variable (eta or H)
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
                    flog.write(str(int(x -total_nodes- num1)))
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
                if max(abs(float(pa.split()[2])),abs(float(pb.split()[2])),abs(float(pc.split()[2]))) > 0.1:
                    cut_element_new = str(a+" "+b+" "+c)



                    # cut_element contains [(x1,y1),(x2,y2),(x3,y3),(x1,y1)] for defining the polygon
                    with open('OUTPUT_FILES/log_file2.txt', 'a') as flog:
                        #flog.write("cut_element=")
                        flog.write(str(cut_element_new))
                        flog.write("\n")
                        
    
           
    
    

    

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




    

    with open('OUTPUT_FILES/coordinate','w') as f3:
        with open(water_depth, "r") as f2:
            for x, line in enumerate(f2):
                if num1-2 < x <= (total_nodes +num1):
                    f3.write(line)

    with open('OUTPUT_FILES/coordinate', "r") as f:
        for x, line in enumerate(f):
            if x>=0:
                points = f.readlines()
    

    with open("OUTPUT_FILES/log_file2.txt","r") as f:
        p2 = f.readlines()
    
    
    #print(points[1])




    
else:
    water_depth = None
    topology = None
    epsilon = None
    alpha = None
    new_points = None 
    FOND = None
    B = None
    all_points = None
    water_depth_difference = None
    DH = None
    DH1 = None
    DH2 = None
    DH3 = None
    lidar = None
    points = None
    p2 = None
    LT = None
    DHanswer1 = None
    DHanswer2 = None
    DHanswer3 = None

    

water_depth = comm.bcast(water_depth,root=0)
topology= comm.bcast(topology,root=0)
epsilon = comm.bcast(epsilon,root=0)
alpha = comm.bcast(alpha,root=0)
new_points = comm.bcast(new_points,root=0)
FOND = comm.bcast(FOND,root=0)
B = comm.bcast(B,root=0)
all_points = comm.bcast(all_points,root=0)
water_depth_difference = comm.bcast(water_depth_difference,root=0)
DH = comm.bcast(DH,root=0)
DH1 = comm.bcast(DH1,root=0)
DH2 = comm.bcast(DH2,root=0)
DH3 = comm.bcast(DH3,root=0)
points = comm.bcast(points,root=0)
p2 = comm.bcast(p2,root=0)
LT = comm.bcast(LT,root=0)
DHanswer1 = comm.bcast(DHanswer1,root=0)
DHanswer2 = comm.bcast(DHanswer2,root=0)
DHanswer3 = comm.bcast(DHanswer3,root=0)



if 0<=rank<LT:

    with open(new_points+str(rank),'a') as f1:
        None

         
    with open("INPUT_FILES/"+str(topology[int(rank)]),"r") as f3:
        lidar = f3.readlines()    

   

    #we want to extract the connectivities of the elements


    #with open("log_file2.txt","r") as f:
    csvfile1 = csv.reader(p2, delimiter =' ')  #  Try to read old connectivities
    
    with open('OUTPUT_FILES/processor_'+str(rank)+'log_file3.txt','a') as flog:
        flog.write("epsilon=")
        flog.write(str(epsilon))
        flog.write("\n")

        flog.write("alpha=")
        flog.write(str(alpha))
        flog.write("\n")


        total_number_newpoints = 0
    with open('OUTPUT_FILES/processor_'+str(rank)+'log_file3.txt', 'a') as flog:
        for x , line in enumerate(csvfile1):
            if x>=0:
           
                flog.write("processing element=")
                flog.write("line"+str(int(x+1)))
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
                        with open(water_depth_difference,'r') as f:

                        # we are trying to find the points which are  making bump(max of z) or valley(min of z)
                            feta.write(str(max(A,key=itemgetter(2))))
                            feta.write("\n")
                            total_number_newpoints= total_number_newpoints + 1
                            if max(A,key=itemgetter(2)) != min(A,key=itemgetter(2)):
                                feta.write(str(min(A,key=itemgetter(2))))
                                feta.write("\n")
                                total_number_newpoints = total_number_newpoints + 1
                            


                            
                                points2=f.readlines()
                                pa2 = points2[int(a)]
                                pb2 = points2[int(b)]
                                pc2 = points2[int(c)]
                                DeltaH= max(abs(float(pa2.split()[2])),abs(float(pb2.split()[2])),abs(float(pc2.split()[2])))
                                    #' selecting max and min z for one step 
                                if DHanswer1 == "yes":
                                    if DH1<=DeltaH<DH2:
                                        A.remove(max(A,key=itemgetter(2)))
                                        if len(A)!=0:
                                            A.remove(min(A,key=itemgetter(2)))

                                            if len(A)!=0:
                                            
                                                AA1=max(A,key=itemgetter(2))
                                            
                                                feta.write(str(AA1))
                                                feta.write("\n")
                                                total_number_newpoints = total_number_newpoints + 1
                                                if max(A,key=itemgetter(2)) != min(A,key=itemgetter(2)):
                                                    AA2=min(A,key=itemgetter(2))
                                                    feta.write(str(AA2))
                                                    feta.write("\n")
                                                    total_number_newpoints = total_number_newpoints + 1
                                               
                                    #'selecting max and min for 2 step
                                if DHanswer2 == "yes":
                                    if  DH2<DeltaH<=DH3:
                                        A.remove(max(A,key=itemgetter(2)))
                                        if len(A)!=0:
                                            A.remove(min(A,key=itemgetter(2)))

                                            if len(A)!=0:
                                            
                                                AA1=max(A,key=itemgetter(2))
                                            
                                                feta.write(str(AA1))
                                                feta.write("\n")
                                                total_number_newpoints = total_number_newpoints + 1
                                                if max(A,key=itemgetter(2)) != min(A,key=itemgetter(2)):
                                                    AA2=min(A,key=itemgetter(2))
                                                    feta.write(str(AA2))
                                                    feta.write("\n")
                                                    total_number_newpoints = total_number_newpoints + 1

                                                    
                                                A.remove(max(A,key=itemgetter(2)))
                                                if len(A)!=0:
                                                    A.remove(min(A,key=itemgetter(2)))

                                                    if len(A)!=0:
                                                
                                                        AA1=max(A,key=itemgetter(2))
                                            
                                                        feta.write(str(AA1))
                                                        feta.write("\n")
                                                        total_number_newpoints = total_number_newpoints + 1
                                                        if max(A,key=itemgetter(2)) != min(A,key=itemgetter(2)):
                                                            AA2=min(A,key=itemgetter(2))
                                                            feta.write(str(AA2))
                                                            feta.write("\n")
                                                            total_number_newpoints = total_number_newpoints + 1
                                    
                                   # 'selecting max and min for 3 step
                                if DHanswer3 == "yes":
                                    if  DeltaH>DH3:
                                        A.remove(max(A,key=itemgetter(2)))
                                        
                                        if len(A)!=0:
                                            A.remove(min(A,key=itemgetter(2)))

                                            if len(A)!=0:    
                                                AA1=max(A,key=itemgetter(2))
                                            
                                                feta.write(str(AA1))
                                                feta.write("\n")
                                                total_number_newpoints = total_number_newpoints + 1
                                                if max(A,key=itemgetter(2)) != min(A,key=itemgetter(2)):
                                                    AA2=min(A,key=itemgetter(2))
                                                    feta.write(str(AA2))
                                                    feta.write("\n")
                                                    total_number_newpoints = total_number_newpoints + 1
                                                if len(A)!=0:
                                                    A.remove(max(A,key=itemgetter(2)))
                                                    if len(A)!=0:
                                                        if max(A,key=itemgetter(2)) != min(A,key=itemgetter(2)):    
                                                            A.remove(min(A,key=itemgetter(2)))
                                            


                                                            if len(A)!=0:
                                                                AA1=max(A,key=itemgetter(2))
                                            
                                                                feta.write(str(AA1))
                                                                feta.write("\n")
                                                                total_number_newpoints = total_number_newpoints + 1
                                                                if max(A,key=itemgetter(2)) != min(A,key=itemgetter(2)):
                                                                    AA2=min(A,key=itemgetter(2))
                                                                    feta.write(str(AA2))
                                                                    feta.write("\n")
                                                                    total_number_newpoints = total_number_newpoints + 1

                                                                    if len(A)!=0:
                                                                        A.remove(max(A,key=itemgetter(2)))
                                                                        if len(A)!=0:
                                                                            if max(A,key=itemgetter(2)) != min(A,key=itemgetter(2)):
                                                                                A.remove(min(A,key=itemgetter(2)))
                                                                                if len(A)!=0:
                                                                                    AA1=max(A,key=itemgetter(2))
                                            
                                                                                    feta.write(str(AA1))
                                                                                    feta.write("\n")
                                                                                    total_number_newpoints = total_number_newpoints + 1
                                                                        
                                                                                if max(A,key=itemgetter(2)) != min(A,key=itemgetter(2)):
                                                                                    AA2=min(A,key=itemgetter(2))
                                                                                    feta.write(str(AA2))
                                                                                    feta.write("\n")
                                                                                    total_number_newpoints = total_number_newpoints + 1
                                    
                                




    with open('OUTPUT_FILES/processor_'+str(rank)+'log_file3.txt', 'a') as flog:
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
        for i in range(1,size,1):
            with open(new_points+str(i),'r') as f1:
                for x,line in enumerate(f1):
                    f.write(line)

    sum_points(all_points,FOND)






