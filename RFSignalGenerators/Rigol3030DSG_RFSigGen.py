from Generic_RFSigGen import *
import telnetlib
from pkg_resources import require
require("numpy")
import numpy as np
import warnings

class Rigol3030DSG_RFSigGen(Generic_RFSigGen):
    """Rigol3030DSG RFSigGen, Child of Generic_RFSigGen.

    This class is for communicating with the Rigol3030 over telnet. The specific API calls abstract the SCPI 
    commands needed to speak with the instrument. Each of these calls is an override of the Generic_RFSigGen.

    Attributes:  
        *Inherited from parent.
    """

    #Private Methods
    def _telnet_query(self, message):
        """Private method that will send a message over telnet to the Rigol3030 and return the reply

        Args:
            message (str): SCPI message to be sent to the Rigol3030

        Returns:
            str: Reply message from the Rigol3030
        """
        self._telnet_write(message)
        return self._telnet_read()

    def _telnet_write(self, message):
        """Private method that will send a message over telnet to the Rigol3030 

        Args:
            message (str): SCPI message to be sent to the Rigol3030
            
        Returns:
            
        """
        # Checks that the telnet message is a string
        if type(message) != str:
            raise TypeError

        self.tn.write(message + "\r\n")  # Writes a telnet message with termination characters

    def _telnet_read(self):
        """Private method that will read a telnet reply from the Rigol3030
        
        Args:
        
        Returns:
            str: Reply message from the Rigol3030
        """
        return self.tn.read_until("\n", self.timeout).rstrip('\n')  # Telnet reply, with termination chars removed

    #Constructor and Deconstructor

    def __init__(self, ipaddress, port = 5555, timeout = 1, limit=-40):
        """Initialises and opens the connection to the Rigol3030 over telnet and informs the user 

        Args:
            ipaddress (str): The IP address of the Rigol3030 
            port (int/str): The port number for the messages to be sent on (default 5555)
            timeout (float): The timeout for telnet commands in seconds (default 1)
            
        Returns:
            
        """
        self.timeout = timeout  # timeout for the telnet comms
        self.tn = telnetlib.Telnet(ipaddress, port, self.timeout)  # connects to the telnet device
        self.get_device_ID()  # gerts the device of the telnet device, makes sure its the right one
        self.turn_off_RF()  # turn off the RF output
        self.set_output_power_limit(limit)  # set the RF output limit

        print("Opened connection to RF source" + self.DeviceID)  # tells the user the device has been connected to

    def __del__(self):
        """Closes the telnet connection to the Rigol3030
        """
        self.turn_off_RF()  # make sure the RF output if off
        self.tn.close()  # close the telnet link
        print("Closed connection to " + self.DeviceID)  # tell the user the telnet link has closed

    #API Calls
    def get_device_ID(self):
        """Override method that will return the device ID.
        
        Uses the SCPI command "*IDN?" to get the device ID. 

        Args:

        Returns:
            str: The DeviceID of the SigGen.
        """
        self.DeviceID = self._telnet_query("*IDN?")  # gets the device information
        if self.DeviceID[0:26] != "Rigol Technologies,DSG3030":  # checks it's the right device
            raise Exception("Wrong hardware device connected")
        return "RF Source "+self.DeviceID

    def get_output_power(self):
        """Override method that will return the output power.
        
        Uses the "commands LEV?" amd "UNIT:POW?" to get the current output power level and units. 
        
        Args:
        
        Returns:
            float: The current power value as a float in dBm
            str: The current output power concatenated with the units.
        """

        self.Output_Power = self._telnet_query("LEV?") + self._telnet_query("UNIT:POW?")  # get the power & power units
        return float(self._split_num_char(self.Output_Power)[0]), self.Output_Power

    def get_frequency(self):
        """Override method that will get the output frequency of the SigGen
        
        Uses the SCPI command "FREQ?" to get the set frequency. 
        
        Args:
        
        Returns:
            float: The current frequency value as a float and assumed units. 
            str: The current output frequency concatenated with the units.
        """

        self.Frequency = self._telnet_query("FREQ?")  # get the device frequency
        return float(self._split_num_char(self.Frequency)[0]), self.Frequency

    def set_frequency(self, frequency):
        """Override method that will set the output frequency.
        
        SCPI command "FREQ" is used to set the output frequency level. 
        
        Args:
            frequency (float): Desired value of the output frequency in MHz.
        Returns:
            float: The current frequency value as a float and assumed units. 
            str: The current output frequency concatenated with the units.
        """
        # check the input is a numeric
        if type(frequency) != float and type(frequency) != int and np.float64 != np.dtype(frequency):
            raise TypeError
        # check the output is a positive number
        elif frequency < 0:
            raise ValueError

        self.Frequency = frequency
        self._telnet_write("FREQ " + str(self.Frequency) + "MHz")  # Write the frequency value in MHz
        return self.get_frequency()

    def set_output_power(self, power):
        """Override method that will set the output power.
        
        The SCPI command "UNIT:POW" is used to set the units of the power output, then the 
        command "LEV" is used to set the output level in those units. 

        Args:
            power (float): Desired value of the output power in dBm.  
        Returns:
            float: The current power value as a float in dBm
            str: The current output power concatenated with the units. 
        """
        # check the input is a numeric
        if type(power) != float and type(power) != int and np.float64 != np.dtype(power):
            raise TypeError
        elif power > self.limit: # If a value that is too high is used, the hardware may break.
            power = self.limit
            # tell the user the limit has been reached and cap the output level
            warnings.warn('Power limit has been reached, output will be capped')
        self.Output_Power = power

        self._telnet_write("UNIT:POW dBm")  # make sure the units are dBm
        self._telnet_write("LEV " + str(power))  # write the new output power
        return self.get_output_power()

    def turn_on_RF(self):
        """Override method that will turn on the RF device output.
        
        Uses SCPI command "OUTP ON" to turn on the device.
        
        Args:
        
        Returns:
            bool: Returns True if the output is enabled, False if it is not. 
        """
        self._telnet_write("OUTP ON")  # turns on the output
        return self.get_output_state()

    def turn_off_RF(self):
        """Override method that will turn off the RF device output.

        Uses SCPI command "OUTP OFF" to turn off the device. 
        
        Args:
        
        Returns:
            bool: Returns True if the output is enabled, False if it is not.
        """
        self._telnet_write("OUTP OFF")  # turns off the output
        return self.get_output_state()

    def get_output_state(self):
        """Override method that will get the current output state. 
    
        This method send the SCPI command "OUTP?" to request the output state from
        the Rigol3030. 
        
        Args:
        
        Returns:
            bool: Returns True if the output is enabled, False if it is not. 
        """
        # checks output state
        if self._telnet_query("OUTP?") == "1":
            self.Output_State = True  # output must be on
            return True
        else:
            self.Output_State = False  # output must be off
            return False

    def set_output_power_limit(self, limit):
        """Override method that will set a hardware limit for the output power
        
        Args:

        Returns:
            float: The power limit 
        """
        # checks the input is a numeric
        if type(limit) != float and type(limit) != int and np.float64 != np.dtype(limit):
            raise TypeError
        self.limit = limit
        self._telnet_write("UNIT:POW dBm")  # makes sure the limit units are in dBm
        self._telnet_write("LEV:LIM "+ str(limit))  # sets the output level
        return self.get_output_power_limit()

    def get_output_power_limit(self):
        """Override method that will get the hardware limit for the output power
        
        Args:

        Returns:
            float: The power limit 
        """
        self.limit = float(self._telnet_query("LEV:LIM?"))  # gets the output limit
        str_limit = self._telnet_query("LEV:LIM?") + self._telnet_query("UNIT:POW?")  # gets the limit and the units
        return self.limit, str_limit