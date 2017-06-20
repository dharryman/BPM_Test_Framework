from Generic_GateSource import *
from pkg_resources import require
require("numpy")
import numpy as np


class Simulated_GateSource(Generic_GateSource):
    """Simulated Gating Device class used for hardware abstraction.

         All of the methods listed here are abstract and will be overridden by child classes, 
        this will abstract hardware as the methods here are called, but the functionality is 
        implemented by the individual children.

        Attributes:

        """

    def __init__(self):
        """Initialises the Simulated GateSource object

        Args:

        Returns:

        """
        self.dutycycle = 0
        self.enable = False
        self.period = 3
        print("Opened connection to \"Simulated GateSource\"")

    def __del__(self):
        """

        Args:

        Returns:

        """
        print("Closed connection to \"Simulated GateSource\"")


    def get_device_ID(self):
        """Override method, that will return device ID.

        Args:

        Returns:
            str: The DeviceID of the gate source.
        """
        return "Simulated GateSource"

    def turn_on_modulation(self):
        """Override method, Turn on the pulse modulation

        Args: 

        Returns:

        """
        self.enable = True
        return self.get_modulation_state()

    def turn_off_modulation(self):
        """Override method, Rurn off the pulse modulation

        Args: 

        Returns:

        """
        self.enable = False
        return self.get_modulation_state()

    def get_modulation_state(self):
        """Override method, Checks if the pulse modulation is on or off

        Args: 

        Returns:

        """
        return self.enable


    def get_pulse_period(self):
        """Override method, gets the total pulse period of the modulation signal

        Args: 
        Returns:
            str: The value of the pulse period with the units concatenated
            float: The pulse period in float form
            str: The units that the pulse period is measured in 

        """
        return self.period, str(self.period)+"uS"

    def set_pulse_period(self, period):
        """Override method, sets the total pulse period of the modulation signal

        Args:
            period (str/float): The period of the pulse modulation signal.
                if a float is used the units will be in seconds, if a string
                is used the units can be changed to ms, us, ns, etc...

        Returns:
            str: The value of the pulse period with the units concatenated.
            float: The pulse period in float form.
        """
        if type(period) != float and type(period) != int:
            raise TypeError
        elif period < 0:
            raise ValueError
        self.period = period
        return self.get_pulse_period()

    def get_pulse_dutycycle(self):
        """Override method, gets the duty cycle of the modulation signal

        The duty cycle of the signal will be set as a decimal of the pulse period.
        If the pulse period is 100us and the duty cycle input is 0.3, the pulse that 
        modulates the RF will be on for 30us, then off for 70us, then repeat. This 
        will return the decimal value.

         Args: 
         Returns:
             float: decimal value (0-1) of the duty cycle of the pulse modulation 
         """
        return self.dutycycle

    def set_pulse_dutycycle(self, dutycycle):
        """Override method, gets the duty cycle of the modulation signal

        The duty cycle of the signal will be set as a decimal of the pulse period.
        If the pulse period is 100us and the duty cycle input is 0.3, the pulse that 
        modulates the RF will be on for 30us, then off for 70us, then repeat. This 
        will return the decimal value.

        Args: 
            dutycycle (float): decimal value of the duty cycle (0-1) for the pulse modulation
        Returns:
            float: decimal value (0-1) of the duty cycle of the pulse modulation 
        """
        if type(dutycycle) != float and type(dutycycle) != int and np.float64 != np.dtype(dutycycle):
            raise TypeError
        elif dutycycle > 1 or dutycycle < 0:
            raise ValueError

        self.dutycycle = dutycycle
        return self.get_pulse_dutycycle()