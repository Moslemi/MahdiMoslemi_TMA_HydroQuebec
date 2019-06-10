from tkinter import *
from tkinter.filedialog import askopenfile, asksaveasfile, askopenfilename, askopenfilenames
from tkinter import filedialog
import csv


class BuckysButtons(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()





        # def Ask_import_Path(self):
        #   self.filenames = filedialog.askopenfilename()
        #  sourceFiles = os.listdir(filenames)
        # for fileName in sourceFiles:
        #    fullName = os.path.join(filenames, fileName)

    #
    #           return open(fullName, 'r')



    #  def Ask_Savefile_path(self):
    #     self.filename = filedialog.asksaveasfilename()
    #
    #       if filename:
    #          return open(filename, 'w')

    def create_widgets(self):
        self.label1 = Label(self, text="Please select input:")
        self.label1.grid(row=0, sticky=W)

        self.var1 = StringVar()
        self.entry1 = Entry(self, textvariable=self.var1)

        self.entry1.grid(row=0, column=1)

        self.browse1 = Button(self, text="Browse1", command=lambda: self.var1.set(filedialog.askopenfilename()))
        self.browse1.grid(row=0, column=2)

        self.label2 = Label(self, text="Please select output:")
        self.label2.grid(row=1, column=0, sticky=W)

        self.var2 = StringVar()
        self.entry2 = Entry(self, textvariable=self.var2)

        self.entry2.grid(row=1, column=1)
        self.browse2 = Button(self, text="Browse2", command=lambda: self.var2.set(filedialog.asksaveasfilename()))
        self.browse2.grid(row=1, column=2)

        self.var3 = StringVar()
        self.entry3 = Entry(self, textvariable=self.var3)
        self.entry3.grid(row=2, column=1, sticky=W)

        self.browse3 = Button(self, text="Browse3", command=lambda: self.var3.set(filedialog.askopenfilename()))
        self.browse3.grid(row=2, column=2)

        self.undolabel3 = Label(self, text="Would you like to clean your nodes ?")
        self.undolabel3.grid(row=2, column=0, sticky=W)

        self.label4 = Label(self, text="Would you like to have a header ? ")
        self.label4.grid(row=3, column=0, sticky=W)

        self.radiobutton1 = Radiobutton(self, text="Yes", value=1, variable=1, command=self.Active_Header)
        self.radiobutton1.grid(row=3, column=1, sticky=W)

        self.radiobutton2 = Radiobutton(self, text="No", value=0, variable=1)
        self.radiobutton2.grid(row=3, column=1)

        self.RunButton = Button(self, text="Run", command=self.copytextfunc)
        self.RunButton.grid(row=3, column=2, pady=30)

        self.undobutton1 = Button(self, text="Substract Nodes", command=self.substractnodes)
        self.undobutton1.grid(row=3, column=2, sticky=S)

    def get_string1(self):
        return self.entry1.get()

    def get_string2(self):
        return self.entry2.get()

    def get_string3(self):
        return self.entry3.get()

    def substractnodes(self):

        url_clean_nodes = self.get_string3()
        with open(url_clean_nodes, 'r') as f1:
            for x, line in enumerate(f1):
                if "NodeCount" in line:
                    num1 = x

        with open(url_clean_nodes, 'r') as f:
            for x, line in enumerate(f):
                if x == num1:
                    num2 = float(line.split()[1])

        with open(url_clean_nodes, 'r') as f1:
            for x, line in enumerate(f1):
                if "EndHeader" in line:
                    num3 = x

        url_new_mesh = self.get_string2()
        filedata = None
        with open(url_new_mesh, 'r') as file:
            filedata = file.read()

        with open(url_clean_nodes, 'r') as f1:
            for i, line in enumerate(f1):
                if num3 < i <= num2 + num3:
                    filedata = filedata.replace(line, '')

        with open(url_new_mesh, 'w') as file:
            file.write(filedata)

    def Active_Header(self):
        url_new_mesh = self.get_string2()
        with open(url_new_mesh, 'a') as csvfile:
            self.writer = csv.DictWriter(csvfile, fieldnames=["X", "Y", "Z"], delimiter=' ')
            self.writer.writeheader()

    def copytextfunc(self):
        url_node_mesh = self.get_string1()
        url_new_mesh = self.get_string2()

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

        with open(url_new_mesh, 'a') as f:
            with open(url_node_mesh, 'r') as f1:
                for i, line in enumerate(f1):
                    if num3 < i <= num2 + num3:
                        f.write(line)


root = Tk()
root.title("Sum and Subtract Nodes")
root.geometry('550x250')
b = BuckysButtons(root)
root.mainloop()

