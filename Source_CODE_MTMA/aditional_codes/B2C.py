from tkinter import *
from tkinter.filedialog import askopenfile, asksaveasfile, askopenfilename, askopenfilenames
from tkinter import filedialog
import csv

class BuckysButtons(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.label1 = Label(self, text="Please Choose The Bluekenue .bc2 file:")
        self.label1.grid(row=0, sticky=W)

        self.var1 = StringVar()
        self.entry1 = Entry(self, textvariable=self.var1)

        self.entry1.grid(row=0, column=1)

        self.browse1 = Button(self, text="Browse1", command=lambda: self.var1.set(filedialog.askopenfilename()))
        self.browse1.grid(row=0, column=2)

        self.RunButton = Button(self, text="Run", command=self.interface)
        self.RunButton.grid(row=3, column=2, pady=30)

    def get_string1(self):
        return self.entry1.get()

    def interface(self):
        url_boundary_bluekenue = self.get_string1()




# Nodes number and Coordinates

        with open(url_boundary_bluekenue, 'r') as f1:
            for x, line in enumerate(f1):
                if "BeginNodes" in line:
                    num1 = x

        with open(url_boundary_bluekenue, 'r') as f:
            for x, line in enumerate(f):
                if x == num1:
                    num2 = float(line.split()[1])


        with open(url_boundary_bluekenue, 'r') as f1:
            for x, line in enumerate(f1):
                if "BeginNodes" in line:
                    num5 = x

        with open('url_nodes', 'w') as f:
            with open(url_boundary_bluekenue, 'r') as f1:
                for i, line in enumerate(f1):
                    if num5 < i <= num2 + num5:
                        f.write(line)

# Table de connectivity and Elements number

        with open(url_boundary_bluekenue, 'r') as f1:
            for x, line in enumerate(f1):
                if "BeginElements" in line:
                    num3 = x

        with open(url_boundary_bluekenue, 'r') as f:
            for x, line in enumerate(f):
                if x == num3:
                    num4 = float(line.split()[1])

        with open(url_boundary_bluekenue, 'r') as f1:
            for x, line in enumerate(f1):
                if "EndHeader" in line:
                    num6 = x

        with open('url_connectivity_nodes', 'w') as f:
            with open(url_boundary_bluekenue, 'r') as f1:
                for i, line in enumerate(f1):
                    if num3 < i <= num3 + num4:
                        f.write(line)

# Inlet Nodes Number &&& List of Inlet Nodes

        with open ('inlet_list_file', 'w') as f1:
            with open(url_boundary_bluekenue, 'r') as f:
                for x , line in enumerate(f):
                    if "4 5 5" in line:


                        num_inlet = int(line.split()[11])
                        f1.write(str(num_inlet))
                        f1.write("\n")



# Outlet Nodes Number &&& List of Outlet Nodes

        with open('outlet_list_file' ,'w') as f2:
            with open(url_boundary_bluekenue, 'r') as f:
                for x, line in enumerate(f):
                    if "5 4 4" in line:




                        num_outlet = int(line.split()[11])
                        f2.write(str(num_outlet))
                        f2.write("\n")


# Wall Nodes Numbers and List of Wall Nodes

        with open(url_boundary_bluekenue, 'r') as f:
            for x, line in enumerate(f):
                if "BeginTable" in line:
                    num_wall = x

        with open(url_boundary_bluekenue, 'r') as f:
            for x, line in enumerate(f):
                if x == num_wall:
                    num_wall_nodes = int(line.split()[1])

        countline = 0
        with open('list_wall_nodes' , 'w') as f1:
            with open(url_boundary_bluekenue, 'r') as f:
                for x, line in enumerate(f):

                    if "0 0 0 0" in line:

                        wall_nodes = int(line.split()[11])
                        f1.write(str(wall_nodes))
                        f1.write('\n')
                        countline += 1




        with open('list_wall_nodes','r') as f2:
            filedata = f2.read()



        countline2 = 0
        with open('outlet_list_file', 'r') as f:
            for x , line in enumerate(f):
                countline2 += 1

        with open('outlet_list_file', 'r') as f:
            for x , line in enumerate(f):
                if 0 <x<countline2-1:
                    l1 = line
                    filedata = filedata.replace(l1 ,'')


        countline1 = 0
        with open('inlet_list_file', 'r') as f:
            for x , line in enumerate(f):
                countline1 += 1

        with open('inlet_list_file', 'r') as f:
            for x , line in enumerate(f):
                if 0 <x< countline1-1:
                    l2 = line
                    filedata = filedata.replace(l2 ,'')

        with open('list_wall_nodes','w') as f2:
            f2.write(filedata)

        count =0
        with open('list_wall_nodes','r') as f3:
            for x , line in enumerate(f3):
                count += 1

root = Tk()
root.title("Collect Nodes")
root.geometry('550x150')
b = BuckysButtons(root)
root.mainloop()


