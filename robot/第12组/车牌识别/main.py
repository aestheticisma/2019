'''
车牌框的识别 剪切保存
'''
# 使用的是HyperLPR已经训练好了的分类器
import os
import cv2
from PIL import Image
import time
import numpy as np
import tensorflow as tf
from pip._vendor.distlib._backport import shutil

def find_car_num_brod():
    watch_cascade = cv2.CascadeClassifier('./py_car_num_tensor/cascade.xml')
    # 先读取图片
    #image = cv2.imread("./py_car_num_tensor/capture_img/car1.jpg")
    image = cv2.imread("F:/frame/frame.jpg")
    #image = cv2.imread("a6.jpg")
    resize_h = 1000
    height = image.shape[0]
    scale = image.shape[1] / float(image.shape[0])
    image = cv2.resize(image, (int(scale * resize_h), resize_h))
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    watches = watch_cascade.detectMultiScale(image_gray, 1.2, 2, minSize=(36, 9), maxSize=(36 * 40, 9 * 40))
    print("检测到车牌数", len(watches))
    for (x, y, w, h) in watches:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cut_img = image[y + 5:y - 5 + h, x + 8:x - 15 + w]  # 裁剪坐标为[y0:y1, x0:x1]
        cut_gray = cv2.cvtColor(cut_img, cv2.COLOR_RGB2GRAY)
        
        cv2.imwrite("./py_car_num_tensor/num_for_car.jpg", cut_gray)
        im = Image.open("./py_car_num_tensor/num_for_car.jpg")
        size = 720, 180
        mmm = im.resize(size, Image.ANTIALIAS)
        mmm.save("./py_car_num_tensor/num_for_car.jpg", "JPEG", quality=95)
        break
'''
剪切后车牌的字符单个拆分保存处理

'''
def cut_car_num_for_chart():
    # 1、读取图像，并把图像转换为灰度图像并显示
    img = cv2.imread("./py_car_num_tensor/num_for_car.jpg")  # 读取图片
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换了灰度化
    #cv2.imshow('gray', img_gray)  # 显示图片
    # 2、将灰度图像二值化，设定阈值是100   转换后 白底黑字 ---》 目标黑底白字
    img_thre = img_gray
    # 灰点  白点 加错
    # cv2.threshold(img_gray, 130, 255, cv2.THRESH_BINARY_INV, img_thre)
    # 二值化处理 自适应阈值   效果不理想
    # th3 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # 高斯除噪 二值化处理
    blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #cv2.imshow('threshold', th3)
    cv2.imwrite('./py_car_num_tensor/wb_img.jpg', th3)
    # src = cv2.imread("D:\PyCharm\Test213\py_car_num_tensor\wb_img.jpg")
    # height, width, channels = src.shape
    # print("width:%s,height:%s,channels:%s" % (width, height, channels))
    # for row in range(height):
    #     for list in range(width):
    #         for c in range(channels):
    #             pv = src[row, list, c]
    #             src[row, list, c] = 255 - pv
    # cv2.imshow("AfterDeal", src)
    # cv2.waitKey(0)
    #
    # # 3、保存黑白图片
    # cv2.imwrite('D:\PyCharm\Test213\py_car_num_tensor\wb_img.jpg', src)
    # img = cv2.imread("D:\PyCharm\Test213\py_car_num_tensor\wb_img.jpg")  # 读取图片
    # src_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换了灰度化
    # src_img = src_gray
    # 4、分割字符
    white = []  # 记录每一列的白色像素总和
    black = []  # ..........黑色.......
    height = th3.shape[0]
    width = th3.shape[1]
    white_max = 0
    black_max = 0
    # 计算每一列的黑白色像素总和
    for i in range(width):
        s = 0  # 这一列白色总数
        t = 0  # 这一列黑色总数
        for j in range(height):
            if th3[j][i] == 255:
                s += 1
            if th3[j][i] == 0:
                t += 1
        white_max = max(white_max, s)
        black_max = max(black_max, t)
        white.append(s)
        black.append(t)
        #print(str(s) + "---------------" + str(t))
    #print("blackmax ---->" + str(black_max) + "------whitemax ------> " + str(white_max))
    # arg = False  # False表示白底黑字；True表示黑底白字
    # if black_max > white_max:
    #     arg = True
    arg = True
    n = 1
    start = 1
    end = 2
    temp = 1
    #print(width)
    while n < width - 2:
        n += 1
        if (white[n] if arg else black[n]) > (0.05 * white_max if arg else 0.05 * black_max):
            # 上面这些判断用来辨别是白底黑字还是黑底白字
            # 0.05这个参数请多调整，对应上面的0.95
            start = n
            if(temp<8):
                end = find_end(start, white, black, arg, white_max, black_max, width)
            elif(temp>8):
                break
            else:
                if(black[width-1]>0.85*black_max):
                    end = find_end(start, white, black, arg, white_max, black_max, width)
                elif(white[width-1]>0.65*white_max):
                    end = find_end(start, white, black, arg, white_max, black_max, width)
                else:
                    end = width-1
            n = end
            #print(n)
            # 车牌框检测分割 二值化处理后 可以看到明显的左右边框  毕竟用的是网络开放资源 所以车牌框定位角度真的不准，
            # 所以我在这里截取单个字符时做处理，就当亡羊补牢吧
            # 思路就是从左开始检测匹配字符，若宽度（end - start）小与20则认为是左侧白条 pass掉  继续向右识别，否则说明是
            # 省份简称，剪切，压缩 保存，还有一个当后五位有数字 1 时，他的宽度也是很窄的，所以就直接认为是数字 1 不需要再
            # 做预测了（不然很窄的 1 截切  压缩后宽度是被拉伸的），
            # shutil.copy()函数是当检测到这个所谓的 1 时，从样本库中拷贝一张 1 的图片给当前temp下标下的字符
            if end - start > 5:  # 车牌左边白条移除
                #print(" end - start" + str(end - start))
                if temp == 1 and end - start < 20:
                    pass
                elif temp > 3 and end - start < 20:
                    #  认为这个字符是数字1   copy 一个 32*40的 1 作为 temp.bmp
                    shutil.copy(os.path.join("./py_car_num_tensor/tf_car_license_dataset/train_images/"
                                             "training-set/1/", "1509806878_75_5.bmp"), # 111.bmp 是一张 1 的样本图片
                                os.path.join("./py_car_num_tensor/img_cut/", str(temp)+'.bmp'))
                    temp = temp + 1
                else:
                    cj = th3[1:height, start:end]
                    cv2.imwrite("./py_car_num_tensor/img_cut_not_3240/" + str(temp) + ".jpg", cj)
                    im = Image.open("./py_car_num_tensor/img_cut_not_3240/" + str(temp) + ".jpg")
                    size = 32, 40
                    mmm = im.resize(size, Image.ANTIALIAS)
                    mmm.save("./py_car_num_tensor/img_cut/" + str(temp) + ".bmp", quality=95)
                    # cv2.imshow('裁剪后：', mmm)
                    # cv2.imwrite("./py_car_num_tensor/img_cut/"+str(temp)+".bmp", cj)
                    temp = temp + 1
                    # cv2.waitKey(0)

# 分割图像
def find_end(start_, white, black, arg, white_max, black_max, width):
    end_ = start_ + 1
    for m in range(start_ + 1, width - 1):
        if (black[m] if arg else white[m]) > (0.95 * black_max if arg else 0.95 * white_max):  # 0.95这个参数请多调整，对应下面的0.05
            end_ = m
            break
    return end_
'''

车牌号码 省份检测：粤   [粤G .SB250]  

'''
SIZE = 1280
WIDTH = 32
HEIGHT = 40
# NUM_CLASSES = 7
PROVINCES = ("京", "闽", "粤", "苏", "沪", "浙")
nProvinceIndex = 0
time_begin = time.time()

# 定义卷积函数
def conv_layer(inputs, W, b, conv_strides, kernel_size, pool_strides, padding):
    L1_conv = tf.nn.conv2d(inputs, W, strides=conv_strides, padding=padding)
    L1_relu = tf.nn.relu(L1_conv + b)
    return tf.nn.max_pool(L1_relu, ksize=kernel_size, strides=pool_strides, padding='SAME')

# 定义全连接层函数
def full_connect(inputs, W, b):
    return tf.nn.relu(tf.matmul(inputs, W) + b)

def province_test():
    province_graph = tf.Graph()
    with province_graph.as_default():
        with tf.Session(graph=province_graph) as sess_p:

            # 定义输入节点，对应于图片像素值矩阵集合和图片标签(即所代表的数字)
            x = tf.placeholder(tf.float32, shape=[None, SIZE])
            x_image = tf.reshape(x, [-1, WIDTH, HEIGHT, 1])
            saver_p = tf.train.import_meta_graph(
                 "./py_car_num_tensor/train-saver/province/model.ckpt.meta")
            # saver_p = tf.train.import_meta_graph(
            #     "./save-vehicle-nums/save-vehicle-PROVINCES/model.ckpt.meta")

            model_file = tf.train.latest_checkpoint("./py_car_num_tensor/train-saver/province")
            saver_p.restore(sess_p, model_file)

            # 第一个卷积层
            W_conv1 = sess_p.graph.get_tensor_by_name("W_conv1:0")
            b_conv1 = sess_p.graph.get_tensor_by_name("b_conv1:0")
            conv_strides = [1, 1, 1, 1]
            kernel_size = [1, 2, 2, 1]
            pool_strides = [1, 2, 2, 1]
            L1_pool = conv_layer(x_image, W_conv1, b_conv1, conv_strides, kernel_size, pool_strides, padding='SAME')

            # 第二个卷积层
            W_conv2 = sess_p.graph.get_tensor_by_name("W_conv2:0")
            b_conv2 = sess_p.graph.get_tensor_by_name("b_conv2:0")
            conv_strides = [1, 1, 1, 1]
            kernel_size = [1, 1, 1, 1]
            pool_strides = [1, 1, 1, 1]
            L2_pool = conv_layer(L1_pool, W_conv2, b_conv2, conv_strides, kernel_size, pool_strides, padding='SAME')

            # 全连接层
            W_fc1 = sess_p.graph.get_tensor_by_name("W_fc1:0")
            b_fc1 = sess_p.graph.get_tensor_by_name("b_fc1:0")
            h_pool2_flat = tf.reshape(L2_pool, [-1, 16 * 20 * 32])
            h_fc1 = full_connect(h_pool2_flat, W_fc1, b_fc1)

            # dropout
            keep_prob = tf.placeholder(tf.float32)
            h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

            # readout层
            W_fc2 = sess_p.graph.get_tensor_by_name("W_fc2:0")
            b_fc2 = sess_p.graph.get_tensor_by_name("b_fc2:0")

            # 定义优化器和训练op
            conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
            for n in range(1, 2):
                path = "./py_car_num_tensor/img_cut/%s.bmp" % (n)
                img = Image.open(path)
                width = img.size[0]
                height = img.size[1]
                img_data = [[0] * SIZE for i in range(1)]
                for h in range(0, height):
                    for w in range(0, width):
                        if img.getpixel((w, h)) < 190:
                            img_data[0][w + h * width] = 1
                        else:
                            img_data[0][w + h * width] = 0
                result = sess_p.run(conv, feed_dict={x: np.array(img_data), keep_prob: 1.0})
                max1 = 0
                max2 = 0
                max3 = 0
                max1_index = 0
                max2_index = 0
                max3_index = 0
                for j in range(6):
                    if result[0][j] > max1:
                        max1 = result[0][j]
                        max1_index = j
                        continue
                    if (result[0][j] > max2) and (result[0][j] <= max1):
                        max2 = result[0][j]
                        max2_index = j
                        continue
                    if (result[0][j] > max3) and (result[0][j] <= max2):
                        max3 = result[0][j]
                        max3_index = j
                        continue
                nProvinceIndex = max1_index
                print("概率：  [%s %0.2f%%]    [%s %0.2f%%]    [%s %0.2f%%]" % (
                    PROVINCES[max1_index], max1 * 100, PROVINCES[max2_index], max2 * 100, PROVINCES[max3_index],
                    max3 * 100))
        print("省份简称是: %s" % PROVINCES[nProvinceIndex])
        return  PROVINCES[nProvinceIndex]

'''
车牌号码第二个字符识别：G   [粤G .SB250]
'''

LETTERS_DIGITS_SECOND = (
    "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y",
    "Z")

def province_letter_test():
    license_num = ""
    letter_graph = tf.Graph()
    with letter_graph.as_default():
        with tf.Session(graph=letter_graph) as sess:
            # 定义输入节点，对应于图片像素值矩阵集合和图片标签(即所代表的数字)
            x = tf.placeholder(tf.float32, shape=[None, SIZE])
            x_image = tf.reshape(x, [-1, WIDTH, HEIGHT, 1])
            saver = tf.train.import_meta_graph(
                "./py_car_num_tensor/train-saver/letters/model.ckpt.meta")
            model_file = tf.train.latest_checkpoint("./py_car_num_tensor/train-saver/letters")
            saver.restore(sess, model_file)
            # 第一个卷积层
            W_conv1 = sess.graph.get_tensor_by_name("W_conv1:0")
            b_conv1 = sess.graph.get_tensor_by_name("b_conv1:0")
            conv_strides = [1, 1, 1, 1]
            kernel_size = [1, 2, 2, 1]
            pool_strides = [1, 2, 2, 1]
            L1_pool = conv_layer(x_image, W_conv1, b_conv1, conv_strides, kernel_size, pool_strides, padding='SAME')

            # 第二个卷积层
            W_conv2 = sess.graph.get_tensor_by_name("W_conv2:0")
            b_conv2 = sess.graph.get_tensor_by_name("b_conv2:0")
            conv_strides = [1, 1, 1, 1]
            kernel_size = [1, 1, 1, 1]
            pool_strides = [1, 1, 1, 1]
            L2_pool = conv_layer(L1_pool, W_conv2, b_conv2, conv_strides, kernel_size, pool_strides, padding='SAME')

            # 全连接层
            W_fc1 = sess.graph.get_tensor_by_name("W_fc1:0")
            b_fc1 = sess.graph.get_tensor_by_name("b_fc1:0")
            h_pool2_flat = tf.reshape(L2_pool, [-1, 16 * 20 * 32])
            h_fc1 = full_connect(h_pool2_flat, W_fc1, b_fc1)

            # dropout
            keep_prob = tf.placeholder(tf.float32)
            h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

            # readout层
            W_fc2 = sess.graph.get_tensor_by_name("W_fc2:0")
            b_fc2 = sess.graph.get_tensor_by_name("b_fc2:0")

            # 定义优化器和训练op
            conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
            for n in range(2, 3):
                path = "./py_car_num_tensor/img_cut/%s.bmp" % (n)
                img = Image.open(path)
                width = img.size[0]
                height = img.size[1]
                img_data = [[0] * SIZE for i in range(1)]
                for h in range(0, height):
                    for w in range(0, width):
                        if img.getpixel((w, h)) < 190:
                            img_data[0][w + h * width] = 1
                        else:
                            img_data[0][w + h * width] = 0

                result = sess.run(conv, feed_dict={x: np.array(img_data), keep_prob: 1.0})
                max1 = 0
                max2 = 0
                max3 = 0
                max1_index = 0
                max2_index = 0
                max3_index = 0
                for j in range(24):
                    if result[0][j] > max1:
                        max1 = result[0][j]
                        max1_index = j
                        continue
                    if (result[0][j] > max2) and (result[0][j] <= max1):
                        max2 = result[0][j]
                        max2_index = j
                        continue
                    if (result[0][j] > max3) and (result[0][j] <= max2):
                        max3 = result[0][j]
                        max3_index = j
                        continue

                if n == 3:
                    license_num += "-"
                license_num = license_num + LETTERS_DIGITS_SECOND[max1_index]
                print("概率：  [%s %0.2f%%]    [%s %0.2f%%]    [%s %0.2f%%]" % (
                    LETTERS_DIGITS_SECOND[max1_index], max1 * 100, LETTERS_DIGITS_SECOND[max2_index], max2 * 100,
                    LETTERS_DIGITS_SECOND[max3_index],
                    max3 * 100))

        print("城市代号是: 【%s】" % license_num)
        return  license_num

'''

车牌号码  后五位识别  SB250 [粤G .SB250]   

'''

LETTERS_DIGITS = (
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N",
    "P",
    "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")

def last_5_num_test():
    license_num = ""
    last_5_num_graph = tf.Graph()
    with last_5_num_graph.as_default():
        with tf.Session(graph=last_5_num_graph) as sess:
            # 定义输入节点，对应于图片像素值矩阵集合和图片标签(即所代表的数字)
            x = tf.placeholder(tf.float32, shape=[None, SIZE])
            x_image = tf.reshape(x, [-1, WIDTH, HEIGHT, 1])
            saver = tf.train.import_meta_graph(
            "./py_car_num_tensor/train-saver/digits_/car_license.ckpt.meta")
            model_file = tf.train.latest_checkpoint("./py_car_num_tensor/train-saver/digits_")

            print("main3")
            saver.restore(sess, model_file)
            # 第一个卷积层
            W_conv1 = sess.graph.get_tensor_by_name("W_conv1:0")
            b_conv1 = sess.graph.get_tensor_by_name("b_conv1:0")
            conv_strides = [1, 1, 1, 1]
            kernel_size = [1, 2, 2, 1]
            pool_strides = [1, 2, 2, 1]
            L1_pool = conv_layer(x_image, W_conv1, b_conv1, conv_strides, kernel_size, pool_strides, padding='SAME')

            # 第二个卷积层
            W_conv2 = sess.graph.get_tensor_by_name("W_conv2:0")
            b_conv2 = sess.graph.get_tensor_by_name("b_conv2:0")
            conv_strides = [1, 1, 1, 1]
            kernel_size = [1, 1, 1, 1]
            pool_strides = [1, 1, 1, 1]
            L2_pool = conv_layer(L1_pool, W_conv2, b_conv2, conv_strides, kernel_size, pool_strides, padding='SAME')

            # 全连接层
            W_fc1 = sess.graph.get_tensor_by_name("W_fc1:0")
            b_fc1 = sess.graph.get_tensor_by_name("b_fc1:0")
            h_pool2_flat = tf.reshape(L2_pool, [-1, 16 * 20 * 32])
            h_fc1 = full_connect(h_pool2_flat, W_fc1, b_fc1)

            # dropout
            keep_prob = tf.placeholder(tf.float32)
            h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

            # readout层
            W_fc2 = sess.graph.get_tensor_by_name("W_fc2:0")
            b_fc2 = sess.graph.get_tensor_by_name("b_fc2:0")

            # 定义优化器和训练op
            conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
            for n in range(4, 9):
                path = "./py_car_num_tensor/img_cut/%s.bmp" % (n)
                img = Image.open(path)
                width = img.size[0]
                height = img.size[1]

                img_data = [[0] * SIZE for i in range(1)]
                for h in range(0, height):
                    for w in range(0, width):
                        if img.getpixel((w, h)) < 190:
                            img_data[0][w + h * width] = 1
                        else:
                            img_data[0][w + h * width] = 0

                result = sess.run(conv, feed_dict={x: np.array(img_data), keep_prob: 1.0})
                max1 = 0
                max2 = 0
                max3 = 0
                max1_index = 0
                max2_index = 0
                max3_index = 0
                for j in range(34):
                    if result[0][j] > max1:
                        max1 = result[0][j]
                        max1_index = j
                        continue
                    if (result[0][j] > max2) and (result[0][j] <= max1):
                        max2 = result[0][j]
                        max2_index = j
                        continue
                    if (result[0][j] > max3) and (result[0][j] <= max2):
                        max3 = result[0][j]
                        max3_index = j
                        continue

                license_num = license_num + LETTERS_DIGITS[max1_index]
                print("概率：  [%s %0.2f%%]    [%s %0.2f%%]    [%s %0.2f%%]" % (
                    LETTERS_DIGITS[max1_index], max1 * 100, LETTERS_DIGITS[max2_index], max2 * 100,
                    LETTERS_DIGITS[max3_index],
                    max3 * 100))

        print("车牌编号是: 【%s】" % license_num)
        return  license_num


if __name__ == '__main__':
#def recog():
    data = "闽C9U25"
    data_2 = "闽C9U2S"
    data_3 = "粤M9025"
    find_car_num_brod()
    cut_car_num_for_chart()
    first = province_test()
    second = province_letter_test()
    last = last_5_num_test()
    result = first+second+last
    print(result)
    # if(result == "闽C9U250"):
    #     return 1
    # if(result == "闽M9025S"):
    #     return 1
    # if(result == "闽C9U256"):
    #     return 1
    # if(result.find(data)!=-1):
    #     return 1
    # if(result.find(data_2)!=-1):
    #     return 1
    # if(result.find(data_3)!=1):
    #     return 1
    # else:
    #     return 0

 
