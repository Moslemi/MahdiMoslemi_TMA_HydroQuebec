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
        self.label1 = Label(self, text="Please select input file(file.t3s):")
        self.label1.grid(row=0, sticky=W)

        self.var1 = StringVar()
        self.entry1 = Entry(self, textvariable=self.var1)

        self.entry1.grid(row=0, column=1)

        self.browse1 = Button(self, text="Browse1", command=lambda: self.var1.set(filedialog.askopenfilename()))
        self.browse1.grid(row=0, column=2)

        self.RunButton = Button(self, text="Run", command=self.FindNodes)
        self.RunButton.grid(row=3, column=2, pady=30)



    def get_string1(self):
        return self.entry1.get()




    def FindNodes(self):
        url_node_mesh = self.get_string1()

        with open(url_node_mesh, 'r') as f1:
            for x, line in enumerate(f1):
                if "NodeCount" in line:
                    num1 = x

        with open(url_node_mesh, 'r') as f:
            for x, line in enumerate(f):
                if x == num1:
                    num2 = float(line.split()[1])

        with open(url_node_mesh, 'r') as f1:
            for x, line in enumerate(f1):
                if "EndHeader" in line:
                    num3 = x

        with open('nodes.txt', 'w') as f:
            with open(url_node_mesh, 'r') as f1:
                for i, line in enumerate(f1):
                    if num3 < i <= num2 + num3:
                        f.write(line)


root = Tk()
root.title("Collect Nodes")
root.geometry('550x250')
b = BuckysButtons(root)
root.mainloop()

