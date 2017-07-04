# application boilerplate
import RFSignalGenerators
import BPMDevice
import Gate_Source
import ProgrammableAttenuator
import Tests
import Latex_Report
import time
import telnetlib
from pkg_resources import require
require("numpy")
require("cothread")
require("matplotlib")
import matplotlib.pyplot as plt
import itertools


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

# Init real devices
#BPM = BPMDevice.Libera_BPMDevice(4)
BPM = BPMDevice.SparkERXR_EPICS_BPMDevice("libera", "fa")
limit = BPM.get_input_tolerance()
RF = RFSignalGenerators.Rigol3030DSG_RFSigGen("172.23.252.51", 5555, 1, limit)
PA = ProgrammableAttenuator.MC_RC4DAT6G95_Prog_Atten("172.23.244.105", 23, 0.1)

RF.set_output_power(-40)
RF.set_frequency(499.6817682)
RF.turn_on_RF()

predicted_x = []
predicted_y = []
measured_x = []
measured_y = []

attenuation_map =  itertools.product([10,30,50], repeat=4)
count = 0
for index in attenuation_map:
    PA.set_channel_attenuation("A", index[0])
    PA.set_channel_attenuation("B", index[1])
    PA.set_channel_attenuation("C", index[2])
    PA.set_channel_attenuation("D", index[3])
    time.sleep(0.5)
    measured_x.append(BPM.get_X_position())
    measured_y.append(BPM.get_Y_position())

    predicted_a = index[0]
    predicted_b = index[1]
    predicted_c = index[2]
    predicted_d = index[3]
    predicted_a = 10 ** (predicted_a / 10.0)
    predicted_b = 10 ** (predicted_b / 10.0)
    predicted_c = 10 ** (predicted_c / 10.0)
    predicted_d = 10 ** (predicted_d / 10.0)
    predicted_x.append(calc_x_pos(predicted_a, predicted_b, predicted_c, predicted_d))
    predicted_y.append(calc_y_pos(predicted_a, predicted_b, predicted_c, predicted_d))
    count = count + 1
    print count

plt.scatter(measured_x,measured_y,s=50)
plt.scatter(predicted_x,predicted_y,s=100, c='r', marker = u'+')
plt.xlim(-11, 11)
plt.ylim(-11, 11)
plt.show()


















