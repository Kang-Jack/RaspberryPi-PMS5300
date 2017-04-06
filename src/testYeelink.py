import unittest
import aqi_yeelink

class TestYeeLink(unittest.TestCase):
    def setUp(self):
        self.pm2_5_CF = 58
        self.pm2_5_ATM = 63
        self.diam_0_3_UM = 9682
        self.sut = aqi_yeelink.aqi_yeelink()

    def test_upload_data(self):
        self.sut.upload_data(self.pm2_5_ATM,self.pm2_5_CF,self.diam_0_3_UM,65,54)
if __name__ == '__main__':
    unittest.main()