from asgiref.sync import sync_to_async

from celery import shared_task
from celery.utils.log import get_task_logger

from discord import Client, Intents

from .models import DiscordMember
from contestsuite.settings import GUILD_ID, SCRAPE_BOT_TOKEN


logger = get_task_logger(__name__)


# Discord bot to scrape guild member list 
class ScrapeBot(Client):
    # Helper method to write new members to database
    @sync_to_async
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


# Celery task which invokes ScrapeBot
@shared_task
def scrape_discord_members():
    intents = Intents.default()
    intents.members = True

    client = ScrapeBot(intents=intents)

    client.run(SCRAPE_BOT_TOKEN)
