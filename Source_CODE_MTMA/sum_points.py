

def sum_points(all_points , GEO_t3s):

    

    with open('INPUT_FILES/parameters.txt', 'r') as f:
        for x, line in enumerate(f):
            if x == 4:
                new_points = line
                new_points = new_points.replace("\n","")
                new_points = "OutPut/" + new_points

    


    with open(all_points,'w') as f3:            #All points is the file which we want all of the point written inside it
        with open(GEO_t3s,"r") as f:
            for x, line in enumerate(f):
                if "EndHeader" in line:
                    num1 = x

        with open(GEO_t3s, 'r') as f:
            for x, line in enumerate(f):
                if "NodeCount" in line:
                    num2 = x
        with open(GEO_t3s, 'r') as f:
            for x, line in enumerate(f):
                if x == num2:  # we want to find when the connectivities start and when they are finished
                    total_nodes = float(line.split()[1])  # THIS IS THE TOTAL NUMBER OF NODES


                    # READ ALL COORDINATES X, Y and the solution variable (eta or H)
        with open(GEO_t3s, "r") as f:
            for x, line in enumerate(f):
                if num1 < x <= (total_nodes + num1):
                    f3.write(line)

        with open(new_points,'r') as f:
            filedata = f.read()

            filedata = filedata.replace("(","")
            filedata = filedata.replace(")", "")
            filedata = filedata.replace(",", "")
            f3.write(filedata)

#sum_points("all_points_14_alpha_2","FOND_13_alpha_40.t3s")
