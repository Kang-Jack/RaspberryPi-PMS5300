
from datetime import datetime
import psutil
import subprocess

class aqi_sysinfo:
    @staticmethod
    def run_cmd(cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = p.communicate()[0]
        return output

    @staticmethod
    def get_cup_temp_C ():
        s = subprocess.check_output(["/opt/vc/bin/vcgencmd","measure_temp"])
        s = s.split('=')[1][:-3]
        return s

    @staticmethod
    def get_ip_adress():
        cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
        ipaddr = aqi_sysinfo.run_cmd(cmd)
        return ipaddr

    @staticmethod
    def get_mem_info_mb():
        phymem = psutil.virtual_memory()#phymem_usage()
        buffers = getattr(psutil, 'phymem_buffers', lambda: 0)()	
        cached = getattr(psutil, 'cached_phymem', lambda: 0)()	
        used = phymem.total - (phymem.free + buffers + cached)
        return [str(int(phymem.total / 1024 / 1024)),str(int(used / 1024 / 1024)),str(phymem.percent)]
    
    @staticmethod
    def get_current_timestamp():
        date_str = datetime.now().strftime('%b %d  %H:%M:%S\n')
        return date_str