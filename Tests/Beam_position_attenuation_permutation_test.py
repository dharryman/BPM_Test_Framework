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

def Beam_position_attenuation_permutation_test(
             RFObject,
             BPMObject,
             ProgAttenObject,
             rf_power,
             rf_frequency,
             attenuator_max,
             attenuator_min,
             attenuator_steps,
             settling_time,
             ReportObject=None,
             sub_directory=""):

    """Moves the beam position by changing the attenuator values with a series of different permutations

    The calc_x_pos and calc_y_pos functions are used to measure the theoretical beam position values.
    The attenuator_max, attenuator_min and attenuator_steps are used to create a series of different 
    combinations of attenuator values. A linear space will be made from the min to the max value of 
    attenuation. These values will then be put into all possible permutations with four values. Each 
    permutation will be fed to the four attenuators, and the BPM position recoded after each 
    attenuation change.

        Args:
            RFObject (RFSignalGenerator Obj): Object to interface with the RF hardware.
            BPMObject (BPMDevice Obj): Object to interface with the BPM hardware.
            ProgAttenObject (Prog_Atten Obj): Object to interface with programmable attenuator hardware
            rf_power (float): Output power of the RF system throughout the test, in dBm 
            rf_frequency (float): Frequency output of the RF throughout the test, in MHz
            attenuator_max (float): max value for the attenuators
            attenuator_min (float): min value for the attenuators
            attenuator_steps (float): steps between the min and max values
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
    intro_text = r""""Moves the beam position by changing the attenuator values with a series of different permutations.
    The calc\_x\_pos and calc\_y\_pos functions are used to measure the theoretical beam position values.
    The attenuator\_max, attenuator\_min and attenuator\_steps are used to create a series of different 
    combinations of attenuator values. A linear space will be made from the min to the max value of 
    attenuation. These values will then be put into all possible permutations with four values. Each 
    permutation will be fed to the four attenuators, and the BPM position recoded after each 
    attenuation change. \\~\\
    Args:\\
        RFObject (RFSignalGenerator Obj): Object to interface with the RF hardware.\\
        BPMObject (BPMDevice Obj): Object to interface with the BPM hardware.\\
        ProgAttenObject (Prog\_Atten Obj): Object to interface with programmable attenuator hardware\\
        rf\_power (float): Output power of the RF system throughout the test, in dBm \\
        rf\_frequency (float): Frequency output of the RF throughout the test, in MHz\\
        attenuator\_max (float): max value for the attenuators\\
        attenuator\_min (float): min value for the attenuators\\
        attenuator\_steps (float): steps between the min and max values\\
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

    attenuation_map = np.linspace(attenuator_min,attenuator_max,attenuator_steps)

    attenuation_map = itertools.product(attenuation_map, repeat=4)

    count = 0

    for index in attenuation_map:
        ProgAttenObject.set_channel_attenuation("A", index[0])
        ProgAttenObject.set_channel_attenuation("B", index[1])
        ProgAttenObject.set_channel_attenuation("C", index[2])
        ProgAttenObject.set_channel_attenuation("D", index[3])
        time.sleep(settling_time)
        measured_x.append(BPMObject.get_X_position())
        measured_y.append(BPMObject.get_Y_position())
        power_out = RFObject.get_output_power()[0]
        power_out = power_out - 6  # Reduce signal by a factor of four as it goes through a 4 way splitter
        predicted_a = power_out - index[0]
        predicted_b = power_out - index[1]
        predicted_c = power_out - index[2]
        predicted_d = power_out - index[3]
        predicted_a = 10 ** (predicted_a / 10.0)
        predicted_b = 10 ** (predicted_b / 10.0)
        predicted_c = 10 ** (predicted_c / 10.0)
        predicted_d = 10 ** (predicted_d / 10.0)
        predicted_x.append(calc_x_pos(predicted_a, predicted_b, predicted_c, predicted_d))
        predicted_y.append(calc_y_pos(predicted_a, predicted_b, predicted_c, predicted_d))
        count = count + 1

    plt.scatter(measured_x, measured_y, s=50)
    plt.scatter(predicted_x, predicted_y, s=100, c='r', marker=u'+')
    plt.xlim(-11, 11)
    plt.ylim(-11, 11)

    # Readies devices that are used in the test so that they can be added to the report
    device_names = []
    device_names.append(RFObject.get_device_ID())
    device_names.append(BPMObject.get_device_ID())
    device_names.append(ProgAttenObject.get_device_ID())

    # # Readies parameters that are used in the test so that they can be added to the report
    parameter_names = []
    parameter_names.append("Fixed RF Output Power: " + str(rf_power) +" dBm")
    parameter_names.append("Fixed Rf Output Frequency: " + str(rf_frequency)+" MHz")
    parameter_names.append("Maximum Attenuation: " + str(attenuator_max)+"dB")
    parameter_names.append("Minimum Attenuation: " + str(attenuator_min)+"dB")
    parameter_names.append("Steps between min and max attenuations: " + str(attenuator_steps))
    parameter_names.append("Settling time: " + str(settling_time)+"s")
    plt.xlabel("Horizontal Beam Position (mm)")
    plt.ylabel("Vertical Beam Position (mm)")
    plt.grid(True)

    if ReportObject == None:
        # If no report is entered as an input to the test, simply display the results
        plt.show()
    else:
        # If there is a report for the data to be copied to, do so.
        plt.savefig(sub_directory+"beam_position_attenuation_permutation" + ".pdf")
        ReportObject.setup_test("beam_position_attenuation_permutation", intro_text, device_names, parameter_names)
        ReportObject.add_figure_to_test(sub_directory+"beam_position_attenuation_permutation")

    return measured_x, measured_y, predicted_x, predicted_y

