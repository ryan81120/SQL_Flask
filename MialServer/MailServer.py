import email.message
import os
import pathlib
import re
import smtplib

from email.mime.text import MIMEText


def send_mail(subject, text, writer):
    """
    信件發送
    :param subject: 標題
    :param text: 內容
    :param writer: 使用者
    :return: bool
    """
    try:

        # region html內容修改
        flag = False
        os.chdir(pathlib.Path(__file__).parent.absolute())
        with open("text.html", mode="r+", encoding="utf-8") as f:
            name = writer
            txt = text
            file_content = re.sub(r"<h3>.*</h3>", f'<h3>使用者: {name} 問題: {subject} <br> 內容:{txt}</h3>', f.read())
            f.truncate(0)
            f.seek(0)
            f.write(file_content)
        # endregion
        # 內容可用html碼(導入html檔案)
        msg = email.message.EmailMessage()
        msg["Subject"] = '全台醫院大平台意見反饋'
        html = open("text.html", encoding="utf-8")
        text = MIMEText(html.read(), _subtype='html')
        msg.add_alternative(text, subtype="html")
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as server:
            server.ehlo()  # 驗證SMTP伺服器
            server.starttls()  # 建立加密傳輸
            server.login({use mail address}, {use key password})
            status = server.sendmail({use mail address}, {use mail address}, msg.as_string())
            if status == {}:
                flag = True
                print("郵件發送成功！")
            else:
                print("郵件發送失敗！")
            server.close()
    except Exception as e:
        print(e)
    return flag
