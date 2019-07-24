# Import OpenCV2 for image processing
import cv2
import os
from tkinter import *
from tkinter import messagebox
from mydb import Sql_operation
import cv2
import dlib
import time
import numpy as np

if __name__ == "__main__":
    # 创建TK实例
    root = Tk()
    # 设置输入的ID
    root.title("Input ID")
    # 设置当前位置、大小--大小300x100 位置x=660 y=260
    root.geometry('300x100+677+260')

    ID = Label(root, text="Please input your id number：")
    ID.pack()
    faceid_text = StringVar()
    ID = Entry(root, textvariable=faceid_text)
    faceid_text.set("")
    ID.pack()

    face_id = ''


    def on_click():
        id = faceid_text.get()
        string = str("Your Face_ID：%s " % (id))
        messagebox.showinfo(title='Successful', message=string)
        global face_id
        face_id = str(faceid_text.get())
        root.destroy()


    Button(root, text="OK", command=on_click).pack()
    root.mainloop()
    class_name = ""
    if (face_id != ''):
        sql_op = Sql_operation("py-database")
        try:
            class_name = sql_op.FindCNAME('tb_student', str(face_id))[0][0]
        except Exception as err:
            messagebox.showwarning('错误', '查无此人')
    if class_name != "":
        image_path = "./dataset/images/" + class_name + "/" + str(face_id)
        print(image_path)
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        vid_cam = cv2.VideoCapture(0)
        # 设置视频参数 set camera
        vid_cam.set(3, 480)
        count = 0
        # Dlib 正向人脸检测器 / frontal face detector
        detector = dlib.get_frontal_face_detector()
        while vid_cam.isOpened():
            _, show_image = vid_cam.read()
            # show_image = cv2.imread('dataset/test_images/major.jpg')
            image_frame = show_image
            key = cv2.waitKey(1)
            gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
            # 人脸数 faces
            faces = detector(gray, 0)

            # 待会要写的字体 / font to write
            font = cv2.FONT_HERSHEY_COMPLEX

            if len(faces) != 0:
                # 矩形框
                for k, d in enumerate(faces):
                    # 计算矩阵大小
                    pos_start = tuple([d.left(), d.top()])  # 左上角
                    pos_end = tuple([d.right(), d.bottom()])  # 右下角

                    # 计算矩形框大小
                    height = d.bottom() - d.top()
                    width = d.right() - d.left()

                    half_h = int(height / 2)
                    half_w = int(width / 2)

                    # 设置矩形框的颜色
                    color_rectangle = (255, 255, 255)

                    # 判断人脸矩形框是否超出 480x640
                    if d.right() + half_w > 640 or d.bottom() + half_h > 480 or d.left() - half_w < 0 or d.top() - half_h < 0:
                        cv2.putText(show_image, "OUT OF RANGE", (20, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                        color_rectangle = (0, 0, 255)
                        if key == ord('s'):
                            print("请调整位置 / Please adjust your position")
                    else:
                        color_rectangle = (255, 255, 255)
                    cv2.rectangle(show_image,
                                  tuple([d.left() - half_w, d.top() - half_h]),
                                  tuple([d.right() + half_w, d.bottom() + half_h]),
                                  color_rectangle, 2)
                if key == ord('s') or cv2.waitKey(1) & 0xFF == ord('s'):
                    count += 1
                    cv2.imencode('.jpg', image_frame)[1].tofile(
                        "./dataset/images/" + class_name + "/" + str(face_id) + "/" + str(
                            face_id) + '_' + str(
                            count) + ".jpg")
                    print("./dataset/images/" + class_name + "/" + str(face_id) + "/" + str(
                        face_id) + '_' + str(count) + ".jpg")


            # 显示人脸数 / show the numbers of faces detected
            cv2.putText(show_image, "Faces: " + str(len(faces)), (20, 100), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

            # 添加说明 / add some statements
            cv2.putText(show_image, "Face Register", (20, 40), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
            if count < 2:
                cv2.putText(show_image, "Please show your frontal face", (20, 350), font, 0.8, (255, 0, 0), 1,
                            cv2.LINE_AA)
            elif count < 4:
                cv2.putText(show_image, "Please show your left face", (20, 350), font, 0.8, (255, 0, 0), 1,
                            cv2.LINE_AA)
            elif count < 6:
                cv2.putText(show_image, "Please show your right face", (20, 350), font, 0.8, (255, 0, 0), 1,
                            cv2.LINE_AA)
            elif count < 8:
                cv2.putText(show_image, "Please bow your head slightly", (20, 350), font, 0.8, (255, 0, 0), 1,
                            cv2.LINE_AA)
            else:
                cv2.putText(show_image, "Please step back", (20, 350), font, 0.8, (255, 0, 0), 1,
                            cv2.LINE_AA)
            cv2.putText(show_image, "S: Save current face", (20, 400), font, 0.8, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(show_image, "Q: Quit", (20, 450), font, 0.8, (255, 0, 0), 1, cv2.LINE_AA)


            cv2.imshow("camera", show_image)

            if key == ord('q') or cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif count >= 10:
                print("Successfully Captured")
                break

        # 释放资源
        vid_cam.release()
        # 关掉窗口
        cv2.destroyAllWindows()