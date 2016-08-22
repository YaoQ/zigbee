#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import serial
import time
import re
import binascii
import threading
import datetime
import sys


# use USB UART or UART on pcDuino to communicate with zigbee gateway
try:
    ser = serial.Serial("/dev/ttyUSB0", 115200,timeout = 0.1)
except Exception:
    try:
        ser = serial.Serial("/dev/ttyS1", 115200,timeout = 0.1)
        with open("/sys/devices/virtual/misc/gpio/mode/gpio0",'w') as UART_RX:
            UART_RX.write('3')
        with open("/sys/devices/virtual/misc/gpio/mode/gpio1",'w') as UART_TX:
            UART_TX.write('3')
    except serial.serialutil.SerialException:
        print "serial failed!"
        exit()

def register():
    while True:
        ser.write('\x02')
        ser.write('\x75')
        ser.write('\x1e')
        data = ser.readline()
        val=hexShow(data)
        leng = len(val)
        if leng > 45:
            a = val.find("0e fc 02 e1",0)
            if a != -1:
                print "add equipment ok"
                b=a+12
                mac = val[b:b+29]
                return mac
                break
        time.sleep(0.2)

def get_info(short_mac):
    send = "04 c8 " + short_mac + "01"
    s = send.replace(' ','')
    a=binascii.a2b_hex(s)
    while True:
        ser.write(a)
        recv=ser.readline()
        rec=hexShow(recv)
        a = rec.find("19 c9 00",0)
        if a != -1:
            print "get_info ok"
            break

def set_target_tmp(short_mac):
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

def set_target_hum(short_mac):
    send = "0c fc 02 01 04 01 01 02 02"+short_mac+"02 0a"
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

def bind_tmp(eq_mac,gat_mac):
    send = "16 d8"+eq_mac+"01 02 04 03"+gat_mac+"01"
    s = send.replace(' ','')
    a=binascii.a2b_hex(s)
    start = datetime.datetime.now()
    while True:
        ser.write(a)
        recv=ser.readline()
        rec=hexShow(recv)
        b = rec.find("02 d9 00",0)
        if b != -1:
            print "bind ok"
            break
        time.sleep(0.2)

def bind_hum(eq_mac,gat_mac):
    send = "16 d8"+eq_mac+"02 05 04 03"+gat_mac+"01"
    s = send.replace(' ','')
    a=binascii.a2b_hex(s)
    start = datetime.datetime.now()
    while True:
        ser.write(a)
        recv=ser.readline()
        rec=hexShow(recv)
        b = rec.find("02 d9 00",0)
        if b != -1:
            print "bind ok"
            break
        time.sleep(0.2)


def report_tmp():
    send = "11 FC 00 02 04 06 01 00 00 00 29 05 00 05 00 01 00 00"
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

def report_hum():
    send = "11 FC 00 05 04 06 01 00 00 00 21 05 00 05 00 01 00 00"
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
    

def msg():
    line = ser.readline()
    val = hexShow(line)
    leng = len(val)
    if leng >= 40:
        print val



