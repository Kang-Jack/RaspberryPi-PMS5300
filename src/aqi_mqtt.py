
import paho.mqtt.publish as publish
import time
debug = aqi_settings.IS_DEBUG
class aqi_mqtt:
    @staticmethod
    def publish_aqi(data):
        if debug: print("Sending 0...")
        publish.single("home/pi/aqi", data, hostname="192.xxx.xxx.xxx")
        time.sleep(1)

