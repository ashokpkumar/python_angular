from flask_mail import Mail, Message
from main import mail


def send_mail(subject, sender, recipients, body, html_body):
   msg = Message(subject=subject, sender=sender, recipients=[recipients])
   msg.html = html_body
   msg.body = body
   mail.send(msg)
