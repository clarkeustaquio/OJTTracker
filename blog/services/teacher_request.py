from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator

account_activation_token = PasswordResetTokenGenerator()

def teacher_request(email_to, name, user_pk, user, instructor_name):
    try:
        subject = 'OJTTracker'
        message = 'Confirm Teacher Request'
        email_from = settings.EMAIL_HOST_USER
        email_to = [email_to]

        site = 'localhost:8000/success-teacher-approve/'

        send_mail(
            subject, message, email_from, email_to,
            fail_silently=True,
            html_message=render_to_string('services/teacher_request.html', {
                'name': name,
                'uid': urlsafe_base64_encode(force_bytes(user_pk)),
                'domain': site,
                'token': account_activation_token.make_token(user),
                'instructor_name': instructor_name
            })
        )
    except Exception as e:
        return False
    else:
        return True
