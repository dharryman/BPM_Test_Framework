from pkg_resources import require
require("numpy")
require("cothread")
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
        caput(self.epicsID + ".PROC", 1)

    def _read_epics_pv(self, pv):
        """Private method to read an Epics process variable.

        Args:
            pv (str): Name of the Epics process variable to read.  

        Returns: 
            variant: Value of requested process variable.
        """
        self._trigger_epics()
        return caget(self.epicsID + pv)

    def _write_epics_pv(self, pv, value):
        """Private method to read an Epics process variable.

        Args:
            pv (str): Name of the Epics process variable to read. 
            value (variant): The value to be written to the epics variable

        Returns: 
            variant: Value of requested process variable after writing to it
        """
        caput(self.epicsID+pv, value)
        return self._read_epics_pv(pv)


    def __init__(self, database, daq_type):
        """Initializes the Libera BPM device object and assigns it an ID. 

        Args:
            dev_ID (str/int): The two digit ID number assigned to that specific BPM device. 
        Returns:
.
        """
        self.epicsID = database+":signals:"+daq_type
        self._write_epics_pv(".SCAN", 0)
        self._trigger_epics()
        print self.get_device_ID()

    def get_X_position(self):
        """Override method, gets the calculated X position of the beam.

        Args:

        Returns: 
            float: X position in mm
        """
        self._trigger_epics()
        x = self._read_epics_pv(".X")
        x = np.mean(x)
        x = x/1000000.0
        return x

    def get_Y_position(self):
        """Override method, gets the calculated X position of the beam.

        Args:

        Returns: 
            float: Y position in mm
        """
        self._trigger_epics()
        y = self._read_epics_pv(".Y")
        y = np.mean(y)
        y = y/1000000.0
        return y

    def get_beam_current(self):
        """Override method, gets the beam current read by the BPMs. 

        Args:

        Returns: 
            float: Current in mA
        """
        self._trigger_epics()
        daq_sum = self._read_epics_pv(".Sum")
        daq_sum = np.mean(daq_sum)
        return daq_sum

    def get_input_power(self):
        """Override method, gets the input power of the signals input to the device 

        Args:

        Returns: 
            float: Input power in dBm
        """
        self._trigger_epics()
        daq_sum = self._read_epics_pv(".Sum")
        daq_sum = np.mean(daq_sum)
        return daq_sum

    def get_ADC_sum(self):
        """Override method, gets the input power of the signals input to the device 

        Args:

        Returns: 
            float: Input power in dBm
        """
        self._trigger_epics()
        daq_sum = self._read_epics_pv(".Sum")
        daq_sum = np.mean(daq_sum)
        return daq_sum

    def get_raw_BPM_buttons(self):
        """Override method, gets the raw signal from each BPM.

        Args: 

        Returns: 
            float: Raw signal from BPM A
            float: Raw signal from BPM B
            float: Raw signal from BPM C
            float: Raw signal from BPM D
        """
        self._trigger_epics()
        a = self._read_epics_pv(".A")
        b = self._read_epics_pv(".B")
        c = self._read_epics_pv(".C")
        d = self._read_epics_pv(".D")
        a = np.mean(a)
        b = np.mean(b)
        c = np.mean(c)
        d = np.mean(d)
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
        self._trigger_epics()
        a, b, c, d = self.get_raw_BPM_buttons()
        sum_button = a + b + c + d
        sum_button = sum_button/4.0
        a = a/sum_button
        b = b/sum_button
        c = c/sum_button
        d = d/sum_button
        return (a,b,c,d)

    def get_device_ID(self):
        """Override method, gets the device's epics ID and MAC address 

        Args:

        Returns: 
            str: Device with epics channel ID and MAC address
        """
        pv = ".X"
        node = cainfo(self.epicsID + pv).host.split(":")[0]
        host_info = Popen(["arp", "-n", node], stdout=PIPE).communicate()[0]
        host_info = host_info.split("\n")[1]
        index = host_info.find(":")
        host_info = host_info[index - 2:index + 15]
        return "Libera BPM with the Epics ID " + "\"" + self.epicsID + "\" and the MAC Address \"" + host_info + "\""

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

    # libera:app - name
    # libera:att:A
    # libera:att:B
    # libera:att:C
    # libera:att:D
    # libera:clocks:adc_frequency
    # libera:clocks:sync_st_m
    # libera:clocks:synchronize
    # libera:clocks:tbt_frequency
    # libera:dsp:adc_mask:offset
    # libera:dsp:adc_mask:window
    # libera:dsp:fa_data_type
    # libera:dsp:kx
    # libera:dsp:ky
    # libera:dsp:off_q
    # libera:dsp:off_x
    # libera:dsp:off_y
    # libera:dsp:phase_offset
    # libera:dsp:tbt_decimation
    # libera:max_adc
    # libera:pll:compensate_offset
    # libera:pll:locked
    # libera:pll:max_err
    # libera:pll:max_err_reset
    # libera:pll:os_unlock_time
    # libera:pll:os_unlock_time_reset
    # libera:pll:vcxo_offset
    # libera:triggers:t2:count
    # libera:triggers:t2:delay
    # libera:triggers:t2:source
    # libera:version
    # libera:signals:adc
    # libera:signals:ddc_raw
    # libera:signals:ddc_synth
    # libera:signals:ddc_synth_d
    # libera:signals:event
    # libera:signals:fa
    # libera:signals:pll
    # libera:signals:sa
    # libera:signals:tbt_window
    # libera:signals:tdp_synth
    # libera:signals:tdp_synth_d


