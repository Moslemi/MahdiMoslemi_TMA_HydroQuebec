
with open("divided_line_by_line.txt","r") as f:
    for x,line in enumerate(f):
        if x ==0:
            file = str(line)
            file = file.replace("\n","")
        if x==1:
            N = int(line)

            
num = 0
with open (file , "r") as f:
    for x, line in enumerate(f) :
        num = num+1
print(num)

for i in range (1,N+1,1):
    with open(file+"_"+str(i),"w") as f1:
        with open (file , "r") as f:
            for x,line in enumerate(f):
                if (i-1)/6*num<=x<(i/6)*num:
                    f1.write(line)
                              
