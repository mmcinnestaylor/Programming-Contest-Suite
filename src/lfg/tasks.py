from celery import shared_task
from celery.utils.log import get_task_logger

from discord import Webhook, RequestsWebhookAdapter, InvalidArgument

from django.contrib.auth.models import User
from django.db import transaction
from django.template.loader import render_to_string

from .models import DiscordMember, LFGProfile
from contestsuite.settings import BOT_CHANNEL_WEBHOOK_URL
from register.models import Team


logger = get_task_logger(__name__)


@shared_task
@transaction.atomic
def cleanup_lfg_rosters():
    """
    Celery task to deactivate LFG profiles where the user is also on a full team.
    """

    members_upper = []
    members_lower = []
    # max team size is 3
    teams = Team.objects.filter(num_members=3)

    for team in teams:
        members = User.objects.filter(profile__team=team)

        for member in members:
            if LFGProfile.objects.filter(user=member).exists() and member.lfgprofile.active == True:
                # Deactivate profile
                member.lfgprofile.active = False
                member.lfgprofile.save()
                
                if member.lfgprofile.division == 1:
                    members_upper.append(member.lfgprofile.get_discord_username())
                else:
                    members_lower.append(member.lfgprofile.get_discord_username())

    # Initializing webhook
    if len(members_upper) > 0 or len(members_lower) > 0:
        try:
            webhook = Webhook.from_url(
                BOT_CHANNEL_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
        except InvalidArgument:
            logger.error('Failed to connect to bot channel webhook')
        else:
            if len(members_upper) > 0:
                # Upper
                members = ','.join([member for member in members_upper])
                message = '$remove_role ' + members + ' LFG_Upper'
                # Executing webhook.
                webhook.send(content=message)
                logger.info(f'Deactivated {len(members_upper)} Upper Division Profiles')

            if len(members_lower) > 0:
                # Lower
                members = ','.join([member for member in members_lower])
                message = '$remove_role ' + members + ' LFG_Lower'
                # Executing webhook.
                webhook.send(content=message)
                logger.info(f'Deactivated {len(members_lower)} Lower Division Profiles')


@shared_task
def manage_discord_lfg_role(username, division, action=None):
    """
    Celery task to update an existing LFG profile.

    action: 'add', 'remove', 'swap'
    """
    
    assert action == 'add' or action == 'remove' or action == 'swap', "Invalid action passed: ['add' | 'remove' | 'swap']"
    
    try:
        webhook = Webhook.from_url(BOT_CHANNEL_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
    except InvalidArgument:
        logger.error('Failed to connect to bot channel webhook')
    else:
        if action == 'add' or action == 'remove':
            if division == 1:
                message = f'${action}_role ' + username + ' LFG_Upper'
            else:
                message = f'${action}_role ' + username + ' LFG_Lower'

            # Executing webhook.
            webhook.send(content=message)
            logger.debug(f'Success - {action} role: {username}')
        else:
            if division == 1:
                message = '$remove_role ' + username + ' LFG_Upper'
                webhook.send(content=message)

                message = '$add_role ' + username + ' LFG_Lower'
                webhook.send(content=message)
            else:
                message = '$remove_role ' + username + ' LFG_Lower'
                webhook.send(content=message)

                message = '$add_role ' + username + ' LFG_Upper'
                webhook.send(content=message)
            
            logger.debug(f'Success - {action} role: {username}')


@shared_task
def scrape_discord_members():
    """
    Celery task to trigger a scrape of the target Discord server member list.
    """

    try:
        webhook = Webhook.from_url(BOT_CHANNEL_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
    except InvalidArgument:
        logger.error('Failed to connect to bot channel webhook')
    else:
        message = '!scrape_members'
        webhook.send(content=message)
        logger.debug('Scrape members call sent')
     

@shared_task
@transaction.atomic
def verify_lfg_profiles():
    """
    Celery task which attempts to verify any unverified LFGProfiles.
    """
    
    lfg_profiles = LFGProfile.objects.filter(completed=True).filter(verified=False)
    count = 0

    for profile in lfg_profiles:
        # verification: provided username + discriminator matches a username scraped from the target Discord server
        if DiscordMember.objects.filter(username=profile.discord_username).filter(discriminator=profile.discord_discriminator).exists():
            profile.verified = True
            profile.save()

            subject = 'Your LFG Profile is verified!'
            message = render_to_string('lfg/lfg_verified_email.html', {'user': profile.user})
            profile.user.email_user(subject, message)

            count += 1
    
    logger.info(f'Verified {count} profiles')
