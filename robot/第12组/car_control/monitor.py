#!/usr/bin/python
#-*-coding:utf-8 -*-
# main.py
from flask import Flask, render_template, Response,request
from camera import VideoCamera
import serial
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/index',methods=['POST','GET'])
def judge():
    if request.method == 'POST':
        data = request.get_data()
        print(data)
        username = request.form.get('username')
        password = request.form.get('password')
        if(username == "admin" and password == "admin"):
            return render_template('index.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')



def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

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
    
    if(data=='stop'):
    	ser.write(('0').encode("ascii"))
    elif(data=='front'):
    	ser.write(('1').encode("ascii"))
    elif(data=='leftFront'):
    	ser.write(('2').encode("ascii"))
    elif(data=='rightFront'):
    	ser.write(('3').encode("ascii"))
    elif(data=='rear'):
    	ser.write(('4').encode("ascii"))
    elif(data=='action'):
        ser.write(('5').encode("ascii"))
    elif(data=='gestureRecognition'):
        ser.write(('6').encode("ascii"))
    elif(data=='recurrence'):
        ser.write(('7').encode("ascii"))
    elif(data=='carstreaming'):
        return render_template(carstreaming.html)
    return render_template('index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5000)

