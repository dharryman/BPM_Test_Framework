# application boilerplate
import RFSignalGenerators
import BPMDevice
import Gate_Source
import ProgrammableAttenuator
import Tests
import Latex_Report
import time
import telnetlib

# Init real devices

#
PA = ProgrammableAttenuator.MC_RC4DAT6G95_Prog_Atten("172.23.244.105", 23, 1)
PA.set_channel_attenuation("C", 17.5)
y = PA.get_global_attenuation()
z = PA.get_channel_attenuation("a")

print (y,z)

# IP = "172.23.252.51"
# Port = "5555"
# message = "*IDN?"

# IP = "172.23.244.105"
# Port = "23"
# message = "SN?"
#
# tn = telnetlib.Telnet()  #MC atten
# tn.open(IP, Port, 5)
# tn.write(message+"\r\n")
# x = tn.read_until("\r\n", 0.1)
# y = tn.read_until("\r\n", 0.1)
# print (x, y)
# tn.close()


















