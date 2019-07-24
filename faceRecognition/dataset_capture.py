from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from mydb import Sql_operation
import wx
import cv2
from utils import file_processing,image_processing
import face_recognition
import xlsxwriter
from PIL import ImageDraw, ImageFont
from PIL import Image
import numpy as np
import os
from tkinter import *
import tkinter
from tkinter import messagebox
import time

class MyfirstFram(wx.Frame,):
    def __init__(self, superior):
        '''
        初始化需要的参数
        :param superior: 布局方式
        '''
        # 连接login_users数据库
        self.op = Sql_operation("py-database")
        self._ClassName = self.op.FindFirst('tb_name')[0][0]

        self.face_id = ''
        self.panel(superior)
    def panel(self, superior):
        '''
        初始化面板的布局
        :param superior:
        :return:
        '''
        dict1 = self.op.School_Major('tb_NAME')
        dict2 = self.op.Major_Class('tb_NAME')
        #print(dict1)
        wx.Frame.__init__(self, parent=superior, title="选择采集数据集的班级", pos=
        (200, 100), size=(500, 300))
        self.CreateStatusBar()
        # 定义一个菜单栏
        menuBar = wx.MenuBar()
        filemenu = wx.Menu()
        menuBar.Append(filemenu, "&菜单")
        # 菜单栏中的选项
        menuCreate = filemenu.Append(0, "&开始采集", "制作选定的班级的人脸向量")
        self.Bind(wx.EVT_MENU, self.dataset_cap, menuCreate)
        QUit = filemenu.Append(wx.ID_EXIT, "&退出", "")
        self.Bind(wx.EVT_MENU, self.OnQuit, QUit)
        self.SetMenuBar(menuBar)
        panel = wx.Panel(self)
        codeSizer = wx.BoxSizer(wx.HORIZONTAL)

        # 面板中的物体
        schoolLable = wx.StaticText(panel, -1, "学院:")
        schoolComboBox = wx.ComboBox(panel, -1, value=list(dict1.keys())[0], choices=list(dict1.keys()),
                                      style=wx.CB_READONLY)
        majorLable = wx.StaticText(panel, -1, "专业:")
        majorComboBox = wx.ComboBox(panel, -1, value=dict1[list(dict1.keys())[0]][0],
                                   choices=dict1[list(dict1.keys())[0]], style=wx.CB_READONLY)
        value1 = dict1[list(dict1.keys())[0]][0]
        classLable = wx.StaticText(panel, -1, "班级:")
        classComboBox = wx.ComboBox(panel, -1, value=dict2[value1][0],
                                   choices=dict2[value1], style=wx.CB_READONLY)
        codeSizer.AddMany([
            (schoolLable, 0,  wx.ALIGN_RIGHT), (schoolComboBox, 0, wx.SHAPED)

            , (majorLable, 0, wx.ALIGN_RIGHT), (majorComboBox, 0, wx.SHAPED)

            ,(classLable, 0, wx.ALIGN_RIGHT), (classComboBox, 0, wx.SHAPED),

        ])
        #定义一级列表刷新时响应二级列表的刷新事件
        self.__SchoolComboBox = schoolComboBox
        panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected1, schoolComboBox, )
        self.__SecityDict = dict1
        self.__majorComboBox = majorComboBox
        panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected2, majorComboBox, )
        #定义二级列表的刷新事件
        self.__SecityDict1 = dict2
        self._ClassCombobox = classComboBox
        panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected3, classComboBox,)

        self.list = wx.ListCtrl(panel, wx.NewId(), style=wx.LC_REPORT,)
        self.list.InsertColumn(0, "开始说明：")
        self.list.SetColumnWidth(0, 500)
        self.list.InsertItem(0,"您可以从菜单开始使用")

        Mysizers = wx.BoxSizer(wx.VERTICAL)
        Mysizers.Add(codeSizer,0,wx.ALL,5 )

        Mysizers.Add(self.list, -1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(Mysizers)

        self.Center()

    def __OnComboBoxSelected1(self, event):
        '''
        下拉列表的第一级联动方式，选择了学院
        :param event:
        :return:
        '''
        currentSchoolIndex1 = self.__SchoolComboBox.GetSelection()

        if wx.NOT_FOUND == currentSchoolIndex1 :return
        value1 = self.__SchoolComboBox.GetItems()[currentSchoolIndex1]

        majorList = self.__SecityDict[value1]
        self.__majorComboBox.SetItems(majorList)
        self.__majorComboBox.SetValue(majorList[0])
        self.__OnComboBoxSelected2(self)
        self._ClassName = self.op.FindName('tb_NAME', 'SNAME', value1, 'CNAME')[0][0]

    def __OnComboBoxSelected2(self, event):
        '''
        下拉列表的第二级，选择了专业
        :param event:
        :return:
        '''
        currentMajorIndex = self.__majorComboBox.GetSelection()

        if wx.NOT_FOUND == currentMajorIndex: return
        value = self.__majorComboBox.GetItems()[currentMajorIndex]

        classList = self.__SecityDict1[value]

        self._ClassCombobox.SetItems(classList)
        self._ClassCombobox.SetValue(classList[0])
        self._ClassName = self.op.FindName('tb_NAME', 'MNAME', value, 'CNAME')[0][0]
    def __OnComboBoxSelected3(self,event):
        '''
        下拉列表的第三级，选择了班级
        :param event:
        :return:
        '''
        currentClassIndex= self._ClassCombobox.GetSelection()
        value = self._ClassCombobox.GetItems()[currentClassIndex]
        self._ClassName = value
    def createHeader2help(self):
        '''
        菜单项
        :return:
        '''
        self.list.InsertColumn(0,'菜单选项')
        self.list.SetColumnWidth(0, 100)
        self.list.InsertColumn(1, "选项说明")
        self.list.SetColumnWidth(1, 800)

    def OnQuit(self, event):
        '''
        退出程序
        :return:
        '''
        self.Close()
        self.Destroy()
    def dataset_cap(self, event):
        '''
        按照选择的班级的学号顺序采集
        :return:
        '''

        ID_list = self.op.FindC_S("tb_student", self._ClassName)
        print(ID_list)
        if ID_list == ():
            print("here")
            self.list.ClearAll()
            self.list.InsertColumn(0, "警告：")
            self.list.SetColumnWidth(0, 500)
            self.list.InsertItem(0, "当前不存在" + self._ClassName + "的名单,请导入相应名单")
            return
        for id in ID_list:
            self.face_id = id[0]

            # 提示框显示
            if messagebox.askokcancel(title='增加人脸', message= '开始增加' + id[1] + '同学'):
                image_path = "./dataset/images/" + self._ClassName + "/" + str(self.face_id)
                print(image_path)
                if not os.path.exists(image_path):
                    os.makedirs(image_path)

                face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                # vid_cam = cv2.VideoCapture(1)
                vid_cam = cv2.VideoCapture(0)
                count = 0
                while (True):
                    _, image_frame = vid_cam.read()
                    gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
                    faces = face_detector.detectMultiScale(gray, 1.3, 5)

                    for (x, y, w, h) in faces:
                        count += 1
                        cv2.imencode('.jpg', image_frame)[1].tofile(
                            "./dataset/images/" + self._ClassName + "/" + str(self.face_id) + "/" + str(
                                self.face_id) + '_' + str(
                                count) + ".jpg")
                        # 显示人脸位置
                        cv2.rectangle(image_frame, (x, y), (x + w, y + h), (64, 224, 208), 2)
                        print("./dataset/images/" + self._ClassName + "/" + str(self.face_id) + "/" + str(self.face_id) + '_' + str(
                            count) + ".jpg")

                        # cv2.imshow('frame', cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB))
                    cv2.imshow('frame', image_frame)

                    if cv2.waitKey(100) & 0xFF == ord('q'):
                        break
                    elif count >= 10:
                        # 提示框显示
                        messagebox.showinfo(title='增加完毕', message=id[1] + '同学完成采集')
                        print("Successfully Captured")
                        break
                # 释放资源
                vid_cam.release()
                # 关掉窗口
                cv2.destroyAllWindows()




if __name__ == '__main__':
    app = wx.App()
    frame = MyfirstFram(None)
    frame.Show(True)
    app.MainLoop()