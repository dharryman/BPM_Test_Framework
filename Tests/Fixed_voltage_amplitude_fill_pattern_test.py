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


def Fixed_voltage_amplitude_fill_pattern_test(
                                   RFObject,
                                   BPMObject,
                                   GateSourceObject,
                                   frequency,
                                   power=0,
                                   samples=10,
                                   pulse_period=1.87319,
                                   settling_time=1,
                                   ReportObject=None,
                                   sub_directory=""):
    """
        This test imitates a fill pattern by modulation the RF signal with a square wave. The up time 
        of the square wave represents when a bunch goes passed, and the downtime the gaps between the 
        bunches. This test will take the pulse length in micro seconds, and then linearly step up the 
        duty cycle of the pulse, from 0.1 to 1. Readings on the BPM are then recorded as the duty cycle
        is changed. While the duty cycle is increased, the peak RF voltage stays fixed, meaning that 
        the average power will change with duty cycle. 
        

        Args:
            RFObject (RFSignalGenerator Obj): Object to interface with the RF hardware.
            BPMObject (BPMDevice Obj): Object to interface with the BPM hardware.
            GateSourceObject: (GateSource Obj): Object used to interface with the gate source
                hardware. 
            frequency (float/str): Output frequency for the tests, set as a float that will 
                use the assumed units of MHz. 
            power (float): Starting output power for the tests, default value is 
                -100 dBm. The input values are floats and dBm is assumed. 
            samples (int): Number of samples take is this value + 1.
            pulse_period (float): The pulse period for the modulation signal, i.e. the bunch length, 
                this is a float that is in micro seconds.
            settling_time (float): Time in seconds, that the program will wait in between 
                setting an  output power on the RF, and reading the values of the BPM. 
            ReportObject (LaTeX Report Obj): Specific report that the test results will be recorded 
                to. If no report is sent to the test then it will just display the results in 
                a graph. 
            sub_directory (str): String that can change where the graphs will be saved to
                
        Returns:
            float array: duty cycle of the modulation signal
            float array: power read from the BPM
            float array: current read fro mthe BPM
            float array: X position read from the BPM
            float array: Y position read from the BPM


    """
    intro_text =r"""
        This test imitates a fill pattern by modulation the RF signal with a square wave. The up time 
        of the square wave represents when a bunch goes passed, and the downtime the gaps between the 
        bunches. This test will take the pulse length in micro seconds, and then linearly step up the 
        duty cycle of the pulse, from 0.1 to 1. Readings on the BPM are then recorded as the duty cycle
        is changed. While the duty cycle is increased, the peak RF voltage stays fixed, meaning that 
        the average power will change with duty cycle. \\~\\
        Args:\\
            RFObject (RFSignalGenerator Obj): Object to interface with the RF hardware.\\
            BPMObject (BPMDevice Obj): Object to interface with the BPM hardware.\\
            GateSourceObject: (GateSource Obj): Object used to interface with the gate source hardware. \\
            frequency (float/str): Output frequency for the tests, set as a float that will use the assumed units of MHz. \\
            power (float): Starting output power for the tests, default value is -100 dBm. The input values are floats and dBm is assumed. \\
            samples (int): Number of samples take is this value + 1.\\
            pulse\_period (float): The pulse period for the modulation signal, i.e. the bunch length, this is a float that is in micro seconds.\\
            settling\_time (float): Time in seconds, that the program will wait in between setting an  output power on the RF, and reading the values of the BPM. \\
            ReportObject (LaTeX Report Obj): Specific report that the test results will be recorded to. If no report is sent to the test then it will just display the results in a graph. \\
            sub\_directory (str): String that can change where the graphs will be saved to\\~\\  
        Returns:\\
            float array: duty cycle of the modulation signal\\
            float array: power read from the BPM\\
            float array: current read from the BPM\\
            float array: X position read from the BPM\\
            float array: Y position read from the BPM\\~\\  
    """



    RFObject.set_frequency(frequency)
    RFObject.set_output_power(power)

    cycle = np.linspace(0.1, 1, samples)  # Creates samples to test
    GateSourceObject.set_pulse_period(pulse_period)
    GateSourceObject.set_pulse_dutycycle(cycle[0])
    RFObject.turn_on_RF()
    GateSourceObject.turn_on_modulation()

    dutycycle = np.array([])
    bpm_power = np.array([])
    bpm_Xpos = np.array([])
    bpm_Ypos = np.array([])
    bpm_current = np.array([])
    ADC_sum = np.array([])

    test_name = __name__
    test_name = test_name.rsplit("Tests.")[1]
    test_name = test_name.replace("_", " ")
    print("Starting test \"" + test_name + "\"")

    device_names = []
    device_names.append(RFObject.get_device_ID())
    device_names.append(GateSourceObject.get_device_ID())
    device_names.append(BPMObject.get_device_ID())

    parameter_names = []
    parameter_names.append("Frequency: " + RFObject.get_frequency()[1])
    parameter_names.append("Output Power: " + RFObject.get_output_power()[1])
    parameter_names.append("Pulse Period: " + GateSourceObject.get_pulse_period()[1])
    parameter_names.append("Samples: " + str(samples))
    parameter_names.append("Settling time: " + str(settling_time) + "s")

    time.sleep(settling_time)
    for index in cycle:
        dutycycle = np.append(dutycycle, GateSourceObject.set_pulse_dutycycle(index))
        time.sleep(settling_time)
        bpm_power = np.append(bpm_power, BPMObject.get_input_power())
        bpm_current = np.append(bpm_current, BPMObject.get_beam_current())
        bpm_Xpos = np.append(bpm_Xpos, BPMObject.get_X_position())
        bpm_Ypos = np.append(bpm_Ypos, BPMObject.get_Y_position())
        ADC_sum = np.append(ADC_sum, BPMObject.get_ADC_sum())


    RFObject.turn_off_RF()
    GateSourceObject.turn_off_modulation()

    ReportObject.setup_test(test_name, intro_text, device_names, parameter_names)

    caption = "Changing gate duty cycle, with fixed RF amplitude "
    headings = [["Duty Cycle", "Input Power", "BPM Current", "X Position", "Y Position", "ADC Sum"],
                ["(0-1)", "(dBm)", "(mA)", "(mm)", "(mm)", "(Counts)"]]
    data = [dutycycle, bpm_power, bpm_current, bpm_Xpos, bpm_Ypos, ADC_sum]

    # copy the values to the report
    ReportObject.add_table_to_test('|c|c|c|c|c|c|', data, headings, caption)

    # make a caption and headings for a table of results


    # Get the plot values in a format thats easy to iterate
    format_plot = []# x axis, y axis, x axis title, y axis title, title of file, caption
    format_plot.append((dutycycle, bpm_power,'Gating signal duty cycle (0-1)', 'Power input at BPM (dBm)',"DC_vs_power.pdf"))
    format_plot.append((dutycycle, bpm_current, 'Gating signal duty cycle (0-1)', 'Beam Current at BPM (mA)', "DC_vs_current.pdf"))
    format_plot.append((dutycycle, bpm_Xpos, 'Gating signal duty cycle (0-1)', 'Horizontal Beam Position (mm)', "DC_vs_X.pdf"))
    format_plot.append((dutycycle, bpm_Ypos, 'Gating signal duty cycle (0-1)', 'Vertical Beam Position (mm)', "DC_vs_Y.pdf"))
    format_plot.append((dutycycle, ADC_sum, 'Gating signal duty cycle (0-1)', 'ADC Sum (counts)', 'DC_vs_ADC_sum.pdf'))

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
    return dutycycle, bpm_power, bpm_current, bpm_Xpos, bpm_Ypos,

