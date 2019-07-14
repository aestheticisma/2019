# -*- coding: utf-8 -*-
import wave
from pyaudio import PyAudio,paInt16
import json
import base64
import os
import requests
import time


RATE = "16000"
FORMAT = "wav"
CUID="wate_play"
DEV_PID="1536"

framerate=16000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2

def getHtml(url):
    requests.packages.urllib3.disable_warnings()
    page = requests.get(url)
    return page.text

def get_answer(string):
    key = "441ca90fb13a42ce9f781fbb8149564d"
    api = "http://www.tuling123.com/openapi/api?key=" + key + "&info="

    request = api + string
    #print(request)
    response = getHtml(request)
    dic_json = json.loads(response)
    print dic_json['text']


def get_token():
    server = "https://openapi.baidu.com/oauth/2.0/token?"
    grant_type = "client_credentials"
    #API Key
    client_id = "qMfgVzwXudihVxbXk852mh3D"
    #Secret Key
    client_secret = "Wt3XiHzlUnrLnYV4gAhB00F7MWIOKghx" 

    #拼url
    url ="%sgrant_type=%s&client_id=%s&client_secret=%s"%(server,grant_type,client_id,client_secret)
    #获取token
    #requests.packages.urllib3.disable_warnings()
    #print(url)
    res = requests.post(url)
    token = json.loads(res.text)["access_token"]
    return token
def get_word(token):
    with open(r'./01.wav', "rb") as f:
        speech = base64.b64encode(f.read()).decode('utf8')
    size = os.path.getsize(r'./01.wav')
    headers = { 'Content-Type' : 'application/json'} 
    url = "https://vop.baidu.com/server_api"
    data={
            "format":FORMAT,
            "rate":RATE,
            "dev_pid":DEV_PID,
            "speech":speech,
            "cuid":CUID,
            "len":size,
            "channel":1,
            "token":token,
        }
    #requests.packages.urllib3.disable_warnings()
    req = requests.post(url,json.dumps(data),headers)
    result = json.loads(req.text)
    #print(result)
    ret=result["result"][0]
    return result

def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    print '...'
    print '录音开始...' 
    while count<TIME*8:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count+=1

    save_wave_file('01.wav',my_buf)
    stream.close()


chunk=512
def play():
    wf=wave.open(r"01.wav",'rb')
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
    wf.getnchannels(),rate=wf.getframerate(),output=True)
    while True:
        data=wf.readframes(chunk)
        if data=="":break
        stream.write(data)
    stream.close()
    p.terminate()

if __name__ == '__main__':
    time.sleep(1)
    my_record()
    token=get_token()
    try:
        ret = get_word(token)
        str = ret['result']
        for a in str:
            string = a
        print string
        get_answer(string)
    except:
        print '失败了'
    