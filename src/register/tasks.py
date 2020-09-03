from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from celery import shared_task
from celery.utils.log import get_task_logger

from .tokens import account_activation_token

logger = get_task_logger(__name__)


@shared_task
def send_validation_email(domain, username):
    user = User.objects.get(username=username)
    subject = 'Activate Your Programming Contest Account'
    message = render_to_string('register/account_activation_email.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })

    user.email_user(subject, message)

    logger.info('Validation sent to %s' % user.email)