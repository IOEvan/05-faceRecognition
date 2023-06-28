# -*- coding: utf-8 -*-
import time
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import xlrd
from openpyxl.compat import range
import os


def send_mail(config):
    print('Sending Mail...')

    message = MIMEMultipart()
    message["Accept-Charset"] = "ISO-8859-1,utf-8"
    message['From'] = 'xxx@126.com'

    message['To'] = ','.join(config['to'])
    message['CC'] = ','.join(config['cc'])
    message['Subject'] = config['subject']
    message['Date'] = time.ctime(time.time())
    message['Reply-To'] = 'xxx@qq.com'
    message['X-Priority'] = '3'
    message['X-MSMail-Priority'] = 'Normal'
    if config['text']:
        text = config['text']
        message.attach(text)

    part = MIMEApplication(open(fileName, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=fileName)
    message.attach(part)

    smtp = SMTP(config['server'], config['port'])

    username = 'xxx@126.com'
    smtp.login(username, '098poilkjmnb')
    while True:
        try:
            smtp.sendmail(username, config['to'], message.as_string())
            print('Send Mail OK')
            break
        except Exception as err:
            print("发送出现错误：" + err)
            continue

    smtp.close()
    time.sleep(1)


def send_mail_to_test(context):
    send_mail({
        'to': ["xxx@126.com"],
        'cc': ['xxxx@qq.com'],
        'server': 'smtp.126.com',
        'port': 25,
        'subject': time.strftime('%Y-%m-%d', time.localtime(time.time())) + ' 考勤结果',
        'username': 'NameIsEvan@126.com',
        'password': '*********',
        'text': context}
    )


def message_from_excel():
    IDS = []
    studentName = []
    if not os.path.exists(fileName):
        print("Can't find ", fileName)
        return
    data = xlrd.open_workbook(fileName)
    table = data.sheets()[0]  # 打开第一张表
    nrows = table.nrows - 1  # 获取表的行数

    for i in range(1, nrows + 1):  # 循环逐行打印
        IDS.append(str(table.row_values(i)[:2][0]))
        studentName.append(str(table.row_values(i)[:2][1]))

    html_data = ""
    for i in range(nrows):
        html_data +=(
        """
        <tr>
            <td >""" + IDS[i] + """</td>
            <td bgcolor="#FF8040">""" + studentName[i] + """</td>
        </tr>
        """)

    html = ("""\
    <!DOCTYPE html>
    <html>
    <meta charset="utf-8">
    <head>
        <title>Attendance 考勤表格</title>
    </head>
    <body>
    <div id="container">
        <div id="content">
            <p>
            """+
                """共出勤"""  + str(nrows) +  """人
                <table width="800" border="2" bordercolor="black" cellspacing="2">
                    <tr>
                        <td><strong>学生学号</strong></td>
                        <td><strong>学生姓名</strong></td>
                    </tr>
                """
        + html_data +
    """
    </table>
</p>
<p>

详情请见附件

</p>
</div>
</div>
</body>
</html>
"""
)

    context = MIMEText(html, _subtype='html', _charset='utf-8')
    send_mail_to_test(context)
dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
sheet_path = "./Attendence/" + dt
fileName = sheet_path + '/data.xlsx'

print(fileName)

if __name__ == '__main__':
    message_from_excel()
