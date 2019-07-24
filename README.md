## 毕设系统代码  

#### 1、功能介绍  
+ 利用现有的CPU资源，使用电脑的摄像头可以实现多目标人脸的识别，识别算法使用了FaceNet和DLib两种方法。由于电脑摄像头的像素限制，识别效果在10个人左右已是计算能力和性能的trade-off点。（这里主要参考了FaceNet论文对应的论文）  
+ 人脸采集部分使用Haar和Dlib两种方式，Haar适用于较多人快速采集人脸，dlib用于修补人脸库；     
+ 根据识别情况，对比数据库（Mysql）构建的表对比，自动生成学号和姓名组成的考勤表；  
+ 为了方便查看，将考勤结果以邮件形式发送给使用者邮箱；   
+ 设计整个系统的界面，可以实现交互；
+ 将整个系统用py2exe打包成一个exe文件，实际就是做了个跳转，演示好看罢了，没啥作用。  

#### 2、系统前提  
+ 使用FaceNeT训练了自己构建的数据集，准确率达到了98%左右。数据集面向亚裔人脸，在LFW上准确率并不高。   
+ 使用已经训练好dlib_face_recognition_resnet_model_v1模型

#### 3、参考链接  
> 由于过于仓促，参考的东西太多，可能会遗漏，如有发现请告知。  
+ [FaceNet项目](https://github.com/davidsandberg/facenet)；  
+ [Dlib_face_recognition_from_camera-master ](https://download.csdn.net/download/weixin_41600500/11012807)：项目代码可以找我免费要；  
+ [tf_facenet](https://github.com/MrZhousf/tf_facenet);  
+ [Face-Recognition-Attendance-System]：这里把地址忘了，有发现相同的请告知；

#### 4、TODO  
+ 待有时间把整个流程说一下；  
+ Facenet训练使用过程；  
+ 数据库说明；
