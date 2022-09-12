from asgiref.sync import sync_to_async
from celery import shared_task
from celery.utils.log import get_task_logger
from discord import Client, Intents, Webhook, RequestsWebhookAdapter, InvalidArgument
from django.contrib.auth.models import User
from django.db import transaction
from django.template.loader import render_to_string

from .models import DiscordMember, LFGProfile
from contestsuite.settings import GUILD_ID, SCRAPE_BOT_TOKEN, BOT_CHANNEL_WEBHOOK_URL
from register.models import Team


logger = get_task_logger(__name__)


# Discord bot to scrape guild member list 
class ScrapeBot(Client):
    # Helper method to write new members to database
    @sync_to_async
    @transaction.atomic
    def save_discord_members(self, members):
        i = 0
        for member in members:
            if not member.bot and not DiscordMember.objects.filter(username=member.name).filter(discriminator=member.discriminator).exists():
                try:
                    DiscordMember.objects.create(
                        username=member.name, discriminator=member.discriminator)
                    i += 1
                except:
                    logger.info('Discord member addition failed for: %s' %
                                (member.name+'#'+str(member.discriminator).zfill(4)))
        logger.info('Added %d Discord members' % i)

    # Bot method runs on successful connection to Discord API
    async def on_ready(self):
        logger.info('Scrape bot ready.')
        try:
            guild = self.get_guild(GUILD_ID)
        except:
            logger.info('Guild fetch failed.')
        else:  
            if guild is not None:
                logger.info('Guild %s fetched.' % guild.name)
                await self.save_discord_members(guild.members)
            else:
                logger.info('No guild with provided id.')

        #await self.close()


@shared_task
@transaction.atomic
def cleanup_lfg_rosters():
    members_upper = []
    members_lower = []
    teams = Team.objects.filter(num_members=3)

    for team in teams:
        members = User.objects.filter(profile__team=team)

        for member in members:
            if LFGProfile.objects.filter(user=member).exists() and member.lfgprofile.active == True:
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
            logger.info('Failed to connect to bot channel webhook')
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
    '''
        action: 'add', 'remove', 'swap'
    '''
    assert action == 'add' or action == 'remove' or action == 'swap', "Invalid action passed: ['add' | 'remove' | 'swap']"
    
    try:
        webhook = Webhook.from_url(BOT_CHANNEL_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
    except InvalidArgument:
        logger.info('Failed to connect to bot channel webhook')
    else:
        if action == 'add' or action == 'remove':
            if division == 1:
                message = f'${action}_role ' + username + ' LFG_Upper'
            else:
                message = f'${action}_role ' + username + ' LFG_Lower'

            # Executing webhook.
            webhook.send(content=message)
            logger.info(f'Success - {action} role: {username}')
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
            
            logger.info(f'Success - {action} role: {username}')


# Celery task which invokes ScrapeBot
@shared_task
def scrape_discord_members():
    intents = Intents.default()
    intents.members = True

    client = ScrapeBot(intents=intents)

    client.run(SCRAPE_BOT_TOKEN)
    #await client.close()


@shared_task
@transaction.atomic
def verify_lfg_profiles():
    lfg_profiles = LFGProfile.objects.filter(completed=True).filter(verified=False)
    count = 0

    for profile in lfg_profiles:
        if DiscordMember.objects.filter(username=profile.discord_username).filter(discriminator=profile.discord_discriminator).exists():
            profile.verified = True
            profile.save()

            subject = 'Your LFG Profile is verified!'
            message = render_to_string('lfg/lfg_verified_email.html', {'user': profile.user})
            profile.user.email_user(subject, message)

            count += 1
    
    logger.info(f'Verified {count} profiles')
