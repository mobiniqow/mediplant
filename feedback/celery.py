from celery import shared_task

@shared_task
def send_feedback_reminder_task():
    send_feedback_reminder()
