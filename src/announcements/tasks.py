from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string

from celery import shared_task
from celery.utils.log import get_task_logger

from discord import Webhook, RequestsWebhookAdapter, Embed, InvalidArgument

from .models import Announcement
from contestsuite.settings import ANNOUNCEMENT_WEBHOOK_URL, DEFAULT_FROM_EMAIL, ALLOWED_HOSTS


logger = get_task_logger(__name__)


@shared_task
def email_annoucement(id):
    try:
        announcement = Announcement.objects.get(id=id)
    except:
        logger.info(f'Failed to send announcement with id {id}')
    else:
        i=0
        users = User.objects.all()
        messages = []
        
        for user in users:
            if user.is_active and not user.profile.announcement_email_opt_out:
                i += 1

                message = render_to_string(
                'announcements/new_announcement_email.html', {'announcement': announcement})

                messages.append((announcement.title, message, DEFAULT_FROM_EMAIL, [user.email]))

        messages = tuple(messages)
        send_mass_mail(messages, fail_silently=False)

        logger.info(f'Sent announcement to {i} users')

@shared_task
def discord_announcement(id):
    try:
        announcement = Announcement.objects.get(id=id)
    except:
        logger.info(f'Failed to send announcement with id {id}')
    else:
        # Initializing webhook
        try:
            webhook = Webhook.from_url(
                ANNOUNCEMENT_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
        except InvalidArgument:
            logger.info('Failed to connect to announcement webhook')
        else:
            url = 'https://'+ALLOWED_HOSTS[0]+announcement.get_absolute_url()
            
            if len(announcement.content) <= 140:
                content = announcement.content
            else:
                content = announcement.content[:140] + '...'
            
            # Initializing an Embed
            embed = Embed(title=announcement.title, description=content, url=url)

            # Executing webhook.
            webhook.send(embed=embed)
