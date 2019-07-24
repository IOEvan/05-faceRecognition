from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import cv2
from scipy import misc
import tensorflow as tf
import numpy as np
import os
import time
from utils import file_processing,image_processing
import face_recognition
resize_width = 160
resize_height = 160

def face_recognition_image(model_path,dataset_path, filename,image_path):
    # 加载数据库的数据
    dataset_emb,names_list=load_dataset(dataset_path, filename) #0.0
    # 初始化mtcnn人脸检测
    face_detect=face_recognition.Facedetection() #1.06
    # 初始化facenet
    face_net=face_recognition.facenetEmbedding(model_path) #7.81
    image=image_processing.read_image(image_path) #0.03
    # 进行人脸检测，获得bounding_box --消耗时间0.17183518409729004
    time1 = time.time()
    bounding_box, points = face_detect.detect_face(image)
    print(time.time() - time1)
    bounding_box = bounding_box[:,0:4].astype(int)
    # if min(min(bounding_box)) < 0:
    #     bounding_box.remove(min(bounding_box))
    print(len(bounding_box))
    # 获得人脸区域 --消耗时间0.0
    # face_images = image_processing.get_crop_images(image,bounding_box,resize_height,resize_width,whiten=False)
    # for face in face_images:
    #     face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    #     cv2.imshow("face",face)
    #     cv2.waitKey(3000)
    # image_processing.show_image("face", face_images[0,:,:,:])
    #消耗时间1.0965726375579834
    # pred_emb=face_net.get_embedding(face_images)
    # pred_name=compare_embadding(pred_emb, dataset_emb, names_list)
    # 在图像上绘制人脸边框和识别的结果 消耗时间0.0624847412109375
    bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # image_processing.cv_show_image_text("face_recognition", bgr_image,bounding_box,pred_name)
    image_processing.cv_show_image_text("face_recognition", bgr_image,bounding_box,[' ' for i in range(len(bounding_box))])
    cv2.waitKey(0)
def load_dataset(dataset_path,filename):
    '''
    加载人脸数据库
    :param dataset_path: embedding.npy文件（faceEmbedding.npy）
    :param filename: labels文件路径路径（name.txt）
    :return:
    '''
    compare_emb=np.load(dataset_path)
    names_list=file_processing.read_data(filename)
    return compare_emb,names_list

def compare_embadding(pred_emb, dataset_emb, names_list):
    # 为bounding_box 匹配标签
    pred_num = len(pred_emb)
    dataset_num = len(dataset_emb)
    pred_name = []
    print (pred_num)
    for i in range(pred_num):
        dist_list = []
        for j in range(dataset_num):
            dist = np.sqrt(np.sum(np.square(np.subtract(pred_emb[i, :], dataset_emb[j, :]))))
            dist_list.append(dist)
        min_value = min(dist_list)
        print(min_value)
        if (min_value > 0.95):
            pred_name.append('unknow')
        else:
            pred_name.append(names_list[dist_list.index(min_value)])
    return pred_name

if __name__=='__main__':
    model_path='models/20190520-143248'
    dataset_path='dataset/emb/信息152/faceEmbedding.npy'
    filename='dataset/emb/name.txt'
    image_path='dataset/test_images/1.jpg'
    face_recognition_image(model_path, dataset_path, filename,image_path)