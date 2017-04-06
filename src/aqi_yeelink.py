
import time
import json
import requests
import aqi_settings
import aqi_sysinfo
# example: http://api.yeelink.net/v1.1/device/115088/sensor/144111/datapoints
debug = aqi_settings.IS_DEBUG
class aqi_yeelink:
    url = 'http://api.yeelink.net/v1.0'
    key = ''
    dev = ''
    hdr = ''

    def __init__(self):
        self.key = aqi_settings.YEELINK_API_KEY
        self.dev =aqi_settings.YEELINK_EQUIP_1_KEY
        self.hdr = {'U-ApiKey':self.key,'content-type': 'application/json'}

    def upload_data(self,_atm_val,_cf1_val,_num_val,aqi_val,cpu_temp_val):
        utime=aqi_sysinfo.aqi_sysinfo.get_current_timestamp()

        post_url_25_atm=r'%s/device/%s/sensor/%s/datapoints' % (self.url, self.dev, aqi_settings.YEELINK_PM2_5_ATM_KEY)
        data={"timestamp":utime , "value": _atm_val}
        res=requests.post(post_url_25_atm,headers=self.hdr,data=json.dumps(data))

        post_url_25_cf1=r'%s/device/%s/sensor/%s/datapoints' % (self.url, self.dev, aqi_settings.YEELINK_PM2_5_CF1_KEY)
        data={"timestamp":utime , "value": _cf1_val}
        res=requests.post(post_url_25_cf1,headers=self.hdr,data=json.dumps(data))

        post_url_25_num=r'%s/device/%s/sensor/%s/datapoints' % (self.url, self.dev, aqi_settings.YEELINK_PM2_5_NUM_KEY)
        data={"timestamp":utime , "value": _num_val}
        res=requests.post(post_url_25_num,headers=self.hdr,data=json.dumps(data))

        post_url_25_aqi=r'%s/device/%s/sensor/%s/datapoints' % (self.url, self.dev, aqi_settings.YEELINK_AQI_2_5_KEY)
        data={"timestamp":utime , "value": aqi_val}
        res=requests.post(post_url_25_aqi,headers=self.hdr,data=json.dumps(data))

        post_url_cpu_temp=r'%s/device/%s/sensor/%s/datapoints' % (self.url, self.dev, aqi_settings.YEELINK_CPU_TEM_KEY)
        data={"timestamp":utime , "value": cpu_temp_val}
        res=requests.post(post_url_cpu_temp,headers=self.hdr,data=json.dumps(data))

        if debug:print("utime:%s, url:%s, status_code:%d" %(utime,post_url_25_atm,res.status_code))
        if debug:print("utime:%s, url:%s, status_code:%d" %(utime,post_url_25_cf1,res.status_code))
        if debug:print("utime:%s, url:%s, status_code:%d" %(utime,post_url_25_num,res.status_code))
        if debug:print("utime:%s, url:%s, status_code:%d" %(utime,post_url_25_aqi,res.status_code))
        if debug:print("utime:%s, url:%s, status_code:%d" %(utime,post_url_cpu_temp,res.status_code))
        if debug:print(self.hdr)
        if debug:print([_atm_val,_cf1_val,_num_val,aqi_val,cpu_temp_val])
 
#if __name__ == "__main__":
        #ydev1 = aqi_yeelink()
        #ydev1.upload_data()
