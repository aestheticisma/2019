#!/usr/bin/python
#-*-coding:utf-8 -*-
import socket
import cv2
import numpy

#socket.AF_INET用于服务器与服务器之间的网络通信'
#socket.SOCK_STREAM代表基于TCP的流式socket通信'
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 连接服务端
address_server = ('192.168.137.1',8013)
sock.connect(address_server)

# 从摄像头采集图像
capture = cv2.VideoCapture(0)
capture.set(3,500)
capture.set(4,400)
ret, frame = capture.read()
#encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90] #设置编码参数
#cv2.imshow('CLIENT',frame)

while ret: 
    # 首先对图片进行编码，因为socket不支持直接发送图片
    result, imgencode = cv2.imencode('.jpg', frame)
    data = numpy.array(imgencode)
    stringData = data.tostring()
    #print(stringData)
    # 首先发送图片编码后的长度
    # 然后一个字节一个字节发送编码的内容
    # 如果是python对python那么可以一次性发送，如果发给c++的server则必须分开发因为编码里面有字符串结束标志位，c++会截断
    #print (len(stringData))
    sock.send(str(len(stringData)).ljust(16))
    print('send_lenth')
    #for i in range (0,len(stringData)):
        #print(bytes(stringData[i]))
    sock.send(bytes(stringData))
    print("send")
    #break
    ret, frame = capture.read()
    if cv2.waitKey(10) == 27:
        break
    # 接收server发送的返回信息
    #data_r = sock.recv(50)
    #print (data_r)

sock.close()
cv2.destroyAllWindows()
