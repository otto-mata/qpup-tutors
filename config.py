from class_utils import SingletonMetaClass
from os.path import dirname, realpath
from pathlib import Path
from logging import Logger
import yaml

LOGGER = Logger("Config")


class Config(metaclass=SingletonMetaClass):
    def __init__(self, environ: dict[str, str]):
        self.client_id = environ.get("CLIENT_ID")
        self.client_secret = environ.get("CLIENT_SECRET")
        self.discord_token = environ.get("TOKEN_DISCORD")
        self.server_id = environ.get("ID_SERVER")

    def as_intra_client_yml(self):
        obj = {
            "intra": {
                "client": self.client_id,
                "secret": self.client_secret,
                "uri": "https://api.intra.42.fr/v2/oauth/token",
                "endpoint": "https://api.intra.42.fr/v2",
                "scopes": "public",
            }
        }
        return obj

    def prepare_config_for_intra_client(self, path: str | Path = None):
        if path is None:
            path = Path(dirname(realpath(__file__))) / "config.yml"
        if isinstance(path, str):
            path = Path(path)
        if not path.exists() or not path.is_file():
            LOGGER.warning(
                "configuration file for the Intra API Client not found"
            )
        yml_conf = self.as_intra_client_yml()
        try:
            with open(path, "w") as conf_file:
                yaml.dump(yml_conf, conf_file)
        except Exception as exc:
            LOGGER.error(f"Caught exception during config file creation: {exc}")
