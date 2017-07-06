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


def quarter_round(x):
    return round(x * 4) / 4


def Beamposition_linear_raster_scan_test(RF,
             BPM,
             PA,
             rf_power,
             rf_frequency,
             total_attenuation,
             x_points,
             y_points,
             settling_time,
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

    ###########################################################
    gradient = np.linspace(0.001, 10, x_points)
    inv_gradient = gradient[::-1]
    a = gradient
    b = inv_gradient
    c = inv_gradient
    d = gradient
    a_total = []
    b_total = []
    c_total = []
    d_total = []
    for index in np.linspace(-5, 5, y_points):  # number of Y samples
        offset = 5  # base power from the device
        a_total = np.append(a_total, (a + index) + offset)
        b_total = np.append(b_total, (b + index) + offset)
        c_total = np.append(c_total, (c - index) + offset)
        d_total = np.append(d_total, (d - index) + offset)
    #############################################################

    for A, B, C, D in zip(a_total, b_total, c_total, d_total):

        abcd_total = A + B + C + D

        A = round(A / abcd_total, 2)
        B = round(B / abcd_total, 2)
        C = round(C / abcd_total, 2)
        D = round(D / abcd_total, 2)

        new_x = calc_x_pos(A, B, C, D)# change these to log values!!!
        new_y = calc_y_pos(A, B, C, D)
        predicted_x.append(new_x)
        predicted_y.append(new_y)

        A = quarter_round(A * total_attenuation)
        B = quarter_round(B * total_attenuation)
        C = quarter_round(C * total_attenuation)
        D = quarter_round(D * total_attenuation)

        A, B, C, D = C, D, A, B

        PA.set_channel_attenuation("A", A)
        PA.set_channel_attenuation("B", B)
        PA.set_channel_attenuation("C", C)
        PA.set_channel_attenuation("D", D)

        time.sleep(settling_time)

        measured_x.append(BPM.get_X_position())
        measured_y.append(BPM.get_Y_position())
        print A+B+C+D
        print BPM.get_X_position(), new_x
        print BPM.get_Y_position(), new_y

    plt.scatter(measured_x, measured_y, s=10)
    plt.scatter(predicted_x, predicted_y, s=10, c='r', marker=u'+')
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)

    # Readies devices that are used in the test so that they can be added to the report
    device_names = []
    device_names.append(RF.get_device_ID())
    device_names.append(BPM.get_device_ID())
    device_names.append(PA.get_device_ID())

    # # Readies parameters that are used in the test so that they can be added to the report
    parameter_names = []
    parameter_names.append("Fixed RF Output Power: " + str(rf_power) +" dBm")
    parameter_names.append("Fixed Rf Output Frequency: " + str(rf_frequency)+" MHz")
    parameter_names.append("Maximum Attenuation: " + str(total_attenuation)+" dB")
    parameter_names.append("Minimum Attenuation: " + str(x_points)+" dB")
    parameter_names.append("Steps between min and max attenuations: " + str(y_points))

    if report == None:
        # If no report is entered as an input to the test, simply display the results
        plt.show()
    else:
        # If there is a report for the data to be copied to, do so.
        plt.savefig("beam_position_raster_scan" + ".pdf")
        report.setup_test("beam_position_raster_scan", intro_text, device_names, parameter_names)
        report.add_figure_to_test("beam_position_raster_scan")


