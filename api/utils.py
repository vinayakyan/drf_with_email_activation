from django.core.mail import EmailMessage
class Util:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(subject=data.get('subject'), body=data.get('email_body'), to=[data.get('to')])
        email.send()