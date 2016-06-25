#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import urllib
import urllib2
import json
import serial
import time
import gpio
import re
import binascii
import threading
import datetime
import sys

# use your deviceID and apikey
deviceID="xxxxxxxxxx"
apikey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
key_pin = "gpio12"

s = ""
door = ""
PIR = ""
Leak = ""
Smoke = ""
Remote = ""

Door_mac = ""
PIR_mac = ""
Leak_mac = ""
Smoke_mac = ""
Remote_mac = ""

# use USB UART or UART on pcDuino to communicate with zigbee gateway
try:
    ser = serial.Serial("/dev/ttyUSB0", 115200,timeout = 0.1)
except serial.serialutil.SerialException:
    try:
	ser = serial.Serial("/dev/ttyS1", 115200,timeout = 0.1)
        with open("/sys/devices/virtual/misc/gpio/mode/gpio0",'w') as UART_RX:
            UART_RX.write('3')
        with open("/sys/devices/virtual/misc/gpio/mode/gpio1",'w') as UART_TX:
            UART_TX.write('3')
    except serial.serialutil.SerialException:
	print "serial failed!"
        exit()

def setup():
    gpio.pinMode(key_pin,gpio.INPUT)

def key_interrupt():
    val=gpio.digitalRead(key_pin)
    if val==0:
        time.sleep(0.010)
        if val==0:
            return '1'
    return '0'

def http_post(data):
    try:
        url = 'http://www.linksprite.io/api/http'
        jdata = json.dumps(data)
        req = urllib2.Request(url, jdata)
        req.add_header('Content-Type','application/json')
        response = urllib2.urlopen(req)
        return response.read()
    except urllib2.URLError:
	print "connect failed"
	return "connect failed"
	pass

def hexShow(argv):
    result = ''
    hLen = len(argv)
    for i in xrange(hLen):
        hvol = ord(argv[i])
        hhex = '%02x'%hvol
        result += hhex+' '
    return result

def register():
    while True:
        ser.write('\x02')
	ser.write('\x75')
        ser.write('\x1e')
        data = ser.readline()
	val=hexShow(data)
	leng = len(val)
        if leng > 45:
	    a = val.find("0e fc 02 e1",1)
	    if a != -1:
		print "add equipment ok"
		b=a+12
		mac = val[b:b+29]
		return mac
		break
	time.sleep(0.2)

def set_target(short_mac):
    send = "0c fc 02 01 04 01 01 01 02"+short_mac+"02 0a"
    s = send.replace(' ','')
    a=binascii.a2b_hex(s)
    while True:
        ser.write(a)
        recv=ser.readline()
        rec=hexShow(recv)
	a = rec.find("04 fd 02 01",0)
	if a != -1:
	    print "set target ok"
	    break
	time.sleep(0.2)

def gateway_mac():
    while True:
	ser.write('\x02')
	ser.write('\x14')
	ser.write('\x6f')
	data = ser.readline()
	dat = hexShow(data)
	leng = len(dat)
	if leng > 30:
	    a = dat.find("0c 15 00 6f",0)
            if a != -1:
		dt = dat[15:38]
		return dt
	        break
	time.sleep(1)

def bind(eq_mac,gat_mac):
    send = "16 d8"+eq_mac+"01 01 00 03"+gat_mac+"01"
    s = send.replace(' ','')
    a=binascii.a2b_hex(s)
    start = datetime.datetime.now()
    while True:
        ser.write(a)
	recv=ser.readline()
 	rec=hexShow(recv)
	b = rec.find("02 d9 00")
	if b != -1:
	    print "bind ok"
	    break
	time.sleep(0.2)

def cluster():
    send = "08 FC 00 00 05 00 01 01 00"
    s = send.replace(' ','')
    a=binascii.a2b_hex(s)
    start = datetime.datetime.now()
    while True:
	ser.write(a)
        recv=ser.readline()
        rec=hexShow(recv)
        leng = len(rec)
        finsh = datetime.datetime.now()
        tim = (finsh-start).seconds
        if tim > 5:
	    print "failure! please add again"
	    return "xxxx"
	    break
        if leng > 30:
   	    b = rec.find("0b fe 03")
	    c = rec.find("00 01 07 fe 03 00")
	    if b != -1:
		return rec[b+30:b+35]
                break
            elif c != -1:
		return "11 00"
	time.sleep(0.2)

def report():
    send = "11 FC 00 01 00 06 01 00 21 00 20 f0 00 f0 00 01 00 00"
    s = send.replace(' ','')
    a=binascii.a2b_hex(s)
    while True:
	ser.write(a)
        recv=ser.readline()
        rec=hexShow(recv)
        leng = len(rec)
	if leng > 15:
	    b = rec.find("06 fd 00")
            if b != -1:
		print "send report ok"
                break
	time.sleep(0.2)

def alarm():
    line = ser.readline()
    val = hexShow(line)
    leng = len(val)
    if leng >= 56:
	#print val
	po = val.find("fe 01")
	if po != -1:
	    aa = val[po+21:po+26]
            sta = val[po+46]
	    s =  aa+sta
	    return s
    return -1

def open_socket():
    send = "05 FC 01 06 00 01"
    s = send.replace(' ','')
    a=binascii.a2b_hex(s)

def close_socket():
    send = "05 FC 01 06 00 00"
    s = send.replace(' ','')
    a=binascii.a2b_hex(s)

def recovery():
    global s
    global PIR
    s = '0'
    PIR = '0'
    values ={
    "action":"update",
    "apikey":apikey,
    "deviceid":deviceID,
    "params":
    {
        "PIR":PIR,
        "SOS":s
    }}
    http_post(values)

def update(mac,sta):
    global Door_mac
    global PIR_mac
    global Leak_mac
    global Smoke_mac
    global Remote_mac

    global s
    global door
    global PIR
    global Leak
    global Smoke
    global Remote

    try:
        f = open('door.txt','r')
        Door_mac=f.read()
        f.close()
    except IOError:
	pass

    try:
        f = open('pir.txt','r')
        PIR_mac=f.read()
        f.close()
    except IOError:
	pass

    try:
        f = open('leak.txt','r')
        Leak_mac=f.read()
        f.close()
    except IOError:
	pass

    try:
        f = open('smoke.txt','r')
        Smoke_mac=f.read()
        f.close()
    except IOError:
	pass

    try:
        f = open('remote.txt','r')
        Remote_mac=f.read()
        f.close()
    except IOError:
	pass

    if mac == Door_mac:
	door =  sta
    elif mac == PIR_mac:
	PIR = sta
    elif mac == Leak_mac:
	Leak = sta
    elif mac == Smoke_mac:
	Smoke = sta
    elif mac == Remote_mac:
	Remote = sta
	if sta == '1':
	    s = sta
    else:
	print "You should add the equipment first"
    values ={
    "action":"update",
    "apikey":apikey,
    "deviceid":deviceID,
    "params":
    {
        "Door":door,
        "PIR":PIR,
	"Leak":Leak,
	"Smoke":Smoke,
	"Remote":Remote,
        "SOS":s
    }}
    http_post(values)
    if s == '1'or PIR == '1':
        timer = threading.Timer(2,recovery)
        timer.start()

def main():
    global Door_mac
    global PIR_mac
    global Leak_mac
    global Smoke_mac
    global Remote_mac
    setup()
    if ser.isOpen() == True:
        print "serial open succeed!"
    else:
        print "serial open failure!"
    while True:
        # If check the GPIO12's status, if it is high, excuete commands to
        # add new zigbee device into zigbee gateway
        a = key_interrupt()
	if a == '1':
	    print "Add equipment!"
            # Set gateway to allow adding device
	    val=register()
	    short = val[0:5]
	    print "short:"+short
            mac = val[6:29]
            print "mac:"+mac

            # Get the gateway MAC address
            gatmac=gateway_mac()
            print "gatewaymac:"+gatmac

            # Configure the communication with zigbee device
            set_target(short)

            # Bind the zigbee device
	    bind(mac,gatmac)

            # Read the zone type to check the type of zigbee device
            # which can identify the alarm information from different zigbee sensor.
	    zone_type=cluster()
	    print "zone_type:"+zone_type
	    if zone_type == "15 00":
		Door_mac = short
		f = open('door.txt','w')
		f.write(short)
		f.close()
		report()
	    elif zone_type == "0d 00":
                PIR_mac = short
		f=open('pir.txt','w')
		f.write(short)
		f.close()
		report()
            elif zone_type == "2a 00":
                Leak_mac = short
		f=open('leak.txt','w')
                f.write(short)
                f.close()
		report()
            elif zone_type == "28 00":
                Smoke_mac = short
		f=open('smoke.txt','w')
                f.write(short)
                f.close()
		report()
	    elif zone_type == "11 00":
		Remote_mac = short
		f=open('remote.txt','w')
                f.write(short)
                f.close()
		report()
        # Check the alarm information from zigbee sensor node
	data=alarm()
	if data != -1:
            short_mac = data[0:5]
	    print"short mac:"+short_mac
	    status = data[5]
	    print"status:"+status

            # upload the alarm information to linksprite.io server
	    update(short_mac,status)

	time.sleep(0.2)

if __name__=='__main__':
    try:
	main()
    except KeyboardInterrupt:
	ser.close()
