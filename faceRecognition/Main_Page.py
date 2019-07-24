from tkinter import *
import os
from tkinter import messagebox
import time


# 创建一个TK实例，用来存放控件
root = Tk()

# 设置TK的背景
root.configure(background="white")

# 设置TK的位置--x坐标670、y坐标165
root.geometry("+670+165")

def face_captrue():
    print("Hello")
    os.system("python dataset_page.py")

def create_dataset():
    os.system("python create_page.py")

def detec_recog():
    os.system("python attendance_page.py")

def view_url():
    os.startfile("https://blog.csdn.net/chao_shine")

def destroy_win():
    root.destroy()
    os.system("python post_mail.py")

def attend():
    dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    sheet_path = str(".\Attendence\\" + str(dt) + "\data.xlsx")
    if not os.path.exists(sheet_path):
        messagebox.showerror("警告！","请先开始考勤！！")
    else:
        os.startfile(sheet_path)
# 窗口标题
root.title("考勤系统")

# 显示当前系统的名称
Label(root, text = "多目标人脸识别考勤系统", font = ("times new roman", 20), fg = "white", bg = "maroon", height = 2).grid(row = 0, rowspan = 2, columnspan = 2, sticky = N + E + W + S, padx = 5, pady = 5)

# 创建增加人脸的button
Button(root, text = "增加人脸数据", font = ("times new roman", 20), bg = "#0D47A1", fg = 'white', command = face_captrue).grid(row = 3, columnspan = 2, sticky = W + E + N + S, padx = 5, pady = 5)

# 创建制作数据集的Button
Button(root, text = "预存人脸向量", font = ("times new roman", 20), bg = "#0D47A1", fg = 'white', command = create_dataset).grid(row = 4, columnspan = 2, sticky = N + E + W + S, padx = 5, pady = 5)

# 创建识别的button
Button(root, text = "开始课堂考勤", font = ('times new roman', 20), bg = "#0D47A1", fg = "white",command = detec_recog).grid(row = 5, columnspan = 2, sticky = N + E + W + S, padx = 5, pady = 5)

# 创建查看考勤的button
Button(root, text = "查看考勤表格", font = ('times new roman', 20), bg = "#0D47A1", fg = "white", command = attend).grid(row = 6, columnspan = 2, sticky = N + E + W + S, padx = 5, pady = 5)

# 创建个人主页button
Button(root, text = "查看开发者主页", font = ('times new roman', 20), bg = "#0D47A1", fg = "white", command = view_url).grid(row = 8,columnspan = 2,sticky = N + E + W + S,padx = 5,pady = 5)

# 创建退出button
Button(root, text = "退出考勤系统", font = ('times new roman', 20), bg = "maroon", fg = "white", command = destroy_win).grid(row = 9,columnspan = 2,sticky = N + E + W + S,padx = 5, pady = 5)

root.mainloop()
