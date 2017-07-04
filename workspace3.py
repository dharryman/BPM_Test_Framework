import itertools
from pkg_resources import require
require("numpy")
require("cothread")
require("matplotlib")
import matplotlib.pyplot as plt
import numpy as np
import time

count = 0

def calc_x_pos(a,b,c,d):
    diff = ((a+d)-(b+c))
    total = (a+b+c+d)
    kx = 10.0
    x = kx*(diff/total)
    return x

def calc_y_pos(a,b,c,d):
    diff = ((a+b)-(c+d))
    total = (a+b+c+d)
    ky = 10.0
    y = ky*(diff/total)
    return y

x_plot = []
y_plot = []

a = np.linspace(0.0,0.666,4) #number of X samples
b = a[::-1]
c = b
d = a

a_total = []
b_total = []
c_total = []
d_total = []

for index in np.linspace(-.333,.333,4): # number of Y samples
    a_total = np.append(a_total, a+index)
    b_total = np.append(b_total, b+index)
    c_total = np.append(c_total, c-index)
    d_total = np.append(d_total, d-index)

for A,B,C,D in zip(a_total,b_total,c_total,d_total):
    print A,B,C,D
    new_x = calc_x_pos(A,B,C,D)
    new_y = calc_y_pos(A,B,C,D)
    x_plot.append(new_x)
    y_plot.append(new_y)
    count = count + 1

# plt.plot(a_total)
# plt.plot(b_total)
# plt.plot(c_total)
# plt.plot(d_total)

plt.scatter(x_plot,y_plot,s=10, c='r', marker = u'+')
plt.show()
