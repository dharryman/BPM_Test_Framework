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
             nominal_attenuation,
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
    gradient = np.linspace(0.0001, 2, x_points)
    inv_gradient = gradient[::-1]
    a = gradient
    b = inv_gradient
    c = inv_gradient
    d = gradient
    a_total = []
    b_total = []
    c_total = []
    d_total = []
    for index in np.linspace(-1, 1, y_points):  # number of Y samples
        offset = 1  # base power from the device
        a_total = np.append(a_total, (a + index) + offset)
        b_total = np.append(b_total, (b + index) + offset)
        c_total = np.append(c_total, (c - index) + offset)
        d_total = np.append(d_total, (d - index) + offset)
    #############################################################

    for A, B, C, D in zip(a_total, b_total, c_total, d_total):

        abcd_total = A+B+C+D
        A = A/abcd_total
        B = B/abcd_total
        C = C/abcd_total
        D = D/abcd_total

        PA.set_global_attenuation(nominal_attenuation)  # sets nominal attenuation value
        power_total = RF.get_output_power()[0] # gets power value in dBm
        power_total = 10.0 ** (power_total / 10.0)  # converts power from dBm
        power_split = power_total / 4.0

        linear_nominal_attenuation = 10.0 ** (-nominal_attenuation / 10.0)
        power_split = power_split * linear_nominal_attenuation
        A_pwr = power_split
        B_pwr = power_split
        C_pwr = power_split
        D_pwr = power_split

        power_total = A_pwr + B_pwr + C_pwr + D_pwr

        A_pwr = A * power_total
        B_pwr = B * power_total
        C_pwr = C * power_total
        D_pwr = D * power_total

        A = 10*np.log10(A_pwr / power_split)
        B = 10*np.log10(B_pwr / power_split)
        C = 10*np.log10(C_pwr / power_split)
        D = 10*np.log10(D_pwr / power_split)

        print A,B,C,D

        new_x = calc_x_pos(A_pwr, B_pwr, C_pwr, D_pwr)
        new_y = calc_y_pos(A_pwr, B_pwr, C_pwr, D_pwr)
        predicted_x.append(new_x)
        predicted_y.append(new_y)

        attenuation = PA.get_channel_attenuation("A")
        PA.set_channel_attenuation("A", attenuation - A)
        attenuation = PA.get_channel_attenuation("B")
        PA.set_channel_attenuation("B", attenuation - B)
        attenuation = PA.get_channel_attenuation("C")
        PA.set_channel_attenuation("C", attenuation - C)
        attenuation = PA.get_channel_attenuation("D")
        PA.set_channel_attenuation("D", attenuation - D)

        time.sleep(settling_time)
        measured_x.append(BPM.get_X_position())
        measured_y.append(BPM.get_Y_position())



    plt.scatter(measured_x, measured_y, s=20)
    plt.scatter(predicted_x, predicted_y, s=20, c='r', marker=u'+')
    plt.xlim(-10.5, 10.5)
    plt.ylim(-10.5, 10.5)

    # Readies devices that are used in the test so that they can be added to the report
    device_names = []
    device_names.append(RF.get_device_ID())
    device_names.append(BPM.get_device_ID())
    device_names.append(PA.get_device_ID())

    # # Readies parameters that are used in the test so that they can be added to the report
    parameter_names = []
    parameter_names.append("Fixed RF Output Power: " + str(rf_power) +" dBm")
    parameter_names.append("Fixed Rf Output Frequency: " + str(rf_frequency)+" MHz")
    parameter_names.append("Maximum Attenuation: " + str(nominal_attenuation)+" dB")
    parameter_names.append("Minimum Attenuation: " + str(x_points)+" dB")
    parameter_names.append("Steps between min and max attenuations: " + str(y_points))
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


