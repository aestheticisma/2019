# -*- coding: utf-8 -*-
from bottle import get,post,run,request,template
import serial

@get("/")
def index():
    return template("index") 
#### 这个是 客户端请求 服务端就发给一个 index.html 控制界面给客户端
@post("/cmd")
def cmd():
    #打开串口
    serialPort="/dev/ttyAMA0"    #串口
    baudRate=9600       #波特率
    ser=serial.Serial(serialPort,baudRate,timeout=0.5)  
    #print("参数设置：串口=%s ，波特率=%d"%(serialPort,baudRate)) 
    adss=request.body.read().decode()#### 接收到 客户端 发过来的数据
    print adss
    if(adss=='stop'):
    	ser.write(('0').encode("ascii"))
    elif(adss=='front'):
    	ser.write(('1').encode("ascii"))
    elif(adss=='leftFront'):
    	ser.write(('2').encode("ascii"))
    elif(adss=='rightFront'):
    	ser.write(('3').encode("ascii"))
    elif(adss=='rear'):
    	ser.write(('4').encode("ascii"))
    elif(adss=='leftRear'):
    	ser.write(('5').encode("ascii"))
    elif(adss=='rightRear'):
    	ser.write(('6').encode("ascii"))
    return "OK"

run(host="0.0.0.0")  #### 开启服务端 

