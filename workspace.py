# application boilerplate
import RFSignalGenerators
import BPMDevice
import Gate_Source
import Tests
import Latex_Report
import time

# Init real devices


BPM = BPMDevice.SparkER_SCPI_BPMDevice("172.23.240.105", 23, 1)
limit = BPM.get_input_tolerance()
RF = RFSignalGenerators.Rigol3030DSG_RFSigGen("172.23.252.51", 5555, 1, limit)
GS = Gate_Source.Rigol3030DSG_GateSource("172.23.252.51", 5555, 1)

print BPM.get_device_ID()



















