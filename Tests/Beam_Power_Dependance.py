from pkg_resources import require

require("numpy")
require("cothread")
require("matplotlib")
import numpy as np
import matplotlib.pyplot as plt
import time


def Beam_Power_Dependance(RF,
                          BPM,
                          frequency,
                          start_power=-100,
                          end_power=0,
                          samples=10,
                          settling_time=1,
                          report=None,
                          sub_directory=""):
    """Tests the relationship between beam current and X Y position read from the BPM.

    An RF signal is output and then read back using the RF and BPM objects respectively. 
    The signal is ramped up in power at a single frequency. The number of samples to take, 
    and settling time between each measurement can be decided using the arguments. 

    Args:
        RF (RFSignalGenerator Obj): RF interface object.
        BPM (BPMDevice Obj): BPM interface object.
        frequency (float/str): Output frequency for the tests, can be a float, where 
            the units will default to MHz, or can be a string where the units can be 
            explicitly stated e.g. kHz, Hz.
        start_power (float/str): Starting output power for the tests, default value is 
            -100 dBm. The input values can be floats, if so, the units will default to 
            dBm. A string input can be used to explicitly state the units, e.g. dBW, mV.
        end_power (float/str): Final output power for the tests, default value is 0 dBm.
            The input values can be floats, if so, the units will default to dBm. A 
            string input can be used to explicitly state the units, e.g. dBW, mV.
        samples (int): Number of samples take is this value + 1.
        settling_time (float): Time in seconds, that the program will wait in between 
            setting an  output power, and reading an input power. 
        report (LaTeX Report Obj): Specific report that the test results will be recorded 
            to. If no report is sent to the test then it will just display the results in 
            a graph. 

Returns:
    float array: Beam current values during the test. 
    float array: Horizontal position of the BPM during the test.
    float array: Vertical position of the BPM  during the test.
"""

    # Text that will be placed at the start of the test in the report.
    intro_text = "Text that will describe the test"



    # Formats the test name and tells the user the test has started
    test_name = __name__
    test_name = test_name.rsplit("Tests.")[1]
    test_name = test_name.replace("_", " ")
    print("Starting test \"" + test_name + "\"")

    # Get the device names for the report
    device_names = []
    device_names.append(RF.get_device_ID())
    device_names.append(BPM.get_device_ID())

    # Get the parameter values for the report
    parameter_names = []
    parameter_names.append("Frequency: " + str(frequency)+"MHz")
    parameter_names.append("Starting output power: "+str(start_power)+"dBm")
    parameter_names.append("Final output power: "+str(end_power)+"dBm")
    parameter_names.append("Samples: " + str(samples))
    parameter_names.append("Settling time: " + str(settling_time)+"s")

    # Set the initial state of the RF device
    power = np.linspace(start_power, end_power, samples)  # Creates samples to test
    RF.set_frequency(frequency)
    RF.set_output_power(start_power)
    RF.turn_on_RF()
    time.sleep(settling_time)

    # Build up the arrays where the final values will be saved
    X_pos = np.array([])
    Y_pos = np.array([])
    beam_current = np.array([])
    output_power = np.array([])
    input_power = np.array([])
    ADC_sum = np.array([])

    # Perform the test
    for index in power:
        RF.set_output_power(index)  # Set next output power value
        time.sleep(settling_time)  # Wait for signal to settle
        beam_current = np.append(beam_current, BPM.get_beam_current())  # record beam current
        X_pos = np.append(X_pos, BPM.get_X_position())  # record X pos
        Y_pos = np.append(Y_pos, BPM.get_Y_position())  # record Y pos
        output_power = np.append(output_power, RF.get_output_power()[0])
        input_power = np.append(input_power, BPM.get_input_power())
        ADC_sum = np.append(ADC_sum, BPM.get_ADC_sum())

    #turn off the RF
    RF.turn_off_RF()

    # add the test details to the report
    report.setup_test(test_name, intro_text, device_names, parameter_names)

    # make a caption and headings for a table of results
    caption = "Beam Power Dependence Results"
    headings = [["Output Power", "Input Power", "BPM Current", "X Position", "Y Position", "ADC Sum"],
                ["(dBm)", "(dBm)", "(mA)", "(mm)", "(mm)", "(Counts)"]]
    data = [output_power, input_power, beam_current, X_pos, Y_pos, ADC_sum]

    # copy the values to the report
    report.add_table_to_test('|c|c|c|c|c|c|', data, headings, caption)

    # Get the plot values in a format thats easy to iterate
    format_plot = []# x axis, y axis, x axis title, y axis title, title of file, caption
    format_plot.append((output_power, input_power,'RF Source Power Output (dBm)', 'Power input at BPM (dBm)',"power_vs_power.pdf"))
    format_plot.append((output_power, beam_current, 'RF Source Power Output (dBm)', 'Beam Current at BPM (mA)', "power_vs_current.pdf"))
    format_plot.append((output_power, X_pos, 'RF Source Power Output (dBm)', 'Horizontal Beam Position (mm)', "power_vs_X.pdf"))
    format_plot.append((output_power, Y_pos, 'RF Source Power Output (dBm)', 'Vertical Beam Position (mm)', "power_vs_Y.pdf"))
    format_plot.append((output_power, ADC_sum, 'RF Source Power Output (dBm)', 'ADC Sum (counts)', 'power_vs_ADC_sum.pdf'))

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
    return output_power, input_power, beam_current, X_pos, Y_pos

