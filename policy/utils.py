from django.core.mail import EmailMessage

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'],from_email='kibetedgar@gmail.com',body=data['email_body'],to=[data['to_email']])
        email.send()