from abc import ABCMeta, abstractmethod

class Generic_RFSigGen():
    """Generic RF signal generator class used for hardware abstraction.
    
    All of the methods listed here are abstract and will be overridden by child classes, 
    this will abstract hardware as the methods here are called, but the functionality is 
    implemented by the individual children.

    Attributes:
        Output_Power (float/str): The output power of the RF SigGen. As a float default units will be 
            dBm, using a string new units can be selected. 
        Frequency (float/str): The frequency output from the RF SigGen. As a float default units will be 
            MHz, using a string new units can be selected. 
        Output_state (bool): RF output enabled flag.
        DeviceID (str): The specific ID or model of the SigGen.
    """
    __metaclass__ = ABCMeta # Allows for abstract methods to be created.

    Output_Power = "0DBM"
    Frequency = "0DBM"
    Output_State = False
    DeviceID = 'Abstract Device Class'

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

        Returns:
            str: The DeviceID of the SigGen.
        """
        pass

    @abstractmethod
    def set_frequency(self,frequency):
        """Abstract method for override that will set the output frequency.

        Args:
            frequency (float/str): Desired value of the output frequency. If a float is sent the default 
                units of MHz are used, otherwise using a string different units can be selected. 
        Returns:
            float: The current frequency value as a float and assumed units. 
            str: The current output frequency concatenated with the units.
        """
        pass

    @abstractmethod
    def get_frequency(self):
        """Abstract method for override that will get the output frequency of the SigGen
        
        Args:
        
        Returns:
            float: The current frequency value as a float and assumed units. 
            str: The current output frequency concatenated with the units.
        """
        pass

    @abstractmethod
    def set_output_power(self, power):
        """Abstract method for override that will set the output power.
        
        Args:
            power (float/str): Desired value of the output power. If a float is sent the default 
                units of dBm are used, otherwise using a string different units can be selected. 
        Returns:
            float: The current power value as a float and assumed units. 
            str: The current output power concatenated with the units.
        """
        pass

    @abstractmethod
    def get_output_power(self):
        """Abstract method for override that will return the output power.
        
        Args:
        
        Returns:
            float: The current power value as a float and assumed units. 
            str: The current output power concatenated with the units.
        """
        pass

    @abstractmethod
    def turn_on_RF(self):
        """Abstract method for override that will turn on the RF device output.
        
        Args: 
            
        Returns:
            bool: Returns True if the output is enabled, False if it is not. 
        """
        pass

    @abstractmethod
    def turn_off_RF(self):
        """Abstract method for override that will turn off the RF device output.
        
        Args:
        
        Returns:
            bool: Returns True if the output is enabled, False if it is not.
        """
        pass

    @abstractmethod
    def get_output_state(self):
        """Abstract method for override that will get the current output state. 
        
        Args:

        Returns:
            bool: Returns True if the output is enabled, False if it is not. 
        """
        pass

    @abstractmethod
    def set_output_power_limit(self, limit):
        """Abstract method for override that will set a hardware limit for the output power
        
        Args:

        Returns:
            float: The power limit 
        """
        pass

    @abstractmethod
    def get_output_power_limit(self):
        """Abstract method for override that will get the hardware limit for the output power
        
        Args:

        Returns:
            float: The power limit 
        """
        pass





