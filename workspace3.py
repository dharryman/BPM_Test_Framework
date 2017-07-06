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
    kx = 1
    x = kx*(diff/total)
    return x

def calc_y_pos(a,b,c,d):
    diff = ((a+b)-(c+d))
    total = (a+b+c+d)
    ky = 1
    y = ky*(diff/total)
    return y

x_plot = []
y_plot = []

gradient = np.linspace(0.001,10,4)
inv_gradient = gradient[::-1]
a = gradient
b = inv_gradient
c = inv_gradient
d = gradient

a_total = []
b_total = []
c_total = []
d_total = []


for index in np.linspace(-5,5,4): # number of Y samples
    offset = 5 # base power from the device
    a_total = np.append(a_total, (a+index)+offset)
    b_total = np.append(b_total, (b+index)+offset)
    c_total = np.append(c_total, (c-index)+offset)
    d_total = np.append(d_total, (d-index)+offset)

for A,B,C,D in zip(a_total,b_total,c_total,d_total):
    abcd_total = A + B + C + D

    A = round(A/ abcd_total, 2)
    B = round(B/ abcd_total, 2)
    C = round(C/ abcd_total, 2)
    D = round(D/ abcd_total, 2)

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
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.show()
