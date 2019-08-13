__author__ = "MAHDI MOSLEMI"
__email__ = "moslemi.mahdi@gmail.com"

from pandas import DataFrame, read_csv
import pandas as pd

with open ("divided_rectangular.txt","r") as f:
    for x,line in enumerate(f):
        if x==0:
            Location = line
            Location=Location.replace("\n","")
        if x ==1:
            Nx = int(line)
        if x==2:
            Ny = int(line)

df = pd.read_csv(Location, names=['X','Y','Z'],delimiter= ' ')
max_value_x = (df['X'].max())
min_value_x = (df['X'].min())
max_value_y = (df['Y'].max())
min_value_y = (df['Y'].min())


for i in range (1,Nx+1,1):
    for j in range(1,Ny+1,1):
        with open(Location+"_"+str(i)+"_"+str(j),"w") as f1:
            with open(Location,"r") as f2:
                for x ,line in enumerate(f2):
                    if ((min_value_x +(i-1)*(max_value_x - min_value_x)/Nx<=float(line.split()[0]) <= (min_value_x +(i*(max_value_x - min_value_x)/Nx)) and
                        (min_value_y +(j-1)*(max_value_y - min_value_y)/Ny<=float(line.split()[1]) <= (min_value_y +(j*(max_value_y - min_value_y)/Ny))))):
                        f1.write(line)
            

                
           
 
