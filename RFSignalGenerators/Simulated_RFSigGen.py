from Generic_RFSigGen import Generic_RFSigGen
from pkg_resources import require
require("numpy")
import numpy as np
import warnings

class CustomException(Exception):
    pass

class Simulated_RFSigGen(Generic_RFSigGen):
    """Simulated_RFSigGen Class, Child of Generic_RFSigGen

    This class is for simulating an RF signal generator device. It is designed 
    to override all of the abstract methods in it's parent. 

    Attributes:
        *Inherited from parent.
    """

    # Constructor and Deconstructor.
    def __init__(self, limit = -40):
        """Informs the user when the simulated device has been created in memory.
        
        The simulated device for the RF sig gen does not need any arguments. It's main 
        purpose is to repeat values that have been given to it with the 'set' methods. 
        
        Args:
            
        Returns:
        
        """
        self.DeviceID = "Simulated RF Device"  # Changed to simulated device ID.
        self.Output_Power = 0
        self.Frequency = 0
        self.Output_State = False
        self.limit = limit
        print("Constructed " + self.DeviceID)

    def __del__(self):
        """Informs the user when the simulated device has been removed from memory.
        
        This is not needed but for some RF devices the connection must be closed, as 
        such they will give a message when this happens, so the simulator should do 
        the same. 
        
        Args:
            
        Returns:
        """
        print("Deconstructed " + self.DeviceID)

    # API Calls

    def get_device_ID(self):
        """Override method that will return the device ID.

        Args:
        
        Returns:
            str: The DeviceID of the SigGen.
        """
        return self.DeviceID

    def get_output_power(self):
        """Override method that will return the output power.
        
        Args:
            
        Returns:
            str: The current output power concatenated with the units.
            float: The current power value as a float and assumed units. 
        """
        return self.Output_Power, str(self.Output_Power) + "dBm"

    def set_output_power(self, power):
        """Override method that will set the output power.
        
        Args:
            power (float): Desired value of the output power. If a float is sent the default 
                units of dBm are used, otherwise using a string different units can be selected. 
        Returns:
            str: The current output power concatenated with the units.
            float: The current power value as a float and assumed units. 
        """
        if type(power) != float and type(power) != int and np.float64 != np.dtype(power):
            raise TypeError
        elif power > self.limit: # If a value that is too high is used, the hardware may break.
            power = self.limit
            warnings.warn('Power limit has been reached, output will be capped')

        self.Output_Power = power
        return self.get_output_power()

    def get_frequency(self):
        """Override method that will get the output frequency of the SigGen
        
        Args:
            
        Returns:
            str: The current output frequency concatenated with the units.
            float: The current frequency value as a float and assumed units. 
        """
        return self.Frequency, str(self.Frequency)+"MHz"

    def set_frequency(self,frequency):
        """Override method that will set the output frequency.

        Args:
            frequency (float/str): Desired value of the output frequency. If a float is sent the default 
                units of MHz are used, otherwise using a string different units can be selected. 
        Returns:
            str: The current output frequency concatenated with the units.
            float: The current frequency value as a float and assumed units. 
        """
        if type(frequency) != float and type(frequency) != int and np.float64 != np.dtype(frequency):
            raise TypeError
        elif frequency < 0:
            raise ValueError

        self.Frequency = frequency
        return self.get_frequency()

    def turn_on_RF(self):
        """Override method that will turn on the RF device output.
        
        Args: 
            
        Returns:
            bool: Returns True if the output is enabled, False if it is not. 
        """
        self.Output_State = True
        return self.Output_State

    def turn_off_RF(self):
        """Override method that will turn off the RF device output.
        
        Args: 
            
        Returns:
            bool: Returns True if the output is enabled, False if it is not.
        """
        self.Output_State = False
        return self.Output_State

    def get_output_state(self):
        """Override method that will get the current output state. 
        
        Args: 
            
        Returns:
            bool: Returns True if the output is enabled, False if it is not. 
        """
        return self.Output_State

    def set_output_power_limit(self, limit):
        """Override method that will set a hardware limit for the output power
        Args:

        Returns:
            float: The power limit 
        """
        if type(limit) != float and type(limit) != int and np.float64 != np.dtype(limit):
            raise TypeError
        self.limit = limit
        return self.get_output_power_limit()

    def get_output_power_limit(self):
        """Override method that will get the hardware limit for the output power
        Args:

        Returns:
            float: The power limit 
        """
        return self.limit, str(self.limit)+"dBm"

