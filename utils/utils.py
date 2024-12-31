import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from kavenegar import *

from utils.constant import KAVE_API_KEY


def send_email(to, subject, body):
    # اطلاعات حساب
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_user = "pythonshafiee@gmail.com"  # ایمیل خود را اینجا وارد کنید
    email_password = "ediv qzpb uasd dkuv"  # رمز عبور خود را اینجا وارد کنی

    to_email = to  # گیرنده ایمیل
    subject = subject
    body = body

    msg = MIMEMultipart()
    msg['Form'] = email_user
    msg['To'] = to_email
    msg['Subject'] = subject
    # اضافه کردن متن به ایمیل

    msg.attach(MIMEText(body, 'html'))

    try:
        # اتصال به سرور و ارسال ایمیل
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, to_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()  # قطع اتصال


def send_sms(to, token, template, token2="", token3=""):
    try:
        api = KavenegarAPI(KAVE_API_KEY)
        params = {
            'receptor' : to,
            'template' : template,
            'token' : token,
            'token2': token2,
            'token3': token3,
            'type' : 'sms', #sms vs call
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)