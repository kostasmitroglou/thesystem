import smtplib
import yaml

def send_mail(message):
    with open('mail.yml') as f:
        data=yaml.load(f,Loader=yaml.FullLoader)
        print(data)
    smtp_username = data['mail']['username']
    smtp_password = data['mail']['password']
    host = data['mail']['host']
    port = data['mail']['port']
    mail_to = data['mail']['mail_to']
    mail_from = data['mail']['mail_from']
    server = smtplib.SMTP(host,port)
    server.login(smtp_username,smtp_password)
    server.sendmail(
        mail_from,
        mail_to,
        message)
    server.quit()