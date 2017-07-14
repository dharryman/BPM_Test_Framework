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
             report=None,
             sub_directory=""):
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
        # Steps here go as follows:
        # - Take the four values given to the loop, and split them into ratios that will sum into 1
        # - Set a nominal attenuation on the attenuator, so amplification can be simulated if needed
        # - Read the power set by the RF and convert it from dB into mW, then divide it by 4 as this is what
        #   the splitter will do.
        # - Put each of the four power values through the nominal attenuation value of each channel, summing these
        #   values after will give the total power delivered into the BPM.
        # - The total power delivered into the BPM can then be multiplied by the ratios given in step 1 to
        #   calculate the desired power to be delivered into each BPM input.
        # - Converting these powers into dB with respect to the origional power delivered to the input, will give the
        #   change in dB value of each attenuator.

        abcd_total = A + B + C + D  # Sum the values given by the loop before
        A = A / abcd_total  # Normalise the A value into a ratio
        B = B / abcd_total  # Normalise the B value into a ratio
        C = C / abcd_total  # Normalise the C value into a ratio
        D = D / abcd_total  # Normalise the D value into a ratio

        PA.set_global_attenuation(nominal_attenuation)  # sets nominal attenuation value on each channel
        power_total = RF.get_output_power()[0] # Gets the power output by the RF, total power into the system
        power_total = 10.0 ** (power_total / 10.0)  # converts power output from dBm into mW
        power_split = power_total / 4.0  # Divide the power by 4 as it goes through a four way splitter

        # Attenuation effect in decimal of the nominal attenuation value
        linear_nominal_attenuation = 10.0 ** (-nominal_attenuation / 10.0)
        # The power delivered into each BPM input after passing through the attenuator with nominal values
        # Assuming no losses through cables etc...
        # Set the power delivered into each BPM as this value
        power_split = power_split * linear_nominal_attenuation
        A_pwr = power_split
        B_pwr = power_split
        C_pwr = power_split
        D_pwr = power_split

        power_total = A_pwr + B_pwr + C_pwr + D_pwr  # Total power into the BPM after each signal is attenuated

        # Desired power into the each input, given their power ratio, and power delivered under nominal attenuation
        A_pwr = A * power_total
        B_pwr = B * power_total
        C_pwr = C * power_total
        D_pwr = D * power_total

        # Calculate new attenuation values by converting the ratio of desired power and previous power into dB
        # Then set the attenuation as the difference between this and the nominal attenuation value.
        A = nominal_attenuation - quarter_round(10*np.log10(A_pwr / power_split))
        B = nominal_attenuation - quarter_round(10*np.log10(B_pwr / power_split))
        C = nominal_attenuation - quarter_round(10*np.log10(C_pwr / power_split))
        D = nominal_attenuation - quarter_round(10*np.log10(D_pwr / power_split))

        # Set the attenuation as the values just calculated.
        PA.set_channel_attenuation("A", A)
        PA.set_channel_attenuation("B", B)
        PA.set_channel_attenuation("C", C)
        PA.set_channel_attenuation("D", D)

        ######################################
        time.sleep(settling_time)  # Let the attenuator values settle
        ######################################
        measured_x.append(BPM.get_X_position())  # Take a reading of X position
        measured_y.append(BPM.get_Y_position())  # Take a reading of Y position

        # Given the power values of each input, calculate the expected position
        predicted_x.append(calc_x_pos(A_pwr, B_pwr, C_pwr, D_pwr))
        predicted_y.append(calc_y_pos(A_pwr, B_pwr, C_pwr, D_pwr))




    plt.scatter(measured_x, measured_y, s=10)
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
        plt.savefig(sub_directory+"beam_position_raster_scan" + ".pdf")
        report.setup_test("beam_position_raster_scan", intro_text, device_names, parameter_names)
        report.add_figure_to_test(sub_directory+"beam_position_raster_scan")


