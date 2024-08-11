from emailservice.celery import app

from mainemail.services import sendEmail

@app.task
def send_verification_email(user_id):
    try:
        sendEmail("TEST", f"celery celery{user_id}", "kristal.as@phystech.edu")
    except Exception as e:
        print(e)


