import sqlite3
import os
from datetime import datetime
from typing import Self


def _adapt_datetime_iso(val):
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return val.isoformat()


def _convert_datetime(val):
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.fromisoformat(val.decode())


sqlite3.register_adapter(datetime, _adapt_datetime_iso)
sqlite3.register_converter("datetime", _convert_datetime)


class Database:

    _instance = None
    _conn: sqlite3.Connection


    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls)
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "projects.db")
            cls._conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
            cls._conn.executescript(
                """
                PRAGMA foreign_keys = ON;
                CREATE TABLE IF NOT EXISTS projects(id INTEGER PRIMARY KEY, name NOT NULL);
                CREATE TABLE IF NOT EXISTS sessions(
                    id INTEGER PRIMARY KEY,
                    project_id NOT NULL,
                    start datetime NOT NULL,
                    end datetime,
                    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
                );
                """
            )
        return cls._instance
        

    def get_project_analytics(self, project_id):
        query = "SELECT COUNT(1), SUM(JULIANDAY(end) - JULIANDAY(start)) * 24 " \
                "FROM sessions WHERE project_id = ?"
        return self._conn.execute(query, (project_id, )).fetchone()


    def get_project_id_by_name(self, name):
        return self._conn.execute("SELECT id FROM projects WHERE name = ?", (name, )).fetchone()


    def get_projects(self):
        return self._conn.execute("SELECT id, name FROM projects").fetchall()


    def get_session_by_id(self, session_id):
        return self._conn.execute(
            "SELECT id, start, end FROM sessions WHERE id = ?",
            (session_id, )
        ).fetchone()


    def get_active_session_id_by_project_id(self, project_id):
        return self._conn.execute(
            "SELECT id FROM sessions WHERE end IS NULL AND project_id = ?",
            (project_id, )
        ).fetchone()


    def insert_session(self, project_id):
        with self._conn:
            self._conn.execute(
                "INSERT INTO sessions (project_id, start) VALUES(?, ?)",
                (project_id, datetime.today())
            )
        

    def insert_project(self, name):
        with self._conn:
            project_id = self._conn.execute("INSERT INTO projects (name) VALUES(?)", (name, )).lastrowid
            return project_id


    def set_session_end(self, session_id):
        with self._conn:
            self._conn.execute("UPDATE sessions SET end = ? WHERE id = ?", (datetime.today(), session_id))

        
    def delete_project(self, project_id):
        with self._conn:
            self._conn.execute("DELETE FROM projects WHERE id = ?", (project_id, ))
