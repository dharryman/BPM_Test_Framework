# application boilerplate
import RFSignalGenerators
import BPMDevice
import Gate_Source
import Tests
import Latex_Report
import time

# Init real devices
report = Latex_Report.Test_Report("BPM Test Report")

#BPM = BPMDevice.SparkERXR_EPICS_BPMDevice("libera", "fa")
BPM = BPMDevice.Libera_BPMDevice(4)
#BPM = BPMDevice.SparkER_SCPI_BPMDevice("172.23.240.105", 23, 1)

limit = BPM.get_input_tolerance()
RF = RFSignalGenerators.Rigol3030DSG_RFSigGen("172.23.252.51", 5555, 1, limit)
GS = Gate_Source.Rigol3030DSG_GateSource("172.23.252.51", 5555, 1)

#RF = RFSignalGenerators.Simulated_RFSigGen()
#GS = Gate_Source.Simulated_GateSource()
#BPM = BPMDevice.Simulated_BPMDevice(RF, GS)

# Test Arguments
dls_RF_frequency = 499.6817682
settling_time = 3
samples = 30
start_power = -70
final_power = -60
sub_directory = "./Results/"
Tests.Beam_Power_Dependance(RF, BPM, dls_RF_frequency, start_power, final_power, samples, settling_time, report,sub_directory)
Tests.Fixed_amplitude_fill_pattern_test(RF, BPM, GS, dls_RF_frequency, final_power, samples, 1.87319, settling_time, report, sub_directory)
Tests.Scaled_amplitude_fill_pattern_test(RF, BPM, GS, dls_RF_frequency, final_power, samples, 1.87319, settling_time, report, sub_directory)
report.create_report()

















