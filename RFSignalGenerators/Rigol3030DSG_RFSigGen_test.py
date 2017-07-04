import unittest
import warnings
from mock import patch
import RFSignalGenerators


# Checks the simple get requests against the criteria set here

output = "1"
power_units = "DBM"
power = "-100.0"
frequency = "499.6817682MHz"

def mocked_rigol_replies(input):
    global output, power_units, power, frequency
    if input == "LEV?":
        return power
    elif input == "UNIT:POW?":
        return power_units
    elif input == "FREQ?":
        return frequency
    elif input == "OUTP?":
        return output
    elif input == "*IDN?":
        return "Rigol Technologies,DSG3030"
    elif input == "LEV:LIM?":
        return "-40.00"

def mocked_rigol_writes(input):
    global output, power_units, power, frequency
    if input == "OUTP OFF":
        output = "0"
    elif input == "OUTP ON":
        output = "1"

    # for set tests to be implimented, reg ex or something similar will go here, to scan
    # the input string. This will then be used to set the globals listed above. Then they
    # can be read back using the 'mocked_rigol_replies' function.

class ExpectedDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Stuff you only run once
        super(ExpectedDataTest, cls).setUpClass()

    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_write")
    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_query", side_effect = mocked_rigol_replies)
    @patch("telnetlib.Telnet")
    def setUp(self, mock_telnet, mock_telnet_read, mock_telnet_write):
        # Stuff you run before each test
        self.RF_test_inst = RFSignalGenerators.Rigol3030DSG_RFSigGen("0", 0, 0)
        unittest.TestCase.setUp(self)

    def tearDown(self):
        # Stuff you want to run after each test
        pass

    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_write")
    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_read")
    def test_set_frequency_if_invalid_input_types_used(self, mock_telnet_read, mock_telnet_write):
        self.assertRaises(ValueError, self.RF_test_inst.set_frequency, -100)
        self.assertRaises(TypeError, self.RF_test_inst.set_frequency, "100")

    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_write")
    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_read")
    def test_set_power_if_invalid_input_types_used(self, mock_telnet_read, mock_telnet_write):
        self.assertRaises(TypeError, self.RF_test_inst.set_output_power, "0")
        self.assertWarns(UserWarning, self.RF_test_inst.set_output_power, -39)

    ################################Simple Get requests################################
    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_read")
    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_write")
    def test_get_device_ID(self, mock_telnet_write, mock_telnet_read):
        DeviceID = "Rigol Technologies,DSG3030"
        mock_telnet_read.return_value = DeviceID
        self.assertEqual(self.RF_test_inst.get_device_ID(), "RF Source " +DeviceID)

    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_query", side_effect = mocked_rigol_replies)
    def test_get_output_power(self, mock_telnet_query):
        self.assertEqual(self.RF_test_inst.get_output_power(), (-100.0, "-100.0DBM"))

    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_query", side_effect = mocked_rigol_replies)
    def test_get_frequency(self, mock_telnet_query):
        self.assertEqual(self.RF_test_inst.get_frequency(), (499.6817682, "499.6817682MHz"))

    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_query", side_effect=mocked_rigol_replies)
    def test_get_output_state(self, mock_telnet_query):
        self.assertEqual(self.RF_test_inst.get_output_state(), True)

    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_write", side_effect=mocked_rigol_writes)
    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_query", side_effect=mocked_rigol_replies)
    def test_turn_off_output_state(self, mock_telnet_query, mock_telnet_write):
        self.assertEqual(self.RF_test_inst.turn_off_RF(), False)
        self.assertTrue(mock_telnet_write.called)

    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_write", side_effect=mocked_rigol_writes)
    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_query", side_effect=mocked_rigol_replies)
    def test_turn_on_output_state(self, mock_telnet_query, mock_telnet_write):
        self.assertEqual(self.RF_test_inst.turn_on_RF(), True)
        self.assertTrue(mock_telnet_write.called)

    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_write", side_effect=mocked_rigol_writes)
    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_query", side_effect=mocked_rigol_replies)
    def test_set_output_power_limit(self, mock_telnet_query, mock_telnet_write):
        self.assertRaises(TypeError, self.RF_test_inst.set_output_power, "0")

    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_write", side_effect=mocked_rigol_writes)
    @patch("RFSignalGenerators.Rigol3030DSG_RFSigGen._telnet_query", side_effect=mocked_rigol_replies)
    def test_get_output_power_limit(self, mock_telnet_query, mock_telnet_write):
        self.assertEqual(self.RF_test_inst.get_output_power_limit(), (-40, "-40.00DBM"))

    def assertWarns(self, warning, callable, *args, **kwds):
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter('always')

            result = callable(*args, **kwds)

            self.assertTrue(any(item.category == warning for item in warning_list))

if __name__ == "__main__":
        unittest.main()