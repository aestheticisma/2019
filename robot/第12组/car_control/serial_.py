# -*- coding: utf-8 -*-
import serial

#打开串口
serialPort="/dev/ttyAMA0"    #串口
baudRate=9600       #波特率
ser=serial.Serial(serialPort,baudRate,timeout=0.5)  
print "参数设置：串口=%s ，波特率=%d"%(serialPort,baudRate)


#ser.write(('1').encode("ascii"))
#收发数据
while 1:
    ser.write(('6').encode("ascii"))
#size = ser.inWaiting()
#if size !=0:
    #response = ser.read(size)
    #print response
    #ser.flushInput()
    #data = ''
    #data = data.encode('ascii')
    #n = ser.inWaiting()
    #if n: 
        #data = data + ser.read(n)
        #print('get data from serial port:', data)
        #print(type(data))
    #str = raw_input("请输入要发送的数据（非中文）并同时接收数据: ")
    print ser.readline()
    print type(ser.readline()) #可以接收中文
    
ser.close() 
