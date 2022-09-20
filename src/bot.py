import logging
import django
import os


from channels.db import database_sync_to_async
from discord import Intents
from discord.ext import commands

from django.db import transaction


# Environment variables
BOT_CHANNEL = os.environ.get('BOT_CHANNEL', 'bot_commands')
if os.environ.get('DEBUG'):
    DEBUG = os.environ.get('DEBUG') == 'True'
else:
    DEBUG = False

# Logging setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('discord')

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# Initialize a Django instance
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'contestsuite.settings')
django.setup()

# Django imports valid after setup()
from lfg.models import DiscordMember
from contestsuite.settings import GUILD_ID, SCRAPE_BOT_TOKEN

# Initialize bot
intents = Intents(messages=True, guilds=True, members=True)
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


'''
    Bot Commands
'''

def bot_channel_only():
    async def predicate(ctx):
        if ctx.channel.name != BOT_CHANNEL:
            # Do the handling here or in on_command_error handler
            message = ctx.message
            await message.delete()
            await ctx.send("You do not have permission to use these commands.")
        return True

    return commands.check(predicate)


@bot.event
@bot_channel_only()
async def on_message(message):
    if message.author:#:.bot:
        ctx = await bot.get_context(message)

    if ctx.valid:
        args = message.content.split(" ")

        if len(args) > 1:
            args  = args[1:]
        else:
            args = []

        await ctx.invoke(ctx.command, *args)


@bot.event
async def on_ready():
    logger.info("ScrapeBot ready")


@bot_channel_only()
@bot.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def help(ctx):
    """
    Overwrites default help command.
    """
    await ctx.send("This bot's commands are private!")


@bot_channel_only()
@bot.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def scrape_members(ctx):
    guild = bot.get_guild(int(GUILD_ID))
    
    if guild:
        members = []

        for member in guild.members:
                if not member.bot:
                    members.append(member)

        if len(members) > 0:
            await create_db_members(members)

    else:
        logger.error("Guild fetch error")


@database_sync_to_async
@transaction.atomic
def create_db_members(members):
    failed_adds = 0

    for member in members:
        if not DiscordMember.objects.filter(username=member.name).filter(discriminator=member.discriminator).exists():
            try:
                DiscordMember.objects.create(username=member.name, discriminator=member.discriminator)
            except:
                failed_adds += 1

    if failed_adds > 0:
        logger.info(f"Failed to write {failed_adds} members to the database")
    else:
        logger.info("Member scrape successful")

if __name__ == "__main__":
    bot.run(SCRAPE_BOT_TOKEN)
