import unittest
from mock import patch
import BPMDevice

daq = "sa"

def mock_get_device_ID():
    return "Libera BPM with the MAC Address \"00:d0:50:31:03:b9\""

def mocked_BPM_replies(pv):
    if pv == "sa:POWER":
        return -100.0
    elif pv == "sa:CURRENT":
        return 10.0
    elif pv == ".A":
        return 800.0
    elif pv == ".B":
        return 900.0
    elif pv == ".C":
        return 1100.0
    elif pv == ".D":
        return 1200.0
    elif pv == ".X":
        return 100.0
    elif pv == ".Y":
        return -100.0
    elif pv == ".Sum":
        return 4000.0
    else:
        print "none found"


class ExpectedDataTest(unittest.TestCase):
    global daq

    @classmethod
    def setUpClass(cls):
        # Stuff you only run once
        super(ExpectedDataTest, cls).setUpClass()

    @patch ("BPMDevice.SparkERXR_EPICS_BPMDevice._trigger_epics")
    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._write_epics_pv")
    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._read_epics_pv")
    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice.get_device_ID")
    def setUp(self, device_mock, epics_read_mock, epics_write_mock, epics_trigger_mock):
        # Stuff you run before each test
        self.BPM_test_inst = BPMDevice.SparkERXR_EPICS_BPMDevice("libera",daq)
        print self.BPM_test_inst.get_device_ID()
        unittest.TestCase.setUp(self)


    def tearDown(self):
        pass
        # Stuff you want to run after each test


    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice.get_device_ID", side_effect=mock_get_device_ID)
    def test_device_ID(self, mock_dev_ID):
        self.assertEqual(self.BPM_test_inst.get_device_ID(),
                         "Libera BPM with the MAC Address \"00:d0:50:31:03:b9\"")
        self.assertTrue(mock_dev_ID.called)

    # @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._read_epics_pv", side_effect=mocked_BPM_replies)
    # def test_get_BPM_power(self, mock_replies):
    #     self.assertEqual(self.BPM_test_inst.get_input_power(), -100)
    #     self.assertTrue(mock_replies.called)

    # @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._read_epics_pv", side_effect=mocked_BPM_replies)
    # def test_get_BPM_current(self, mock_replies):
    #     self.assertEqual(self.BPM_test_inst.get_beam_current(), 10)
    #     self.assertTrue(mock_replies.called)

    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._trigger_epics")
    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._read_epics_pv", side_effect=mocked_BPM_replies)
    def test_get_raw_BPM_buttons(self, mock_replies, epics_trigger_mock):
        self.assertEqual(self.BPM_test_inst.get_raw_BPM_buttons(), (800,900,1100,1200))
        self.assertTrue(mock_replies.called)

    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._trigger_epics")
    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._read_epics_pv", side_effect=mocked_BPM_replies)
    def test_get_normalised_BPM_buttons(self, mock_replies, epics_trigger_mock):
        self.assertEqual(self.BPM_test_inst.get_normalised_BPM_buttons(), (0.8,0.9,1.1,1.2))
        self.assertTrue(mock_replies.called)

    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._trigger_epics")
    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._read_epics_pv", side_effect=mocked_BPM_replies)
    def test_get_X_position(self, mock_replies, epics_trigger_mock):
        self.assertEqual(self.BPM_test_inst.get_X_position(), 100/1000000.0) # divide by 1000 to change to mm
        self.assertTrue(mock_replies.called)

    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._trigger_epics")
    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._read_epics_pv", side_effect=mocked_BPM_replies)
    def test_get_Y_position(self, mock_replies, epics_trigger_mock):
        self.assertEqual(self.BPM_test_inst.get_Y_position(), -100/1000000.0) # divide by 1000 to change to mm
        self.assertTrue(mock_replies.called)

    def test_get_input_tolerance(self):
        self.assertEqual(self.BPM_test_inst.get_input_tolerance(), -40)

    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._trigger_epics")
    @patch("BPMDevice.SparkERXR_EPICS_BPMDevice._read_epics_pv", side_effect=mocked_BPM_replies)
    def test_get_ADC_sum(self, mock_replies, epics_trigger_mock):
        self.assertEqual(self.BPM_test_inst.get_ADC_sum(), 4000) # divide by 1000 to change to mm
        self.assertTrue(mock_replies.called)


if __name__ == "__main__":
    unittest.main()