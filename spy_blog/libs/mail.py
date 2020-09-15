__author__ = 'SPing'

import re
import os
import base64

from flask import current_app, render_template, render_template_string
from flask_mail import Mail, Message
from retry import retry
from config import static_dir


mail = Mail()


class MailSender:
    """
    发送邮件
    """
    def __init__(self, subject: str, to: list or str, body: str = ''):
        self.subject = subject
        self.to = to if type(to) == list else [to]
        self.body = body
        self.message = Message(subject, recipients=self.to, body=body)

    @retry(tries=3, delay=0.5)
    def send(self):
        mail.send(self.message)


    def str_email(self):
        """
        文本邮件
        """
        try:
            self.send()
        except Exception as e:
            current_app.logger.error('邮件发送失败')
            return e

    def html_email(self, template_name: str, pwd: str):
        """
        html样式文件
        """
        try:
            # 发送渲染一个模板
            img_stream = ''
            with open(os.path.join(static_dir, 'images/logo.png'), 'r', encoding='UTF-8') as f:
                img_stream = f.read()
                img_stream = base64.b64encode(img_stream)
            self.message.html = render_template(template_name, pwd=pwd, img_stream=img_stream)
            self.send()
        except Exception as e:
            current_app.logger.error('邮件发送失败')
            import traceback
            print(traceback.format_exc())
            return e

    def attach_email(self, filepath: str, content_type: str = "image/jpg"):
        """
        附件邮件
        """
        try:
            filename = os.path.split(filepath)[-1]
            with open(filepath, 'rb') as fp:
                self.message.attach(filename, content_type, fp.read())
            self.send()
        except Exception as e:
            current_app.logger.error('邮件发送失败')
            return e


def check_email(email: str) -> bool:
    reg = r"^[a-zA-Z0-9_][^@]+@[^\.]+.*?[^@\.]$"
    if re.match(reg, email):
        return True
    return False
