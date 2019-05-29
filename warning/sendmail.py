# coding:utf8
'''
日报
'''
import datetime
import email
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, to):
        self._user = 'lei.liao@phkjcredit.com'
        self._passwd = 'Ll159852'
        self._to_list = to
        self._cc_list = []

    def send(self, msg):
        '''
        发送邮件
        '''
        try:
            server = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465)
            server.login(self._user, self._passwd)
            server.sendmail(self._user, self._to_list + self._cc_list, self._get_attach(msg))
            server.close()
            print("send email successful")
        except Exception as e:
            print(e)

    def _get_attach(self, msg):
        '''
        构造邮件内容
        '''
        attach = MIMEMultipart()
        attach["Subject"] = '预警'
        attach["From"] = "廖雷"
        attach["To"] = ";".join(self._to_list)
        if self._cc_list:
            # 抄送列表
            attach["Cc"] = ";".join(self._cc_list)
        # if self.doc:
        #     # 估计任何文件都可以用base64，比如rar等
        #     # 文件名汉字用gbk编码代替
        #     name = os.path.basename(self.doc).encode("gbk")
        #     f = open(self.doc, "rb")
        #     doc = MIMEText(f.read(), "base64", "gb2312")
        #     doc["Content-Type"] = 'application/octet-stream'
        #     doc["Content-Disposition"] = 'attachment; filename="' + name + '"'
        #     attach.attach(doc)
        #     f.close()
        txt = MIMEText(msg)
        attach.attach(txt)
        return attach.as_string()
