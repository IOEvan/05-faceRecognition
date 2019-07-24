from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from mydb import Sql_operation
import wx
import cv2
import xlsxwriter
import numpy as np
import os
import time
import face_recognition
from utils import file_processing,image_processing
import dlib          # 人脸处理的库 Dlib
import numpy as np   # 数据处理的库 numpy
import cv2           # 图像处理的库 OpenCv
import pandas as pd  # 数据处理的库 Pandas
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
        self.model_path = 'models/20190520-143248'
        # self.model_path = 'models/20180408-102900'
        self.resize_width = 160
        self.resize_height = 160
        self.panel(superior)
        # 初始化mtcnn人脸检测
        self.face_detect = face_recognition.Facedetection()  # 1.06
        # 初始化facenet
        # self.face_net = face_recognition.facenetEmbedding(self.model_path)  # 7.81
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')
        # 人脸识别模型，提取128D的特征矢量
        self.facerec = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")
    def panel(self, superior):
        '''
        初始化面板的布局
        :param superior:
        :return:
        '''
        dict1 = self.op.School_Major('tb_NAME')
        dict2 = self.op.Major_Class('tb_NAME')
        #print(dict1)
        wx.Frame.__init__(self, parent=superior, title="考勤界面", pos=
        (200, 100), size=(1000, 600))
        self.CreateStatusBar()
        # 定义一个菜单栏
        menuBar = wx.MenuBar()
        filemenu = wx.Menu()
        filemenu1 = wx.Menu()
        menuBar.Append(filemenu, "&菜单")
        menuBar.Append(filemenu1, "&菜单1")
        # 菜单栏中的选项
        menuAttendance = filemenu.Append(0, "&开始考勤", "对于选定的班级进行考勤")
        self.Bind(wx.EVT_MENU, self.attendance, menuAttendance)
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
        majorComboBox = wx.ComboBox(panel, -1, value=dict1[list(dict1.keys())[0]][0],choices=dict1[list(dict1.keys())[0]], style=wx.CB_READONLY)
        value1 = dict1[list(dict1.keys())[0]][0]
        classLable = wx.StaticText(panel, -1, "班级:")
        classComboBox = wx.ComboBox(panel, -1, value=dict2[value1][0],choices=dict2[value1], style=wx.CB_READONLY)
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
        self.list.InsertColumn(0, "开始说明")
        self.list.SetColumnWidth(0, 500)
        self.list.InsertItem(0,"您可以从菜单开始考勤使用")

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

        if wx.NOT_FOUND == currentSchoolIndex1 :
            return
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

        if wx.NOT_FOUND == currentMajorIndex:
            return
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
    def helps(self, event):
        '''
        获得帮助
        :return:
        '''
        self.list.ClearAll()
        self.createHeader2help()
        ANniu = ['开始考勤','帮助','退出']
        text1 = '根据前面所选的专业班级，进行考勤'
        text2 = '获取帮助信息'
        text3 = '退出该程序'
        text = [text1,text2,text3]
        pos = 0
        for i in range(3):
            pos = self.list.InsertItem(pos + 1, ANniu[i])
            print(type(text[i]))
            self.list.SetItem(pos, 1, text[i])
            if pos % 2 == 0:
                # Set new look and feel for odd lines
                self.list.SetItemBackgroundColour(pos, (134, 225, 249))

    def loadface(self, dataset_path, filename):
        '''
        加载所需要的模型
        :param dataset_path: .npy文件，包含的是人脸的向量
        :param filename:.txt文件，包含人的名字
        :return:
        '''
        # 加载数据库的数据
        self.dataset_emb = np.load(dataset_path)
        self.names_list = file_processing.read_data(filename)

    # 计算两个128D向量间的欧式距离
    def return_euclidean_distance(self, feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        return dist

    def compare_embadding(self, pred_emb):
        '''

        :param pred_emb:
        :return:
        '''
        # 为bounding_box 匹配标签
        pred_num = len(pred_emb)
        dataset_num = len(self.dataset_emb)
        pred_name = {}
        for i in range(pred_num):
            dist_list = []
            for j in range(dataset_num):
                dist = np.sqrt(np.sum(np.square(np.subtract(pred_emb[i, :], self.dataset_emb[j, :]))))
                dist_list.append(dist)
            min_value = min(dist_list)
            if (min_value > 0.95):
                print(min_value)
                pred_name['unknow'] = 'unknow'

            else:
                pred_id = self.names_list[dist_list.index(min_value)]
                pred_chinese = self.op.FindSNAME('tb_student', pred_id)
                pred_name[pred_id] = pred_chinese[0][0]
        return pred_name
    '''

    def attendance(self, event):
        # 这里可以选择哪个班级的向量进行对比
        self.dataset_path = 'dataset/emb/' + self._ClassName + '/faceEmbedding.npy'
        self.filename = 'dataset/emb/' + self._ClassName + '/name.txt'
        path_features_known_csv = 'dataset/emb/' + self._ClassName + "/features_all.csv"
        print(path_features_known_csv)
        if not os.path.exists(path_features_known_csv):
            self.list.ClearAll()
            self.list.InsertColumn(0, "警告：")
            self.list.SetColumnWidth(0, 500)
            self.list.InsertItem(0, "当前不存在" + self._ClassName + "的数据集,请选择制作数据集")
            return
        csv_rd = pd.read_csv(path_features_known_csv, header=None)

        # 用来存放所有录入人脸特征的数组
        features_known_arr = []

        # 读取已知人脸数据
        for i in range(csv_rd.shape[0]):
            features_someone_arr = []
            for j in range(0, len(csv_rd.ix[i, :])):
                features_someone_arr.append(csv_rd.ix[i, :][j])
            features_known_arr.append(features_someone_arr)
        print("Faces in Database：", len(features_known_arr))

        # 完成模型的加载
        if os.path.exists(self.dataset_path):
            self.loadface(self.dataset_path, self.filename)
        else:
            self.list.ClearAll()
            self.list.InsertColumn(0, "警告：")
            self.list.SetColumnWidth(0, 500)
            self.list.InsertItem(0, "当前不存在" + self._ClassName + "的数据集,请选择制作数据集")
            return

        # 开始识别
        # 调用电脑的摄像头
        video_capture = cv2.VideoCapture(0)
        # video_capture = cv2.VideoCapture(1)
        # 开启ip摄像头
        # video = "http://10.22.70.36:1998/video"  # 此处@后的ipv4 地址需要修改为自己的地址

        # video_capture(propId, value)
        # 设置视频参数，propId 设置的视频参数，value 设置的参数值
        video_capture.set(3, 480)

        Attendence = {}
        while video_capture.isOpened():
            key = cv2.waitKey(1)
            if key == 27 or cv2.waitKey(1) == 27:
                cv2.destroyWindow("face_recognition")
                # 用来制作考勤表
                dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                sheet_path = "./Attendence/" + dt

                if not os.path.exists(sheet_path):
                    os.makedirs(sheet_path)
                workbook = xlsxwriter.Workbook(sheet_path + '/data.xlsx')  # 创建一个Excel文件
                worksheet = workbook.add_worksheet()  # 创建一个sheet
                title = [U'ID']  # 表格title
                worksheet.write_row('A1', title)  # title 写入Excel
                title = [U'姓名']  # 表格title
                worksheet.write_row('B1', title)  # title 写入Excel

                row_num = 2
                if "unknow" in Attendence:
                    Attendence.pop("unknow") #这个地方造成名称不对应
                Attendence_list = sorted(Attendence.keys())
                for ID in Attendence_list:
                    print(ID)
                    print(Attendence[ID])
                    row = 'A' + str(row_num)
                    data = [U'' + ID, U'' + Attendence[ID]]
                    worksheet.write_row(row, data)
                    row_num += 1
                # esc键退出
                workbook.close()
                print("考勤结束...")
                break
            ret, image = video_capture.read()
            bounding_box, points = self.face_detect.detect_face(image)


            if (len(bounding_box) != 0):
                bounding_box = bounding_box[:, 0:4].astype(int)
                # 获得人脸区域 --消耗时间0.0
                face_images = image_processing.get_crop_images(image, bounding_box, self.resize_height, self.resize_width,whiten=True)
                # 消耗时间1.0965726375579834
                pred_emb = self.face_net.get_embedding(face_images)

                pred_name = self.compare_embadding(pred_emb)
                Attendence.update(pred_name)
                # 在图像上绘制人脸边框和识别的结果 消耗时间0.0624847412109375
                print(pred_name.values())
                image_processing.cv_show_image_text("face_recognition", image, bounding_box, pred_name.values())
            else:
                image_processing.cv_show_image_text("face_recognition", image, [], [])
    '''
    def get_name(self):
        pass

    def attendance(self, event):
        # 这里可以选择哪个班级的向量进行对比
        path_features_known_csv = "dataset/features_all.csv"
        self.images_dir = 'dataset/images/' + self._ClassName
        if not os.path.exists(path_features_known_csv):
            self.list.ClearAll()
            self.list.InsertColumn(0, "警告：")
            self.list.SetColumnWidth(0, 500)
            self.list.InsertItem(0, "当前不存在" + self._ClassName + "的数据集,请选择制作数据集")
            return
        csv_rd = pd.read_csv(path_features_known_csv, header=None)

        # 用来存放所有录入人脸特征的数组
        features_known_arr = []

        # 读取已知人脸数据
        for i in range(csv_rd.shape[0]):
            features_someone_arr = []
            for j in range(0, len(csv_rd.ix[i, :])):
                features_someone_arr.append(csv_rd.ix[i, :][j])
            features_known_arr.append(features_someone_arr)
        print("Faces in Database：", len(features_known_arr))

        # 开始识别
        # 调用电脑的摄像头
        # video_capture = cv2.VideoCapture(0)
        video_capture = cv2.VideoCapture('video/8.mp4')
        # 开启ip摄像头
        # video = "http://10.22.70.36:1998/video"  # 此处@后的ipv4 地址需要修改为自己的地址

        # video_capture(propId, value)
        # 设置视频参数，propId 设置的视频参数，value 设置的参数值
        video_capture.set(3, 480)
        video = 'res.avi'
        fps = 4
        img_size = (1280, 720)
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')  # opencv3.0
        videoWriter = cv2.VideoWriter(video, fourcc, fps, img_size)

        Attendence = []
        while video_capture.isOpened():
            # key = cv2.waitKey(1)
            # if key == 27 or cv2.waitKey(1) == 27:
            try:
                ret, image = video_capture.read()
                print(image.shape)
            except:
                videoWriter.release()
                cv2.destroyWindow("face_recognition")
                # 用来制作考勤表
                dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                sheet_path = "./Attendence/" + dt

                if not os.path.exists(sheet_path):
                    os.makedirs(sheet_path)
                workbook = xlsxwriter.Workbook(sheet_path + '/data.xlsx')  # 创建一个Excel文件
                worksheet = workbook.add_worksheet()  # 创建一个sheet
                title = [U'ID']  # 表格title
                worksheet.write_row('A1', title)  # title 写入Excel
                title = [U'姓名']  # 表格title
                worksheet.write_row('B1', title)  # title 写入Excel

                row_num = 2
                Attendence.sort()
                for ID in Attendence:
                    print(type(ID))
                    print(self.op.FindSNAME('tb_student', ID))
                    row = 'A' + str(row_num)
                    data = [U'' + ID, U'' + self.op.FindSNAME('tb_student', ID)[0][0]]
                    worksheet.write_row(row, data)
                    row_num += 1
                # esc键退出
                workbook.close()
                print("考勤结束...")
                break
            # ret, image = video_capture.read()
            bounding_box, points = self.face_detect.detect_face(image)

            time1 = time.time()
            if (len(bounding_box) != 0):
                bounding_box = bounding_box[:, 0:4].astype(int)
                print(bounding_box)
                # 获得人脸区域 --消耗时间0.0

                face_images = image_processing.get_crop_images(image, bounding_box, self.resize_height, self.resize_width,
                                                               whiten=False)
                features_cap_arr = []
                point = dlib.rectangle(int(0), int(0), int(159), int(159))
                for face in face_images:
                    shape = self.predictor(face, point)
                    features_cap_arr.append(self.facerec.compute_face_descriptor(face, shape))


                self.person_list = os.listdir(self.images_dir)
                self.person_list.sort()
                pred_names = []
                for k in range(len(features_cap_arr)):
                    e_distance_list = []
                    for i in range(len(features_known_arr)):
                        # 如果 person_X 数据不为空
                        if str(features_known_arr[i][0]) != '0.0':
                            # print(str(k) + " with person", str(i + 1), "the e distance: ", end='')
                            e_distance_tmp = self.return_euclidean_distance(features_cap_arr[k], features_known_arr[i])
                            # print(e_distance_tmp)
                            e_distance_list.append(e_distance_tmp)
                        else:
                            # 空数据 person_X
                            e_distance_list.append(999999999)
                    similar_person_num = e_distance_list.index(min(e_distance_list))
                    print(str(k) + ' = ' + str(similar_person_num))
                    Attendence.append(self.person_list[similar_person_num])

                    pred_name = self.op.FindSNAME('tb_student', self.person_list[similar_person_num])[0][0]
                    pred_names.append(pred_name)

                    print("Minimum e distance with person", pred_name, min(e_distance_list))
                Attendence = list(set(Attendence))
                print(Attendence)
                pred_name_tmp = list(set(pred_name))
                if len(pred_name) == len(pred_name_tmp):
                    image_processing.cv_show_image_text(videoWriter, "face_recognition", image, bounding_box, pred_names)
            else:
                image_processing.cv_show_image_text(videoWriter, "face_recognition", image, [], [])
            print('单帧处理时间:',time.time() - time1)
if __name__ == '__main__':
    app = wx.App()
    frame = MyfirstFram(None)
    frame.Show(True)
    app.MainLoop()