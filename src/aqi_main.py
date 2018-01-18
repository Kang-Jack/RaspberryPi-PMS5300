import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os
import httplib, urllib
import serial
import logging
import aqi_enum
import aqi_settings
import aqi_plantower_ctrl
import aqi_aqi_caculator
import aqi_data_parser
import aqi_sysinfo
import aqi_yeelink
import aqi_lcd
import aqi_mqtt

debug = aqi_settings.IS_DEBUG
iAQIs = None
display = None
has_net = 1
model = 1
aqi_lcd_monitor = aqi_lcd.aqi_lcd()
sensor = aqi_plantower_ctrl.aqi_plantower_ctrl()
yeelink = aqi_yeelink.aqi_yeelink()

logging.basicConfig(level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='log1.txt',
        filemode='a')

def display_pi_info():
    global model
    global aqi_lcd_monitor
    global has_net
    ipaddr = aqi_lcd_monitor.display_ip_adress()
    if(ipaddr == '0.0.0.0')or(ipaddr == '255.255.255.255')or(ipaddr == '')or(ipaddr == None):
        has_net = 0
    if debug: print ("model: %s" %str(model))
    if debug: print ("has_net: %s" %str(has_net))
    time.sleep(5)
    aqi_lcd_monitor.display_cpu_info()
    time.sleep(2)
    aqi_lcd_monitor.display_mem_info()
    time.sleep(2)
    return

def display_pi_info_task():
    global has_net
    global scheduled
    display_pi_info()
    if aqi_settings.IF_UPLOADING_YEELINK: 
        if has_net == 0 :scheduled.pause_job('yeelink_task')
        else:scheduled.resume_job('yeelink_task')
    return

def set_sleeping_mode():
    global model
    global sensor
    global has_net
    if (model == 1):
        sensor.set_sleep_mode()
        model = 0
        if debug: print ("sleeping mode")
    return 0

def set_working_mode():
    global model
    global sensor
    global has_net
    if (model == 0):
        sensor.set_work_mode()
        model = 1
        if debug: print ("working mode")
    return 1

def get_iAQIs():
    global model
    global sensor
    global iAQIs
    global display
    if debug: print("---------call getAirQuality-------------")
    if (model ==0):return None
    iAQIs = sensor.getAirQuality()
    if (None != iAQIs): display =iAQIs

def display_AQIs():
    global aqi_lcd_monitor
    global iAQIs
    global display
    if(display == None):return
    if debug: print (display)
    if aqi_settings.IS_DISPLAY_CF_IAQI: aqi_lcd_monitor.display_CF_iaqis(display)
    aqi_lcd_monitor.display_iaqis(display)

    if debug: print "=====US AQI======"
    us_pm2_5_display = aqi_aqi_caculator.aqi_aqi_caculator.us_pm2_5_aqi_caculator(display[4])
    us_pm10_display = aqi_aqi_caculator.aqi_aqi_caculator.us_pm10_aqi_caculator(display[5])
    if debug: print us_pm2_5_display
    if debug: print us_pm10_display
    aqi_mqtt.aqi_mqtt.publish_aqi.(us_pm2_5_display[0])
    aqi_lcd_monitor.display_us_pm2_5_aqi(us_pm2_5_display[0],us_pm2_5_display[1])

    if debug: print "=====CHN AQI======"
    chn_pm2_5_display = aqi_aqi_caculator.aqi_aqi_caculator.chn_pm2_5_aqi_caculator(display[4])
    chn_pm10_display = aqi_aqi_caculator.aqi_aqi_caculator.chn_pm10_aqi_caculator(display[5])
    if debug: print chn_pm2_5_display
    if debug: print chn_pm10_display
    aqi_lcd_monitor.display_chn_pm2_5_aqi(chn_pm2_5_display[0],chn_pm2_5_display[1])


def upload_yeelink ():
    global model
    global yeelink
    global has_net
    global display
    if (has_net == 0 ):return
    if(display == None):return
    cpu_tem=aqi_sysinfo.aqi_sysinfo.get_cup_temp_C()
    if debug: print ("yeelink cpu_tem")
    if debug: print (cpu_tem)
    us_pm2_5_display = aqi_aqi_caculator.aqi_aqi_caculator.us_pm2_5_aqi_caculator(display[4])
    us_pm10_display = aqi_aqi_caculator.aqi_aqi_caculator.us_pm10_aqi_caculator(display[5])
    yeelink.upload_data(display[4],display[1],display[6],us_pm2_5_display[0],cpu_tem)

def init():
    global model
    global iAQIs
    global has_net
    global display
    iAQIs = None
    display = None
    has_net = 1
    model = 1
    display_pi_info()

if __name__ == '__main__':
    init()
    scheduled = BackgroundScheduler()
    scheduled.add_job(display_pi_info_task, 'interval', minutes=21, id='pi_info_task')
    scheduled.add_job(display_AQIs, 'interval', seconds=30, id='lcd_task')
    if aqi_settings.IF_UPLOADING_YEELINK: scheduled.add_job(upload_yeelink, 'interval', seconds=300, id='yeelink_task')
    scheduled.add_job(set_sleeping_mode, 'interval', minutes=20, id='sleeping_mode_task')
    scheduled.add_job(set_working_mode, 'interval', minutes=41, id='working_mod_task')
    if debug: print 'jobs::%s'%scheduled.get_jobs()
    scheduled._logger = logging
    scheduled.start()
    global model
    while True:
        try:
            if model:
                get_iAQIs()
                time.sleep(0.1)
            else:
                time.sleep(31)
        except (KeyboardInterrupt, SystemExit):
            sensor.close()
        finally:
            sensor.close()