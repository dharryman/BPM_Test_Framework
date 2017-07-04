import RFSignalGenerators
import BPMDevice
import Gate_Source
import ProgrammableAttenuator
import Tests
import Latex_Report
import time


# Testing the BPM position tests using the programmable attenuator

report = Latex_Report.Test_Report("BPM Test Report")
BPM = BPMDevice.SparkERXR_EPICS_BPMDevice("libera", "fa")
limit = BPM.get_input_tolerance()
RF = RFSignalGenerators.Rigol3030DSG_RFSigGen("172.23.252.51", 5555, 1, limit)
GS = Gate_Source.Rigol3030DSG_GateSource("172.23.252.51", 5555, 1)
PA = ProgrammableAttenuator.MC_RC4DAT6G95_Prog_Atten("172.23.244.105", 23, 0.1)

Tests.Beamposition_raster_scan_test(RF, BPM, PA, -40, 499.6817682, 50,10,2, report)

report.create_report()