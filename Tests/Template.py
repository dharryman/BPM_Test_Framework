import RFSignalGenerators
import BPMDevice
from pkg_resources import require

require("numpy")
require("cothread")
require("matplotlib")
import numpy as np
import matplotlib.pyplot as plt
import time



def Template(RF,
             BPM,
             argument1 = 1,
             argument2 = 2,
             argument3 = 3,
             argument4 = 4,
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

    # Readies devices that are used in the test so that they can be added to the report
    device_names = []
    device_names.append(RF.get_device_ID())
    device_names.append(BPM.get_device_ID())

    # Readies parameters that are used in the test so that they can be added to the report
    parameter_names = []
    parameter_names.append("Argument1: " + str(argument1))
    parameter_names.append("Argument2: " + str(argument2))
    parameter_names.append("Argument3: " + str(argument3))
    parameter_names.append("Argument4: " + str(argument4))

    # Perform the test and plot the results
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = []
    for index in x:
        y.append(2*index)

    plt.plot(x,y)

    if report == None:
        # If no report is entered as an input to the test, simply display the results
        plt.show()
    else:
        # If there is a report for the data to be copied to, do so.
        plt.savefig(test_name + ".pdf")
        report.setup_test(test_name, intro_text, device_names, parameter_names)
        report.add_figure_to_test(test_name)


