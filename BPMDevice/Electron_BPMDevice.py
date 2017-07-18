from pkg_resources import require
require("cothread==2.14")
from cothread.catools import *
import cothread
from Generic_BPMDevice import *
from subprocess import Popen, PIPE
import numpy as np

class Electron_BPMDevice(Generic_BPMDevice):
    """Libera Electron BPM Device class that uses Epics to communicate with PVs.

    All of the methods here will attempt to be generic enough to work for Libera
    devices that have the same PV names. If these names change, then a different 
    class will have to be used. Most data is acquired using the slow acquisition 
    method as the tests are not intensive, for noise tests and the such, direct 
    access to the data buffers may be needed. 

    Attributes:
        epicsID (str): Channel identifier string that will be used to access PVs.  
    """

    def _read_epics_pv (self,pv):
        """Private method to read an Epics process variable.
        
        Wraps up caget call, makes it easy for multiple reads to be programmed 
        and a timeout added if required. 
        
        Args:
            pv (str): Name of the Epics process variable to read.  
        Returns: 
            variant: Value of requested process variable.
        """
        return caget(self.epicsID+pv)  # Get PV data

    def __init__(self, dev_ID):
        """Initializes the Libera BPM device object and assigns it an ID. 
        
        Args:
            dev_ID (str/int): The ID number assigned to that specific BPM device. 
        Returns:
.
        """
        if type(dev_ID) != str:  # Makes sure the ID is an integer
            raise TypeError  # Raises a type error if integer is not used
        else:
            self.epicsID = dev_ID # TS-DI-EBPM-04:

        pv = "SA:X"  # Any PV hosts on the device could be used here
        node = connect(self.epicsID + pv, cainfo=True).host.split(":")[0]  # Get the IP address of the host
        host_info = Popen(["arp", "-n", node], stdout=PIPE).communicate()[0]  # Uses arp to get more info about the host
        host_info = host_info.split("\n")[1]  # Splits the data about the host
        index = host_info.find(":")  # Gets the first ":", used in the MAC address
        host_info = host_info[index - 2:index + 15]  # Gets the devices MAC address
        self.macaddress = host_info
        print "Opened connection to "+self.get_device_ID()  # Informs the user the device is now connected to

    def __del__(self):
        """Informs the user that this object has been destroyed 
        
        Args:
        Returns:
         
        """
        print "Closed connection to "+self.get_device_ID()

    def get_X_position(self):
        """Override method, gets the calculated X position of the beam.
        
        Args:   
        Returns: 
            float: X position in mm
        """
        return self._read_epics_pv("SA:X")  # Reads the requested PV

    def get_Y_position(self):
        """Override method, gets the calculated Y position of the beam.
        
        Args:  
        Returns: 
            float: Y position in mm
        """
        return self._read_epics_pv("SA:Y")  # Reads the requested PV

    def get_beam_current(self):
        """Override method, gets the beam current read by the BPMs. 
        
        Args:
        Returns: 
            float: Current in mA
        """
        return self._read_epics_pv("SA:CURRENT")  # Reads the requested PV

    def get_input_power(self):
        """Override method, gets the input power of the signals input to the device 
        
        Args:
        Returns: 
            float: Input power in dBm
        """
        return self._read_epics_pv("SA:POWER")  # Reads the requested PV

    def get_raw_BPM_buttons(self):
        """Override method, gets the raw signal from each BPM.
        
        Args: 
        Returns: 
            float: Raw signal from BPM A
            float: Raw signal from BPM B
            float: Raw signal from BPM C
            float: Raw signal from BPM D
        """
        return (self._read_epics_pv("SA:A"),
                self._read_epics_pv("SA:B"),
                self._read_epics_pv("SA:C"),
                self._read_epics_pv("SA:D"))  # Reads the requested PVs

    def get_normalised_BPM_buttons(self):
        """Override method, gets the normalised signal from each BPM.
        
        Args: 
        Returns: 
            float: Normalised signal from BPM A
            float: Normalised signal from BPM B
            float: Normalised signal from BPM C
            float: Normalised signal from BPM D
        """
        return (self._read_epics_pv("SA:AN"),
                self._read_epics_pv("SA:BN"),
                self._read_epics_pv("SA:CN"),
                self._read_epics_pv("SA:DN"))  # Reads the requested PVs

    def get_ADC_sum(self):
        """Override method, gets the sum of all of the buttons ADCs

        A+B+C+D

        Args:
        Returns: 
            int: ADC sum in counts
        """
        a, b, c, d = self.get_raw_BPM_buttons()  # Reads the requested PVs
        sum = a + b + c + d  # Sums the values of the PVs
        return sum

    def get_device_ID(self):
        """Override method, gets the device's epics ID and MAC address 
        
        Args:
        Returns: 
            str: Device with epics channel ID and MAC address
        """

        return "Libera Electron BPM with the Epics ID "+ "\""+self.epicsID+"\" and the MAC Address \""+self.macaddress+"\""

    def get_input_tolerance(self):
        """Override method, gets the maximum input power the device can take

        The devices will break if the input power is too high, as such, each device has their
        own tolerances, this function will return this tolerance. It should be used to ensure 
        that the power put into the device is not too high to break the device. 

        Args:
        Returns: 
            float: max input power in dBm
        """
        return -20 # The maximum continuous input power the Electron can handle in dBm

