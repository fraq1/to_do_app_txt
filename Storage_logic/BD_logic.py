from Storage_logic.Storage import Storage
import sqlite3
class BDStorage(Storage):
    def __init__(self):
        self.con = sqlite3.connect("notes.db")
        self.con.execute("PRAGMA foreign_keys = ON")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS dates ("
                    "id INTEGER PRIMARY KEY,"
                    "date TEXT NOT NULL UNIQUE"
                    ");")
        self.cur.execute("CREATE TABLE IF NOT EXISTS  notes("
                    "id INTEGER PRIMARY KEY,"
                    "start_time TEXT NOT NULL,"
                    "end_time TEXT NOT NULL,"
                    "note text NOT NULL,"
                    "date_id INTEGER NOT NULL REFERENCES dates(id)"
                    ");")
        self.con.commit()

    def close(self):
        self.con.close()

    def read_day(self, date:str):
        self.cur.execute("""
            SELECT notes.*
            FROM dates
            INNER JOIN notes
                ON dates.id = notes.fk_date_id
            WHERE dates.date = ?
            """, (date,))
        print(self.cur.fetchall())


bd = BDStorage()
bd.read_day('01-01-2026')