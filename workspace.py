import RFSignalGenerators
import BPMDevice
import Gate_Source
import ProgrammableAttenuator
import Tests
import Latex_Report

report = Latex_Report.Test_Report(
    fname="BPM test Report")  # filename the output report will have

BPM = BPMDevice.SparkERXR_EPICS_BPMDevice(
    database="libera",  # libera is the prefix used in the EPICS database
    daq_type="fa")  # set as "fa" for fast acquisition

RF = RFSignalGenerators.Rigol3030DSG_RFSigGen(
    ipaddress="172.23.252.51",  # IP address of the Rigol3030
    port=5555,  # Telnet port used to communicate with the Rigol3030
    timeout=1,  # Timeout in seconds to wait for a reply
    limit=BPM.get_input_tolerance())  # Sets the max power limit of the RF

PA = ProgrammableAttenuator.MC_RC4DAT6G95_Prog_Atten(
    ipaddress="172.23.244.105",  # IP address of the programmable attenuator
    port=23,  # Telnet port used to communicate with the attenuator
    timeout=1)  # Timeout in seconds to wait for a reply

dls_RF_frequency = 499.6817682
sub_directory = "./Results/"

Tests.Beamposition_linear_raster_scan_test(
    RF=RF,  # Uses the RF object instantiated to output RF signals
    BPM=BPM,  # Performs test on the BPM object instantiated
    PA=PA,  # Changes attenuation values on the attenuator instantiated
    rf_power=-40,  # Sets a constant RF output power of -40 dBm
    rf_frequency=dls_RF_frequency,  # Sets the RF output frequency
    nominal_attenuation=10,  # Given each attenuator a starting value of 10 dB
    x_points=5,  # Number of points to take in the x plane
    y_points=5,  # Number of points to take in the y plane
    settling_time=3,  # time to wait in seconds between changing value and taking a reading
    report=report,  # The report class that the results are saved to
    sub_directory=sub_directory)  # The sub directory that output graphs are saved to

report.create_report()
