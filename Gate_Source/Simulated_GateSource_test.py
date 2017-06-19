import unittest
from mock import patch
from Simulated_GateSource import *

class ExpectedDataTest(unittest.TestCase):

    GSSim = Simulated_GateSource()

    @classmethod
    def setUpClass(cls):
        # Stuff you only run once
        super(ExpectedDataTest, cls).setUpClass()

    def setUp(self):
        # Stuff you run before each test
        unittest.TestCase.setUp(self)

    def tearDown(self):
        # Stuff you want to run after each test
        self.GSSim.__init__()
        pass

    def test_get_device_ID(self):
        self.assertEqual(self.GSSim.get_device_ID(), "Simulated GateSource")

    def test_set_pulse_dutycycle_with_invalid_input(self):
        self.assertRaises(ValueError,self.GSSim.set_pulse_dutycycle, -0.1)
        self.assertRaises(ValueError, self.GSSim.set_pulse_dutycycle, 1.1)
        self.assertRaises(TypeError,self.GSSim.set_pulse_dutycycle, "0.5")

    def test_set_pulse_period_with_invalid_input(self):
        self.assertRaises(ValueError, self.GSSim.set_pulse_period, -0.1)
        self.assertRaises(TypeError, self.GSSim.set_pulse_period, "1.1")

    def test_modulation_state_when_output_state_is_changed(self):
        self.assertEqual(self.GSSim.turn_on_modulation(), True)
        self.assertEqual(self.GSSim.get_modulation_state(), True)
        self.assertEqual(self.GSSim.turn_off_modulation(), False)
        self.assertEqual(self.GSSim.get_modulation_state(), False)


    def test_get_set_dutycycle_return_values_if_expected_input_types_used(self):
        sent = (0.1, 0.9)
        exp_reply = (0.1, 0.9)

        for test_sent, test_exp_reply in zip(sent,exp_reply):
            self.assertEqual(self.GSSim.set_pulse_dutycycle(test_sent), (test_exp_reply))
            self.assertEqual(self.GSSim.get_pulse_dutycycle(), (test_exp_reply))

    def test_get_set_pulse_period_return_values_if_expected_input_types_used(self):
        sent = (3, 100)
        exp_reply = ((3,"3uS"), (100,"100uS"))

        for test_sent, test_exp_reply in zip(sent,exp_reply):
            self.assertEqual(self.GSSim.set_pulse_period(test_sent), (test_exp_reply))
            self.assertEqual(self.GSSim.get_pulse_period(), (test_exp_reply))



if __name__ == "__main__":
        unittest.main()