import sqlite3


conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    chat_id TEXT UNIQUE
);
"""
)
conn.commit()

__all__ = ['conn', 'cursor']
