import random
import smtplib
import os
from email.mime.multipart import MIMEMultipart


ttt = []
lll = 1

def send_email(email):
    global token
    addr_from = os.getenv("FROM")
    password = os.getenv("PASSWORD")

    lis = []
    token = ''
    las = ['abcdefghijklmnopqrstuvwxyz', '1234567890', '`~!@#$%^&*()_+=-/.?><']
    for i in range(4):
        lis.append(las[0][random.randint(0, len(las[0]) - 1)])
        lis.append(las[1][random.randint(0, len(las[1]) - 1)])
        lis.append(las[2][random.randint(0, len(las[2]) - 1)])
    for i in lis:
        token += i
    ttt.append(token)
    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = email
    msg['Subject'] = token


    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login(addr_from, password)

    server.send_message(msg)
    server.quit()
    return True

