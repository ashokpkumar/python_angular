from flask_mail import Mail, Message
from main import mail


def send_mail(subject, sender, recipients, body, cc, bcc):
   msg = Message(subject=subject, sender=sender, recipients=[recipients], body=body, cc=[cc], bcc=[bcc])
   mail.send(msg)

   return "Email Sent successfully"

