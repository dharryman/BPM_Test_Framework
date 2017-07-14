from Generic_BPMDevice import *
#import sys, os
#sys.path.insert(0, os.path.abspath('..'))
from pkg_resources import require
require("numpy")
import numpy as np


class Simulated_BPMDevice(Generic_BPMDevice):
    """Simulated BPM device used for testing without the hardware. 

    All of the abstract methods in the parent class must be overridden. This class has
    access to the RF device used in the testing so that it can read in the signals that
    are supposedly provided to it via it's RF inputs. 

    Attributes:
        attenuation (float): Attenuation produced by the virtual splitter and cables
        RFSim (RF Simulator Obj) : Reference to an RF simulator 
        GateSim (Gate Source Simulator Obj) : Reference to a gate source simulator
    """

    def __init__(self, RFSim, GateSim=None):
        """Initializes the Libera BPM device object and assigns it an ID. 
        
        Args:
            RFSim (RFSignalGenerator Obj): The interface object that has access to an RF device 
                this is needed in the simulator so it can access the input values that would 
                normally come through the signals supplied to the devices inputs.
            GateSim (Gate_Source Object): The interface object that has access to a Gate Source
                device. This will typically be a simulated GateSource, this is an input to this 
                class so it know what signals are being sent to it. 
                
        Returns: 
            
        """
        print("Simulated BPM device accessed on virtual channel")
        self.attenuation = 12  # Typical attenuation when using a 4 way splitter and cables
        self.RFSim = RFSim  # Instance of the RF source used, allows the simulator to know what signals are output
        self.GateSim = GateSim  # Instance of the Gate device, allows the simulator to know what signals are output

    def get_X_position (self):
        """Override method, gets the calculated X position of the beam.
        
        Args:
        
        Returns: 
            float: X position in mm
        """
        return 0.0  # With an equal splitter there should be no X shift

    def get_Y_position(self):
        """Override method, gets the calculated X position of the beam.
        
        Args:
        
        Returns: 
            float: Y position in mm
        """
        return 0.0 # With an equal splitter there should be no Y shift

    def get_beam_current(self):
        """Override method, gets the beam current read by the BPMs. 
        
        By measuring the output power from the RF device, the input power can be assumed, then an equation extracted
        from the Rigol 30303 and Libera BPM device can be used to give an estimate of the current. 
        
        Args:
            
        Returns: 
            float: Current in mA
        """
        current = self.get_input_power()  # Gets the current input power
        current = 1000 * (1.1193) ** current # Extracted equation from Rigol3030 vs Libera BPM measurements
        return current

    def get_input_power(self):
        """Override method, gets the input power of the signals input to the device 
        
        This function assumes that a standard 4 way splitter is used, that combined with the cable losses give an 
        estimated loss of 12 dBm. This is then taken off of the output power set by the RF device giving the result. 
        
        Args:
        
        Returns: 
            float: Input power in dBm
        """
        if self.GateSim == None:  # Checks if the simulation is using a gate source
            return self.RFSim.get_output_power()[0] - self.attenuation
        elif self.GateSim.get_modulation_state() == False:  # Checks if the simulated gate source is enabled
            return self.RFSim.get_output_power()[0] - self.attenuation
        else:  # gate source must be present and enabled
            dutycycle = self.GateSim.get_pulse_dutycycle()  # Get the current duty cycle
            log_cycle = 20 * np.log10(dutycycle)  # Convert the duty cycle into dB
            # factor the duty cycle into the power read by the simulated BPM
            return (self.RFSim.get_output_power()[0] - np.absolute(log_cycle)) - self.attenuation

    def get_raw_BPM_buttons(self):
        """Override method, gets the raw signal from each BPM.
        
        Args:
            
        Returns: 
            int: Raw signal from BPM A
            int: Raw signal from BPM B
            int: Raw signal from BPM C
            int: Raw signal from BPM D
        """
        ADC = 1000 * self.get_beam_current()  # Gets a linear value for the BPM
        return ADC, ADC, ADC, ADC

    def get_normalised_BPM_buttons(self):
        """Override method, gets the normalised signal from each BPM.
        
        Args:
        
        Returns: 
            float: Normalised signal from BPM A
            float: Normalised signal from BPM B
            float: Normalised signal from BPM C
            float: Normalised signal from BPM D
        """
        return 1, 1, 1, 1  # Assumes all BPM pickups are equal

    def get_device_ID(self):
        """Override method, gets the type of BPM device that the device is
        
        Args:
        
        Returns: 
            str: Device type 
        """
        return "Simulated BPM Device"

    def get_ADC_sum(self):
        """Override method, gets the maximum input power the device can take

        The devices will break if the input power is too high, as such, each device has their
        own tolerances, this function will return this tolerance. It should be used to ensure 
        that the power put into the device is not too high to break the device. 

        Args:
        Returns: 
            float: max input power in dBm
        """
        a, b, c, d = self.get_raw_BPM_buttons()
        sum = a + b + c + d  # Sums the BPM values used in the simulator
        return sum

    def get_input_tolerance(self):
        """Override method, gets the maximum input power the device can take

        The devices will break if the input power is too high, as such, each device has their
        own tolerances, this function will return this tolerance. It should be used to ensure 
        that the power put into the device is not too high to break the device. 

        Args:

        Returns: 
            float: max input power in dBm
        """
        return -40  # Max tolerance of the simulated device, as low as the most susceptible real device

