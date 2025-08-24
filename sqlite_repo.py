import sqlite3
from logging import Logger

LOGGER = Logger("SqliteRepository")


class DbUser:
    def __init__(self, row: tuple):
        self.id = row[0]
        self.login = row[1]
        self.img_url = row[2]
        self.infos = row[3]
        self.notes = row[4]


class SqliteRepository:
    def __init__(self, db_file_path: str):
        self.conn = sqlite3.connect(db_file_path)
        self.cur = self.conn.cursor()
        self.setup()

    def setup(self):
        LOGGER.info("Setting up db")
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS key_value (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """
        )
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT,
            img_url TEXT,
            infos TEXT,
            notes TEXT
        )
        """
        )
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
        """
        )

    def user_create(
        self, login: str, img_url: str, infos: str, notes: str = None
    ):
        self.cur.execute(
            """
        INSERT INTO users (login, img_url, infos, notes)
        VALUES (?, ?, ?, ?)
        """,
            (login, img_url, infos, notes),
        )
        self.conn.commit()

    def find_user_by_login(self, login: str):
        self.cur.execute(
            """
        SELECT *
        FROM users
        WHERE login=?
        """,
            (login,),
        )
        user = self.cur.fetchone()
        if user is not None:
            return DbUser(user)
        return user

    

def start_sqlite():
    conn = sqlite3.connect("sbrooks.db")
    cur = conn.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS key_value (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """
    )
    return (cur, conn)


def insert_key_value(key, value, cur, conn):
    cur.execute(
        """
    INSERT OR REPLACE INTO key_value (key, value) 
    VALUES (?, ?)
    """,
        (key, value),
    )
    conn.commit()


def get_value(key, cur):
    cur.execute(
        """
    SELECT value FROM key_value WHERE key = ?
    """,
        (key,),
    )
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None
