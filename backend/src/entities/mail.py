from flask_mail import Mail, Message
#from main import mail

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import email, smtplib, ssl


# def send_mail(subject, sender, recipients, body, html_body):
#    msg = Message(subject=subject, sender=sender, recipients=[recipients])
#    msg.html = html_body
#    msg.body = body
#    mail.send(msg)

fromaddr = "deepuk9801@gmail.com"
password = "199980801"   
   
def send_mail(subject,content,toaddr):
    try:
        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject

        # Add body to email
        msg.attach(MIMEText(content, "html"))
        
        text = msg.as_string()
        
        #server = smtplib.SMTP('smtp.office365.com', 587)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr,toaddr, text)
        print('email sent successfully')
        server.quit()
    except Exception as e:
        print("Mail not sent successfully.")

