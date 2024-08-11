import logging
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from emailservice.celery import app

from mainemail.views import sendEmail

@app.task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        sendEmail("TEST", f"celery celery{user_id}", "kristal.as@phystech.edu")
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)

