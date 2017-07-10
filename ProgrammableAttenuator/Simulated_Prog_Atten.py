from ProgrammableAttenuator import *
import telnetlib
from pkg_resources import require
require("numpy")
import numpy as np

class Simulated_Prog_Atten(Generic_Prog_Atten):

    def __init__(self, ipaddress, port, timeout):
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0

    def __del__(self):
        pass

    def _check_attenuation(self, attenuation):
        if type(attenuation) != float and type(attenuation) != int and np.float64 != np.dtype(attenuation):
            raise TypeError
        elif attenuation > 95 or attenuation < 0:
            raise ValueError

    def _check_channel(self, channel):
        if type(channel) == str:
            channel = channel.upper()
            while channel not in ["A", "B", "C", "D"]:
                raise ValueError
        elif type(channel) == int:
            while channel not in [1,2,3,4]:
                raise ValueError
        else:
            raise TypeError

    def get_device_ID(self):
        return "Simulated programmable attenuator device"

    def set_global_attenuation(self, attenuation):
        self._check_attenuation(attenuation)
        self.A = attenuation
        self.B = attenuation
        self.C = attenuation
        self.D = attenuation

    def get_global_attenuation(self):
        return (self.A, self.B, self.C, self.D)

    def set_channel_attenuation(self, channel, attenuation):

        self._check_attenuation(attenuation)
        self._check_channel(channel)

        if channel.upper() == "A":
            self.A = attenuation
        elif channel.upper() == "B":
            self.B = attenuation
        elif channel.upper() == "C":
            self.C = attenuation
        elif channel.upper() == "D":
            self.D = attenuation

    def get_channel_attenuation(self, channel):
        self._check_channel(channel)
        if channel.upper() == "A":
            return self.A
        elif channel.upper() == "B":
            return self.B
        elif channel.upper() == "C":
            return self.C
        elif channel.upper() == "D":
            return self.D
