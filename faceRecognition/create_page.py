# Import OpenCV2 for image processing
import cv2
import os
from tkinter import *
from tkinter import messagebox
from mydb import Sql_operation
import cv2
import dlib
import numpy as np

if __name__ == "__main__":
    # 创建一个TK实例，用来存放控件
    root = Tk()

    # 设置TK的背景
    root.configure(background="white")

    # 设置TK的位置--x坐标670、y坐标165
    root.geometry("+724+255")
    def single():
        os.system("python create_dataset_gui.py")
    def double():
        os.system("python create_dataset_gui_1.py")
    def destroy_win():
        root.destroy()


    # 窗口标题
    root.title("特征向量制作界面")

    # 创建增单张人脸
    Button(root, text="仅使用FaceNet", font=("times new roman", 20), bg="#0D47A1", fg='white', command=single).grid(row=1, columnspan=2, sticky=W + E + N + S, padx=10, pady=10)

    # 创建整个班级
    Button(root, text="结合DLib算法", font=("times new roman", 20), bg="#0D47A1", fg='white', command=double).grid(row=2, columnspan=2, sticky=N + E + W + S, padx=10, pady=10)

    # 创建退出button
    Button(root, text="退出制作界面", font=('times new roman', 20), bg="maroon", fg="white", command=destroy_win).grid(row=9,columnspan=2,sticky=N + E + W + S, padx=10, pady=10)

    root.mainloop()