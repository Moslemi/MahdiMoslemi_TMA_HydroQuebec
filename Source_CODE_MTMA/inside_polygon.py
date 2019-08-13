__author__ = "MAHDI MOSLEMI"
__email__ = "moslemi.mahdi@gmail.com"


def inside(x,y,x1,y1,x2,y2,x3,y3):
    import numpy as np
    from numpy.linalg import inv
    from numpy import matrix

    a = (x2-x1)
    b = (x3-x1)
    c = (y2-y1)
    d = (y3-y1)

    deteA = (a*d - b*c)

   
    B = (1/deteA) * np.matrix([[d, -b],[-c, a]]) * np.matrix(([x-x1], [y-y1]))
    xsi = B[0][0]
    eta = B[1][0]

    return xsi , eta

