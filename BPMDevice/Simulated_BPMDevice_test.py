# import unittest
# from mock import patch
# from Simulated_BPMDevice import *
# import RFSignalGenerators
#
# # Needs to be redesigned to take into account the gate source object....
#
# class ExpectedDataTest(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         # Stuff you only run once
#         super(ExpectedDataTest, cls).setUpClass()
#
#     def setUp(self):
#         # Stuff you run before each test
#         unittest.TestCase.setUp(self)
#
#     def tearDown(self):
#         # Stuff you want to run after each test
#         pass
#
#     @patch("RFSignalGenerators.Simulated_RFSigGen")
#     def test_Sim_BPM_get_output_power(self, mock_RFDev):
#         test_output_values = -100
#         simulator_attenuation = 12
#         mock_RFDev.get_output_power.return_value = test_output_values
#
#         SimRF = Simulated_BPMDevice(mock_RFDev)
#         SimRF.get_input_power()
#         self.assertTrue(mock_RFDev.get_output_power.called)
#         self.assertEqual(SimRF.get_input_power(), test_output_values - simulator_attenuation)
#
#     def test_get_input_tolerance(self):
#         self.assertEqual(self.BPM_test_inst.get_input_tolerance(), -40)
#
#
# if __name__ == "__main__":
#         unittest.main()