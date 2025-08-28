import random
import sqlite3
import discord
from discord.ext import commands
from discord import Embed

from otto_api42.intra import IntraAPIClient
from config import Config
from question_service import QuestionService
from sqlite_repo import MicrORM


class QuestionPourUnBot(commands.Bot):
    def __init__(self, config: Config, intra_client: IntraAPIClient):
        self.config = config
        self.sql = MicrORM("qpup.db")
        self.api42 = intra_client
        self.current_session = None
        self.current_question = None
        self.question_service = QuestionService(
            self.sql.questions, self.sql.question_sources, self.sql.session_questions
        )
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
            (
                "start_session",
                "Start a new Question pour un piscineux session",
                self.start_session,
            ),
            ("summarize_session", "Summarize a session", self.summarize_session),
            (
                "tally_session",
                "Show the total score coalition score for a session",
                self.tally_session,
            ),
            ("show_session", "Show informations about a session", self.show_session),
            ("end_session", "End the current session", self.end_session),
        ]
        for cmd in commands_object:
            self.add_command_to_tree(cmd[0], cmd[1], cmd[2])
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
    ):
        self.sql.question_sources.create(question, answer)
        await interaction.response.send_message("Question registered.")

    async def delete_question(self, interaction: discord.Interaction, identifier: str):
        _id: int
        try:
            _id = int(identifier)
        except ValueError:
            await interaction.response.send_message(f"Invalid ID '{identifier}'")
            return
        self.sql.question_sources.delete_one(_id)
        await interaction.response.send_message(f"Deleted question.")

    async def edit_question(
        self,
        interaction: discord.Interaction,
        identifier: str,
        question: str,
        answer: str,
    ):

        _id: int
        try:
            _id = int(identifier)
        except ValueError:
            await interaction.response.send_message(f"Invalid ID '{identifier}'")
            return
        self.sql.question_sources.update_one(_id, question, answer)
        await interaction.response.send_message(f"Modified question with ID '{_id}'.")

    async def ask_question(self, interaction: discord.Interaction):
        if self.current_session is None:
            await interaction.response.send_message(
                "Cannot ask a question while not in a session. Do /start_session first"
            )
            return
        max_id = self.sql.questions.count()
        if max_id == 0:
            await interaction.response.send_message(
                "No question were setup for this pool. "
                "Either you did not register any question, "
                "or there was an unexpected error."
            )
            return

        random_id = random.randrange(max_id)
        q_entry = self.sql.questions.fetch_one(random_id)
        self.current_question = q_entry.id
        sq_entry = self.sql.session_questions.create(self.current_session, q_entry.id)
        if sq_entry is None:
            await interaction.response.send_message(
                "Fatal: An error occurred while setting up the question. This is unexpected."
            )
            return
        await interaction.response.send_message(
            f"Question: {sq_entry.question.question_source.text}. "
            f"Answer: {sq_entry.question.question_source.answer}"
        )

    async def answered(self, interaction: discord.Interaction, login: str):
        if self.current_session is None:
            await interaction.response.send_message(
                "Cannot mark a question as answered while not in a session."
                " Do /start_session first, then /ask_question."
            )
            return
        if self.current_question is None:
            await interaction.response.send_message(
                "Cannot mark a question as answered, no question have been asked."
                " Do /ask_question."
            )
            return
        self.sql.questions.update_one(self.current_question, {"answered": True})
        self.current_question = None
        await interaction.response.send_message("Marked last question as answered")

    async def timeup(self, interaction: discord.Interaction, login: str):
        if self.current_session is None:
            await interaction.response.send_message(
                "Cannot mark a question as timed out while not in a session."
                " Do /start_session first, then /ask_question."
            )
            return
        if self.current_question is None:
            await interaction.response.send_message(
                "Cannot mark a question as timed out, no question have been asked."
                " Do /ask_question."
            )
            return
        self.sql.questions.update_one(self.current_question, {"timeout": True})
        self.current_question = None
        await interaction.response.send_message("Marked last question as timed out")

    async def start_session(self, interaction: discord.Interaction, session_name: str):
        if self.current_session is not None:
            await interaction.response.send_message(
                "Cannot start a session while one is already running. (this is a work in progress)"
            )
            return
        s_entry = self.sql.sessions.create(session_name)
        if s_entry is None:
            await interaction.response.send_message(
                "Fatal: An error occurred while setting up the session. This is unexpected."
            )
            return
        self.current_session = s_entry.id
        self.question_service.generate_all_for_session(self.current_session)
        await interaction.response.send_message(
            f"Started new session with ID '{self.current_session}'"
        )

    async def summarize_session(
        self, interaction: discord.Interaction, session_id: str
    ):
        await interaction.response.send_message("NotImplemented")

    async def tally_session(self, interaction: discord.Interaction, session_id: str):
        await interaction.response.send_message("NotImplemented")

    async def show_session(self, interaction: discord.Interaction):
        await interaction.response.send_message("NotImplemented")

    async def end_session(self, interaction: discord.Interaction):
        if self.current_session is None:
            await interaction.response.send_message(
                "Cannot end session: no session in progress."
            )
            return
        if self.current_question is not None:
            await interaction.response.send_message(
                "Cannot end session: a question is still pending an answer."
            )
            return
        self.sql.sessions.update_one(self.current_session, {"finished": True})
        self.current_session = None
        await interaction.response.send_message("Successfully ended session.")
