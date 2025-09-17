import smtplib
from email.mime.text import MIMEText

def send_email(email , link):
    subject = "password reset"
    body = f"your reset password link : + {link}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "zidanbushnaq@gmail.com"
    msg["To"] = email

    with smtplib.SMTP_SSL("smtp.gmail.com" ,465) as server:
        #server.starttls()
        server.login("zidanbushnaq@gmail.com" , "fhof fabx mqsk klxe")
        server.send_message(msg)