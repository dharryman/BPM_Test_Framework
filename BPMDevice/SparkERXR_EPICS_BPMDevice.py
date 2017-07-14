from pkg_resources import require
require("cothread==2.14")
from cothread.catools import *
import cothread
from Generic_BPMDevice import *
from subprocess import Popen, PIPE
import numpy as np


class SparkERXR_EPICS_BPMDevice(Generic_BPMDevice):
    """Libera BPM Device class that uses Epics to communicate with PVs.

    All of the methods here will attempt to be generic enough to work for most Libera devices.
    Some libera BPM devices will have extra functionality. To implement this make a child class 
    that will extend this one.

    Attributes:
        epicsID (str): Channel identifier string that will be used to access PVs.  
    """

    def _trigger_epics(self):
        """Private method to update the EPICS variables
        
        This will write a value to the .PROC record that will update all of the 
        process variables on that database. 

        Args: 

        Returns: 
        """
        caput(self.epicsID + ".PROC", 1)  # Write to the .PROC data base to update all of the values

    def _read_epics_pv(self, pv):
        """Private method to read an Epics process variable.

        Args:
            pv (str): Name of the Epics process variable to read.  

        Returns: 
            variant: Value of requested process variable.
        """
        self._trigger_epics()  # Update all values before reading
        return caget(self.epicsID + pv)  # Read selected epics PV

    def _write_epics_pv(self, pv, value):
        """Private method to read an Epics process variable.

        Args:
            pv (str): Name of the Epics process variable to read. 
            value (variant): The value to be written to the epics variable

        Returns: 
            variant: Value of requested process variable after writing to it
        """
        caput(self.epicsID+pv, value)  # Write to EPICs PV
        return self._read_epics_pv(pv)

    def __init__(self, database, daq_type):
        """Initializes the Libera BPM device object and assigns it an ID. 

        Args:
            dev_ID (str/int): The two digit ID number assigned to that specific BPM device. 
        Returns:
.
        """
        if type(database) and type(daq_type) != str:
            raise TypeError
        self.epicsID = database+":signals:"+daq_type  # Different signal types can be used
        self._write_epics_pv(".SCAN", 0)  # Required so that values can be read from he database
        self._trigger_epics()  # Triggers the first count

        pv = ".X"  # Pick a PV that is hosted on the device
        node = connect(self.epicsID + pv, cainfo=True).host.split(":")[0]  # Get the IP address of the host
        host_info = Popen(["arp", "-n", node], stdout=PIPE).communicate()[0]  # Get info about the host using arp
        host_info = host_info.split("\n")[1]  # Split the info sent back
        index = host_info.find(":")  # Find the first ":", used in the MAC address
        host_info = host_info[index - 2:index + 15]  # Get the MAC address
        self.macaddress = host_info
        print "Opened link with" + self.get_device_ID()  # Tells the user they have connected to the device

    def __del__(self):
        print "Closed link with" + self.get_device_ID()  # Tells the user they have connected to the device


    def get_X_position(self):
        """Override method, gets the calculated X position of the beam.

        Args:

        Returns: 
            float: X position in mm
        """
        self._trigger_epics()  # Triggers the acquisition
        x = self._read_epics_pv(".X")  # Gets the PV value
        x = np.mean(x)  # Gets the mean PV value
        x = x/1000000.0  # Converts from nm to mm
        return x

    def get_Y_position(self):
        """Override method, gets the calculated X position of the beam.

        Args:

        Returns: 
            float: Y position in mm
        """
        self._trigger_epics()  # Triggers the acquisition
        y = self._read_epics_pv(".Y")  # Gets the PV value
        y = np.mean(y)  # Gets the mean PV value
        y = y/1000000.0  # Converts from nm to mm
        return y

    def get_beam_current(self):
        """Override method, gets the beam current read by the BPMs. 

        Args:

        Returns: 
            float: Current in mA
        """
        # This function is not finished it needs to convert from ADC counts to mA
        self._trigger_epics()  # Triggers the acquisition
        daq_sum = self._read_epics_pv(".Sum")  # Gets the PV value
        daq_sum = np.mean(daq_sum)  # Gets the mean PV value
        return daq_sum

    def get_input_power(self):
        """Override method, gets the input power of the signals input to the device 

        Args:

        Returns: 
            float: Input power in dBm
        """
        # This function is not finished it needs to convert from ADC counts to dBm
        self._trigger_epics()  # Triggers the acquisition
        daq_sum = self._read_epics_pv(".Sum")  # Gets the PV value
        daq_sum = np.mean(daq_sum)  # Gets the mean PV value
        return daq_sum

    def get_ADC_sum(self):
        """Override method, gets the input power of the signals input to the device 

        Args:

        Returns: 
            int: Input power in dBm
        """
        self._trigger_epics()  # Triggers the acquisition
        daq_sum = self._read_epics_pv(".Sum")
        daq_sum = np.mean(daq_sum)  # Gets the PV value
        daq_sum = np.round(daq_sum)  # Rounds the mean to the nearest integer
        return daq_sum

    def get_raw_BPM_buttons(self):
        """Override method, gets the raw signal from each BPM.

        Args: 

        Returns: 
            int: Raw signal from BPM A
            int: Raw signal from BPM B
            int: Raw signal from BPM C
            int: Raw signal from BPM D
        """
        self._trigger_epics()  # triggers the acquisition
        a = self._read_epics_pv(".A")  # gets the PV value
        b = self._read_epics_pv(".B")
        c = self._read_epics_pv(".C")
        d = self._read_epics_pv(".D")
        a = np.mean(a)  # gets the mean PV value
        b = np.mean(b)
        c = np.mean(c)
        d = np.mean(d)
        a = np.round(a)  # Round the PV to the nearest integer
        b = np.round(b)
        c = np.round(c)
        d = np.round(d)
        return a, b, c, d

    def get_normalised_BPM_buttons(self):
        """Override method, gets the normalised signal from each BPM.

        Args: 
        Returns: 
            float: Normalised signal from BPM A
            float: Normalised signal from BPM B
            float: Normalised signal from BPM C
            float: Normalised signal from BPM D
        """
        self._trigger_epics()  # Triggers the acquisition
        a, b, c, d = self.get_raw_BPM_buttons()  # Gets the RAW bpm buttons
        sum_button = a + b + c + d  # Calculates the BPM sum
        sum_button = sum_button/4.0  # Gets the average BPM sum
        a = a/sum_button  # Normalises the A button
        b = b/sum_button  # Normalises the B button
        c = c/sum_button  # Normalises the C button
        d = d/sum_button  # Normalises the D button
        return (a,b,c,d)

    def get_device_ID(self):
        """Override method, gets the device's epics ID and MAC address 

        Args:
        Returns: 
            str: Device with epics channel ID and MAC address
        """

        return "Libera BPM with the Epics ID " + "\"" + self.epicsID + "\" and the MAC Address \"" + self.macaddress + "\""

    def get_input_tolerance(self):
        """Override method, gets the maximum input power the device can take
        
        The devices will break if the input power is too high, as such, each device has their
        own tolerances, this function will return this tolerance. It should be used to ensure 
        that the power put into the device is not too high to break the device. 
        
        Args:
        Returns: 
            float: max input power in dBm
        """
        return -40  # The max continuous input the spark can withstand in dBm


