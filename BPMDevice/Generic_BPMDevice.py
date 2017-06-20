from abc import ABCMeta, abstractmethod

class Generic_BPMDevice():
    """Generic BPM Device class used for hardware abstraction.

    All of the methods listed here are abstract and will be overridden by child classes, 
    this will abstract hardware as the methods here are called, but the functionality is 
    implemented by the individual children.

    Attributes:
    """

    __metaclass__ = ABCMeta  # Allows for abstract methods to be created.

    @abstractmethod
    def get_X_position (self):
        """Abstract method for override, gets the calculated X position of the beam.
        
        Args:
        Returns: 
            float: X position in mm
        """
        pass

    @abstractmethod
    def get_Y_position(self):
        """Abstract method for override, gets the calculated X position of the beam.
        
        Args:
        Returns: 
            float: Y position in mm
        """
        pass

    @abstractmethod
    def get_beam_current(self):
        """Abstract method for override, gets the beam current read by the BPMs. 
        
        Args:
        Returns: 
            float: Current in mA
        """
        pass

    @abstractmethod
    def get_input_power(self):
        """ Abstract method for override, gets the input power of the signals input to the device 
        
        Args:  
        Returns: 
            float: Input power in dBm
            
        """
        pass

    @abstractmethod
    def get_raw_BPM_buttons(self):
        """Abstract method for override, gets the raw signal from each BPM.
        
        Args:
        Returns: 
            
            int: Raw signal from BPM A
            int: Raw signal from BPM B
            int: Raw signal from BPM C
            int: Raw signal from BPM D
        """
        pass

    @abstractmethod
    def get_normalised_BPM_buttons(self):
        """Abstract method for override, gets the normalised signal from each BPM.
        
        Args:
        Returns: 
            float: Normalised signal from BPM A
            float: Normalised signal from BPM B
            float: Normalised signal from BPM C
            float: Normalised signal from BPM D
        """
        pass

    @abstractmethod
    def get_device_ID(self):
        """Abstract method for override, gets the device name or type of the BPM.

        Args:
        Returns: 
            str: Type of BPM with MAC address
        """
        pass

    @abstractmethod
    def get_input_tolerance(self):
        """Abstract method for override, gets the maximum input power the device can take

        Args:
        Returns: 
            float: max input power in dBm
        """
        pass

    @abstractmethod
    def get_ADC_sum(self):
        """Abstract method for override, gets the sum of all of the buttons ADCs
        
        A+B+C+D

        Args:
        Returns: 
            int: ADC sum in counts
        """
        pass



