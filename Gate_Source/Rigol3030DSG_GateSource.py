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
        self.tn.write(message + "\r\n")

    def _telnet_read(self):
        """Private method that will read a telnet reply from the Rigol3030
        
        Args:
            
        Returns:
            str: Reply message from the Rigol3030
        """
        return self.tn.read_until("\n", self.timeout).rstrip('\n')

    # Constructor and Deconstructor

    def __init__(self, ipaddress, port=5555, timeout=1):
        """Initialises and opens the connection to the Rigol3030 over telnet and informs the user 

        Args:
            ipaddress (str): The IP address of the Rigol3030 
            port (int/str): The port number for the messages to be sent on (default 5555)
            timeout (float): The timeout for telnet commands in seconds (default 1)
            
        Returns:
            
        """
        self.timeout = timeout
        self.tn = telnetlib.Telnet(ipaddress, port, self.timeout)
        self.get_device_ID()
        self.modulation_state = False
        self.turn_off_modulation()
        self._telnet_write("PULM:SOUR INT")
        self._telnet_write("PULM:TRIG:MODE AUTO")
        self.pulse_period = self.set_pulse_period(3)
        self.set_pulse_dutycycle(0)

        print("Opened connection to gate source " + self.DeviceID)

    def __del__(self):
        """Closes the telnet connection to the Rigol3030
        
        Args:
            
        Returns:
        
        """
        self.turn_off_modulation()
        self.tn.close()
        print("Closed connection to " + self.DeviceID)

    # API Methods
    def get_device_ID(self):
        """Override method, Gets the Device Id of the Rigol3030
        
        Args:
            
        Returns:
            str: The DeviceID of the gate source.
        """
        self.DeviceID = self._telnet_query("*IDN?")
        if self.DeviceID[0:26] != "Rigol Technologies,DSG3030":
            raise Exception("Wrong hardware device connected")
        return "Gating Device "+self.DeviceID

    def turn_on_modulation(self):
        """Override method, Turns on the pulse modulation.

        When used in conjunction with the Rigol3030 RF SigGen class, This 
        function will turn on the pulse output, and modulation the RF output 
        with this signal. The RF output must turned off/on independently.

        Args: 
            
        Returns:

        """
        self._telnet_write("PULM:OUT:STAT ON")
        self._telnet_write("PULM:STAT ON")
        self._telnet_write("MOD:STAT ON")
        return self.get_modulation_state()

    def turn_off_modulation(self):
        """Override method, Turns on the pulse modulation.

        When used in conjunction with the Rigol3030 RF SigGen class, This 
        function will turn off the pulse output, and modulation the RF output 
        with this signal. The RF output must turned off/on independently.

        Args: 

        Returns:

        """
        self._telnet_write("PULM:OUT:STAT OFF")
        self._telnet_write("PULM:STAT OFF")
        self._telnet_write("MOD:STAT OFF")
        return self.get_modulation_state()

    def get_modulation_state(self):
        """Override method, Checks if the pulse modulation is on or off

        Args: 

        Returns:

        """
        modulation  = self._telnet_query("MOD:STAT?")
        if modulation == "0":
            self.modulation_state = False
        elif modulation == "1":
            self.modulation_state = True

        return self.modulation_state

    def get_pulse_period(self):
        """Override method, Gets the total pulse period of the modulation signal

            Args: 

            Returns:
                str: The value of the pulse period with the units concatenated
                float: The pulse period in float form
                str: The units that the pulse period is measured in 

        """
        self.pulse_period = self._telnet_query("PULM:PER?")
        return float(self._split_num_char(self.pulse_period)[0]), self.pulse_period


    def set_pulse_period(self, period):
        """Override method, Sets the total pulse period of the modulation signal

            Args:
                period (float): The period of the pulse modulation signal is uS.

            Returns:
                float: The pulse period in float form.
                str: The value of the pulse period with the units concatenated.
        """

        if type(period) != float and type(period) != int and np.float64 != np.dtype(period):
            raise TypeError
        elif period < 0:
            raise ValueError

        self._telnet_write("PULM:PER "+str(period)+"us")
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
        pulse_width = self._telnet_query("PULM:WIDT?")
        pulse_width = self._split_num_char(pulse_width)[0]
        period = self.get_pulse_period()[0]
        pulse_width = float(pulse_width)
        return pulse_width/period


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
        if type(dutycycle) != float and type(dutycycle) != int and np.float64 != np.dtype(dutycycle):
            raise TypeError
        elif dutycycle > 1 or dutycycle < 0:
            raise ValueError

        dutycycle = (self.get_pulse_period()[0])*dutycycle
        self._telnet_write("PULM:WIDT "+str(dutycycle)+"us")
        return self.get_pulse_dutycycle()


    def invert_pulse_polarity(self, polarity):
        """Inverts the polarity of the gate signal
        
        True will invert the signal, false will return it to it's default state. 

        Args: 
            polarity (bool): boolean that decides the inversion state
        Returns:
            bool: The current state of the inversion
        """
        if type(polarity) != bool:
            raise TypeError

        if polarity == True:
            self._telnet_write("PULM:POL INV")
        else:
            self._telnet_write("PULM:POL NORM")

        return self.get_pulse_polarity()

    def get_pulse_polarity(self):
        """Checks if the signal is inverted or not

        Args: 
        Returns:
            bool: The current state of the inversion
        """
        return self._telnet_query("PULM:POL?")