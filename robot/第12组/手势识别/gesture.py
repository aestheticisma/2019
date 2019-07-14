from aip import AipBodyAnalysis

filePath = "F:/frame/gesture.jpg"
def gesture(filePath):
    """ 你的 APPID AK SK """
    APP_ID = '16708865'
    API_KEY = 'G14M52g6f1FkbEuGisr7LO17'
    SECRET_KEY = 'AYTIoj7saZIlDLp9tDDj9YG6qDhztjcx'

    client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)


    """ 读取图片 """
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    image = get_file_content(filePath)

    """ 调用手势识别 """
    gesture_info = client.gesture(image)


    num = gesture_info['result_num']

    if(num!=0):
        result = gesture_info['result']

    for i in range(0,num):
        classname = result[i]['classname']
        if(classname!='Face'):
            print(classname)
            return classname
        
