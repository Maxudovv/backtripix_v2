import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings


def send_otp_message(email, code):
    msg = MIMEMultipart()
    message = f"Verification code: {code}"

    password = settings.EMAIL_PASSWORD
    msg["From"] = settings.EMAIL_NAME
    msg["To"] = email
    msg["Subject"] = "Tripix"
    msg.attach(MIMEText(message, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(msg["From"], password)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()

    return msg


def send_thank_you_message(email):
    msg = MIMEMultipart()
    message = "Спасибо! Ваше обращение успешно доставлено в команду TRIPIX"

    msg["From"] = settings.EMAIL_NAME
    msg["To"] = email
    msg["Subject"] = "Tripix"
    msg.attach(MIMEText(message, "plain"))

    server = smtplib.SMTP("smtp.gmail.com: 587")
    server.starttls()
    server.login(msg["From"], settings.EMAIL_PASSWORD)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()

    return msg


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def reduce_path(file_name, times):
    result = os.path.realpath(file_name)
    for i in range(times):
        result = os.path.dirname(result)
    return result
