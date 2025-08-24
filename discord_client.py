import sqlite3
import discord
from discord.ext import commands
from discord import Embed

from otto_api42.intra import IntraAPIClient
from config import Config
from sqlite_repo import SqliteRepository


class QuestionPourUnClient(discord.Client):
    def __init__(self, config: Config):
        self.config = config
        super().__init__(intents=discord.Intents.all())

    def start_investigation(self):
        self.run(self.config.discord_token)

    async def on_ready(self):
        print("Client Ready!")

    async def on_message(self, message: discord.Message):
        if self.user == message.author:
            return
        await message.channel.send("no")
