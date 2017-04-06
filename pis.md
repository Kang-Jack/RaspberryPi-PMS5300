## Setup **Raspberry Pi**

### Config raspberry release the serial port

**opt1:**

Modify '/boot/cmdline.txt'

```
   remove 'console=ttyAMA0,115200' or 'console=ttyAMA0,115200 kgdboc=ttyAMA0,115200，'
```

**opt2:**

Close the service \(depends on system version\)

```
   sudo systemctl stop serial-getty@ttyAMA0.service

   sudo systemctl disable serial-getty@ttyAMA0.service
```

restart raspberry pi

### Prepare running Python ENV.

```
sudo apt-get install python-dev

sudo apt-get install python-pip

sudo easy\_install -U distribute

sudo pip install rpi.gpi


sudo pip install serial

sudo pip install psutil

sudo pip install lcd2usb

sudo pip install apscheduler
```

### Clone code and modify bash file

1. Download code from github
2. modify file AQI with your user name and install folder path

   ```
   sudo cp /home/{user name}/{install folder}/AQI /etc/init.d/AQI

   sudo chmod +x /etc/init.d/AQI
   ```

** start / stop service    
**

```
   sudo service AQI start \#start

   sudo service AQI stop \#stop
```

**make bash auto start**

```
    sudo update-rc.d AQI defaults
```



