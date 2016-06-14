# 如何构建基于ZigBee的智能家居

本文将介绍如何使用Zigbee gateway模块与多种Zigbee设备进行通信，实现智能家居解决方案。

![](http://openhapp.com/wp-content/uploads/2016/05/zigbee-6-768x470.jpg)

### 准备材料
* pcDuino3B 或 pcDuino8 Uno x 1  
* [Zigbee Gateway 模块](http://openhapp.com/linker-zigbee-module/) x 1 
* Linker Button x 1  
* Linker Base shield x 1
* [Zigbee 漏水传感器](http://openhapp.com/zigbee-sensors/) x 1

## 具体步骤
为了简化整个流程，本文只使用了一个Zigbee漏水警报器。

#### 1. 注册登录[LinkSprite.io](www.linksprite.com)
网页登录www.linksprite.io注册一个账号，并登录，在自己的账号下面建一个DIY设备，设备类型为00(Custom device type),设备名和设备分组可以随便。

* 注册[www.linksprite.io](www.linksprite.com)
* 登录此账号  
* 创建一个设备，设备编号为00，设备名和设备分组可以自己DIY。 
![](picture/1.png)

* 获取设备的deviceID
![](picture/2.png)

* 获取设备的apikey
![](picture/3.png)

### 硬件连接
根据下图将Zigbee gateway等设备与pcDuino 3B相连。
![](picture/4.png) 

### 下载并运行Zigbee code
启动pcDuino3B，
打开一个终端，在github上获取需要的代码，修改代码中的deviceID和apikey,运行代码并添加一个设备。

* 下载源文件
`git clone https://github.com/YaoQ/zigbee.git`
* 根据上面获取的apikey和deviceID修改代码中的apikey和deviceID
```
cd zigbee
vim zigbee.py
```
![](picture/5.png)

* 添加第一个设备Leak Sensors    

运行zigbee.py程序
```
python zigbee.py
```
![](picture/6.png)  
用卡针戳Leak Sensor的RST，直至上面的绿色LED快速闪烁,此时便可以添加设备，按下Linker button添加设备。
![](picture/7.png) 
![](picture/8.png)  
  
到这里我们的Leak Sensor已经添加成功，此时我们可以linksprite.io观察Leak Sensor的状态了。Leak Sensor是一个漏水检测的传感器，我们此时将它的触角放到有水的地方，然后便可以在linksprite.io看到状态的变化了。
![](picture/9.png)

### 如何添加更多的zigbee设备
按照上述的步骤我们已经可以添加一个设备了，接着我们继续添加其它设备。在zigbee.py程序运行的情况下：
* 按住复位空若干秒，使得传感器的绿色LED灯快速闪烁，进入复位状态
* 按下Linker button添加设备，等待添加完成
* 当程序添加完设备，获取zone type信息时，设备添加完成
* 此时，gateway已经可以获取传感器的报警信息，并可以上传到了LinkSprite.io

### 更多设备
**1. 人体热释电传感器**

![](http://openhapp.com/wp-content/uploads/2016/04/PIR-250x250.jpg)

**2. 烟雾报警器**

![](http://openhapp.com/wp-content/uploads/2016/04/Smoke_sensor-300x300.jpg)

**3. 门磁传感器**

<img src="http://openhapp.com/wp-content/uploads/2016/04/DoorSensor-768x768.png" width=300>

更多zigbee设备可以参考如下链接：
http://openhapp.com/zigbee-sensors/

