import time
import sys
from struct import *
import aqi_settings
from aqi_enum import *
debug = aqi_settings.IS_DEBUG
class aqi_data_parser:
    @staticmethod
    def vertify_G3data(data):
    	if debug: print data
        n = 2
        sum = int('42',16)+int('4d',16)
        for i in range(0, len(data)-12, n):
            #print data[i:i+n]
            sum=sum+int(data[i:i+n],16)
        versum = int(data[44]+data[45]+data[46]+data[47],16)
        if debug: print sum
        if debug: print versum
        if sum == versum:
            print "data correct"

    @staticmethod
    def read_G3data(data):
        # data = self.serial.read(22)
        data_hex=data.encode('hex')
        if debug: print (data_hex[0])
        if debug: print (data_hex[1])
        if debug: print (data_hex[2])
        if debug: print (data_hex[3])
        if debug: aqi_data_parser.vertify_G3data(data_hex)
        frameLength=int(data_hex[4]+data_hex[5]+data_hex[6]+data_hex[7],16)
        pm1_cf=int(data_hex[8]+data_hex[9]+data_hex[10]+data_hex[11],16)
        pm25_cf=int(data_hex[12]+data_hex[13]+data_hex[14]+data_hex[15],16)
        pm10_cf=int(data_hex[16]+data_hex[17]+data_hex[18]+data_hex[19],16)
        pm1=int(data_hex[20]+data_hex[21]+data_hex[22]+data_hex[23],16)
        pm25=int(data_hex[24]+data_hex[25]+data_hex[26]+data_hex[27],16)
        pm10=int(data_hex[28]+data_hex[29]+data_hex[30]+data_hex[31],16)
        if debug: print "pm1_cf: "+str(pm1_cf)
        if debug: print "pm25_cf: "+str(pm25_cf)
        if debug: print "pm10_cf: "+str(pm10_cf)
        if debug: print "pm1: "+str(pm1)
        if debug: print "pm25: "+str(pm25)
        if debug: print "pm10: "+str(pm10)
        data = [pm1_cf, pm25_cf,pm10_cf, pm1, pm25,pm10,]
    	# self.serial.close()
        return data

    @staticmethod
    def vertify_G5data(data):
    	if debug: print data
        n = 2
        check_sum_computed = int('42',16)+int('4d',16)
        for i in range(0, len(data)-4, n):
            if debug: print (len(data))
            if debug: print data[i:i+n]
            check_sum_computed=check_sum_computed+int(data[i:i+n],16)

        #check_sum_computed = sum(int(data[0:30],16))
        # get low 16 bit
        #check_sum_computed = check_sum_computed & 0xffff
        #versum = int(data[60]+data[61]+data[62]+data[63],16)
        versum = int(data[56]+data[57]+data[58]+data[59],16)
        if debug: print check_sum_computed
        if debug: print versum
        if check_sum_computed == versum:
            print "data correct"
    @staticmethod

    def read_G5data(data):
        # data = self.serial.read(22)
        data_hex=data.encode('hex')

        if  False == aqi_data_parser.vertify_G5data(data_hex): return None

        frameLength=int(data_hex[0]+data_hex[1]+data_hex[2]+data_hex[3],16)
        pm1_cf=int(data_hex[4]+data_hex[5]+data_hex[6]+data_hex[7],16)
        pm25_cf=int(data_hex[8]+data_hex[9]+data_hex[10]+data_hex[11],16)
        pm10_cf=int(data_hex[12]+data_hex[13]+data_hex[14]+data_hex[15],16)
        pm1=int(data_hex[16]+data_hex[17]+data_hex[18]+data_hex[19],16)
        pm25=int(data_hex[20]+data_hex[21]+data_hex[22]+data_hex[23],16)
        pm10=int(data_hex[24]+data_hex[25]+data_hex[26]+data_hex[27],16)
        diam_0_3_UM=int(data_hex[28]+data_hex[29]+data_hex[30]+data_hex[31],16)
        diam_0_5_UM = int(data_hex[32]+data_hex[33]+data_hex[34]+data_hex[35],16)
        diam_1_0_UM = int(data_hex[36]+data_hex[37]+data_hex[38]+data_hex[39],16)
        diam_2_5_UM = int(data_hex[40]+data_hex[41]+data_hex[42]+data_hex[43],16)
        diam_5_0_UM = int(data_hex[44]+data_hex[45]+data_hex[46]+data_hex[47],16)
        diam_10_UM = int(data_hex[48]+data_hex[49]+data_hex[50]+data_hex[51],16)
        if debug: print "length: "+str(frameLength)
        if debug: print "pm1_cf: "+str(pm1_cf)
        if debug: print "pm25_cf: "+str(pm25_cf)
        if debug: print "pm10_cf: "+str(pm10_cf)
        if debug: print "pm1: "+str(pm1)
        if debug: print "pm25: "+str(pm25)
        if debug: print "pm10: "+str(pm10)
        if debug: print "diam_0_3_UM: "+str(diam_0_3_UM)
        if debug: print "diam_0_5_UM: "+str(diam_0_5_UM)
        if debug: print "diam_1_0_UM: "+str(diam_1_0_UM)
        if debug: print "diam_2_5_UM: "+str(diam_2_5_UM)
        if debug: print "diam_5_0_UM: "+str(diam_5_0_UM)
        if debug: print "diam_10_UM: "+str(diam_10_UM)
        iaqi_data = [pm1_cf, pm25_cf,pm10_cf, pm1, pm25,pm10,diam_0_3_UM,diam_0_5_UM,diam_1_0_UM,diam_2_5_UM,diam_5_0_UM,diam_10_UM]
    	# self.serial.close()
        return iaqi_data

    @staticmethod
    def combineTwoByte(frame, start):
        return (frame[start] << 8) + frame[start+1]

    @staticmethod
    def vertify_G7frame(frame):
        #transport protocol-Active Mode
         #Default baud rate:9600bps Check bit:None Stop 
         #bit:1 bit 
         #32 Bytes (8bits = 1byte)
        if len(frame) != 32: 
            print("The frame's length is not 32 bytes! The frame is %s bytes" %(len(frame)))
            return False
        startSymbol0 = frame[0] # Start character 1 0x42 (fixed)
        startSymbol1 = frame[1] # Start character 2 0x4d (fixed)
        if (startSymbol0 != 0x42 or startSymbol1 != 0x4d) & (startSymbol0 != 'B' or startSymbol1 != 'M'):
            print("The frame's start symbol is not correct" + str(startSymbol0) + " " + str(startSymbol1))
            return False
        frameLength = aqi_data_parser.combineTwoByte(frame, 2)  
        if frameLength != 28: # Frame length=2x13+2(data+check bytes) 
            print("The frame's length data error, the frameLength data is" + str(frameLength))
            return False
        check_sum_computed = sum(frame[0:30])
        print (check_sum_computed)
        # get low 16 bit
        check_sum_computed = check_sum_computed & 0xffff
        print (check_sum_computed)
        check_sum = aqi_data_parser.combineTwoByte(frame, 30)
        print (check_sum)
        if check_sum != check_sum_computed:
            print("Check sum is not correct")
            return False
        return True

    @staticmethod
    def read_G7data(frame):
        if False == aqi_data_parser.vertify_G7frame(frame): return None

        airQuality = {}

        pm1_0_CF = aqi_data_parser.combineTwoByte(frame, 4)
        airQuality[PM1_0_CF] = pm1_0_CF
        print("PM1_0 (CF=1) %s ug/m3" %(pm1_0_CF))


        pm2_5_CF = aqi_data_parser.combineTwoByte(frame, 6)
        print("PM2.5 (CF=1) %s ug/m3" %(pm2_5_CF))
        airQuality[PM2_5_CF] = pm2_5_CF

        pm10_CF = aqi_data_parser.combineTwoByte(frame, 8)
        airQuality[PM10_CF] = pm10_CF
        print("PM10 (CF=1) %s ug/m3" %(pm10_CF))


        pm1_0_atm = aqi_data_parser.combineTwoByte(frame, 10)
        airQuality[PM1_0_ATM] = pm1_0_atm
        print("PM1.0 in the atmosphere %s ug/m3" %(pm1_0_atm))

        pm2_5_atm = aqi_data_parser.combineTwoByte(frame, 12)
        airQuality[PM2_5_ATM] = pm2_5_atm
        print("PM2.5 in the atmosphere %s ug/m3" %(pm2_5_atm))

        pm10_atm = aqi_data_parser.combineTwoByte(frame, 14)
        airQuality[PM10_ATM] = pm10_atm
        print("PM10 in the atmosphere %s ug/m3" %(pm10_atm))

        diam_0_3_UM = aqi_data_parser.combineTwoByte(frame, 16)
        airQuality[DIAM_0_3_UM] = diam_0_3_UM
        print(" %s paticles(diameter beyond 0.3um) in 0.1L of air" %(diam_0_3_UM))

        diam_0_5_UM = aqi_data_parser.combineTwoByte(frame, 18)
        airQuality[DIAM_0_5_UM] = diam_0_5_UM
        print(" %s paticles(diameter beyond 0.5um) in 0.1L of air" %(diam_0_5_UM))

        diam_1_0_UM = aqi_data_parser.combineTwoByte(frame, 20)
        airQuality[DIAM_1_0_UM] = diam_1_0_UM
        print(" %s paticles(diameter beyond 1.0um) in 0.1L of air" %(diam_1_0_UM))

        diam_2_5_UM = aqi_data_parser.combineTwoByte(frame, 22)
        airQuality[DIAM_2_5_UM] = diam_2_5_UM
        print(" %s paticles(diameter beyond 2.5um) in 0.1L of air" %(diam_2_5_UM))

        diam_5_0_UM = aqi_data_parser.combineTwoByte(frame, 24)
        airQuality[DIAM_5_0_UM] = diam_5_0_UM
        print(" %s paticles(diameter beyond 5.0um) in 0.1L of air" %(diam_5_0_UM))

        diam_10_UM = aqi_data_parser.combineTwoByte(frame, 26)
        airQuality[DIAM_10_UM] = diam_10_UM
        print(" %s paticles(diameter beyond 10um) in 0.1L of air" %(diam_10_UM))

        return airQuality

    #ser = serial.Serial(SERIAL_PORT, 9600)
    #ser.inWaiting()
