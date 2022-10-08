from django.contrib.auth.models import User
from django.template.loader import render_to_string

from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task
def send_credentials(username):
    user = User.objects.get(username=username)
    
    subject = 'Programming Contest DOMjudge Credentials'
    message = render_to_string('checkin/team_credentials_email.html', {'user': user})
    user.email_user(subject, message)

    logger.info('Sent credentials to %s' % username)
