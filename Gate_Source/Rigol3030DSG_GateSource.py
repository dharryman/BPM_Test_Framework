from Generic_GateSource import *
import telnetlib
from pkg_resources import require
require("numpy")
import numpy as np

class CustomException(Exception):
    pass

class Rigol3030DSG_GateSource(Generic_GateSource):

    # Private Methods
    def _telnet_query(self, message):
        """Private method that will send a message over telnet to the Rigol3030 and return the reply

        Args:
            message (str)l: SCPI message to be sent to the Rigol3030

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
        self.tn.write(message + "\r\n")  # Writes telnet message to connected device, with termination chars added

    def _telnet_read(self):
        """Private method that will read a telnet reply from the Rigol3030
        
        Args:
            
        Returns:
            str: Reply message from the Rigol3030
        """
        return self.tn.read_until("\n", self.timeout).rstrip('\n')  # Reads reply from device, strips termination char

    # Constructor and Deconstructor

    def __init__(self, ipaddress, port=5555, timeout=1):
        """Initialises and opens the connection to the Rigol3030 over telnet and informs the user 

        Args:
            ipaddress (str): The IP address of the Rigol3030 
            port (int/str): The port number for the messages to be sent on (default 5555)
            timeout (float): The timeout for telnet commands in seconds (default 1)
            
        Returns:
            
        """
        self.timeout = timeout  # Sets timeout for the telnet calls
        self.tn = telnetlib.Telnet(ipaddress, port, self.timeout)  # Connects to the IP via telnet
        self.get_device_ID()  # Gets the device ID, checks connection is made
        self.modulation_state = False  # Default parameter for the modulation state
        self.turn_off_modulation()  # Turns off the signal modulation
        self._telnet_write("PULM:SOUR INT")  # Sets the trigger source for the pulse
        self._telnet_write("PULM:TRIG:MODE AUTO")  # Sets the trigger mode for the source
        self.pulse_period = self.set_pulse_period(3)  # Sets the pulse period to 3us by default
        self.set_pulse_dutycycle(0)  # Sets the duty cycle to 0 by default
        print("Opened connection to gate source " + self.DeviceID)  # Inform the user the device is connected to

    def __del__(self):
        """Closes the telnet connection to the Rigol3030
        
        Args:
            
        Returns:
        
        """
        self.turn_off_modulation()  # Turns off the signal modulation
        self.tn.close()  # Closes the telnet connection
        print("Closed connection to gate source " + self.DeviceID)  # Lets the user know connection is closed

    # API Methods
    def get_device_ID(self):
        """Override method, Gets the Device Id of the Rigol3030
        
        Args:
            
        Returns:
            str: The DeviceID of the gate source.
        """
        self.DeviceID = self._telnet_query("*IDN?")  # Asks the device to identify itself
        #if self.DeviceID[0:26] != "Rigol Technologies,DSG3030":  # Checks the right device is connected
        #    raise Exception("Wrong hardware device connected")  # Error if wrong device
        return "Gating Device "+self.DeviceID  # Returns the device info

    def turn_on_modulation(self):
        """Override method, Turns on the pulse modulation.

        When used in conjunction with the Rigol3030 RF SigGen class, This 
        function will turn on the pulse output, and modulation the RF output 
        with this signal. The RF output must turned off/on independently.

        Args: 
            
        Returns:

        """
        self._telnet_write("PULM:OUT:STAT ON")  # Turns on the pulse output switch
        self._telnet_write("PULM:STAT ON")  # Enables the modulation state function
        self._telnet_write("MOD:STAT ON")  # Turns on the modulation state output
        return self.get_modulation_state()

    def turn_off_modulation(self):
        """Override method, Turns on the pulse modulation.

        When used in conjunction with the Rigol3030 RF SigGen class, This 
        function will turn off the pulse output, and modulation the RF output 
        with this signal. The RF output must turned off/on independently.

        Args: 

        Returns:

        """
        self._telnet_write("PULM:OUT:STAT OFF")  # Turns off the pulse output switch
        self._telnet_write("PULM:STAT OFF")  # Disables the modulation state function
        self._telnet_write("MOD:STAT OFF")  # Turns off the modulation state output
        return self.get_modulation_state()

    def get_modulation_state(self):
        """Override method, Checks if the pulse modulation is on or off

        Args: 

        Returns:

        """
        modulation  = self._telnet_query("MOD:STAT?")  # Checks the modulation state
        if modulation == "0":
            self.modulation_state = False  # If it isn't, return a False
        elif modulation == "1":
            self.modulation_state = True  # If it is, return a True
        return self.modulation_state

    def get_pulse_period(self):
        """Override method, Gets the total pulse period of the modulation signal

        Args: 

        Returns:
            str: The value of the pulse period with the units concatenated
            float: The pulse period in float form
            str: The units that the pulse period is measured in 

        """
        self.pulse_period = self._telnet_query("PULM:PER?")  # Gets the pulse period of the device
        # Returns the pulse period as a float, and a string with the units
        return float(self._split_num_char(self.pulse_period)[0]), self.pulse_period

    def set_pulse_period(self, period):
        """Override method, Sets the total pulse period of the modulation signal

        Args:
            period (float): The period of the pulse modulation signal is uS.

        Returns:
            float: The pulse period in float form.
            str: The value of the pulse period with the units concatenated.
        """
        # if the period input is not a numeric type then error out
        if type(period) != float and type(period) != int and np.float64 != np.dtype(period):
            raise TypeError
        # if the period is a negative number it is invalid, so error out
        elif period < 0:
            raise ValueError

        self._telnet_write("PULM:PER "+str(period)+"us")  # use default units of microseconds, and set the period
        return self.get_pulse_period()

    def get_pulse_dutycycle(self):
        """Override method, Gets the duty cycle of the modulation signal

        The duty cycle of the signal will be set as a decimal of the pulse period.
        If the pulse period is 100us and the duty cycle input is 0.3, the pulse that 
        modulates the RF will be on for 30us, then off for 70us, then repeat. This 
        will return the decimal value.

         Args: 

         Returns:
             float: decimal value (0-1) of the duty cycle of the pulse modulation 
         """
        pulse_width = self._telnet_query("PULM:WIDT?")  # Gets the pulse width
        pulse_width = self._split_num_char(pulse_width)[0]  # converts the pulse width into a numeric
        period = self.get_pulse_period()[0]  # gets the pulse period numeric
        pulse_width = float(pulse_width) # makes sure the pulse width is a numeric
        return pulse_width/period  # calculates the duty cycle and returns it

    def set_pulse_dutycycle(self, dutycycle):
        """Override method, Gets the duty cycle of the modulation signal

        The duty cycle of the signal will be set as a decimal of the pulse period.
        If the pulse period is 100us and the duty cycle input is 0.3, the pulse that 
        modulates the RF will be on for 30us, then off for 70us, then repeat. This 
        will return the decimal value.

        Args: 
            dutycycle (float): decimal value of the duty cycle (0-1) for the pulse modulation
        Returns:
            float: decimal value (0-1) of the duty cycle of the pulse modulation 
        """
        # makes sure the udty cycle value is a numeric
        if type(dutycycle) != float and type(dutycycle) != int and np.float64 != np.dtype(dutycycle):
            raise TypeError
        # makes sure the duty cycle value is a decimal between 0 and 1
        elif dutycycle > 1 or dutycycle < 0:
            raise ValueError

        dutycycle = (self.get_pulse_period()[0])*dutycycle  # calculates the pulse width given the desired duty cycle
        self._telnet_write("PULM:WIDT "+str(dutycycle)+"us")  # writes the calculated pulse width
        return self.get_pulse_dutycycle()

    def invert_pulse_polarity(self, polarity):
        """Inverts the polarity of the gate signal
        
        True will invert the signal, false will return it to it's default state. 

        Args: 
            polarity (bool): boolean that decides the inversion state
        Returns:
            bool: The current state of the inversion
        """
        # makes sure a boolean is the input type
        if type(polarity) != bool:
            raise TypeError

        # if a true is used, invert the pulse polarity
        if polarity == True:
            self._telnet_write("PULM:POL INV")
        # if a false if used reset the pulse polarity to default
        else:
            self._telnet_write("PULM:POL NORM")

        return self.get_pulse_polarity()

    def get_pulse_polarity(self):
        """Checks if the signal is inverted or not

        Args: 
        Returns:
            bool: The current state of the inversion
        """
        return self._telnet_query("PULM:POL?")  # check if the polarity is inverted or not