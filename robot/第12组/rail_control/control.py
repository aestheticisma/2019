#!/usr/bin/python
#-*-coding:utf-8 -*-
# main.py
from flask import Flask, render_template, Response,request
#from camera import VideoCamera
import serial
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login2.html')

@app.route('/index',methods=['POST','GET'])
def judge():
    if request.method == 'POST':
        data = request.get_data()
        print(data)
        username = request.form.get('username')
        password = request.form.get('password')
        if(username == "admin" and password == "admin"):
            return render_template('control.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route("/cmd",methods = ['POST','GET'])
def cmd():
    #打开串口
    serialPort="/dev/ttyAMA0"    #串口
    baudRate=9600       #波特率
    ser=serial.Serial(serialPort,baudRate,timeout=0.5)  
    print("参数设置：串口=%s ，波特率=%d"%(serialPort,baudRate)) 
    #adss=request.body.read().decode()#### 接收到 客户端 发过来的数据
    data = request.get_data().decode()
    print(data)
    
    if(data=='raiseup'):
    	ser.write(('1').encode("ascii"))
    elif(data=='putdown'):
    	ser.write(('0').encode("ascii"))
    return render_template('control.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5001)