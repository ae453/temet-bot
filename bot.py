import logging
import os
import platform
import random
import time

import colorama
import discord
from discord import app_commands, ui
from discord.ext import commands, tasks
from discord.ui import Button, View
from dotenv import dotenv_values

from embed_generator import embed_generator

# from interactions import ban_input_other


config = dotenv_values(".env")

colorama.init(autoreset=True)

dir_path = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists(f'{dir_path}\\logs'):
    os.makedirs(f'{dir_path}\\logs')

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(filename)s | %(levelname)s | %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

stream_h = logging.StreamHandler()
file_h = logging.FileHandler(f"logs/{time.strftime('%m-%d-%Y %H %M %S', time.localtime())}.log")

stream_h.setLevel(logging.WARNING)
file_h.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(filename)s | %(levelname)s | %(message)s', '%m/%d/%Y %H:%M:%S')
stream_h.setFormatter(formatter)
file_h.setFormatter(formatter)

logger.addHandler(stream_h)
logger.addHandler(file_h)


@tasks.loop(minutes=1)
async def status():
    choices = [
        discord.Activity(type=discord.ActivityType.playing, name="Valorant"),
    ]
    chosen = random.choice(choices)
    await client.change_presence(activity=chosen)


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(config["BOT_PREFIX"]), case_insensitive=True, intents=discord.Intents.all())
        self.cogs_list = ['jishaku']
        
    async def is_owner(self, user: discord.User):
        if user.id in []:
            return True
        return await super().is_owner(user)

    async def setup_hook(self):
        for ext in self.cogs_list:
            await self.load_extension(ext)

    async def on_ready(self):
        logger.info(f"Logging in as {self.user.name}")
        logger.info(f"Client ID: {self.user.id}")
        logger.info(f"Discord Version: {discord.__version__}")
        logger.info(f"Python Version: {platform.python_version()}")
        status.start()
        logger.info(f"Status Loop Started")

        channel = client.get_channel(1202323434940661834)
        await channel.send(f'{client.user.mention} is now online!')
        
client = Client()
client.remove_command("help")

@client.event
async def on_error():
    pass


if __name__ == "__main__":
    client.run(token=config["BOT_TOKEN"])