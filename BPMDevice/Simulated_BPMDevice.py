from Generic_BPMDevice import *
#import sys, os
#sys.path.insert(0, os.path.abspath('..'))


class Simulated_BPMDevice(Generic_BPMDevice):
    """Simulated BPM device used for testing without the hardware. 

    All of the abstract methods in te parent class must be overridden. This class has
    access to the RF device used in the testing so that it can read in the signals that
    are supposedly provided to it via it's RF inputs. 

    Attributes:
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
        self.attenuation = 12
        self.RFSim = RFSim
        self.GateSim = GateSim

    def get_X_position (self):
        """Override method, gets the calculated X position of the beam.
        
        Args:
        
        Returns: 
            float: X position in mm
        """
        return 0.0

    def get_Y_position(self):
        """Override method, gets the calculated X position of the beam.
        
        Args:
        
        Returns: 
            float: Y position in mm
        """
        return 0.0

    def get_beam_current(self):
        """Override method, gets the beam current read by the BPMs. 
        
        By measuring the output power from the RF device, the input power can be assumed, then an equation extracted
        from the Rigol 30303 and Libera BPM device can be used to give an estimate of the current. 
        
        Args:
            
        Returns: 
            float: Current in mA
        """
        current = self.get_input_power()
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
        if self.GateSim == None:
            return self.RFSim.get_output_power()[0] - self.attenuation
        elif self.GateSim.get_modulation_state() == False:
            return self.RFSim.get_output_power()[0] - self.attenuation
        else:
            return (self.GateSim.get_pulse_dutycycle()*self.RFSim.get_output_power()[0]) - self.attenuation

    def get_raw_BPM_buttons(self):
        """Override method, gets the raw signal from each BPM.
        
        Args:
            
        Returns: 
            int: Raw signal from BPM A
            int: Raw signal from BPM B
            int: Raw signal from BPM C
            int: Raw signal from BPM D
        """
        ADC = 100 * self.get_beam_current()
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
        return 1, 1, 1, 1

    def get_device_ID(self):
        """Override method, gets the type of BPM device that the device is
        
        Args:
        
        Returns: 
            str: Device type 
        """
        return "Simulated BPM Device"

    def get_ADC_sum(self):
        a, b, c, d = self.get_raw_BPM_buttons()
        sum = a + b + c + d
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
        return -40

