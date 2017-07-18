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


def Beam_position_equidistant_grid_raster_scan_test(
             RFObject,
             BPMObject,
             ProgAttenObject,
             rf_power,
             rf_frequency,
             nominal_attenuation,
             x_points,
             y_points,
             settling_time,
             ReportObject=None,
             sub_directory=""):
    """Moves the beam position to -5 to 5 in the XY plane and recods beam position

    The calc_x_pos and calc_y_pos functions are used to measure the theoretical beam position values.
    A set of ABCD values are created that will move the beam position from -5 to 5 in both the X and Y
    plane. This is then converted into attenuation values to put into the attenuator. A fixed RF frequency 
    and power is used while the attenuator values are changed. Finally the predicted values are compared 
    with the measured values of position. 

        Args:
            RFObject (RFSignalGenerator Obj): Object to interface with the RF hardware.
            BPMObject (BPMDevice Obj): Object to interface with the BPM hardware.
            ProgAttenObject (Prog_Atten Obj): Object to interface with programmable attenuator hardware
            rf_power (float): Output power of the RF system throughout the test, in dBm 
            rf_frequency (float): Frequency output of the RF throughout the test, in MHz
            nominal_attenuation (float): starting attenuation values of each attenuator, in dB
            x_points (int): number of samples in the X plane
            y_points (int) number of samples in the Y plane 
            settling_time (float): time in seconds to wait between changing an attenuator value and 
                taking a reading from the BPM. 
            ReportObject (LaTeX Report Obj): Specific report that the test results will be recorded 
                to. If no report is sent to the test then it will just display the results in 
                a graph. 
            sub_directory (str): String that can change where the graphs will be saved to
                
        Returns:
            float array: measured X values of position
            float array: measured Y values of position
            float array: predicted X values of position
            float array: predicted Y values of position
    """

    # Readies text that will introduce this test in the report
    intro_text = r"""Moves the beam position to -5 to 5 in the XY plane and recods beam position.
    The calc\_x\_pos and calc\_y\_pos functions are used to measure the theoretical beam position values.
    A set of ABCD values are created that will move the beam position from -5 to 5 in both the X and Y
    plane. This is then converted into attenuation values to put into the attenuator. A fixed RF frequency 
    and power is used while the attenuator values are changed. Finally the predicted values are compared 
    with the measured values of position. \\~\\
    Args:\\
        RFObject (RFSignalGenerator Obj): Object to interface with the RF hardware.\\
        BPMObject (BPMDevice Obj): Object to interface with the BPM hardware.\\
        ProgAttenObject (Prog\_Atten Obj): Object to interface with programmable attenuator hardware\\
        rf\_power (float): Output power of the RF system throughout the test, in dBm \\
        rf\_frequency (float): Frequency output of the RF throughout the test, in MHz\\
        nominal\_attenuation (float): starting attenuation values of each attenuator, in dB\\
        x\_points (int): number of samples in the X plane\\
        y\_points (int) number of samples in the Y plane \\
        settling\_time (float): time in seconds to wait between changing an attenuator value and 
            taking a reading from the BPM. \\
        ReportObject (LaTeX Report Obj): Specific report that the test results will be recorded 
            to. If no report is sent to the test then it will just display the results in 
            a graph. \\
        sub\_directory (str): String that can change where the graphs will be saved to\\~\\
    Returns:\\
        float array: measured X values of position\\
        float array: measured Y values of position\\
        float array: predicted X values of position\\
        float array: predicted Y values of position\\~\\
    """

    # Formats the name of plot that is saved as, and also informs the user that the test has started
    test_name = __name__
    test_name = test_name.rsplit("Tests.")[1]
    test_name = test_name.replace("_", " ")
    print("Starting test \"" + test_name + "\"")

    RFObject.set_output_power(rf_power)
    RFObject.set_frequency(rf_frequency)
    RFObject.turn_on_RF()

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

        ProgAttenObject.set_global_attenuation(nominal_attenuation)  # sets nominal attenuation value on each channel
        power_total = RFObject.get_output_power()[0] # Gets the power output by the RF, total power into the system
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
        ProgAttenObject.set_channel_attenuation("A", A)
        ProgAttenObject.set_channel_attenuation("B", B)
        ProgAttenObject.set_channel_attenuation("C", C)
        ProgAttenObject.set_channel_attenuation("D", D)

        ######################################
        time.sleep(settling_time)  # Let the attenuator values settle
        ######################################
        measured_x.append(BPMObject.get_X_position())  # Take a reading of X position
        measured_y.append(BPMObject.get_Y_position())  # Take a reading of Y position

        # Given the power values of each input, calculate the expected position
        predicted_x.append(calc_x_pos(A_pwr, B_pwr, C_pwr, D_pwr))
        predicted_y.append(calc_y_pos(A_pwr, B_pwr, C_pwr, D_pwr))




    plt.scatter(measured_x, measured_y, s=10)
    plt.scatter(predicted_x, predicted_y, s=20, c='r', marker=u'+')
    plt.xlim(-10.5, 10.5)
    plt.ylim(-10.5, 10.5)

    # Readies devices that are used in the test so that they can be added to the report
    device_names = []
    device_names.append(RFObject.get_device_ID())
    device_names.append(BPMObject.get_device_ID())
    device_names.append(ProgAttenObject.get_device_ID())

    # # Readies parameters that are used in the test so that they can be added to the report
    parameter_names = []
    parameter_names.append("Fixed RF Output Power: " + str(rf_power) +"dBm")
    parameter_names.append("Fixed Rf Output Frequency: " + str(rf_frequency)+"MHz")
    parameter_names.append("Nominal Attenuation: " + str(nominal_attenuation)+"dB")
    parameter_names.append("Number of X points: " + str(x_points))
    parameter_names.append("Nunber of Y points: " + str(y_points))
    parameter_names.append("Settling time: "+str(settling_time)+"s")
    plt.xlabel("Horizontal Beam Position (mm)")
    plt.ylabel("Vertical Beam Position (mm)")
    plt.grid(True)

    if ReportObject == None:
        # If no report is entered as an input to the test, simply display the results
        plt.show()
    else:
        # If there is a report for the data to be copied to, do so.
        plt.savefig(sub_directory+"Beam_position_equidistant_grid_raster_scan_test" + ".pdf")
        ReportObject.setup_test(test_name, intro_text, device_names, parameter_names)
        ReportObject.add_figure_to_test(sub_directory+"Beam_position_equidistant_grid_raster_scan_test")

    return measured_x, measured_y, predicted_x, predicted_y


