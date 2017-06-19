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


def Scaled_amplitude_fill_pattern_test(RF,
                                   BPM,
                                   GS,
                                   frequency,
                                   desired_power=0,
                                   samples=10,
                                   pulse_period=1.87319,
                                   settling_time=1,
                                   report=None,
                                   sub_directory = ""):

    intro_text = "Scaled output fill pattern test intro text"
    test_name = __name__
    test_name = test_name.rsplit("Tests.")[1]
    test_name = test_name.replace("_", " ")
    print("Starting test \"" + test_name + "\"")

    device_names = []
    device_names.append(RF.get_device_ID())
    device_names.append(GS.get_device_ID())
    device_names.append(BPM.get_device_ID())

    RF.set_frequency(frequency)
    RF.set_output_power(desired_power)
    RF.turn_on_RF()
    GS.set_pulse_period(pulse_period)
    cycle = np.linspace(0.1, 1, samples)  # Creates samples to test
    GS.turn_on_modulation()
    GS.set_pulse_dutycycle(cycle[0])

    parameter_names = []
    parameter_names.append("Frequency: " + RF.get_frequency()[1])
    parameter_names.append("Desired Power: " + str(desired_power))
    parameter_names.append("Pulse Period: " + GS.get_pulse_period()[1])
    parameter_names.append("Samples: " + str(samples))
    parameter_names.append("Settling time: "+ str(settling_time)+"s")

    dutycycle = np.array([])
    bpm_power = np.array([])
    bpm_Xpos = np.array([])
    bpm_Ypos = np.array([])
    bpm_current = np.array([])
    rf_output = np.array([])
    ADC_sum = np.array([])


    time.sleep(settling_time)
    for index in cycle:
        current_cycle = GS.set_pulse_dutycycle(index)
        dutycycle = np.append(dutycycle, current_cycle)
        log_cycle = 20*np.log10(current_cycle)
        RF.set_output_power(desired_power + np.absolute(log_cycle))
        time.sleep(settling_time)
        rf_output = np.append(rf_output, RF.get_output_power()[0])
        bpm_power = np.append(bpm_power, BPM.get_input_power())
        bpm_current = np.append(bpm_current, BPM.get_beam_current())
        bpm_Xpos = np.append(bpm_Xpos, BPM.get_X_position())
        bpm_Ypos = np.append(bpm_Ypos, BPM.get_Y_position())
        ADC_sum = np.append(ADC_sum, BPM.get_ADC_sum())

    report.setup_test(test_name, intro_text, device_names, parameter_names)

    # make a caption and headings for a table of results
    caption = "Changing gate duty cycle, with fixed RF amplitude "
    headings = [["Duty Cycle","Output Power" , "Input Power", "BPM Current", "X Position", "Y Position", "ADC Sum"],
                ["(0-1)","(dBm)", "(dBm)", "(mA)", "(mm)", "(mm)", "(Counts)"]]
    data = [dutycycle, rf_output ,bpm_power, bpm_current, bpm_Xpos, bpm_Ypos, ADC_sum]

    # copy the values to the report
    report.add_table_to_test('|c|c|c|c|c|c|c|', data, headings, caption)

    # Get the plot values in a format thats easy to iterate
    format_plot = []# x axis, y axis, x axis title, y axis title, title of file, caption
    format_plot.append((dutycycle, rf_output, 'Gating signal duty cycle (0-1)', 'RF power ar source (dBm)', "scaled_DC_vs_Out_power.pdf"))
    format_plot.append((dutycycle, bpm_power,'Gating signal duty cycle (0-1)', 'Power input at BPM (dBm)',"scaled_DC_vs_In_power.pdf"))
    format_plot.append((dutycycle, bpm_current, 'Gating signal duty cycle (0-1)', 'Beam Current at BPM (mA)', "scaled_DC_vs_current.pdf"))
    format_plot.append((dutycycle, bpm_Xpos, 'Gating signal duty cycle (0-1)', 'Horizontal Beam Position (mm)', "scaled_DC_vs_X.pdf"))
    format_plot.append((dutycycle, bpm_Ypos, 'Gating signal duty cycle (0-1)', 'Vertical Beam Position (mm)', "scaled_DC_vs_Y.pdf"))
    format_plot.append((dutycycle, ADC_sum, 'Gating signal duty cycle (0-1)', 'ADC Sum (counts)', "scaled_DC_vs_ADC_Sum.pdf"))

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
    return dutycycle, rf_output, bpm_power, bpm_current, bpm_Xpos, bpm_Ypos
