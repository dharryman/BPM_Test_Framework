import RFSignalGenerators
import BPMDevice
import ProgrammableAttenuator
from pkg_resources import require

require("numpy")
require("cothread")
require("matplotlib")
import numpy as np
import matplotlib.pyplot as plt
import time
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

def Beamposition_raster_scan_test(RF,
             BPM,
             PA,
             rf_power,
             rf_frequency,
             attenuator_max,
             attenuator_min,
             attenuator_steps,
             report=None):
    """One line introduction to the test
    A more detailed introduction to the test, this can be over multiple lines
    Args:
        RF (RFSignalGenerator Obj): RF interface object.
        BPM (BPMDevice Obj): BPM interface object.
        argument1 (argument type): detail of what the argument is and what it's used for.
        argument2 (argument type): detail of what the argument is and what it's used for.
        argument3 (argument type): detail of what the argument is and what it's used for.
        argument4 (argument type): detail of what the argument is and what it's used for.
        report (LaTeX Report Obj):
    Returns:
        float array: Values of the X axis on the graph shown
        float array: Values of the Y axis on the graph shown 
    """

    # Readies text that will introduce this test in the report
    intro_text = r"This is a template test"

    # Formats the name of plot that is saved as, and also informs the user that the test has started
    test_name = __name__
    test_name = test_name.rsplit("Tests.")[1]
    test_name = test_name.replace("_", " ")
    print("Starting test \"" + test_name + "\"")

    RF.set_output_power(rf_power)
    RF.set_frequency(rf_frequency)
    RF.turn_on_RF()

    predicted_x = []
    predicted_y = []
    measured_x = []
    measured_y = []

    attenuation_map = np.linspace(attenuator_min,attenuator_max,attenuator_steps)

    attenuation_map = itertools.product(attenuation_map, repeat=4)

    count = 0

    for index in attenuation_map:
        PA.set_channel_attenuation("A", index[0])
        PA.set_channel_attenuation("B", index[1])
        PA.set_channel_attenuation("C", index[2])
        PA.set_channel_attenuation("D", index[3])
        time.sleep(1)
        measured_x.append(BPM.get_X_position())
        measured_y.append(BPM.get_Y_position())

        predicted_a = index[2] # Swop with opposites, this is because they are attenuation not power totals
        predicted_b = index[3]
        predicted_c = index[1]
        predicted_d = index[0]
        predicted_a = 10 ** (predicted_a / 10.0)
        predicted_b = 10 ** (predicted_b / 10.0)
        predicted_c = 10 ** (predicted_c / 10.0)
        predicted_d = 10 ** (predicted_d / 10.0)
        predicted_x.append(calc_x_pos(predicted_a, predicted_b, predicted_c, predicted_d))
        predicted_y.append(calc_y_pos(predicted_a, predicted_b, predicted_c, predicted_d))
        count = count + 1
        print count

    plt.scatter(measured_x, measured_y, s=50)
    plt.scatter(predicted_x, predicted_y, s=100, c='r', marker=u'+')
    plt.xlim(-11, 11)
    plt.ylim(-11, 11)

    # Readies devices that are used in the test so that they can be added to the report
    device_names = []
    device_names.append(RF.get_device_ID())
    device_names.append(BPM.get_device_ID())
    device_names.append(PA.get_device_ID())

    # # Readies parameters that are used in the test so that they can be added to the report
    parameter_names = []
    parameter_names.append("Fixed RF Output Power: " + str(rf_power) +" dBm")
    parameter_names.append("Fixed Rf Output Frequency: " + str(rf_frequency)+" MHz")
    parameter_names.append("Maximum Attenuation: " + str(attenuator_max)+"dB")
    parameter_names.append("Minimum Attenuation: " + str(attenuator_min)+"dB")
    parameter_names.append("Steps between min and max attenuations: " + str(attenuator_steps))
    plt.xlabel("Horizontal Beam Position (mm)")
    plt.ylabel("Vertical Beam Position (mm)")
    plt.grid(True)

    if report == None:
        # If no report is entered as an input to the test, simply display the results
        plt.show()
    else:
        # If there is a report for the data to be copied to, do so.
        plt.savefig("beam_position_raster_scan" + ".pdf")
        report.setup_test("beam_position_raster_scan", intro_text, device_names, parameter_names)
        report.add_figure_to_test("beam_position_raster_scan")