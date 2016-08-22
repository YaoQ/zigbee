# How to use ZigBee Temperature and Humdity Sensor

|**Temperature and Humidity Sensor**|
|:---:|
|<img src="http://openhapp.com/wp-content/uploads/2016/04/temperatuer_humidatiy-768x797.png" width=200>|


These ZigBee node devices support ZHA standard protocol.

Linker ZigBee gateway module is one kind of Linker modules which can communicate with up to 32 ZigBee node devices. It is powered by Marvell 88MZ100 ZigBee microcontroller SoC chip. This ZigBee offers advantages for many application scenarios, including lighting control, smart metering, home/building automation, remote controls and health care applications.


## Tutorial
This tutorial will introduce how to interface ZigBee temperature and sensor using the Linker ZigBee gateway.


## Prerequisites

* [ZigBee Gateway module](http://store.cutedigi.com/linker-zigbee-module-for-deepcam-zigbee-sensors/) x 1 
* [ZigBee temperature and humidity sensor](http://openhapp.com/temperature-and-humidity-sensor/)

## Commands to communicate ZigBee sensor

Setting the temperature and  humidity report are different.So we separate theses commands into two sections.
 
### Temperature

**1. Set Permit Join**
send: 02 75 1e

recv: 02 8a 00
recv: 0E FC 02 E1 *B1 96* **5E 59 39 53 C9 43 50 00** FF

Get the short address of device : B1 96
Get the MAC address of device : 5E 59 39 53 C9 43 50 00

**2. Get the information**
send: 04 c8 b1 96 01

recv: 19 C9 00 B1 96 14 01 04 01 02 03 00 05 00 00 03 00 02 04 01 00 09 00 01 19 00

**3. set target**
send: 0c fc 02 01 04 01 01 01 02 **b1 96** 02 0a

recv: 04 FD 02 01 00 

**4. Get the MAC address of ZiBee gateway**
send: 02 14 6f

recv: 0C 15 00 6F 08 62 43 39 1F C9 43 50 00 
Gateway Mac: 62 43 39 1F C9 43 50 00 

** 5. Bind device to communication**
send: 16 d8 **5E 59 39 53 C9 43 50 00** 01 02 04 03 **62 43 39 1F C9 43 50 00** 01

recv: 02 D9 00

** 6. Configure report **
send: 11 fc 00 02 04 06 01 00 00 00 29 05 00 05 00 01 00 00

recv: 06 FD 00 02 04 06 00 

** 7. Temperature report message**
recv: 14 FE 03 **02 04** 0A 01 02 B1 96 00 96 00 01 00 00 00 00 29 **F5 0A**

Temperature is : 0x0AF5/100=28.05℃


#### Humidity
** 1. Set Permit Join**

send:02 75 1e

recv: 02 8a 00
recv: 0E FC 02 E1 1B 37 5E 59 39 53 C9 43 50 00 FF  
Get the short address of device : 1B 37
Get the MAC address of device : 5E 59 39 53 C9 43 50 00

** 2. Get the information ** 
send: 04 c8 1b 37 01

recv: 19 C9 00 1B 37 14 01 04 01 02 03 00 05 00 00 03 00 02 04 01 00 09 00 01 19 00  

**3. set target**
send: 0c fc 02 01 04 01 01 02 02 1b 37 02 0a

recv: 04 FD 02 01 00 

**4. Get the MAC address of ZiBee gateway**

send: 02 14 6f

recv: 0C 15 00 6F 08 62 43 39 1F C9 43 50 00 

Gateway Mac: 62 43 39 1F C9 43 50 00


** 5. Bind device to communication**

send: 16 d8 5E 59 39 53 C9 43 50 00 02 05 04 03 62 43 39 1F C9 43 50 00 01

recv: 02 D9 00

** 6. Configure report **
send: 11 fc 00 05 04 06 01 00 00 00 21 05 00 05 00 01 00 00   

recv: 06 FD 00 05 04 06 00 

** 7. Humidity report message**
recv: 14 FE 03 **05 04** 0A 02 02 1B 37 00 37 00 01 00 00 00 00 21 FA 17

Humidity is :0x17fa/100=61.38%
