import unittest
from mock import patch
from Simulated_RFSigGen import *
import warnings


class ExpectedDataTest(unittest.TestCase):

    RFSim = Simulated_RFSigGen()

    @classmethod
    def setUpClass(cls):
        # Stuff you only run once
        super(ExpectedDataTest, cls).setUpClass()

    def setUp(self):
        # Stuff you run before each test
        unittest.TestCase.setUp(self)

    def tearDown(self):
        # Stuff you want to run after each test
        self.RFSim.__init__()
        pass

    def test_get_device_ID(self):
        self.assertEqual(self.RFSim.get_device_ID(), "Simulated RF Device")

    def test_get_set_output_power_return_values_if_expected_input_types_used(self):
        sent = (-40, -80)
        exp_reply = ((-40.0, "-40dBm"),(-80, "-80dBm"))

        for test_sent, test_exp_reply in zip(sent,exp_reply):
            self.assertEqual(self.RFSim.set_output_power(test_sent), (test_exp_reply))
            self.assertEqual(self.RFSim.get_output_power(), (test_exp_reply))
        del sent , exp_reply ,test_sent, test_exp_reply

    def test_get_set_frequency_return_values_if_expected_input_types_used(self):
        sent = (1,22, 499.6817682)
        exp_reply = ((1,"1MHz"), (22,"22MHz"), (499.6817682, "499.6817682MHz"))

        for test_sent, test_exp_reply in zip(sent, exp_reply):
            self.assertEqual(self.RFSim.set_frequency(test_sent), (test_exp_reply))
            self.assertEqual(self.RFSim.get_frequency(), (test_exp_reply))
        del sent, exp_reply, test_sent, test_exp_reply

    def test_output_state_when_output_state_is_changed(self):
        self.assertEqual(self.RFSim.turn_on_RF(),True)
        self.assertEqual(self.RFSim.get_output_state(),True)
        self.assertEqual(self.RFSim.turn_off_RF(),False)
        self.assertEqual(self.RFSim.get_output_state(),False)

    def test_set_frequency_if_invalid_input_types_used(self):
        self.assertRaises(ValueError, self.RFSim.set_frequency, -100)
        self.assertRaises(TypeError, self.RFSim.set_frequency, "100")

    def test_set_power_if_invalid_input_types_used(self):
        self.assertRaises(TypeError, self.RFSim.set_output_power, "0")
        self.assertWarns(UserWarning, self.RFSim.set_output_power, -39)

    def test_set_output_power_limit(self):
        self.assertRaises(TypeError, self.RFSim.set_output_power_limit, "0")

    def test_get_output_power_limit(self):
        self.assertEqual(self.RFSim.get_output_power_limit(), (-40, "-40dBm"))


    def assertWarns(self, warning, callable, *args, **kwds):
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter('always')

            result = callable(*args, **kwds)

            self.assertTrue(any(item.category == warning for item in warning_list))



if __name__ == "__main__":
        unittest.main()

