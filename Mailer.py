# -*- coding: utf-8 -*-

#Importando bibliotecas padrao
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import Config

def Send(param_subject, param_message, param_send_to):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(Config.EMAIL_ADRESS, Config.EMAIL_PASSWORD)
        message = 'Subject: {}\n\n{}'.format(param_subject, param_message)
        #Sempre quem envia, depois para quem envia
        server.sendmail(Config.EMAIL_ADRESS, param_send_to, message)
        server.quit()
        print('Success email sent.')
    except:
        print('Email failed to send.')

def SendHTML(param_subject, param_message, param_send_to):
    try:
        message = MIMEMultipart('alternative')
        message['Subject'] = param_subject
        message['From'] = Config.EMAIL_ADRESS
        message['To'] = param_send_to
        html = u''.join(param_message).encode('utf-8').strip()
        part = MIMEText(html, 'html')
        message.attach(part)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(Config.EMAIL_ADRESS, Config.EMAIL_PASSWORD)
        #Sempre quem envia, depois para quem envia
        server.sendmail(Config.EMAIL_ADRESS, param_send_to, message.as_string())
        server.quit()
        print(''.join(['Success email sent to ', param_send_to ,' .']))
    except:
        print('Email failed to send.')



#Testa o envio de mensagens
#subject = "Test subject"
#msg = "Hello there"
#Send(subject, msg)