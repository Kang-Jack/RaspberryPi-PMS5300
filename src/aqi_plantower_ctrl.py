import RPi.GPIO as GPIO
import serial
import time
import aqi_settings
from aqi_data_parser import * 
debug = aqi_settings.IS_DEBUG
##transport protocol-Passive Mode
#Host Protocol
#Default baud rate: 9600bps Check bit:None Stop bit:1 bit
#Host Protocol
#Start Byte 1|Start Byte 2| Command | Data 1 | Data 2 | Verify Byte | Verify Byte 2
# 0x42       |     0x4d   |   CMD   | DATAH  | DATAL  |    LRCH     |     LRCL

#=====================================================================================
# Command Definition
# CMD         DATAH          DATAL                               COMMENTS
# 0xe2         X               X                           Read in passivemode
# 0xe1         X             00H-passive / 01H-active      Change mode
# 0xe4         X             00H-sleep / 01H-wakeup        Sleep set
#=====================================================================================
# Answer
# 0xe2: 32 bytes , same as appendix I
# Verify Bytes:
# Add of all the bytes except verify bytes.
#=====================================================================================

class aqi_plantower_ctrl :
    pin = aqi_settings.PT_SET_PIN3

    def __init__(self):
        self.pin = aqi_settings.PT_SET_PIN3
        GPIO.setmode(GPIO.BCM) # set up BCM GPIO numbering 
        GPIO.cleanup(self.pin)
        GPIO.setwarnings(False)
         #GPIO.setup(self.pin, GPIO.OUT) # set a port/pin as an output
         #GPIO.output(self.pin, GPIO.HIGH)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.HIGH)
          # 17 pin3 in plantower sensor  connect to raspi  pin 11 and map to BCM pin 17  
        self.conn_serial_port()
    
    def close(self):
        GPIO.close()
        print "exit"
#PIN3  :SET :Standby mode (when 0), operating mode (when 1)
#SET = 1 working in continuous sampling mode, the module automatically update sampling data after each sampling, 
# the sampling response time is less than 600 milliseconds, the data update time is less than 2 seconds.
#SET = 0 The module enters the low-power standby mode

    def set_work_mode (self): 
        GPIO.output(self.pin, GPIO.HIGH) #set port/pin value to 1/GPIO.HIGH/True   ---working mode 
        return "Work"
  
    def set_sleep_mode (self): 
        GPIO.output(self.pin, GPIO.LOW) #set port/pin value to 0/GPIO.LOW/False   ---standby mode
        return "Sleep"
        
    def conn_serial_port(self):
        #if debug: print aqi_settings.PT_SERIAL_PORT
        self.ser = serial.Serial(
            port=aqi_settings.PT_SERIAL_PORT,
            baudrate=aqi_settings.PT_BAUDRATE,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=False,
            timeout=3.0
        )
        self.ser.inWaiting()
        if debug:print(self.ser.name)
        if debug: print "conn ok"

    def check_keyword(self,bufferlength):
        if debug: print "check_keyword"
        for i in range(bufferlength):
            token = self.ser.read()
            #i=i+1
            token_hex=token.encode('hex')
            if debug: print token_hex
            if token_hex == '42':
                if debug: print "get 42"
                token2 = self.ser.read()
                #i=i+1
                token2_hex=token2.encode('hex')
                if debug: print token2_hex
                if token2_hex == '4d':
                    if debug: print "get 4d"
                    return True
                elif token2_hex == '00': # fixme
                    if debug: print "get 00"
                    token3 = self.ser.read()
                    #i=i+1
                    token3_hex = token3.encode('hex')
                    if token3_hex == '4d':
                        if debug: print "get 4d"
                        return True

    def getAirQuality(self):
        bufferLength = self.ser.inWaiting()
        if debug: print "=====length=== \n %s"%bufferLength
        if bufferLength >= 3:
            try:
                if self.check_keyword(bufferLength):
                    data = self.ser.read(30)
                    if debug: print data
                    airQuality = aqi_data_parser.read_G5data(data)
                    return airQuality
            except:
                if debug: print "exception"
                self.ser.close()
                self.conn_serial_port()
                return None
        return None

if __name__ == '__main__':
    sensor = aqi_plantower_ctrl()
    while True:
        if debug: print"---------call getAirQuality-------------"
        if debug: print sensor.getAirQuality()
        #print("\n %s"%(sensor.ser.inWaiting()))
        if debug: print "----------================--------"
        time.sleep(1)
        #sensor.ser.close()