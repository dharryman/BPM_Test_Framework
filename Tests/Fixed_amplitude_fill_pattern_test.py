import RFSignalGenerators
import BPMDevice
import Gate_Source
from pkg_resources import require
require("numpy")
require("cothread")
require("matplotlib")
import numpy as np
import matplotlib.pyplot as plt
import time


def Fixed_amplitude_fill_pattern_test(RF,
                                   BPM,
                                   GS,
                                   frequency,
                                   power=0,
                                   samples=10,
                                   pulse_period="1.87319us",
                                   settling_time=1,
                                   report=None,
                                   sub_directory=""):
    """Tests the relationship between power output from the RF device and the power read by the BPM.

        An RF signal is output and then read back using the RF and BPM objects respectively. The signal is 
        ramped up in power at a single frequency. The number of samples to take, and settling time between
         each measurement can be decided using the arguments. 

        Args:
            RF (RFSignalGenerator Obj): RF interface object. 
            BPM (BPMDevice Obj): BPM interface object.
            GS (GateSource Obj): Gate Source interface object.
            frequency (float/str): Output frequency for the tests, can be a float, where the units will 
                default to MHz, or can be a string where the units can be explicitly stated e.g. kHz, Hz.
            power (float/str): Output power for the tests, default value is 0 dBm. The 
                input values can be floats, if so, the units will default to dBm. A string input can be 
            samples (int): Number of samples taken as the duty cycle increases from 10% to 100%
            pulse_period (float/str): Period of the pulse that will have it's duty cycle changed,
                the input can be as a float where this will default to seconds, or as a string 
                where units such as us, or ms can be used. Default value is 1.87319us. 
            settling_time (float): The time in seconds that the program will wait in between changing
                the duty cycle, and taking a measurement. 
            report (LaTeX Report Obj): Specific report that the test results will be recorded to. If 
                no report is sent to the test then it will just display the results in a graph.

        Returns:
            float array: dutycycle, array of the duty cycle values output during the test.
            float array: bpm_power, array of the BPM's measured power values during the test.
            float array: bpm_current, array of the BPM's measured current values during the test.
            float array: bpm_Xpos, array of the BPM's measured X position values during the test.
            float array: bpm_Ypos, array of the BPM's measured Y position values during the test

    """
    intro_text = "The \"Fixed output fill pattern test\" is supposed to test the BPM parameters reliance on" \
                 "the bunch shape that has a variable charge size. The signal suppled by the RF signal generator" \
                 "will have a fixed frequency and power output, this is then mixed with a gating signal, " \
                 "modulating the RF signal. The duty cycle of the gating signal is then changed and the BPM " \
                 "parameters recorded. This test will see how these parameters change as the duty cycle is changed." \
                 "For example, ss the signal provided by the RF is constant the power at the BPM will drop the lower " \
                 "the duty cycle."



    RF.set_frequency(frequency)
    RF.set_output_power(power)

    cycle = np.linspace(0.1, 1, samples)  # Creates samples to test
    GS.set_pulse_period(pulse_period)
    GS.set_pulse_dutycycle(cycle[0])
    RF.turn_on_RF()
    GS.turn_on_modulation()

    dutycycle = np.array([])
    bpm_power = np.array([])
    bpm_Xpos = np.array([])
    bpm_Ypos = np.array([])
    bpm_current = np.array([])

    test_name = __name__
    test_name = test_name.rsplit("Tests.")[1]
    test_name = test_name.replace("_", " ")
    print("Starting test \"" + test_name + "\"")

    device_names = []
    device_names.append(RF.get_device_ID())
    device_names.append(GS.get_device_ID())
    device_names.append(BPM.get_device_ID())

    parameter_names = []
    parameter_names.append("Frequency: " + RF.get_frequency()[1])
    parameter_names.append("Output Power: " + RF.get_output_power()[1])
    parameter_names.append("Pulse Period: " + GS.get_pulse_period()[1])
    parameter_names.append("Samples: " + str(samples))

    time.sleep(settling_time)
    for index in cycle:
        dutycycle = np.append(dutycycle, GS.set_pulse_dutycycle(index))
        time.sleep(settling_time)
        bpm_power = np.append(bpm_power, BPM.get_input_power())
        bpm_current = np.append(bpm_current, BPM.get_beam_current())
        bpm_Xpos = np.append(bpm_Xpos, BPM.get_X_position())
        bpm_Ypos = np.append(bpm_Ypos, BPM.get_Y_position())

    RF.turn_off_RF()
    GS.turn_off_modulation()

    report.setup_test(test_name, intro_text, device_names, parameter_names)

    caption = "Changing gate duty cycle, with fixed RF amplitude "
    headings = [["Duty Cycle", "Input Power", "BPM Current", "X Position", "Y Position"],
                ["(0-1)", "(dBm)", "(mA)", "(mm)", "(mm)"]]
    data = [dutycycle, bpm_power, bpm_current, bpm_Xpos, bpm_Ypos]

    # copy the values to the report
    report.add_table_to_test('|c|c|c|c|c|', data, headings, caption)

    # make a caption and headings for a table of results


    # Get the plot values in a format thats easy to iterate
    format_plot = []# x axis, y axis, x axis title, y axis title, title of file, caption
    format_plot.append((dutycycle, bpm_power,'Gating signal duty cycle (0-1)', 'Power input at BPM (dBm)',"DC_vs_power.pdf"))
    format_plot.append((dutycycle, bpm_current, 'Gating signal duty cycle (0-1)', 'Beam Current at BPM (mA)', "DC_vs_current.pdf"))
    format_plot.append((dutycycle, bpm_Xpos, 'Gating signal duty cycle (0-1)', 'Horizontal Beam Position (mm)', "DC_vs_X.pdf"))
    format_plot.append((dutycycle, bpm_Ypos, 'Gating signal duty cycle (0-1)', 'Vertical Beam Position (mm)', "DC_vs_Y.pdf"))

    # plot all of the graphs
    for index in format_plot:
        plt.plot(index[0], index[1])
        plt.xlabel(index[2])
        plt.ylabel(index[3])
        plt.grid(True)
        plt.savefig(sub_directory+index[4])
        plt.cla()  # Clear axis
        plt.clf()  # Clear figure
        report.add_figure_to_test(sub_directory + index[4], "")

    # return the full data sets
    return dutycycle, bpm_power, bpm_current, bpm_Xpos, bpm_Ypos,

