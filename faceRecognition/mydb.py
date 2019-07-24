# 导入pymysql模块
import pymysql

# 创建数据库操作类
class Sql_operation(object):
    '''
    数据库操作
    '''

    # 用构造函数实现数据库连接，并引入mydb参数，实现调用不同的数据库
    def __init__(self, mydb):
        # 实例变量
        self.mydb = mydb
        # 打开数据库连接
        self.db = pymysql.connect(host="127.0.0.1",port = 3306, user="root", password="12345678", db=self.mydb, charset="utf8")
        # 创建游标对象
        self.cursor = self.db.cursor()

    # 定义查看数据表信息函数，并引入table_field、table_name参数，实现查看不同数据表的建表语句
    def School_Major(self, table_name):

        # 实例变量
        self.table_name = table_name
        # 定义SQL语句
        sql = "select DISTINCT (SNAME) from %s" % (self.table_name)
        dict1 = {}
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 处理结果
            School_list = [School[0] for School in self.cursor.fetchall()]
            for school in School_list:
                select_sql = "select DISTINCT (MNAME) from %s WHERE SNAME = '%s'" % (self.table_name, school)
                self.cursor.execute(select_sql)
                major_list = [major[0] for major in self.cursor.fetchall()]
                dict1[school] = major_list
            return dict1
        except Exception as err:
            print("SQL执行错误，原因：", err)

    def Major_Class(self, table_name):
        # 实例变量
        self.table_name = table_name
        # 定义SQL语句
        sql = "select DISTINCT (MNAME) from %s" % (self.table_name)
        dict1 = {}
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 处理结果
            major_list = [major[0] for major in self.cursor.fetchall()]
            for major in major_list:
                select_sql = "select DISTINCT (CNAME) from %s WHERE MNAME = '%s'" % (self.table_name, major)
                self.cursor.execute(select_sql)
                class_list = [clas[0] for clas in self.cursor.fetchall()]
                dict1[major] = class_list
            return dict1
        except Exception as err:
            print("SQL执行错误，原因：", err)

    def FindName(self, table_name, src_name, src_value, target_name):
        select_sql = "select %s from %s WHERE %s = '%s'" %(target_name, table_name, src_name, src_value)
        try:
            self.cursor.execute(select_sql)
            return self.cursor.fetchall()
        except Exception as err:
            print("SQL执行错误，原因:", err)

    def FindAll(self, table_name, class_name):
        select_sql = "select * from %s WHERE CNAME = '%s'" %(table_name, class_name)
        try:
            self.cursor.execute(select_sql)
            return self.cursor.fetchall()
        except Exception as err:
            print("SQL执行错误，原因:", err)
    def FindCNAME(self, table_name, SID):
        select_sql = "select S_C from %s WHERE SID = '%s'" %(table_name, SID)
        try:
            self.cursor.execute(select_sql)
            return self.cursor.fetchall()
        except Exception as err:
            print("SQL执行错误，原因：", err)
    def FindSNAME(self, table_name, SID):
        select_sql = "select SNAME from %s WHERE SID = '%s'" %(table_name, SID)
        try:
            self.cursor.execute(select_sql)
            return self.cursor.fetchall()
        except Exception as err:
            print("SQL执行错误，原因：", err)
    def FindFirst(self, table_name):
        select_sql = "select CNAME from %s LIMIT 1" %table_name
        try:
            self.cursor.execute(select_sql)
            return self.cursor.fetchall()
        except Exception as err:
            print("SQL执行错误，原因：", err)
    def FindC_S(self, table_name, Classname):
        select_sql = "select SID, SNAME from %s WHERE S_C = \'%s\'" %(table_name, Classname)
        try:
            self.cursor.execute(select_sql)
            return self.cursor.fetchall()
        except Exception as err:
            print("SQL执行错误，原因：", err)
    # 定义添加表数据函数
    def Insert(self, stu_name, stu_gender, stu_age, stu_cid, stu_classid, stu_phone):
        # 实例变量
        self.stu_name = stu_name
        self.stu_gender = stu_gender
        self.stu_age = stu_age
        self.stu_cid = stu_cid
        self.stu_classid = stu_classid
        self.stu_phone = stu_phone
        # 定义SQL语句
        sql = "insert into stu_info(stu_name,stu_gender,stu_age,stu_cid,stu_classid,stu_phone) values('%s','%s','%s','%s','%s','%s')" % (
        self.stu_name, self.stu_gender, self.stu_age, self.stu_cid, self.stu_classid, self.stu_phone)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)

    # 定义删除表数据函数
    def Del(self, stu_id):
        # 实例变量
        self.stu_id = stu_id
        # 定义SQL语句
        sql = "delete from stu_info where id=%d" % (self.stu_id)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)

    # 用析构函数实现数据库关闭
    def __del__(self):
        # 关闭数据库连接
        self.db.close()