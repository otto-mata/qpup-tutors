from __future__ import annotations
import sqlite3
from logging import Logger

LOGGER = Logger("SqliteRepository")


class QuestionSourceEntry:
    id: int
    text: str
    answer: str

    def __init__(self, _id, _text, _answer):
        self.id = _id
        self.text = _text
        self.answer = _answer


class SessionEntry:
    id: int
    name: str
    finished: bool

    def __init__(self, _id, _name, _finished):
        self.id = _id
        self.name = _name
        self.finished = _finished


class QuestionEntry:
    id: int
    question_source: QuestionSourceEntry
    qs_id: int
    answered: bool
    timeout: bool

    def __init__(
        self,
        qs_entry: QuestionSourceEntry,
        row: list,
    ):
        self.id, self.qs_id, self.answered, self.timeout = row
        self.question_source = qs_entry


class SessionQuestionEntry:
    id: int
    session_id: int
    question_id: int
    question: QuestionEntry
    session: SessionEntry

    def __init__(self, q_entry: QuestionEntry, s_entry: SessionEntry, row: list):
        self.id, self.session_id, self.question_id = row
        self.question = q_entry
        self.session = s_entry


class QuestionSourceRepo:
    def __init__(
        self, conn: sqlite3.Connection, cur: sqlite3.Cursor, parent: "MicrORM"
    ):
        self.parent = parent
        self.conn = conn
        self.cur = cur

    def create(self, q: str, a: str):
        self.cur.execute(
            """INSERT INTO question_sources ("text", "answer")
            VALUES (?, ?)""",
            (q, a),
        )
        self.conn.commit()
        self.cur.execute("SELECT * FROM question_sources ORDER BY rowid DESC LIMIT 1")
        entry = self.cur.fetchone()
        if entry is not None:
            return QuestionSourceEntry(*entry)
        return None

    def count(self) -> int: ...

    def update_one(self, id: int, q: str, a: str): ...
    def update_many(self, id: int, q: str, a: str): ...
    def delete_one(self, id: int): ...
    def delete_many(self, filter: dict): ...
    def fetch_one(self, id: int) -> QuestionSourceEntry: ...
    def fetch_many(self, filter: dict) -> list[QuestionSourceEntry]: ...


class SessionRepo:
    def __init__(
        self, conn: sqlite3.Connection, cur: sqlite3.Cursor, parent: "MicrORM"
    ):
        self.parent = parent
        self.conn = conn
        self.cur = cur

    def create(self, name: str):
        self.cur.execute(
            """INSERT INTO sessions ("name", "finished")
            VALUES (?, ?)""",
            (name, 0),
        )
        self.conn.commit()
        self.cur.execute("SELECT * FROM sessions ORDER BY rowid DESC LIMIT 1")
        entry = self.cur.fetchone()
        if entry is not None:
            return SessionEntry(*entry)
        return None

    def count(self) -> int: ...

    def update_one(self, id: int, q: str, a: str): ...
    def update_many(self, id: int, q: str, a: str): ...
    def delete_one(self, id: int): ...
    def delete_many(self, filter: dict): ...
    def fetch_one(self, id: int): ...
    def fetch_many(self, filter: dict): ...


class QuestionRepo:
    def __init__(
        self, conn: sqlite3.Connection, cur: sqlite3.Cursor, parent: "MicrORM"
    ):
        self.parent = parent
        self.conn = conn
        self.cur = cur

    def create(self, qs_id: int):
        self.cur.execute(
            """INSERT INTO questions ("qs_id", "answered", "timeout")
            VALUES (?, ?, ?)""",
            (qs_id, 0, 0),
        )
        self.conn.commit()
        self.cur.execute("SELECT * FROM questions ORDER BY rowid DESC LIMIT 1")
        entry = self.cur.fetchone()
        if entry is not None:
            qs = self.parent.question_sources.fetch_one(entry[1])
            return QuestionEntry(qs, entry)
        return None

    def count(self) -> int: ...

    def update_one(self, id: int, q: str, a: str): ...
    def update_many(self, id: int, q: str, a: str): ...
    def delete_one(self, id: int): ...
    def delete_many(self, filter: dict): ...
    def fetch_one(self, id: int) -> QuestionEntry: ...
    def fetch_many(self, filter: dict) -> list[QuestionEntry]: ...


class SessionQuestionRepo:
    def __init__(
        self, conn: sqlite3.Connection, cur: sqlite3.Cursor, parent: "MicrORM"
    ):
        self.parent = parent
        self.conn = conn
        self.cur = cur

    def create(self, s_id: int, q_id: int):
        self.cur.execute(
            """INSERT INTO session_questions ("session_id", "question_id")
            VALUES (?, ?)""",
            (s_id, q_id),
        )
        self.conn.commit()
        self.cur.execute("SELECT * FROM session_questions ORDER BY rowid DESC LIMIT 1")
        entry = self.cur.fetchone()
        if entry is not None:
            s = self.parent.sessions.fetch_one(entry[1])
            q = self.parent.questions.fetch_one(entry[2])
            return SessionQuestionEntry(q_entry=q, s_entry=s, row=entry)
        return None

    def count(self) -> int: ...
    def update_one(self, id: int, q: str, a: str): ...
    def update_many(self, id: int, q: str, a: str): ...
    def delete_one(self, id: int): ...
    def delete_many(self, filter: dict): ...
    def fetch_one(self, id: int) -> SessionQuestionEntry: ...
    def fetch_many(self, filter: dict) -> list[SessionQuestionEntry]: ...


class MicrORM:
    def __init__(self, db_file_path: str):
        self.conn = sqlite3.connect(db_file_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.cur = self.conn.cursor()
        self.setup()
        self.question_sources = QuestionSourceRepo(self.conn, self.cur)
        self.sessions = SessionRepo(self.conn, self.cur)
        self.questions = QuestionRepo(self.conn, self.cur)
        self.session_questions = SessionQuestionRepo(self.conn, self.cur)

    def setup(self):
        LOGGER.info("Setting up db")
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            finished INTEGER
        )
        """
        )
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS question_sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            answer TEXT
        )
        """
        )
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            qs_id INTEGER NOT NULL,
            answered INTEGER,
            timeout INTEGER,
            FOREIGN KEY(qs_id) REFERENCES question_sources(qs_id)
        )
        """
        )
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS session_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            FOREIGN KEY(session_id) REFERENCES sessions(session_id),
            FOREIGN KEY(question_id) REFERENCES questions(questions)
        )
        """
        )
