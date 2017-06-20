import unittest
from mock import patch
import Gate_Source
import telnetlib

# Checks the simple get requests against the criteria set here

output = "1"
period = "3uS"
dutycycle = "0.03uS"


def mocked_rigol_replies(input):
    global output, period, dutycycle

    if input == "MOD:STAT?":
        return output
    elif input == "PULM:PER?":
        return period
    elif input == "PULM:WIDT?":
        return dutycycle
    elif input == "*IDN?":
        return "Rigol Technologies,DSG3030"

def mocked_rigol_writes(input):
    global output, period, dutycycle
    if input == "PULM:OUT:STAT OFF":
        output = "0"
    elif input == "PULM:OUT:STAT ON":
        output = "1"


    # for set tests to be implimented, reg ex or something similar will go here, to scan
    # the input string. This will then be used to set the globals listed above. Then they
    # can be read back using the 'mocked_rigol_replies' function.

class ExpectedDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Stuff you only run once
        super(ExpectedDataTest, cls).setUpClass()

    @patch("Gate_Source.Rigol3030DSG_GateSource._telnet_write")
    @patch("Gate_Source.Rigol3030DSG_GateSource._telnet_query", side_effect=mocked_rigol_replies)
    @patch("telnetlib.Telnet")
    def setUp(self, mock_telnet, mock_telnet_query, mock_telnet_write):
        # Stuff you run before each test
        self.GS_test_inst = Gate_Source.Rigol3030DSG_GateSource("0", 0, 0)
        unittest.TestCase.setUp(self)

    def tearDown(self):
        # Stuff you want to run after each test
        pass

    @patch("Gate_Source.Rigol3030DSG_GateSource._telnet_write")
    @patch("Gate_Source.Rigol3030DSG_GateSource._telnet_read")
    def test_set_pulse_dutycycle_with_invalid_input(self, mock_telnet_read, mock_telnet_write):
        self.assertRaises(ValueError, self.GS_test_inst.set_pulse_dutycycle, -0.1)
        self.assertRaises(ValueError, self.GS_test_inst.set_pulse_dutycycle, 1.1)
        self.assertRaises(TypeError, self.GS_test_inst.set_pulse_dutycycle, "0.5")

    @patch("Gate_Source.Rigol3030DSG_GateSource._telnet_write")
    @patch("Gate_Source.Rigol3030DSG_GateSource._telnet_read")
    def test_set_pulse_period_with_invalid_input(self, mock_telnet_read, mock_telnet_write):
        self.assertRaises(ValueError, self.GS_test_inst.set_pulse_period, -0.1)
        self.assertRaises(TypeError, self.GS_test_inst.set_pulse_period, "1.1")

#######################################################

    @patch("Gate_Source.Rigol3030DSG_GateSource._telnet_write", side_effect=mocked_rigol_writes)
    @patch("Gate_Source.Rigol3030DSG_GateSource._telnet_query", side_effect=mocked_rigol_replies)
    def test_modulation_state_when_output_state_is_changed(self, mock_query, mock_write):
        self.assertEqual(self.GS_test_inst.turn_on_modulation(), True)
        self.assertEqual(self.GS_test_inst.get_modulation_state(), True)
        self.assertEqual(self.GS_test_inst.turn_off_modulation(), False)
        self.assertEqual(self.GS_test_inst.get_modulation_state(), False)

    @patch("Gate_Source.Rigol3030DSG_GateSource._telnet_write", side_effect=mocked_rigol_writes)
    @patch("Gate_Source.Rigol3030DSG_GateSource._telnet_query", side_effect=mocked_rigol_replies)
    def test_get_dutycycle_return_values_if_expected_input_types_used(self, mock_query, mock_write):
        self.assertEqual(self.GS_test_inst.get_pulse_dutycycle(), (0.01))

    @patch("Gate_Source.Rigol3030DSG_GateSource._telnet_write", side_effect=mocked_rigol_writes)
    @patch("Gate_Source.Rigol3030DSG_GateSource._telnet_query", side_effect=mocked_rigol_replies)
    def test_get_pulse_period_return_values_if_expected_input_types_used(self, mock_query, mock_write):
        self.assertEqual(self.GS_test_inst.get_pulse_period(), (3,"3uS"))

if __name__ == "__main__":
        unittest.main()