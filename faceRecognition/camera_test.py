from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import cv2
import xlsxwriter
import tensorflow as tf
import numpy as np
import os
import time
import face_recognition
from utils import file_processing,image_processing
resize_width = 160
resize_height = 160
model_path = 'models/20180408-102900'
dataset_path = 'dataset/emb/15080201/faceEmbedding.npy'
filename = 'dataset/emb/name.txt'

def load_dataset(dataset_path,filename):
    '''
    加载人脸数据库
    :param dataset_path: faceEmbedding.npy 存放的是人脸的向量
    :param filename: labels文件路径路径（name.txt） 存放的是人脸的标签
    :return compare_emb: 用于对比的向量
    :return name_list: 对应的名字标签
    '''
    compare_emb=np.load(dataset_path)
    names_list=file_processing.read_data(filename)
    return compare_emb,names_list

def compare_embadding(pred_emb, dataset_emb, names_list):
    # 为bounding_box 匹配标签
    pred_num = len(pred_emb)
    dataset_num = len(dataset_emb)
    pred_name = []
    for i in range(pred_num):
        dist_list = []
        for j in range(dataset_num):
            dist = np.sqrt(np.sum(np.square(np.subtract(pred_emb[i, :], dataset_emb[j, :]))))
            dist_list.append(dist)
        min_value = min(dist_list)
        if (min_value > 0.95):
            pred_name.append('unknow')
        else:
            pred_name.append(names_list[dist_list.index(min_value)])
    return pred_name

if __name__=='__main__':

    # 加载数据库的数据
    dataset_emb, names_list = load_dataset(dataset_path, filename)  # 0.0
    # 初始化mtcnn人脸检测
    face_detect = face_recognition.Facedetection()  # 1.06
    # 初始化facenet
    face_net = face_recognition.facenetEmbedding(model_path)  # 7.81
    #调用电脑的摄像头
    video_capture = cv2.VideoCapture(0)
    # video_capture = cv2.VideoCapture(1)
    # 开启ip摄像头
    #video = "http://10.22.70.36:1998/video"  # 此处@后的ipv4 地址需要修改为自己的地址
    # 参数为0表示打开内置摄像头，参数是视频文件路径则打开视频
    #video_capture1 = cv2.VideoCapture(video)
    Attendence = []
    while (True):
        ret, image = video_capture.read()
        # 进行人脸检测，获得bounding_box --消耗时间0.17183518409729004
        bounding_box, points = face_detect.detect_face(image)

        if (len(bounding_box) != 0):
            bounding_box = bounding_box[:, 0:4].astype(int)
            # 获得人脸区域 --消耗时间0.0
            face_images = image_processing.get_crop_images(image, bounding_box, resize_height, resize_width, whiten=True)
            # image_processing.show_image("face", face_images[0,:,:,:])
            # 消耗时间1.0965726375579834
            pred_emb = face_net.get_embedding(face_images)
            pred_name = compare_embadding(pred_emb, dataset_emb, names_list)
            Attendence.extend(pred_name)
            # 出勤表的列表，已经去重复
            Attendence = sorted(set(Attendence), key=Attendence.index)
            # 在图像上绘制人脸边框和识别的结果 消耗时间0.0624847412109375
            image_processing.cv_show_image_text("face_recognition", image, bounding_box, pred_name)
        else:
            image_processing.cv_show_image_text("face_recognition", image, [], [])
        key = cv2.waitKey(3)
        if key == 27:
            # 用来制作考勤表
            dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            sheet_path = "./Attendence/" + dt

            if not os.path.exists(sheet_path):
                os.makedirs(sheet_path)
            workbook = xlsxwriter.Workbook(sheet_path + '/data.xlsx')  # 创建一个Excel文件
            worksheet = workbook.add_worksheet()  # 创建一个sheet
            title = [U'ID']  # 表格title
            worksheet.write_row('A1', title)  # title 写入Excel
            row_num = 2
            for name in Attendence:
                row = 'A' + str(row_num)
                data = [U'' + str(name)]
                worksheet.write_row(row, data)
                row_num += 1
            # esc键退出
            workbook.close()
            print("考勤结束...")
            break
