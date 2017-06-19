import BPMDevice
import unittest
from mock import patch

def mock_get_device_ID():
    return "Libera BPM \"00:d0:50:31:03:b9\""

def mock_BPM_replies(message):
    if message == "TBT_XY 100":
        return "1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2"
    elif message == "ADC 200":
        return "800 900 1100 1200 800 900 1100 1200 800 900 1100 1200 800 900 1100 1200"
    elif message == "TBT_QSUM 100":
        return "1000 4000"


class ExpectedDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Stuff you only run once
        super(ExpectedDataTest, cls).setUpClass()

    @patch("BPMDevice.SparkER_SCPI_BPMDevice._telnet_write")
    @patch("BPMDevice.SparkER_SCPI_BPMDevice._telnet_read")
    @patch("telnetlib.Telnet")
    def setUp(self, mock_telnet, mock_telnet_read, mock_telnet_write):
        # Stuff you run before each test
        self.Spark_test_inst = BPMDevice.SparkER_SCPI_BPMDevice("0", 0, 0)
        unittest.TestCase.setUp(self)

    def tearDown(self):
        # Stuff you want to run after each test
        pass

    @patch("BPMDevice.SparkER_SCPI_BPMDevice.get_device_ID", side_effect=mock_get_device_ID)
    def test_device_ID(self, mock_dev_ID):
        self.assertEqual(self.Spark_test_inst.get_device_ID(),"Libera BPM \"00:d0:50:31:03:b9\"")
        self.assertTrue(mock_dev_ID.called)


    # @patch("BPMDevice.SparkER_SCPI_BPMDevice._telnet_query",side_effect=mock_BPM_replies)
    # def test_get_BPM_power(self, mock_replies):
    #     self.assertEqual(self.Spark_test_inst.get_input_power(), -100)
    #     self.assertTrue(mock_replies.called)
    #
    # @patch("BPMDevice.SparkER_SCPI_BPMDevice._telnet_query", side_effect=mock_BPM_replies)
    # def test_get_BPM_current(self, mock_replies):
    #     self.assertEqual(self.Spark_test_inst.get_beam_current(), 10)
    #     self.assertTrue(mock_replies.called)

    @patch("BPMDevice.SparkER_SCPI_BPMDevice._telnet_query", side_effect=mock_BPM_replies)
    def test_get_raw_BPM_buttons(self, mock_replies):
        self.assertEqual(self.Spark_test_inst.get_raw_BPM_buttons(), (800, 900, 1100, 1200))
        self.assertTrue(mock_replies.called)

    @patch("BPMDevice.SparkER_SCPI_BPMDevice._telnet_query", side_effect=mock_BPM_replies)
    def test_get_normalised_BPM_buttons(self, mock_replies):
        self.assertEqual(self.Spark_test_inst.get_normalised_BPM_buttons(), (0.8, 0.9, 1.1, 1.2))
        self.assertTrue(mock_replies.called)

    @patch("BPMDevice.SparkER_SCPI_BPMDevice._telnet_query", side_effect=mock_BPM_replies)
    def test_get_X_position(self, mock_replies):
        self.assertEqual(self.Spark_test_inst.get_X_position(), 0.001)
        self.assertTrue(mock_replies.called)

    @patch("BPMDevice.SparkER_SCPI_BPMDevice._telnet_query", side_effect=mock_BPM_replies)
    def test_get_Y_position(self, mock_replies):
        self.assertEqual(self.Spark_test_inst.get_Y_position(), 0.002)
        self.assertTrue(mock_replies.called)

    def test_get_input_tolerance(self):
        self.assertEqual(self.Spark_test_inst.get_input_tolerance(), -40)

    @patch("BPMDevice.SparkER_SCPI_BPMDevice._telnet_query", side_effect=mock_BPM_replies)
    def test_ADC_sum(self, mock_replies):
        self.assertEqual(self.Spark_test_inst.get_ADC_sum(), 4000)
        self.assertTrue(mock_replies.called)

if __name__ == "__main__":
    unittest.main()