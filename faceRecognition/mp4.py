# coding:utf-8
import cv2
video = "video/three.mp4"  # 此处@后的ipv4 地址需要修改为自己的地址
video_capture = cv2.VideoCapture(video)

# video_capture(propId, value)
# 设置视频参数，propId 设置的视频参数，value 设置的参数值
video_capture.set(3, 480)

while video_capture.isOpened():
    ret, image = video_capture.read()
    try:
        print(image.shape)
        cv2.imshow("window", image)
        cv2.waitKey(10)
    except:
        break

