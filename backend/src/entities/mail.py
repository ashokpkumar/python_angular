from flask_mail import Mail, Message
from main import mail


# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'indium@gmail.com'
# app.config['MAIL_PASSWORD'] = 'xxxxxx'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
#
# mail= Mail(app)

def send_mail():
   msg = Message('test', sender = 'indium@gmail.com', recipients = ['xxx@indiumsoft.com','yyy@indiumsoft.com'])
   msg.add_recipient('zzz@indiumsoft.com')
   #msg.cc(["",""])
   #msg.bcc(["",""])
   msg.body = "RMG app mail test"
   mail.send(msg)
   return "Sent"

