import csv


                
def check_element(i,j,k,alpha,epsilon):

    with open('INPUT_FILES/parameters.txt', 'r') as f:
        for x, line in enumerate(f):
            if x == 2:
                epsilon = float(line)

            if x == 3:
                alpha = float(line)

            icount = 0
            if float(i.split()[2]) < alpha * epsilon:
                icount = icount + 1
            if float(j.split()[2]) < alpha * epsilon:
                icount = icount + 1
            if float(k.split()[2]) < alpha * epsilon:
                icount = icount + 1

        if (icount == 1 or icount == 2):

# I returned the polygon related to the cut_element
            return [(float(i.split()[0]), (float(i.split()[1]))), (float(j.split()[0]), (float(j.split()[1]))),
                   (float(k.split()[0]), (float(k.split()[1]))), (float(i.split()[0]), (float(i.split()[1])))]

        else:
            return []


