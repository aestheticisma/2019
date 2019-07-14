#!/usr/bin/python
#-*-coding:utf-8 -*-
import socket
import cv2
import numpy as np
import serial
import time

out_path='/home/pi/demo/face/temp/face_stream'
outfile = out_path+'/face.jpg'

host_port = ('192.168.137.1',7023)
# capture_frame_width = 640
# capture_frame_height = 480
class ClientSocket(object):
    def __init__(self):
        # socket.AF_INET用于服务器与服务器之间的网络通信
        # socket.SOCK_STREAM代表基于TCP的流式socket通信
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect(host_port) #链接服务器
        self.capture = cv2.VideoCapture(0)
        capture_frame_width,capture_frame_height = self.capture.get(3),self.capture.get(4)
        self.capture.set(3, capture_frame_width)
        self.capture.set(4, capture_frame_height)
        self.encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]  #设置编码参数
        
        #打开串口
        serialPort="/dev/ttyAMA0"    #串口
        baudRate=9600       #波特率
        self.ser=serial.Serial(serialPort,baudRate,timeout=0.5)  
        print "参数设置：串口=%s ，波特率=%d"%(serialPort,baudRate)
        
        while(1):
            data_stm = self.ser.readline()
            if(data_stm=='2'):
                print(data_stm)
                break
    def run(self):
        #从摄像头获取图片
        ret , frame = self.capture.read()
        #cv2.imwrite("temp.jpg",frame)
        #encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        while ret:
            #print(frame)
        # 首先对图片进行编码，因为socket不支持直接发送图片
            result, imgencode = cv2.imencode('.jpg', frame)
            #print(imgencode)
            #print(type(imgencode))
            data = np.array(imgencode)
            #print(data)
            #print(type(data))
            #print(data.shape)
            stringData = data.tostring()
            #print(type(stringData))
        # 首先发送图片编码后的长度
            self.client_socket.send(str(len(stringData)).ljust(16))
        # 然后一个字节一个字节发送编码的内容
        # 如果是python对python那么可以一次性发送，如果发给c++的server则必须分开发因为编码里面有字符串结束标志位，c++会截断
        #for i in range (0,len(stringData)):
            self.client_socket.send(bytes(stringData))
            print("send")
            #ret, frame = self.capture.read()
            #if cv2.waitKey(10) == 27:

            #接受返回结果
            data_r = self.client_socket.recv(50)
            print(data_r)
            print(type(data_r))
            if(data_r == '1'):
                self.ser.write(('1').encode("ascii"))
            #print(type(data_r))
            break
        self.capture.release()
        self.client_socket.close()
        cv2.destroyAllWindows()
if __name__ == '__main__':
    while(1):
        print("Begin")
        s = ClientSocket()
        #time.sleep(1)
        print("Begin to send")
        s.run()

