import dotenv
import os
from config import Config
from otto_api42.intra import IntraAPIClient as Client42
from discord_client import QuestionPourUnClient
from discord_commands import QuestionPourUnBot

if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    Config(os.environ)
    Config().prepare_config_for_intra_client()
    bot = QuestionPourUnBot(Config(), Client42("./config.yml"))
    client = QuestionPourUnClient(Config())
    client.start_investigation()
