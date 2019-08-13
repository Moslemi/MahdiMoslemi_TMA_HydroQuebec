__author__ = "MAHDI MOSLEMI"
__email__ = "moslemi.mahdi@gmail.com"

import numpy as np
import csv
def interpol(x1,y1,h1,x2,y2,h2,x3,y3,h3,x,y):

    determin = (x2*y3)-(x3*y2)+(x1*y2)-(x2*y1)

    N1 = (1/determin)*((x2*y3)-(x3*y2)+((y2-y3)*x)+((x3-x2)*y))
    N2 = (1/determin)*((x3*y1)-(x1*y3)+((y3-y1)*x)+((x1-x3)*y))
    N3 = (1/determin)*((x1*y2)-(x2*y1)+((y1-y2)*x)+((x2-x1)*y))

    return N1*h1 + N2*h2 + N3*h3

