
import unittest
import uuid , binascii
from aqi_data_parser import *
import aqi_aqi_caculator

class TestDataParser(unittest.TestCase):
    # test data
    #g7frame = 42 4D 00 1C 00 45 00 62 00 6B 00 2D 00 41 00 52 2D A2 0A F8 01 B2 00 2E 00 04 00 03 67 00 05 9D
    #g7frame = b'\x42\x4D\x00\x1C\x00\x45\x00\x62\x00\x6B\x00\x2D\x00\x41\x00\x52\x2D\xA2\x0A\xF8\x01\xB2\x00\x2E\x00\x04\x00\x03\x67\x00\x05\x9D'
     # g7bframe = b'\x42\x4d\x00\x1c\x00\x45\x00\x62\x00\x6b\x00\x2d\x00\x41\x00\x52\x2d\xa2\x0a\xf8\x01\xb2\x00\x2e\x00\x04\x00\x03\x67\x00\x05\x9d'
    def setUp(self):
        self.g7hexframe = "424d001c00450062006b002d004100522da20af801b2002e000400036700059d" #"424D001C00450062006B002D004100522DA20AF801B2002E000400036700059D"
        self.g7bframe = b'\x42\x4D\x00\x1C\x00\x45\x00\x62\x00\x6B\x00\x2D\x00\x41\x00\x52\x2D\xA2\x0A\xF8\x01\xB2\x00\x2E\x00\x04\x00\x03\x67\x00\x05\x9D'# b'\x42\x4d\x00\x1c\x00\x45\x00\x62\x00\x6b\x00\x2d\x00\x41\x00\x52\x2d\xa2\x0a\xf8\x01\xb2\x00\x2e\x00\x04\x00\x03\x67\x00\x05\x9d'
        self.g5bframe = b'\x00\x1C\x00\x45\x00\x62\x00\x6B\x00\x2D\x00\x41\x00\x52\x2D\xA2\x0A\xF8\x01\xB2\x00\x2E\x00\x04\x00\x03\x67\x00\x05\x9D'# b'\x42\x4d\x00\x1c\x00\x45\x00\x62\x00\x6b\x00\x2d\x00\x41\x00\x52\x2d\xa2\x0a\xf8\x01\xb2\x00\x2e\x00\x04\x00\x03\x67\x00\x05\x9d'
        
        self.g7frame = [0x42,0x4D,0x00,0x1C,0x00,0x45,0x00,0x62,0x00,0x6B,0x00,0x2D,0x00,0x41,0x00,0x52,0x2D,0xA2,0x0A,0xF8,0x01,0xB2,0x00,0x2E,0x00,0x04,0x00,0x03,0x67,0x00,0x05,0x9D]
        self.pm1_0_CF = 69
        self.pm2_5_CF = 98
        self.pm10_CF  = 107
        self.pm1_0_ATM = 45
        self.pm2_5_ATM = 65
        self.pm10_ATM  = 82
        self.diam_0_3_UM = 11682
        self.diam_0_5_UM = 2808
        self.diam_1_0_UM = 434
        self.diam_2_5_UM = 46
        self.diam_5_0_UM = 4
        self.diam_10_UM = 3
    def ByteToHex(self,byteStr ):
        """
        Convert a byte string to it's hex string representation e.g. for output.
        """
        
        # Uses list comprehension which is a fractionally faster implementation than
        # the alternative, more readable, implementation below
        #   
        #    hex = []
        #    for aChar in byteStr:
        #        hex.append( "%02X " % ord( aChar ) )
        #
        #    return ''.join( hex ).strip()        

        return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()


    def HexToByte(self,hexStr ):
        """
        Convert a string hex byte values into a byte string. The Hex Byte values may
        or may not be space separated.
        """
        # The list comprehension implementation is fractionally slower in this case    
        #
        #hexStr = ''.join( hexStr.split(" ") )
        #return ''.join( ["%c" % chr( int ( hexStr[i:i+2],16 ) ) \
        #                                for i in range(0, len( hexStr ), 2) ] )
    
        bytes = []

        hexStr = ''.join( hexStr.split(" ") )

        for i in range(0, len(hexStr), 2):
            bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

        return ''.join( bytes )


    def test_parse_read_G7data(self):
        
        print ("==G7data==")
        data=self.g7frame
        print(type(self.g7bframe))
        print(type(self.g7frame))
        data_Hex=binascii.hexlify(self.g7bframe)
        data_bytes=binascii.a2b_hex(self.g7hexframe)

        #data_Hex=data.encode('hex')
        #a=data[0:]
        print(data_Hex)
        print(self.g7hexframe)
        print(data_Hex==self.g7hexframe)
        print(data_bytes==self.g7bframe)
        print ("===")
        result = aqi_data_parser.read_G7data(self.g7frame)
        print result
        self.assertEqual(result[PM1_0_CF],self.pm1_0_CF,"pm1_0_CF not equal")
        self.assertEqual(result[PM2_5_CF],self.pm2_5_CF,"pm2_5_CF not equal")
        self.assertEqual(result[PM10_CF],self.pm10_CF,"pm10_CF not equal")
        self.assertEqual(result[PM1_0_ATM],self.pm1_0_ATM,"pm1_0_ATM not equal")
        self.assertEqual(result[PM2_5_ATM],self.pm2_5_ATM,"pm2_5_ATM not equal")
        self.assertEqual(result[PM10_ATM],self.pm10_ATM,"pm10_ATM not equal")
        
        self.assertEqual(result[DIAM_0_3_UM],self.diam_0_3_UM,"diam_0_3_UM not equal")
        self.assertEqual(result[DIAM_0_5_UM],self.diam_0_5_UM,"diam_0_5_UM not equal")
        self.assertEqual(result[DIAM_1_0_UM],self.diam_1_0_UM,"diam_1_0_UM not equal")
        self.assertEqual(result[DIAM_2_5_UM],self.diam_2_5_UM,"diam_2_5_UM not equal")
        self.assertEqual(result[DIAM_5_0_UM],self.diam_5_0_UM,"diam_5_0_UM not equal")
        self.assertEqual(result[DIAM_10_UM],self.diam_10_UM,"diam_10_UM not equal")


    def test_parse_read_G3data(self):
        print ("==G3data=")
        result = aqi_data_parser.read_G3data(self.g7bframe)
        print result
        self.assertEqual(result[0],self.pm1_0_CF,"pm1_0_CF not equal")
        self.assertEqual(result[1],self.pm2_5_CF,"pm2_5_CF not equal")
        self.assertEqual(result[2],self.pm10_CF,"pm10_CF not equal")
        self.assertEqual(result[3],self.pm1_0_ATM,"pm1_0_ATM not equal")
        self.assertEqual(result[4],self.pm2_5_ATM,"pm2_5_ATM not equal")
        self.assertEqual(result[5],self.pm10_ATM,"pm10_ATM not equal")
        
        #self.assertEqual(result[DIAM_0_3_UM],self.diam_0_3_UM,"diam_0_3_UM not equal")
        #self.assertEqual(result[DIAM_0_5_UM],self.diam_0_5_UM,"diam_0_5_UM not equal")
        #self.assertEqual(result[DIAM_1_0_UM],self.diam_1_0_UM,"diam_1_0_UM not equal")
        #self.assertEqual(result[DIAM_2_5_UM],self.diam_2_5_UM,"diam_2_5_UM not equal")
        #self.assertEqual(result[DIAM_5_0_UM],self.diam_5_0_UM,"diam_5_0_UM not equal")
        #self.assertEqual(result[DIAM_10_UM],self.diam_10_UM,"diam_10_UM not equal"

    def test_parse_read_G5data(self):
        print ("==G5data=")
        result = aqi_data_parser.read_G5data(self.g5bframe)
        print result
        self.assertEqual(result[0],self.pm1_0_CF,"pm1_0_CF not equal")
        self.assertEqual(result[1],self.pm2_5_CF,"pm2_5_CF not equal")
        self.assertEqual(result[2],self.pm10_CF,"pm10_CF not equal")
        self.assertEqual(result[3],self.pm1_0_ATM,"pm1_0_ATM not equal")
        self.assertEqual(result[4],self.pm2_5_ATM,"pm2_5_ATM not equal")
        self.assertEqual(result[5],self.pm10_ATM,"pm10_ATM not equal")
        self.assertEqual(result[6],self.diam_0_3_UM,"diam_0_3_UM not equal")
        self.assertEqual(result[7],self.diam_0_5_UM,"diam_0_5_UM not equal")
        self.assertEqual(result[8],self.diam_1_0_UM,"diam_1_0_UM not equal")
        self.assertEqual(result[9],self.diam_2_5_UM,"diam_2_5_UM not equal")
        self.assertEqual(result[10],self.diam_5_0_UM,"diam_5_0_UM not equal")
        self.assertEqual(result[11],self.diam_10_UM,"diam_10_UM not equal")

    def test_pm2_5_nagtive_caculator(self):
        print("===pm2_5_caculator==-99===")
        result = aqi_aqi_caculator.aqi_aqi_caculator.us_pm2_5_aqi_caculator(-99)        
        print result
        self.assertEqual(result[1],"Good","Nagtive case faild")

    def test_pm2_5_0_caculator(self):
        print("===pm2_5_caculator==0===")
        result = aqi_aqi_caculator.aqi_aqi_caculator.us_pm2_5_aqi_caculator(0)        
        print result
        self.assertEqual(result[1],"Good","US 0 case faild")

    def test_pm2_5_55_caculator(self):
        print("===pm2_5_caculator= 55==")
        result = aqi_aqi_caculator.aqi_aqi_caculator.us_pm2_5_aqi_caculator(55)        
        print result
        self.assertEqual(result[1],"Moderate","US 55 case faild")

    def test_pm2_5_20_caculator(self):
        print("===pm2_5_caculator=20==")
        result = aqi_aqi_caculator.aqi_aqi_caculator.us_pm2_5_aqi_caculator(20)        
        print result
        self.assertEqual(result[1],"Lightly","US 20 case faild")

    def test_pm2_5_99_caculator(self):
        print("===pm2_5_caculator==99===")
        result = aqi_aqi_caculator.aqi_aqi_caculator.us_pm2_5_aqi_caculator(99)        
        print result
        self.assertEqual(result[1],"Unhealthy","US 99 case faild")

    def test_pm2_5_199_caculator(self):
        print("===pm2_5_caculator= 199==")
        result = aqi_aqi_caculator.aqi_aqi_caculator.us_pm2_5_aqi_caculator(199)        
        print result
        self.assertEqual(result[1],"Heavily","US 199 case faild")

    def test_pm2_5_299_caculator(self):
        print("===pm2_5_caculator==299===")
        result = aqi_aqi_caculator.aqi_aqi_caculator.us_pm2_5_aqi_caculator(299)        
        print result
        self.assertEqual(result[1],"Hazardous","US 299 case faild")

    def test_pm2_5_399_caculator(self):
        print("===pm2_5_caculator= 399=")
        result = aqi_aqi_caculator.aqi_aqi_caculator.us_pm2_5_aqi_caculator(399)        
        print result
        self.assertEqual(result[1],"Severely","US 399 case faild")

    def test_pm2_5_500_caculator(self):
        print("===pm2_5_caculator= 500=")
        result = aqi_aqi_caculator.aqi_aqi_caculator.us_pm2_5_aqi_caculator(500)        
        print result
        self.assertEqual(result[1],"Severely","US 500 case faild")

    def test_good_US_caculator(self):
        print("===us_value 12 _caculator===")
        result = aqi_aqi_caculator.aqi_aqi_caculator.caculator(aqi_aqi_caculator.us_pm2_5_category[0],12)        
        print result
        self.assertEqual(result,50.0)
    def test_unhealth_US_caculator(self):
        print("===us_value 4 _caculator===")
        result = aqi_aqi_caculator.aqi_aqi_caculator.caculator(aqi_aqi_caculator.us_pm2_5_category[0],4)        
        print result
#=================================================

    def test_chnpm2_5_nagtive_caculator(self):
        print("===chnpm2_5_caculator==-99===")
        result = aqi_aqi_caculator.aqi_aqi_caculator.chn_pm2_5_aqi_caculator(-99)        
        print result
        self.assertEqual(result[1],"Excellent","chn Nagtive case faild")

    def test_chnpm2_5_0_caculator(self):
        print("===pm2_5_caculator==0===")
        result = aqi_aqi_caculator.aqi_aqi_caculator.chn_pm2_5_aqi_caculator(0)        
        print result
        self.assertEqual(result[1],"Excellent","chn 0 case faild")

    def test_chnpm2_5_55_caculator(self):
        print("===pm2_5_caculator= 55==")
        result = aqi_aqi_caculator.aqi_aqi_caculator.chn_pm2_5_aqi_caculator(55)        
        print result
        self.assertEqual(result[1],"Good","chn 55 case faild")

    def test_chnpm2_5_20_caculator(self):
        print("===pm2_5_caculator=20==")
        result = aqi_aqi_caculator.aqi_aqi_caculator.chn_pm2_5_aqi_caculator(20)        
        print result
        self.assertEqual(result[1],"Excellent","chn 20 case faild")

    def test_chnpm2_5_99_caculator(self):
        print("===pm2_5_caculator==99===")
        result = aqi_aqi_caculator.aqi_aqi_caculator.chn_pm2_5_aqi_caculator(99)        
        print result
        self.assertEqual(result[1],"Lightly","chn 99 case faild")

    def test_chnpm2_5_199_caculator(self):
        print("===pm2_5_caculator= 199==")
        result = aqi_aqi_caculator.aqi_aqi_caculator.chn_pm2_5_aqi_caculator(199)        
        print result
        self.assertEqual(result[1],"Heavily","chn 199 case faild")

    def test_chnpm2_5_299_caculator(self):
        print("===pm2_5_caculator==299===")
        result = aqi_aqi_caculator.aqi_aqi_caculator.chn_pm2_5_aqi_caculator(299)        
        print result
        self.assertEqual(result[1],"Hazardous","chn 299 case faild")

    def test_chnpm2_5_399_caculator(self):
        print("===pm2_5_caculator= 399=")
        result = aqi_aqi_caculator.aqi_aqi_caculator.chn_pm2_5_aqi_caculator(399)        
        print result
        self.assertEqual(result[1],"Severely","chn 399 case faild")

    def test_chnpm2_5_500_caculator(self):
        print("===pm2_5_caculator= 500=")
        result = aqi_aqi_caculator.aqi_aqi_caculator.chn_pm2_5_aqi_caculator(500)        
        print result
        self.assertEqual(result[1],"Severely","chn 500 case faild")

if __name__ == '__main__':
    unittest.main()