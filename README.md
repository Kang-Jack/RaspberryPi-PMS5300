# Raspberry Pi & Plantower for AQI monitor

An instruction of How to build up AQI monitor by using Raspberry Pi and Plantower sensor

The project builds up an Air Quality Index monitor, by using a Raspberry Pi \(version 1b in my case\) and Plantower PMS5300 sensor.  
 It is a python project which can be setup as a startup bash, running automatically when power up Raspberry Pi

the corresponding python code for Raspberry pi, please see : [https://github.com/Kang-Jack/RaspberryPi-PMS5300](https://github.com/Kang-Jack/RaspberryPi-PMS5300)

The corresponding How to book, please see : [https://kang-jack.gitbooks.io/raspberrypi-pms5300/](https://kang-jack.gitbooks.io/raspberrypi-pms5300/)

** Features**

* Detecting the quality and number of each particles with different size per unit volume:

    1. Concentration of PM1.0/PM2.5/PM10 

     2. The number of particles with of PM1.0/PM2.5/PM10

```
      *Range of measurement 0.3 ~ 1.0 / 1. 0 ~ 2.5 / 2.5 ~ 10 Micrometer\(μ m\)

      *The unit volume of particle number is 0.1L. 

      *The unit of mass concentration is μ g/m³.
```

* Caculate Air Quality Index based on concentration of PM2.5 with US and Chinese standard respectively.

* Display the result on a LCD or upload to yeelink [http://www.yeelink.net/](http://www.yeelink.net/) \(Wifi connection required\)

* Power saving strategies: by default the AQI monitor will be actived as initiative modle for first 20 mintues,

then will switch back and forth between working model and sleeping model automaticlly with embeded power saving strategy.

![](/assets/2.png)

Display  PM2.5 iAQI with US standard

![](/assets/3.png)

Display  PM2.5 iAQI with Chinese standard

![](/assets/yeelink.png)Upload PM2.5 iAQI to Yeelink \(with internet available\)

