from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from mydb import Sql_operation
import wx

import cv2
import xlsxwriter
import tensorflow as tf
import numpy as np
import os
import time
import face_recognition
from utils import file_processing,image_processing
import cv2
import os
import dlib
from skimage import io
import csv
import numpy as np
ID_EVENT_REFRESH = 9999
class MyfirstFram(wx.Frame,):
    def __init__(self, superior):
        '''
        初始化需要的参数
        :param superior: 布局方式
        '''
        # Dlib 正向人脸检测器
        self.detector = dlib.get_frontal_face_detector()
        # Dlib 人脸预测器
        self.predictor = dlib.shape_predictor("data/data_dlib/shape_predictor_5_face_landmarks.dat")
        # Dlib 人脸识别模型
        self.face_rec = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")
        # 连接login_users数据库
        self.op = Sql_operation("py-database")
        self._ClassName = self.op.FindFirst('tb_name')[0][0]
        self.emb_face_dir = './dataset/emb_face/' + self._ClassName
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
        wx.Frame.__init__(self, parent=superior, title="制作数据集界面", pos=
        (200, 100), size=(500, 300))
        self.CreateStatusBar()
        # 定义一个菜单栏
        menuBar = wx.MenuBar()
        filemenu = wx.Menu()
        menuBar.Append(filemenu, "&菜单")
        # 菜单栏中的选项
        menuCreate = filemenu.Append(0, "&开始制作", "制作选定的班级的人脸向量")
        self.Bind(wx.EVT_MENU, self.write_csv, menuCreate)
        myhelps = filemenu.Append(1, "&帮助", "获得帮助")
        self.Bind(wx.EVT_MENU, self.helps, myhelps)
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
    def createHeader2showname(self):
        '''
        菜单项
        :return:
        '''
        self.list.InsertColumn(0,'已添加的学号')
        self.list.SetColumnWidth(0, 225)
        self.list.InsertColumn(1, "已添加的姓名")
        self.list.SetColumnWidth(1, 225)

    def OnQuit(self, event):
        '''
        退出程序
        :return:
        '''
        self.Close()
        self.Destroy()
    def helps(self, event):
        '''
        获得帮助
        :return:
        '''
        self.list.ClearAll()
        self.createHeader2help()
        ANniu = ['开始制作','帮助','退出']
        text1 = '根据前面所选的专业班级，制作对应的人脸向量集合'
        text2 = '获取帮助信息'
        text3 = '退出该程序'
        text = [text1,text2,text3]
        pos = 0
        for i in range(3):
            pos = self.list.InsertItem(pos + 1, ANniu[i])
            self.list.SetItem(pos, 1, text[i])
            if pos % 2 == 0:
                # Set new look and feel for odd lines
                self.list.SetItemBackgroundColour(pos, (134, 225, 249))

    # 返回单张图像的 128D 特征
    def return_128d_features(self, path_img):
        img_rd = io.imread(path_img)
        img_gray = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
        faces = self.detector(img_gray, 1)

        print("%-40s %-20s" % ("检测到人脸的图像 / image with faces detected:", path_img), '\n')

        # 因为有可能截下来的人脸再去检测，检测不出来人脸了
        # 所以要确保是 检测到人脸的人脸图像 拿去算特征
        if len(faces) != 0:
            shape = self.predictor(img_gray, faces[0])
            face_descriptor = self.face_rec.compute_face_descriptor(img_gray, shape)
        else:
            face_descriptor = 0
            print("no face")

        return face_descriptor

    # 将文件夹中照片特征提取出来, 写入 CSV
    def return_features_mean_personX(self, path_faces_personX):
        features_list_personX = []
        photos_list = os.listdir(path_faces_personX)
        if photos_list:
            for i in range(len(photos_list)):
                # 调用return_128d_features()得到128d特征
                print("%-40s %-20s" % ("正在读的人脸图像 / image to read:", path_faces_personX + "/" + photos_list[i]))
                features_128d = self.return_128d_features(path_faces_personX + "/" + photos_list[i])
                #  print(features_128d)
                # 遇到没有检测出人脸的图片跳过
                if features_128d == 0:
                    i += 1
                else:
                    features_list_personX.append(features_128d)
        else:
            print("文件夹内图像文件为空 / Warning: No images in " + path_faces_personX + '/', '\n')

        # 计算 128D 特征的均值
        # personX 的 N 张图像 x 128D -> 1 x 128D
        if features_list_personX:
            features_mean_personX = np.array(features_list_personX).mean(axis=0)
        else:
            features_mean_personX = '0'

        return features_mean_personX

    def write_csv(self, event):
        # 定义图像地址
        self.images_dir = 'dataset/images/' + self._ClassName
        if not os.path.exists(self.images_dir):
            self.list.ClearAll()
            self.list.InsertColumn(0, "警告：")
            self.list.SetColumnWidth(0, 500)
            self.list.InsertItem(0, "当前不存在" + self._ClassName + "的数据集,请选择增加人脸集")
            return
        # 完成数据的加载
        if not os.path.exists('dataset/emb/' + self._ClassName):
            os.makedirs('dataset/emb/' + self._ClassName)
        self.out_features_path = 'dataset/emb/' + self._ClassName + '/features_all.csv'

        self.person_list = os.listdir(self.images_dir)
        self.person_list.sort()

        with open(self.out_features_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for person_file in self.person_list:
                # Get the mean/average features of face/personX, it will be a list with a length of 128D
                print(self.images_dir + "/" + str(person_file))
                features_mean_personX = self.return_features_mean_personX(
                    self.images_dir + "/" + str(person_file))
                writer.writerow(features_mean_personX)
                print("特征均值 / The mean of features:", list(features_mean_personX))
                print("长度均值 / The length of mean:", len(features_mean_personX))
                print('\n')
            print("所有录入人脸数据存入 / Save all the features of faces registered into: data/features_all.csv")
        id_set = list(set(self.person_list))
        id_set.sort()

        # 显示处理完成
        self.list.ClearAll()
        print(self._ClassName + "数据集制作完成")
        self.createHeader2showname()
        pos = 0

        for id in id_set:
            student_name = self.op.FindSNAME('tb_student', id)[0][0]
            pos = self.list.InsertItem(pos + 1, id)
            print(student_name)
            self.list.SetItem(pos, 1, student_name)
            if pos % 2 == 0:
                # Set new look and feel for odd lines
                self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            # pos += 1

if __name__ == '__main__':
    app = wx.App()
    frame = MyfirstFram(None)
    frame.Show(True)
    app.MainLoop()