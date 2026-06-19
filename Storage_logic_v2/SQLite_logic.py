from ctypes import c_ushort

from Storage_logic_v2.Storage import Storage
import sqlite3
from Business_logic.Models.Note import Note

class SQLiteDB(Storage):
    def __init__(self):
        self.con = sqlite3.connect("notes.db")
        self.con.execute("PRAGMA foreign_keys = ON")
        cursor = self.con.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS dates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        CONSTRAINT fk_user_dates
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        UNIQUE(user_id, date)
        );''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        note_text TEXT NOT NULL,
        date_id INTEGER NOT NULL,
        CONSTRAINT fk_date_notes
        FOREIGN KEY (date_id) REFERENCES dates (id) ON DELETE CASCADE
        );''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        telegram_id INTEGER UNIQUE NOT NULL
        );''')
        self.con.commit()

    def register_user(self, user):
        cursor = self.con.cursor()
        cursor.execute('''INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?,?)''', (user.telegram_id, user.username))
        self.con.commit()

    def get_user_id(self, telegram_id):
        cursor = self.con.cursor()
        cursor.execute('''
        SELECT id FROM users
        WHERE telegram_id = ?''', (telegram_id, ))
        user_id = cursor.fetchone()
        if user_id is None:
            return None

        return user_id[0]

    def get_or_create_date(self, date, user_id):
        cursor = self.con.cursor()
        cursor.execute('''
        SELECT id FROM dates
        WHERE date = (?) AND user_id = (?)''', (str(date), user_id))
        date_id = cursor.fetchone()
        if date_id:
            return date_id[0]
        cursor.execute('''INSERT INTO dates (date, user_id) VALUES (?,?)''', (str(date), user_id))
        self.con.commit()
        return cursor.lastrowid

    def delete_date(self, date, user_id):
        cursor = self.con.cursor()
        cursor.execute('''
        DELETE FROM dates
        WHERE date = (?) AND user_id = (?)''', (date, user_id))
        self.con.commit()

    def create_note(self, date_id, note: Note):
        cursor = self.con.cursor()
        cursor.execute('''
        INSERT INTO notes (start_time, end_time, note_text, date_id) VALUES (?, ?, ?, ?)
        ''', (note.start_time.strftime("%H:%M"), note.end_time.strftime("%H:%M"), note.text, date_id))
        self.con.commit()

    def get_notes_by_date_id(self, date_id):
        cursor = self.con.cursor()
        cursor.execute('''
        SELECT id, start_time, end_time, note_text
        FROM notes
        WHERE date_id = ?
        ORDER BY start_time DESC
        ''', (date_id, ))
        notes_raw = cursor.fetchall()
        notes = [Note.from_sqlite(i[0], i[1], i[2], i[3]) for i in notes_raw]
        return notes

    def get_notes_id(self, date_id, start_time, user_id):
        cursor = self.con.cursor()
        cursor.execute('''
        SELECT notes.id FROM notes
        JOIN dates ON dates.id = notes.date_id
        WHERE dates.id = ? AND notes.start_time = ? AND dates.user_id = ?
        ''', (date_id, start_time, user_id))
        return cursor.fetchone()[0]

    def update_note_text(self, note_id: int, new_text):
        cursor = self.con.cursor()
        cursor.execute('''
        UPDATE notes
        SET note_text = ?
        WHERE id = ?''', (new_text, note_id))
        self.con.commit()

    def update_note_time(self, note_id, start_time, end_time):
        cursor = self.con.cursor()
        cursor.execute('''
                UPDATE notes
                SET start_time = ?, end_time = ?
                WHERE id = ?''', (start_time.strftime("%H:%M"), end_time.strftime("%H:%M"), note_id))
        self.con.commit()

    def update_note(
        self,
        note_id,
        text=None,
        start_time=None,
        end_time=None
    ):
        cursor = self.con.cursor()
        updates = []
        values = []
        if text is not None:
            updates.append('note_text = ?')
            values.append(text)
        if start_time is not None and end_time is not None:
            updates.append('start_time = ?')
            updates.append('end_time = ?')
            values.append(start_time)
            values.append(end_time)

        if not updates:
            return False

        values.append(note_id)
        query = (f'''
        UPDATE notes
        SET {', '.join(updates)}
        WHERE id = ?
        ''')

        cursor.execute(query, values)

        self.con.commit()
        return True

    def delete_note(self, note_id):
        cursor = self.con.cursor()
        cursor.execute('''
        DELETE FROM notes
        WHERE id = ?
        ''', (note_id, ))
        self.con.commit()
