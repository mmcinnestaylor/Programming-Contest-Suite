from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string

from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Announcement


logger = get_task_logger(__name__)


@shared_task
def email_annoucement(id):
    try:
        announcement = Announcement.objects.get(id=id)
    except:
        logger.info('Failed to send announcement with id %d ' % id)
    else:
        i=0
        users = User.objects.all()
        messages = []
        
        for user in users:
            i += 1

            message = render_to_string(
            'announcements/new_announcement_email.html', {'announcement': announcement})

            messages.append((announcement.title, message, 'ACM Programming Contest<acm@cs.fsu.edu>', [user.email]))

        messages = tuple(messages)
        send_mass_mail(messages, fail_silently=False)

        logger.info('Sent announcement to %d users' % i)
