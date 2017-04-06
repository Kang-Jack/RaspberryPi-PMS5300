import sys
import os
import atexit
import psutil
import subprocess
from subprocess import *
from time import sleep, strftime
from datetime import datetime
from lcd2usb import LCD
from aqi_enum import *
import aqi_settings

debug = aqi_settings.IS_DEBUG
class aqi_lcd:
    lcd = LCD()

    def __init__(self):
        self.lcd = LCD()
    def display_CF_iaqis(self,aqis):
        self.display_aqi(PM1_0_CF,aqis[0])
        sleep(2)
        self.display_aqi(PM2_5_CF,aqis[1])
        sleep(2)
        self.display_aqi(PM10_CF,aqis[2])
        sleep(2)
        
    def display_iaqis(self,aqis):
        self.display_aqi(PM1_0_ATM,aqis[3])
        sleep(2)
        self.display_aqi(PM2_5_ATM,aqis[4])
        sleep(2)
        self.display_aqi(PM10_ATM,aqis[5])
        sleep(2)

    def display_aqi(self,aqiType,aqi):
        self.lcd.clear()
        self.lcd.goto(0,0)
        #date_str = datetime.now().strftime('%b %d  %H:%M:%S\n')
        #print(date_str)
        str_aqi=self.get_aqi_display(aqiType)

        self.lcd.write(str_aqi)
        self.lcd.goto(0,1)
        str_val="  "+ str(aqi) +" ug/m3"
        if debug:print (str_val)
        self.lcd.write(str_val)

    def display_us_pm2_5_aqi(self,aqi_val,category):
        self.lcd.clear()
        self.lcd.goto(0,0)
        #date_str = datetime.now().strftime('%b %d  %H:%M:%S\n')
        if debug:print(category)

        self.lcd.write(category)
        self.lcd.goto(0,1)
        str_val="AQI US: "+ aqi_val 
        if debug:print (str_val)
        self.lcd.write(str_val)
        sleep(5)
    
    def display_chn_pm2_5_aqi(self,aqi_val,category):
        self.lcd.clear()
        self.lcd.goto(0,0)
        #date_str = datetime.now().strftime('%b %d  %H:%M:%S\n')
        if debug:print(category)

        self.lcd.write(category)
        self.lcd.goto(0,1)
        str_val="AQI CHN: "+ aqi_val 
        if debug:print (str_val)
        self.lcd.write(str_val)
        sleep(2)

    def get_aqi_display (self,aqiType): 
        display_name = "==== AQI Monitor ===="
        if debug:print(aqiType)
        if aqiType == PM1_0_CF: 
            display_name = "PM1_0(CF=1)"
        if aqiType == PM2_5_CF:
            display_name = "PM2.5(CF=1)"
        if aqiType == PM10_CF:
            display_name = "PM10(CF=1)"
        if aqiType == PM1_0_ATM: 
            display_name = "PM1.0(ATM)"
        if aqiType == PM2_5_ATM: 
            display_name = "PM2.5(ATM)"
        if aqiType == PM10_ATM: 
            display_name = "PM10(ATM) "
        return display_name

    def display_ip_adress(self):
        #cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
        cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
        self.lcd.clear()
        ipaddr = self.run_cmd(cmd)
        self.lcd.goto(0,0)
        self.lcd.write('IP Address :')
        self.lcd.goto(0,1)
        self.lcd.write('%s' % (ipaddr))
        return ipaddr
        
    def display_all_adress(self,isWifi):
        if isWifi: cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
        else:cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
        self.lcd.clear()
        ipaddr = self.run_cmd(cmd)
        self.lcd.goto(0,0)
        if isWifi: self.lcd.write('wlan Address :')
        else: self.lcd.write('eth Address :')
        self.lcd.goto(0,1)
        self.lcd.write('%s' % (ipaddr))
        return ipaddr
    def run_cmd(self,cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output

    def display_cpu_info(self):
        self.lcd.clear()
        self.lcd.goto(0,0) #first line
        s = subprocess.check_output(["/opt/vc/bin/vcgencmd","measure_temp"])
        s = s.split('=')[1][:-3]
        str_temp = "Cpu Temp=" + s + "C"
        if debug:print (str_temp)
        self.lcd.write(str_temp) #print CPU temp
        self.lcd.goto(0,1) # second line

        str_usage = "Cpu Usage: " + str(psutil.cpu_percent(1)) + "%"
        if debug:print (str_usage)
        self.lcd.write(str_usage) #CPU usage

    def display_mem_info(self):
        phymem = psutil.virtual_memory()#phymem_usage()
        buffers = getattr(psutil, 'phymem_buffers', lambda: 0)()	
        cached = getattr(psutil, 'cached_phymem', lambda: 0)()	
        used = phymem.total - (phymem.free + buffers + cached)
        if debug:print (str(phymem.total))
        if debug:print (str(used))
        if debug:print (str(phymem.percent))

        self.lcd.clear()
        self.lcd.goto(0,0)
        self.lcd.write("Mem Usage: " + str(phymem.percent) + "%" )
        self.lcd.goto(0,1)
        self.lcd.write("Mem: " + str(int(used / 1024 / 1024)) + "M/" +str(int(phymem.total / 1024 / 1024)) + "M")

if __name__ == '__main__': 
    aqi_lcd=aqi_lcd()
    count=0
    while (count<20):
        try:
            aqi_lcd.display_all_adress(True)
            sleep(15)
            aqi_lcd.display_all_adress(False)
            sleep(15)
            '''aqi_lcd.display_cpu_info()
            sleep(10)
            aqi_lcd.display_mem_info()
            sleep(10)
            aqi_lcd.display_aqi(PM1_0_CF,40)
            sleep(2)
            aqi_lcd.display_aqi(PM2_5_CF,25)
            sleep(2)
            aqi_lcd.display_aqi(PM10_CF,50)
            sleep(2)
            aqi_lcd.display_aqi(PM1_0_ATM,75)
            sleep(2)
            aqi_lcd.display_aqi(PM2_5_ATM,8)
            sleep(2)
            aqi_lcd.display_aqi(PM10_ATM,10)
            sleep(10)'''
            count=count+1
        except:
            if debug:print ("Except")
            count=count+1
        if count > 10:
            break
    exit()