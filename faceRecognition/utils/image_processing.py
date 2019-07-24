# -*-coding: utf-8 -*-
"""
    @Project: faceRecognition
    @File   : image_processing.py
"""
import cv2
import matplotlib.pyplot as plt
from PIL import ImageDraw, ImageFont
from PIL import Image
import cv2
import numpy as np
from scipy import misc

###############################################图片显示############################################
def show_image(win_name, rgb_image):
    plt.title(win_name)
    plt.imshow(rgb_image)
    plt.show()
def show_image_rect(win_name, rgb_image, rect):
    '''
    :param win_name:
    :param rgb_image:
    :param rect: x,y,w,h
    :return:
    '''
    plt.figure()
    plt.title(win_name)
    plt.imshow(rgb_image)
    rect =plt.Rectangle((rect[0], rect[1]), rect[2], rect[3], linewidth=2, edgecolor='r', facecolor='none')
    plt.gca().add_patch(rect)
    plt.show()

def show_image_boxes(win_name, rgb_image, boxes):
    '''
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)画矩行
    :param rgb_image:
    :param bounding_boxes:[[x1,y1,x2,y2]]
    :return:
    '''
    plt.title(win_name)
    for box in boxes:
        # box = box.astype(int)
        cv2.rectangle(rgb_image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
    plt.imshow(rgb_image)
    plt.show()

def show_image_box(win_name, rgb_image, box):
    '''
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)画矩行
    :param rgb_image:
    :param bounding_boxes:[[x1,y1,x2,y2]]
    :return:
    '''
    plt.title(win_name)
    # box = box.astype(int)
    cv2.rectangle(rgb_image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
    plt.imshow(rgb_image)
    plt.show()

def cv_show_image_text(videoWriter, win_name, image, boxes, boxes_name):
    if len(boxes) != 0:
        for name, box in zip(boxes_name,boxes):
            cv2.rectangle(image, (box[0],box[1]),(box[2],box[3]), (255, 255, 255), 2, 8, 0)

            # cv2img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同
            pilimg = Image.fromarray(image)

            # PIL图片上打印汉字
            draw = ImageDraw.Draw(pilimg)  # 图片上打印
            font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
            draw.text((box[0], box[1]), name, (255, 0, 0), font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体

            # PIL图片转cv2 图片
            # cv2charimg = np.array(pilimg)
            image = np.array(pilimg)

        # cv2.putText(cv2charimg, "Press 'Esc': Quit", (20, 450), cv2.FONT_HERSHEY_COMPLEX, 0.8, (84, 255, 159), 1, cv2.LINE_AA)
        cv2.imshow(win_name, image)
        videoWriter.write(image)
        # save_image('ans.jpg', cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    else:
        cv2.putText(image, "Press 'Esc': Quit", (20, 450), cv2.FONT_HERSHEY_COMPLEX, 0.8, (84, 255, 159), 1, cv2.LINE_AA)
        cv2.imshow(win_name, image)
        videoWriter.write(image)
    cv2.waitKey(30)



###############################################图片读取和保存############################################
def read_image(image_path, resize_height=0, resize_width=0, normalization=False):
    '''
    读取图片数据,默认返回的是uint8,[0,255]
    :param image_path:
    :param resize_height:
    :param resize_width:
    :param normalization:是否归一化到[0.,1.0]
    :return: 返回的图片数据
    '''

    # bgr_image = cv2.imread(image_path)
    # 读取中文路径
    bgr_image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
    if len(bgr_image.shape) == 2:  # 若是灰度图则转为三通道
        print("Warning:gray image", image_path)
        bgr_image = cv2.cvtColor(bgr_image, cv2.COLOR_GRAY2BGR)

    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)  # 将BGR转为RGB
    # show_image(filename,rgb_image)
    # rgb_image=Image.open(filename)
    if resize_height > 0 and resize_width > 0:
        rgb_image = cv2.resize(rgb_image, (resize_width, resize_height))
    rgb_image = np.asanyarray(rgb_image)
    if normalization:
        # 不能写成:rgb_image=rgb_image/255
        rgb_image = rgb_image / 255.0
    # show_image("src resize image",image)
    return rgb_image

def save_image(image_path, rgb_image):
    plt.imsave(image_path, rgb_image)

###############################################图片裁剪############################################
def crop_image(image, box):
    '''
    :param image: rgb image
    :param box: [x1,y1,x2,y2]
    :return:
    '''
    crop_img= image[box[1]:box[3], box[0]:box[2]]
    return crop_img

def crop_img1(image, box):
    det = np.squeeze(box[0:4])
    bb = np.zeros(4, dtype=np.int32)
    bb[0] = np.maximum(det[0] - 22 / 2, 0)
    bb[1] = np.maximum(det[1] - 22 / 2, 0)
    bb[2] = np.minimum(det[2] + 22 / 2, 480)
    bb[3] = np.minimum(det[3] + 22 / 2, 640)

    crop_img = image[bb[1]:bb[3], bb[0]:bb[2]]
    return crop_img




def crop_images(image, boxes, resize_height=0, resize_width=0):
    '''
    :param image: rgb image
    :param boxes:  [[x1,y1,x2,y2],[x1,y1,x2,y2]]
    :param resize_height:
    :param resize_width:
    :return:
    '''
    crops=[]
    for box in boxes:
        crop_img=crop_image(image, box)
        if resize_height > 0 and resize_width > 0:
            # crop_img = cv2.resize(crop_img, (resize_width, resize_height))
            crop_img = misc.imresize(crop_img, (resize_width, resize_height), interp='bilinear')
        crops.append(crop_img)
    crops=np.stack(crops)
    return crops

def get_crop_images(image, boxes, resize_height=0, resize_width=0, whiten=False):
    '''

    :param image: rgb image
    :param boxes:[[x1,y1,x2,y2],[x1,y1,x2,y2]]
    :param resize_height:
    :param resize_width:
    :param whiten:
    :return:
    '''
    crops=[]
    for box in boxes:
        # crop_img=crop_img1(image, box)
        crop_img=crop_image(image, box)
        if resize_height > 0 and resize_width > 0:
            try:
                # crop_img = cv2.resize(crop_img, (resize_width, resize_height))
                crop_img = misc.imresize(crop_img, (resize_width, resize_height), interp='bilinear')
            except:
                pass
        if whiten:
            crop_img = prewhiten(crop_img)
        crops.append(crop_img)
    crops=np.stack(crops)
    return crops
###############################################图片操作############################################
def resize_image(image,resize_height,resize_width):
    '''
    :param image: rgb image
    :param resize_height:
    :param resize_width:
    :return:
    '''
    # print(image)
    image = cv2.resize(image, (resize_width, resize_height))
    return image

def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1/std_adj)
    return y

def get_images(image_list,resize_height=0,resize_width=0,whiten=False):
    images = []
    for image_path in image_list:
        # img = misc.imread(os.path.join(images_dir, i), mode='RGB')
        image=read_image(image_path)
        if resize_height > 0 and resize_width > 0:
            image = cv2.resize(image, (resize_width, resize_height))
        if whiten:
            image = prewhiten(image)
        images.append(image)
    images = np.stack(images)
    return images

