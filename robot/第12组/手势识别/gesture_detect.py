import cv2
import numpy as np
import gesture
#import serial
def main():

    gesture1=""
    flag=0
    #cap = cv2.VideoCapture(0)
    
        #ret,img = cap.read()
        #l=cv2.waitKey(1)
        #if l == 99 :
            #cv2.imwrite('example.jpg',img)
    gesture1=gesture.gesture("F:/frame/gesture.jpg")
        



        # skinMask = HSVBin(img)
        # contours = getContours(skinMask)
        # cv2.drawContours(img,contours,-1,(0,255,0),2)
        # cv2.imshow('capture',img)
        # k = cv2.waitKey(10)
    if gesture1 == "Ok":
        return 1
    elif gesture1 =="Five":
        return 0
    else:
        print("识别失败")
        return -1
    # if k == 27:
    #     cap.release()
   #cv2.destroyAllWindows()


# def getContours(img):
#     kernel = np.ones((5,5),np.uint8)
#     closed = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
#     closed = cv2.morphologyEx(closed,cv2.MORPH_CLOSE,kernel)
#     contours,h = cv2.findContours(closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#     vaildContours = []
#     for cont in contours:
#         if cv2.contourArea(cont)>9000:
#             #x,y,w,h = cv2.boundingRect(cont)
#             #if h/w >0.75:
#             #filter face failed
#             vaildContours.append(cv2.convexHull(cont))
#             #rect = cv2.minAreaRect(cont)
#             #box = cv2.cv.BoxPoint(rect)
#             #vaildContours.append(np.int0(box))
#     return  vaildContours

# def HSVBin(img):
#     hsv = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)

#     lower_skin = np.array([100,50,0])
#     upper_skin = np.array([125,255,255])

#     mask = cv2.inRange(hsv,lower_skin,upper_skin)

#     #res = cv2.bitwise_and(img,img,mask=mask)
#     return mask

# if __name__ =='__main__':
#     main()
    
