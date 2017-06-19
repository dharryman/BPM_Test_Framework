from Generic_RFSigGen import *

class Template_RFSigGen(Generic_RFSigGen):
    """template, Child of Generic_RFSigGen.

    Attributes:  
        *Inherited from parent.
    """

    # Private Methods go here

    # Constructor and Deconstructor
    def __init__(self):
        """

        Args:
            
        Returns:
            
        """

    def __del__(self):
        """

        Args:

        Returns:

        """

    # API Calls
    def get_device_ID(self):
        """Override method that will return the device ID.

        Returns:
            str: The DeviceID of the SigGen.
        """

    def get_output_power(self):
        """Override method that will return the output power.. 

        Returns:
            str: The current output power concatenated with the units.
            float: The current power value as a float and assumed units. 
        """

    def get_frequency(self):
        """Override method that will get the output frequency of the SigGen

        Returns:
            str: The current output frequency concatenated with the units.
            float: The current frequency value as a float and assumed units. 
        """

    def set_frequency(self, frequency):
        """Override method that will set the output frequency.

        Args:
            frequency (float/str): Desired value of the output frequency. If a float is sent the default 
                units of MHz are used, otherwise using a string different units can be selected. 
        Returns:
            str: The current output frequency concatenated with the units.
            float: The current frequency value as a float and assumed units. 
        """

    def set_output_power(self, power):
        """Override method that will set the output power.

        Args:
            power (float/str): Desired value of the output power. If a float is sent the default 
                units of dBm are used, otherwise using a string different units can be selected. 
        Returns:
            str: The current output power concatenated with the units.
            float: The current power value as a float and assumed units. 
        """

    def turn_on_RF(self):
        """Override method that will turn on the RF device output.

        Returns:
            bool: Returns True if the output is enabled, False if it is not. 
        """

    def turn_off_RF(self):
        """Override method that will turn off the RF device output. 

        Returns:
            bool: Returns True if the output is enabled, False if it is not.
        """

    def get_output_state(self):
        """Override method that will get the current output state. 

        Returns:
            bool: Returns True if the output is enabled, False if it is not. 
        """

