import sqlite3
import discord
from discord.ext import commands
from discord import Embed

from otto_api42.intra import IntraAPIClient
from config import Config
from sqlite_repo import SqliteRepository


class QuestionPourUnBot(commands.Bot):
    def __init__(self, config: Config, intra_client: IntraAPIClient):
        self.config = config
        self.sql = SqliteRepository("qpup.db")
        self.api42 = intra_client
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    def startup(self):
        commands_object = [
            (
                "reqister_question",
                "Register a new question, along with an answer",
                self.register_question,
            ),
            (
                "delete_question",
                "Delete a question from the pool",
                self.delete_question,
            ),
            ("edit_question", "Edit a question and its answer", self.edit_question),
            ("ask_question", "Randomly show an unanswered question", self.ask_question),
            ("answered", "Mark the last question as answered", self.answered),
            (
                "timeup",
                "Mark the last question as timed out (answered, but flagged timeout)",
                self.timeup,
            ),
            ("start_session", "Start a new Question pour un piscineux session", self.start_session),
            ("summarize_session", "Summarize a session", self.summarize_session),
            ("tally_session", "Show the total score coalition score for a session", self.tally_session),
            ("show_session", "Show informations about a session", self.show_session),
            ("end_session", "End the current session", self.end_session),
            
        ]
        self.run(self.config.discord_token)

    def add_command_to_tree(self, cmd_name: str, description: str, f_obj: callable):
        decorator = self.tree.command(
            name=cmd_name,
            description=description,
            guild=discord.Object(id=self.config.server_id),
        )
        decorator(f_obj)

    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=self.config.server_id))
        print("Bot Ready!")

    async def register_question(
        self, interaction: discord.Interaction, question: str, answer: str
    ): ...
    async def delete_question(
        self, interaction: discord.Interaction, identifier: str
    ): ...
    async def edit_question(
        self, interaction: discord.Interaction, identifier: str
    ): ...
    async def ask_question(self, interaction: discord.Interaction): ...
    async def answered(self, interaction: discord.Interaction, login: str): ...
    async def timeup(self, interaction: discord.Interaction, login: str): ...
    async def start_session(
        self, interaction: discord.Interaction, session_name: str
    ): ...
    async def summarize_session(
        self, interaction: discord.Interaction, session_name: str
    ): ...
    async def tally_session(
        self, interaction: discord.Interaction, session_name: str
    ): ...
    async def show_session(self, interaction: discord.Interaction): ...
    async def end_session(self, interaction: discord.Interaction): ...
