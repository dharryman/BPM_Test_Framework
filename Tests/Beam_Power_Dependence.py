from pkg_resources import require
require("numpy")
require("cothread")
require("matplotlib")
import numpy as np
import matplotlib.pyplot as plt
import time


def Beam_Power_Dependence(
                          RFObject,
                          BPMObject,
                          frequency,
                          start_power=-100,
                          end_power=0,
                          samples=10,
                          settling_time=1,
                          ReportObject=None,
                          sub_directory=""):
    """Tests the relationship between RF output power and values read from the BPM.

    An RF signal is output, and then different parameters are measured from the BPM. 
    The signal is linearly ramped up in dBm at a single frequency. The number of samples to take, 
    and settling time between each measurement can be decided using the arguments. 

    Args:
        RFObject (RFSignalGenerator Obj): Object to interface with the RF hardware.
        BPMObject (BPMDevice Obj): Object to interface with the BPM hardware.
        frequency (float): Output frequency for the tests, set as a float that will 
            use the assumed units of MHz. 
        start_power (float): Starting output power for the tests, default value is 
            -100 dBm. The input values are floats and dBm is assumed. 
        end_power (float): Final output power for the tests, default value is 0 dBm.
            The input values are floats and dBm assumed. 
        samples (int): Number of samples take is this value + 1.
        settling_time (float): Time in seconds, that the program will wait in between 
            setting an  output power on the RF, and reading the values of the BPM. 
        ReportObject (LaTeX Report Obj): Specific report that the test results will be recorded 
            to. If no report is sent to the test then it will just display the results in 
            a graph. 
        sub_directory (str): String that can change where the graphs will be saved to.

    Returns:
        float array: Power output from the RF
        float array: Power read at the BPM
        float array: Beam Current read at the BPM
        float array: X Positions read from the BPM
        float array: Y Positions read from the BPM
    """


    intro_text = r"""Tests the relationship between RF output power and values read from the BPM. 
    An RF signal is output, and then different parameters are measured from the BPM. 
    The signal is linearly ramped up in dBm at a single frequency. The number of samples to take, 
    and settling time between each measurement can be decided using the arguments. \\~\\
    Args:\\
        RFObject (RFSignalGenerator Obj): Object to interface with the RF hardware.\\
        BPMObject (BPMDevice Obj): Object to interface with the BPM hardware.\\
        frequency (float): Output frequency for the tests, set as a float that will 
            use the assumed units of MHz. \\
        start\_power (float): Starting output power for the tests, default value is 
            -100 dBm. The input values are floats and dBm is assumed. \\
        end\_power (float): Final output power for the tests, default value is 0 dBm.
            The input values are floats and dBm assumed. \\
        samples (int): Number of samples take is this value + 1.\\
        settling\_time (float): Time in seconds, that the program will wait in between 
            setting an  output power on the RF, and reading the values of the BPM. \\
        ReportObject (LaTeX Report Obj): Specific report that the test results will be recorded 
            to. If no report is sent to the test then it will just display the results in 
            a graph. \\
        sub\_directory (str): String that can change where the graphs will be saved to.\\~\\
    Returns:\\
        float array: Power output from the RF\\
        float array: Power read at the BPM\\
        float array: Beam Current read at the BPM\\
        float array: X Positions read from the BPM\\
        float array: Y Positions read from the BPM\\~\\
    """



    # Formats the test name and tells the user the test has started
    test_name = __name__
    test_name = test_name.rsplit("Tests.")[1]
    test_name = test_name.replace("_", " ")
    print("Starting test \"" + test_name + "\"")

    # Get the device names for the report
    device_names = []
    device_names.append(RFObject.get_device_ID())
    device_names.append(BPMObject.get_device_ID())

    # Get the parameter values for the report
    parameter_names = []
    parameter_names.append("Frequency: " + str(frequency)+"MHz")
    parameter_names.append("Starting output power: "+str(start_power)+"dBm")
    parameter_names.append("Final output power: "+str(end_power)+"dBm")
    parameter_names.append("Samples: " + str(samples))
    parameter_names.append("Settling time: " + str(settling_time)+"s")

    # Set the initial state of the RF device
    power = np.linspace(start_power, end_power, samples)  # Creates samples to test
    RFObject.set_frequency(frequency)
    RFObject.set_output_power(start_power)
    RFObject.turn_on_RF()
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
        RFObject.set_output_power(index)  # Set next output power value
        time.sleep(settling_time)  # Wait for signal to settle
        beam_current = np.append(beam_current, BPMObject.get_beam_current())  # record beam current
        X_pos = np.append(X_pos, BPMObject.get_X_position())  # record X pos
        Y_pos = np.append(Y_pos, BPMObject.get_Y_position())  # record Y pos
        output_power = np.append(output_power, RFObject.get_output_power()[0])
        input_power = np.append(input_power, BPMObject.get_input_power())
        ADC_sum = np.append(ADC_sum, BPMObject.get_ADC_sum())

    #turn off the RF
    RFObject.turn_off_RF()

    # add the test details to the report
    ReportObject.setup_test(test_name, intro_text, device_names, parameter_names)

    # make a caption and headings for a table of results
    caption = "Beam Power Dependence Results"
    headings = [["Output Power", "Input Power", "BPM Current", "X Position", "Y Position", "ADC Sum"],
                ["(dBm)", "(dBm)", "(mA)", "(mm)", "(mm)", "(Counts)"]]
    data = [output_power, input_power, beam_current, X_pos, Y_pos, ADC_sum]

    # copy the values to the report
    ReportObject.add_table_to_test('|c|c|c|c|c|c|', data, headings, caption)

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
        ReportObject.add_figure_to_test(sub_directory + index[4], "")

    # return the full data sets
    return output_power, input_power, beam_current, X_pos, Y_pos

