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
ID_EVENT_REFRESH = 9999
class MyfirstFram(wx.Frame,):
    def __init__(self, superior):
        '''
        初始化需要的参数
        :param superior: 布局方式
        '''
        # 连接login_users数据库
        self.op = Sql_operation("py-database")
        self._ClassName = self.op.FindFirst('tb_name')[0][0]
        self.model_path = 'models/20190604-135111'
        # self.model_path = 'models/20180408-102900'
        self.face_net = face_recognition.facenetEmbedding(self.model_path)
        self.emb_face_dir = './dataset/emb_face/' + self._ClassName
        self.out_emb_path = 'dataset/emb/' + self._ClassName + '/faceEmbedding.npy'
        self.out_filename = 'dataset/emb/' + self._ClassName + '/name.txt'
        self.resize_width = 160
        self.resize_height = 160
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
        self.Bind(wx.EVT_MENU, self.create_embedding, menuCreate)
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

    def loadmodel(self, dataset_path, filename):
        '''
        加载所需要的模型
        :param dataset_path: .npy文件，包含的是人脸的向量
        :param filename:.txt文件，包含人的名字
        :return:
        '''
        # 加载数据库的数据
        self.dataset_emb = np.load(dataset_path)
        self.names_list = file_processing.read_data(filename)
        # 初始化mtcnn人脸检测
        self.face_detect = face_recognition.Facedetection()  # 1.06
        # 初始化facenet
        self.face_net = face_recognition.facenetEmbedding(self.model_path)  # 7.81

    def create_face(self):
        '''
        生成人脸数据图库，保存在out_face_dir中，这些数据库将用于生成embedding数据库
        :return:
        '''
        self.image_list, self.ids_list = file_processing.gen_files_labels(self.images_dir, postfix='jpg')
        if self.ids_list == []:
            return

        face_detect = face_recognition.Facedetection()
        # 创建不存在的文件夹
        for image_path, name in zip(self.image_list, self.ids_list):
            out_path = os.path.join(self.out_face_dir, name)
            if not os.path.exists(out_path):
                os.makedirs(out_path)

        # 每次只处理不存在的图片
        for image_path, name in zip(self.image_list, self.ids_list):
            out_path = os.path.join(self.out_face_dir, name)
            basename = os.path.basename(image_path)
            out_path = os.path.join(out_path, basename)
            if not os.path.exists(out_path):
                image = image_processing.read_image(image_path, resize_height=0, resize_width=0, normalization=False)
                # 获取 判断标识 bounding_box crop_image
                bounding_box, points = face_detect.detect_face(image)
                bounding_box = bounding_box[:, 0:4].astype(int)
                bounding_box = bounding_box[0, :]
                face_image = image_processing.crop_image(image, bounding_box)
                try:
                    face_image = image_processing.resize_image(face_image, self.resize_height, self.resize_width)
                    image_processing.save_image(out_path, face_image)
                except:
                    pass
    def create_embedding(self, event):
        # 定义图像地址
        self.images_dir = 'dataset/images/' + self._ClassName
        self.out_face_dir = 'dataset/emb_face/' + self._ClassName
        # 裁剪图像
        self.create_face()
        if self.ids_list == []:
            self.list.ClearAll()
            self.list.InsertColumn(0, "警告：")
            self.list.SetColumnWidth(0, 500)
            self.list.InsertItem(0, "当前不存在" + self._ClassName + "的数据集,请选择增加人脸集")
            return
        # 完成数据的加载
        self.emb_face_dir = './dataset/emb_face/' + self._ClassName
        if not os.path.exists('dataset/emb/' + self._ClassName):
            os.makedirs('dataset/emb/' + self._ClassName)
        self.out_emb_path = 'dataset/emb/' + self._ClassName + '/faceEmbedding.npy'
        self.out_filename = 'dataset/emb/' + self._ClassName + '/name.txt'

        id_set = list(set(self.ids_list))
        print(self.image_list)
        images = image_processing.get_images(self.image_list, self.resize_height, self.resize_width, whiten=True)
        compare_emb = self.face_net.get_embedding(images)
        np.save(self.out_emb_path, compare_emb)

        file_processing.write_data(self.out_filename, self.ids_list, model='w')
        # 显示处理完成
        self.list.ClearAll()
        print(self._ClassName + "数据集制作完成")
        self.createHeader2showname()
        pos = 0
        length = len(id_set)

        for i in range (length):
            student_name = self.op.FindSNAME('tb_student', id_set[i])[0][0]
            pos = self.list.InsertItem(pos + 1, id_set[i])
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