from abc import ABCMeta, abstractmethod


class Generic_GateSource():
    """Generic Gating Device class used for hardware abstraction.
    
     All of the methods listed here are abstract and will be overridden by child classes, 
    this will abstract hardware as the methods here are called, but the functionality is 
    implemented by the individual children.
    
    Attributes:

    """
    __metaclass__ = ABCMeta  # Allows for abstract methods to be created.

    def _split_num_char(self, s):
        """Private method to split up a numeric and characters. 

        This should be used to split a value with it's units into two separate strings.
        i.e. "-70.5 dBm" will return "-70.5" and "dBm" separately. 
        Args:
            s (str): The string that is to be disseminated.

        Returns:
            str: The numeric characters in the string provided.  
            str: The non numeric characters in the string provided. 
        """

        number = ''
        unit = ''
        s = str(s)
        for c in s:
            if c.isdigit() or c == "." or c == "-":
                number += c
            else:
                unit += c

        return (number, unit)

    @abstractmethod
    def get_device_ID(self):
        """Abstract method for override that will return device ID.
        
        Args:
        
        Returns:
            str: The DeviceID of the gate source.
        """
        pass

    @abstractmethod
    def turn_on_modulation(self):
        """Abstract method for override that will turn on the pulse modulation
        
        Args: 

        Returns:
            
        """
        pass

    @abstractmethod
    def turn_off_modulation(self):
        """Abstract method for override that will turn off the pulse modulation

        Args: 

        Returns:

        """
        pass

    @abstractmethod
    def get_modulation_state(self):
        """Abstract method for override, checks if the pulse modulation is on or off

        Args: 
 
        Returns:

        """
        pass

    @abstractmethod
    def get_pulse_period(self):
        """Abstract method for override, gets the total pulse period of the modulation signal
        
        Args: 

        Returns:
            str: The value of the pulse period with the units concatenated
            float: The pulse period in float form
            str: The units that the pulse period is measured in 
        
        """
        pass

    @abstractmethod
    def set_pulse_period(self, period):
        """Abstract method for override sets the total pulse period of the modulation signal
        
        Args:
            period (str/float): The period of the pulse modulation signal.
                if a float is used the units will be in seconds, if a string
                is used the units can be changed to ms, us, ns, etc...

        Returns:
            str: The value of the pulse period with the units concatenated.
            float: The pulse period in float form.
            str: The units that the pulse period is measured in.
        """
        pass

    @abstractmethod
    def get_pulse_dutycycle(self):
        """Abstract method for override, gets the duty cycle of the modulation signal
        
        The duty cycle of the signal will be set as a decimal of the pulse period.
        If the pulse period is 100us and the duty cycle input is 0.3, the pulse that 
        modulates the RF will be on for 30us, then off for 70us, then repeat. This 
        will return the decimal value.

         Args: 
             
         Returns:
             float: decimal value (0-1) of the duty cycle of the pulse modulation 
         """
        pass

    @abstractmethod
    def set_pulse_dutycycle(self, dutycycle):
        """Abstract method for override, gets the duty cycle of the modulation signal

        The duty cycle of the signal will be set as a decimal of the pulse period.
        If the pulse period is 100us and the duty cycle input is 0.3, the pulse that 
        modulates the RF will be on for 30us, then off for 70us, then repeat. This 
        will return the decimal value.

        Args: 
            dutycycle (float): decimal value of the duty cycle (0-1) for the pulse modulation
        Returns:
            float: decimal value (0-1) of the duty cycle of the pulse modulation 
        """
        pass