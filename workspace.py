# application boilerplate
import RFSignalGenerators
import BPMDevice
import Gate_Source
import ProgrammableAttenuator
import Tests
import Latex_Report
import time
import telnetlib
from pkg_resources import require
require("numpy")
require("cothread")
require("matplotlib")
import matplotlib.pyplot as plt
import itertools


x = -46.0

y  = 10**(x/10)
print y


